# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SDN controller descriptor loader

# Usage example (WebUI):
#    descriptors = json.loads(
#       descriptors=descriptors_data_from_client, num_workers=10,
#       context_client=..., device_client=..., service_client=..., slice_client=...)
#    descriptor_loader = DescriptorLoader(descriptors)
#    results = descriptor_loader.process()
#    for message,level in compose_notifications(results):
#        flash(message, level)

# Usage example (pytest):
#    descriptor_loader = DescriptorLoader(
#       descriptors_file='path/to/descriptor.json', num_workers=10,
#       context_client=..., device_client=..., service_client=..., slice_client=...)
#    results = descriptor_loader.process()
#    check_results(results, descriptor_loader)
#    descriptor_loader.validate()
#    # do test ...
#    descriptor_loader.unload()

import concurrent.futures, copy, json, logging, operator
from typing import Any, Dict, List, Optional, Tuple, Union
from common.proto.context_pb2 import (
    Connection, Context, ContextId, Device, DeviceId, Empty,
    Link, LinkId, Service, ServiceId, Slice, SliceId,
    Topology, TopologyId , OpticalLink
)
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from slice.client.SliceClient import SliceClient
from vnt_manager.client.VNTManagerClient import VNTManagerClient
from .Tools import (
    format_device_custom_config_rules, format_service_custom_config_rules,
    format_slice_custom_config_rules, get_descriptors_add_contexts,
    get_descriptors_add_services, get_descriptors_add_slices,
    get_descriptors_add_topologies, split_controllers_and_network_devices,
    split_devices_by_rules, split_links_by_type
)

LOGGER = logging.getLogger(__name__)
LOGGERS = {
    'success': LOGGER.info,
    'danger' : LOGGER.error,
    'error'  : LOGGER.error,
}

ENTITY_TO_TEXT = {
    # name      => singular,     plural
    'context'   : ('Context',    'Contexts'   ),
    'topology'  : ('Topology',   'Topologies' ),
    'controller': ('Controller', 'Controllers'),
    'device'    : ('Device',     'Devices'    ),
    'link'      : ('Link',       'Links'      ),
    'service'   : ('Service',    'Services'   ),
    'slice'     : ('Slice',      'Slices'     ),
    'connection': ('Connection', 'Connections'),
}

ACTION_TO_TEXT = {
    # action =>  infinitive,  past
    'add'     : ('Add',       'Added'     ),
    'update'  : ('Update',    'Updated'   ),
    'config'  : ('Configure', 'Configured'),
}

TypeResults = List[Tuple[str, str, int, List[str]]] # entity_name, action, num_ok, list[error]
TypeNotification = Tuple[str, str] # message, level
TypeNotificationList = List[TypeNotification]

SLICE_TEMPLATE = {
    "slice_id": {
        "context_id": {"context_uuid": {"uuid": "admin"}},
        "slice_uuid": {"uuid": None}
    },
    "name": {},
    "slice_config": {"config_rules": [
        {"action": 1, "custom": {"resource_key": "/settings", "resource_value": {
            "address_families": ["IPV4"], "bgp_as": 65000,
            "bgp_route_target": "65000:333", "mtu": 1512
        }}}
    ]},
    "slice_constraints": [
        {"sla_capacity": {"capacity_gbps": 20.0}},
        {"sla_availability": {"availability": 20.0, "num_disjoint_paths": 1, "all_active": True}},
        {"sla_isolation": {"isolation_level": [0]}}
    ],
    "slice_endpoint_ids": [

    ],
    "slice_status": {"slice_status": 1}
}


class DescriptorLoader:
    def __init__(
        self, descriptors : Optional[Union[str, Dict]] = None, descriptors_file : Optional[str] = None,
        num_workers : int = 1,
        context_client : Optional[ContextClient] = None, device_client : Optional[DeviceClient] = None,
        service_client : Optional[ServiceClient] = None, slice_client : Optional[SliceClient] = None,
        vntm_client : Optional[VNTManagerClient] = None
    ) -> None:
        if (descriptors is None) == (descriptors_file is None):
            # pylint: disable=broad-exception-raised
            raise Exception('Exactly one of "descriptors" or "descriptors_file" is required')
        
        if descriptors_file is not None:
            with open(descriptors_file, 'r', encoding='UTF-8') as f:
                self.__descriptors = json.loads(f.read())
            self.__descriptor_file_path = descriptors_file
        else: # descriptors is not None
            self.__descriptors = json.loads(descriptors) if isinstance(descriptors, str) else descriptors
            self.__descriptor_file_path = '<dict>'

        self.__num_workers = num_workers

        self.__dummy_mode    = self.__descriptors.get('dummy_mode' ,  False)
        self.__contexts      = self.__descriptors.get('contexts'   ,  [])
        self.__topologies    = self.__descriptors.get('topologies' ,  [])
        self.__devices       = self.__descriptors.get('devices'    ,  [])
        self.__links         = self.__descriptors.get('links'      ,  [])
        self.__optical_links = self.__descriptors.get('optical_links',[])
        self.__services      = self.__descriptors.get('services'   ,  [])
        self.__slices        = self.__descriptors.get('slices'     ,  [])
        self.__ietf_slices   = self.__descriptors.get('ietf-network-slice-service:network-slice-services', {})
        self.__connections   = self.__descriptors.get('connections',  [])

        if len(self.__ietf_slices) > 0:
            for slice_service in self.__ietf_slices["slice-service"]:
                tfs_slice = copy.deepcopy(SLICE_TEMPLATE)
                tfs_slice["slice_id"]["slice_uuid"]["uuid"] = slice_service["id"]
                tfs_slice["name"] = slice_service["description"]
                for sdp in slice_service["sdps"]["sdp"]:
                    sdp_id = sdp["id"]
                    for attcircuit in sdp["attachment-circuits"]["attachment-circuit"]:
                        att_cir_tp_id = attcircuit["ac-tp-id"]
                        RESOURCE_KEY = "/device[{:s}]/endpoint[{:s}]/settings"
                        resource_key = RESOURCE_KEY.format(str(sdp_id), str(att_cir_tp_id))

                        for tag in attcircuit['ac-tags']['ac-tag']:
                            if tag.get('tag-type') == 'ietf-nss:vlan-id':
                                vlan_id = tag.get('value')
                            else:
                                vlan_id = 0

                        tfs_slice["slice_config"]["config_rules"].append({
                            "action": 1, "custom": {
                                "resource_key": resource_key, "resource_value": {
                                    "router_id": sdp.get("node-id",[]),
                                    "sub_interface_index": 0,
                                    "vlan_id": vlan_id
                                }
                            }
                        })
                        tfs_slice["slice_endpoint_ids"].append({
                            "device_id": {"device_uuid": {"uuid": sdp_id}},
                            "endpoint_uuid": {"uuid": att_cir_tp_id},
                            "topology_id": {"context_id": {"context_uuid": {"uuid": "admin"}}, 
                            "topology_uuid": {"uuid": "admin"}}
                        })
                        #tfs_slice["slice_constraints"].append({
                        #    "endpoint_location": {
                        #        "endpoint_id": {
                        #            "device_id": {"device_uuid": {"uuid": sdp["id"]}},
                        #            "endpoint_uuid": {"uuid": attcircuit["ac-tp-id"]}
                        #        },
                        #        "location": {"region": "4"}
                        #    }
                        #})
                self.__slices.append(tfs_slice)

        self.__contexts_add   = None
        self.__topologies_add = None
        self.__devices_add    = None
        self.__devices_config = None
        self.__services_add   = None
        self.__slices_add     = None

        self.__ctx_cli = ContextClient()    if context_client is None else context_client
        self.__dev_cli = DeviceClient()     if device_client  is None else device_client
        self.__svc_cli = ServiceClient()    if service_client is None else service_client
        self.__slc_cli = SliceClient()      if slice_client   is None else slice_client
        self.__vnt_cli = VNTManagerClient() if vntm_client    is None else vntm_client

        self.__results : TypeResults = list()

    @property
    def descriptor_file_path(self) -> Optional[str]: return self.__descriptor_file_path

    @property
    def num_workers(self) -> int: return self.__num_workers

    @property
    def context_client(self) -> Optional[ContextClient]: return self.__ctx_cli

    @property
    def device_client(self) -> Optional[DeviceClient]: return self.__dev_cli

    @property
    def service_client(self) -> Optional[ServiceClient]: return self.__svc_cli

    @property
    def slice_client(self) -> Optional[SliceClient]: return self.__slc_cli

    @property
    def contexts(self) -> List[Dict]: return self.__contexts

    @property
    def num_contexts(self) -> int: return len(self.__contexts)

    @property
    def topologies(self) -> Dict[str, List[Dict]]:
        _topologies = {}
        for topology in self.__topologies:
            context_uuid = topology['topology_id']['context_id']['context_uuid']['uuid']
            _topologies.setdefault(context_uuid, []).append(topology)
        return _topologies

    @property
    def num_topologies(self) -> Dict[str, int]:
        _num_topologies = {}
        for topology in self.__topologies:
            context_uuid = topology['topology_id']['context_id']['context_uuid']['uuid']
            _num_topologies[context_uuid] = _num_topologies.get(context_uuid, 0) + 1
        return _num_topologies

    @property
    def devices(self) -> List[Dict]: return self.__devices

    @property
    def num_devices(self) -> int: return len(self.__devices)

    @property
    def links(self) -> List[Dict]: return self.__links

    @property
    def num_links(self) -> int: return len(self.__links)

    @property
    def optical_links(self) -> List[Dict]: return self.__optical_links

    @property
    def num_optical_links(self) -> int: return len(self.__optical_links)

    @property
    def services(self) -> Dict[str, List[Dict]]:
        _services = {}
        for service in self.__services:
            context_uuid = service['service_id']['context_id']['context_uuid']['uuid']
            _services.setdefault(context_uuid, []).append(service)
        return _services

    @property
    def num_services(self) -> Dict[str, int]:
        _num_services = {}
        for service in self.__services:
            context_uuid = service['service_id']['context_id']['context_uuid']['uuid']
            _num_services[context_uuid] = _num_services.get(context_uuid, 0) + 1
        return _num_services

    @property
    def slices(self) -> Dict[str, List[Dict]]:
        _slices = {}
        for slice_ in self.__slices:
            context_uuid = slice_['slice_id']['context_id']['context_uuid']['uuid']
            _slices.setdefault(context_uuid, []).append(slice_)
        return _slices

    @property
    def num_slices(self) -> Dict[str, int]:
        _num_slices = {}
        for slice_ in self.__slices:
            context_uuid = slice_['slice_id']['context_id']['context_uuid']['uuid']
            _num_slices[context_uuid] = _num_slices.get(context_uuid, 0) + 1
        return _num_slices

    @property
    def connections(self) -> List[Dict]: return self.__connections

    @property
    def num_connections(self) -> int: return len(self.__connections)

    def process(self) -> TypeResults:
        # Format CustomConfigRules in Devices, Services and Slices provided in JSON format
        self.__devices  = [format_device_custom_config_rules (device ) for device  in self.__devices ]
        self.__services = [format_service_custom_config_rules(service) for service in self.__services]
        self.__slices   = [format_slice_custom_config_rules  (slice_ ) for slice_  in self.__slices  ]

        # Context and Topology require to create the entity first, and add devices, links, services,
        # slices, etc. in a second stage.
        self.__contexts_add = get_descriptors_add_contexts(self.__contexts)
        self.__topologies_add = get_descriptors_add_topologies(self.__topologies)

        if self.__dummy_mode:
            self._load_dummy_mode()
        else:
            self._load_normal_mode()
        
        return self.__results

    def _load_dummy_mode(self) -> None:
        # Dummy Mode: used to pre-load databases (WebUI debugging purposes) with no smart or automated tasks.

        controllers, network_devices = split_controllers_and_network_devices(self.__devices)

        self.__ctx_cli.connect()
        self._process_descr('context',    'add',    self.__ctx_cli.SetContext,     Context,     self.__contexts_add  )
        self._process_descr('topology',   'add',    self.__ctx_cli.SetTopology,    Topology,    self.__topologies_add)
        self._process_descr('controller', 'add',    self.__ctx_cli.SetDevice,      Device,      controllers          )
        self._process_descr('device',     'add',    self.__ctx_cli.SetDevice,      Device,      network_devices      )
        self._process_descr('link',       'add',    self.__ctx_cli.SetLink,        Link,        self.__links         )
        self._process_descr('link',       'add',    self.__ctx_cli.SetOpticalLink, OpticalLink, self.__optical_links )
        self._process_descr('service',    'add',    self.__ctx_cli.SetService,     Service,     self.__services      )
        self._process_descr('slice',      'add',    self.__ctx_cli.SetSlice,       Slice,       self.__slices        )
        self._process_descr('connection', 'add',    self.__ctx_cli.SetConnection,  Connection,  self.__connections   )

        # By default the Context component automatically assigns devices and links to topologies based on their
        # endpoints, and assigns topologies, services, and slices to contexts based on their identifiers.

        # The following statement is useless; up to now, any use case requires assigning a topology, service, or
        # slice to a different context.
        #self._process_descr('context',    'update', self.__ctx_cli.SetContext,    Context,    self.__contexts      )

        # In some cases, it might be needed to assign devices and links to multiple topologies; the
        # following statement performs that assignment.
        self._process_descr('topology',   'update', self.__ctx_cli.SetTopology,   Topology,   self.__topologies    )

        #self.__ctx_cli.close()

    def _load_normal_mode(self) -> None:
        # Normal mode: follows the automated workflows in the different components
        # assert len(self.__connections) == 0, 'in normal mode, connections should not be set'

        # Device, Service and Slice require to first create the entity and the configure it
        self.__devices_add, self.__devices_config = split_devices_by_rules(self.__devices)
        self.__services_add = get_descriptors_add_services(self.__services)
        self.__slices_add = get_descriptors_add_slices(self.__slices)

        controllers_add, network_devices_add = split_controllers_and_network_devices(self.__devices_add)

        typed_links = split_links_by_type(self.__links)
        typed_normal_links  = typed_links.get('normal',  list())
        typed_optical_links = typed_links.get('optical', list())
        typed_optical_links.extend(self.__optical_links)
        typed_virtual_links = typed_links.get('virtual', list())

        self.__ctx_cli.connect()
        self.__dev_cli.connect()
        if len(self.__services    ) > 0: self.__svc_cli.connect()
        if len(self.__slices      ) > 0: self.__slc_cli.connect()
        if len(typed_virtual_links) > 0: self.__vnt_cli.connect()

        self._process_descr('context',    'add',    self.__ctx_cli.SetContext,      Context,     self.__contexts_add  )
        self._process_descr('topology',   'add',    self.__ctx_cli.SetTopology,     Topology,    self.__topologies_add)
        self._process_descr('controller', 'add',    self.__dev_cli.AddDevice,       Device,      controllers_add      )
        self._process_descr('device',     'add',    self.__dev_cli.AddDevice,       Device,      network_devices_add  )
        self._process_descr('device',     'config', self.__dev_cli.ConfigureDevice, Device,      self.__devices_config)
        self._process_descr('link',       'add',    self.__ctx_cli.SetLink,         Link,        typed_normal_links   )

        if len(typed_optical_links) > 0:
            self._process_descr('link',   'add',    self.__ctx_cli.SetOpticalLink,  OpticalLink, typed_optical_links  )
        
        if len(typed_virtual_links) > 0:
            self._process_descr('link',   'add',    self.__vnt_cli.SetVirtualLink,  Link,        typed_virtual_links  )
        
        if len(self.__services) > 0:
            self._process_descr('service','add',    self.__svc_cli.CreateService,   Service,     self.__services_add  )
            self._process_descr('service','update', self.__svc_cli.UpdateService,   Service,     self.__services      )

        if len(self.__slices) > 0:
            self._process_descr('slice',  'add',    self.__slc_cli.CreateSlice,     Slice,       self.__slices_add    )
            self._process_descr('slice',  'update', self.__slc_cli.UpdateSlice,     Slice,       self.__slices        )

        # By default the Context component automatically assigns devices and links to topologies based on their
        # endpoints, and assigns topologies, services, and slices to contexts based on their identifiers.

        # The following statement is useless; up to now, any use case requires assigning a topology, service, or
        # slice to a different context.
        #self._process_descr('context',  'update', self.__ctx_cli.SetContext,      Context,  self.__contexts      )

        # In some cases, it might be needed to assign devices and links to multiple topologies; the
        # following statement performs that assignment.
        self._process_descr('topology', 'update', self.__ctx_cli.SetTopology,     Topology, self.__topologies    )

        #self.__slc_cli.close()
        #self.__svc_cli.close()
        #self.__dev_cli.close()
        #self.__ctx_cli.close()

    @staticmethod
    def worker(grpc_method, grpc_class, entity) -> Any:
        return grpc_method(grpc_class(**entity))

    def _process_descr(self, entity_name, action_name, grpc_method, grpc_class, entities) -> None:
        num_ok, error_list = 0, []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__num_workers) as executor:
            future_to_entity = {
                executor.submit(DescriptorLoader.worker, grpc_method, grpc_class, entity): (i, entity)
                for i,entity in enumerate(entities)
            }

            for future in concurrent.futures.as_completed(future_to_entity):
                i, entity = future_to_entity[future]
                try:
                    _ = future.result()
                    num_ok += 1
                except Exception as e:  # pylint: disable=broad-except
                    error_list.append((i, f'{str(entity)}: {str(e)}'))

        error_list = [str_error for _,str_error in sorted(error_list, key=operator.itemgetter(0))]
        self.__results.append((entity_name, action_name, num_ok, error_list))

    def validate(self) -> None:
        self.__ctx_cli.connect()

        contexts = self.__ctx_cli.ListContexts(Empty())
        # assert len(contexts.contexts) == self.num_contexts

        for context_uuid, num_topologies in self.num_topologies.items():
            response = self.__ctx_cli.ListTopologies(ContextId(**json_context_id(context_uuid)))
            # assert len(response.topologies) == num_topologies

        response = self.__ctx_cli.ListDevices(Empty())
        # assert len(response.devices) == self.num_devices

        response = self.__ctx_cli.ListLinks(Empty())
        # assert len(response.links) == self.num_links

        response = self.__ctx_cli.GetOpticalLinkList(Empty())
        # assert len(response.optical_links) == self.num_optical_links

        for context_uuid, num_services in self.num_services.items():
            response = self.__ctx_cli.ListServices(ContextId(**json_context_id(context_uuid)))
            # assert len(response.services) == num_services

        for context_uuid, num_slices in self.num_slices.items():
            response = self.__ctx_cli.ListSlices(ContextId(**json_context_id(context_uuid)))
            # assert len(response.slices) == num_slices

    def _unload_dummy_mode(self) -> None:
        # Dummy Mode: used to pre-load databases (WebUI debugging purposes) with no smart or automated tasks.
        self.__ctx_cli.connect()

        for _, slice_list in self.slices.items():
            for slice_ in slice_list:
                self.__ctx_cli.RemoveSlice(SliceId(**slice_['slice_id']))

        for _, service_list in self.services.items():
            for service in service_list:
                self.__ctx_cli.RemoveService(ServiceId(**service['service_id']))

        for optical_link in self.optical_links:
            self.__ctx_cli.DeleteOpticalLink(LinkId(**optical_link['link_id']))

        for link in self.links:
            self.__ctx_cli.RemoveLink(LinkId(**link['link_id']))

        for device in self.devices:
            self.__ctx_cli.RemoveDevice(DeviceId(**device['device_id']))

        for _, topology_list in self.topologies.items():
            for topology in topology_list:
                self.__ctx_cli.RemoveTopology(TopologyId(**topology['topology_id']))

        for context in self.contexts:
            self.__ctx_cli.RemoveContext(ContextId(**context['context_id']))

        #self.__ctx_cli.close()

    def _unload_normal_mode(self) -> None:
        # Normal mode: follows the automated workflows in the different components
        typed_links = split_links_by_type(self.links)
        typed_normal_links  = typed_links.get('normal',  list())
        typed_optical_links = typed_links.get('optical', list())
        typed_optical_links.extend(self.optical_links)
        typed_virtual_links = typed_links.get('virtual', list())

        self.__ctx_cli.connect()
        self.__dev_cli.connect()
        if len(self.services      ) > 0: self.__svc_cli.connect()
        if len(self.slices        ) > 0: self.__slc_cli.connect()
        if len(typed_virtual_links) > 0: self.__vnt_cli.connect()

        for _, slice_list in self.slices.items():
            for slice_ in slice_list:
                self.__slc_cli.DeleteSlice(SliceId(**slice_['slice_id']))

        for _, service_list in self.services.items():
            for service in service_list:
                self.__svc_cli.DeleteService(ServiceId(**service['service_id']))

        for virtual_link in typed_virtual_links:
            self.__vnt_cli.RemoveVirtualLink(LinkId(**virtual_link['link_id']))

        for optical_link in typed_optical_links:
            self.__ctx_cli.DeleteOpticalLink(LinkId(**optical_link['link_id']))

        for link in typed_normal_links:
            self.__ctx_cli.RemoveLink(LinkId(**link['link_id']))

        for device in self.devices:
            self.__dev_cli.DeleteDevice(DeviceId(**device['device_id']))

        for _, topology_list in self.topologies.items():
            for topology in topology_list:
                self.__ctx_cli.RemoveTopology(TopologyId(**topology['topology_id']))

        for context in self.contexts:
            self.__ctx_cli.RemoveContext(ContextId(**context['context_id']))

        #self.__ctx_cli.close()
        #self.__dev_cli.close()
        #self.__svc_cli.close()
        #self.__slc_cli.close()

    def unload(self) -> None:
        if self.__dummy_mode:
            self._unload_dummy_mode()
        else:
            self._unload_normal_mode()

def compose_notifications(results : TypeResults) -> TypeNotificationList:
    notifications = []
    for entity_name, action_name, num_ok, error_list in results:
        entity_name_singluar,entity_name_plural = ENTITY_TO_TEXT[entity_name]
        action_infinitive, action_past = ACTION_TO_TEXT[action_name]
        num_err = len(error_list)
        for error in error_list:
            notifications.append((f'Unable to {action_infinitive} {entity_name_singluar} {error}', 'error'))
        if num_ok : notifications.append((f'{str(num_ok)} {entity_name_plural} {action_past}', 'success'))
        if num_err: notifications.append((f'{str(num_err)} {entity_name_plural} failed', 'danger'))
    return notifications

def check_descriptor_load_results(results : TypeResults, descriptor_loader : DescriptorLoader) -> None:
    num_errors = 0
    for message,level in compose_notifications(results):
        LOGGERS.get(level)(message)
        if level != 'success': num_errors += 1
    if num_errors > 0:
        MSG = 'Failed to load descriptors from "{:s}"'
        raise Exception(MSG.format(str(descriptor_loader.descriptor_file_path)))

def validate_empty_scenario(context_client : ContextClient) -> None:
    response = context_client.ListContexts(Empty())
    # assert len(response.contexts) == 0

    response = context_client.ListDevices(Empty())
    # assert len(response.devices) == 0

    response = context_client.ListLinks(Empty())
    # assert len(response.links) == 0

    response = context_client.GetOpticalLinkList(Empty())
    # assert len(response.optical_links) == 0
