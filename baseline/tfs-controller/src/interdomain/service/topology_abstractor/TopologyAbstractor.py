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

import logging, threading
from typing import Dict, Optional, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME, ServiceNameEnum
from common.DeviceTypes import DeviceTypeEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, find_environment_variables, get_env_var_name)
from common.proto.context_pb2 import (
    ContextEvent, ContextId, Device, DeviceEvent, DeviceId, EndPoint, EndPointId, Link, LinkEvent, TopologyId,
    TopologyEvent)
from common.tools.context_queries.CheckType import (
    device_type_is_datacenter, device_type_is_network, endpoint_type_is_border)
from common.tools.context_queries.Context import create_context
from common.tools.context_queries.Device import get_uuids_of_devices_in_topology #, get_devices_in_topology
#from common.tools.context_queries.Link import get_links_in_topology
from common.tools.context_queries.Topology import create_missing_topologies
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from dlt.connector.client.DltConnectorClient import DltConnectorClient
from .AbstractDevice import AbstractDevice
from .AbstractLink import AbstractLink
from .DltRecordSender import DltRecordSender
from .Types import EventTypes

LOGGER = logging.getLogger(__name__)

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))
INTERDOMAIN_TOPOLOGY_ID = TopologyId(**json_topology_id(INTERDOMAIN_TOPOLOGY_NAME, context_id=ADMIN_CONTEXT_ID))

class TopologyAbstractor(threading.Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.terminate = threading.Event()

        self.context_client = ContextClient()
        self.context_event_collector = EventsCollector(self.context_client)

        self.real_to_abstract_device_uuid : Dict[str, str] = dict()
        self.real_to_abstract_link_uuid : Dict[str, str] = dict()

        self.abstract_device_to_topology_id : Dict[str, TopologyId] = dict()
        self.abstract_link_to_topology_id : Dict[str, TopologyId] = dict()

        self.abstract_devices : Dict[str, AbstractDevice] = dict()
        self.abstract_links : Dict[Tuple[str,str], AbstractLink] = dict()

    def stop(self):
        self.terminate.set()

    def run(self) -> None:
        self.context_client.connect()
        create_context(self.context_client, DEFAULT_CONTEXT_NAME)
        topology_uuids = [DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME]
        create_missing_topologies(self.context_client, ADMIN_CONTEXT_ID, topology_uuids)

        self.context_event_collector.start()

        while not self.terminate.is_set():
            event = self.context_event_collector.get_event(timeout=0.1)
            if event is None: continue
            #if self.ignore_event(event): continue
            LOGGER.info('Processing Event({:s})...'.format(grpc_message_to_json_string(event)))
            self.update_abstraction(event)

        self.context_event_collector.stop()
        self.context_client.close()

    #def ignore_event(self, event : EventTypes) -> List[DltRecordIdTypes]:
    #    # TODO: filter events resulting from abstraction computation
    #    # TODO: filter events resulting from updating remote abstractions
    #    if self.own_context_id is None: return False
    #    own_context_uuid = self.own_context_id.context_uuid.uuid
    #
    #    if isinstance(event, ContextEvent):
    #        context_uuid = event.context_id.context_uuid.uuid
    #        return context_uuid == own_context_uuid
    #    elif isinstance(event, TopologyEvent):
    #        context_uuid = event.topology_id.context_id.context_uuid.uuid
    #        if context_uuid != own_context_uuid: return True
    #        topology_uuid = event.topology_id.topology_uuid.uuid
    #        if topology_uuid in {INTERDOMAIN_TOPOLOGY_NAME}: return True
    #
    #    return False

    def _get_or_create_abstract_device(
        self, device_uuid : str, device_name : str, device_type : DeviceTypeEnum, dlt_record_sender : DltRecordSender,
        abstract_topology_id : TopologyId
    ) -> AbstractDevice:
        abstract_device = self.abstract_devices.get(device_uuid)
        changed = False
        if abstract_device is None:
            abstract_device = AbstractDevice(device_uuid, device_name, device_type)
            changed = abstract_device.initialize()
            if changed: dlt_record_sender.add_device(abstract_topology_id, abstract_device.device)
            self.abstract_devices[device_uuid] = abstract_device
            self.abstract_device_to_topology_id[device_uuid] = abstract_topology_id
        return abstract_device

    def _update_abstract_device(
        self, device : Device, dlt_record_sender : DltRecordSender, abstract_topology_id : TopologyId,
        abstract_device_uuid : Optional[str] = None
    ) -> None:
        device_uuid = device.device_id.device_uuid.uuid
        device_name = device.name
        if device_type_is_datacenter(device.device_type):
            abstract_device_uuid = device_uuid
            abstract_device = self._get_or_create_abstract_device(
                device_uuid, device_name, DeviceTypeEnum.EMULATED_DATACENTER, dlt_record_sender, abstract_topology_id)
        elif device_type_is_network(device.device_type):
            LOGGER.warning('device_type is network; not implemented')
            return
        else:
            abstract_device = self._get_or_create_abstract_device(
                abstract_device_uuid, None, DeviceTypeEnum.NETWORK, dlt_record_sender, abstract_topology_id)
        self.real_to_abstract_device_uuid[device_uuid] = abstract_device_uuid
        changed = abstract_device.update_endpoints(device)
        if changed: dlt_record_sender.add_device(abstract_topology_id, abstract_device.device)

    def _get_or_create_abstract_link(
        self, link_uuid : str, dlt_record_sender : DltRecordSender, abstract_topology_id : TopologyId
    ) -> AbstractLink:
        abstract_link = self.abstract_links.get(link_uuid)
        changed = False
        if abstract_link is None:
            abstract_link = AbstractLink(link_uuid)
            changed = abstract_link.initialize()
            if changed: dlt_record_sender.add_link(abstract_topology_id, abstract_link.link)
            self.abstract_links[link_uuid] = abstract_link
            self.abstract_link_to_topology_id[link_uuid] = abstract_topology_id
        return abstract_link

    def _get_link_endpoint_data(self, endpoint_id : EndPointId) -> Optional[Tuple[AbstractDevice, EndPoint]]:
        device_uuid : str = endpoint_id.device_id.device_uuid.uuid
        endpoint_uuid : str = endpoint_id.endpoint_uuid.uuid
        abstract_device_uuid = self.real_to_abstract_device_uuid.get(device_uuid)
        if abstract_device_uuid is None: return None
        abstract_device = self.abstract_devices.get(abstract_device_uuid)
        if abstract_device is None: return None
        endpoint = abstract_device.get_endpoint(device_uuid, endpoint_uuid)
        if endpoint is None: return None
        return abstract_device, endpoint

    def _compute_abstract_link(self, link : Link) -> Optional[str]:
        if len(link.link_endpoint_ids) != 2: return None

        link_endpoint_data_A = self._get_link_endpoint_data(link.link_endpoint_ids[0])
        if link_endpoint_data_A is None: return None
        abstract_device_A, endpoint_A = link_endpoint_data_A
        if not endpoint_type_is_border(endpoint_A.endpoint_type): return None

        link_endpoint_data_Z = self._get_link_endpoint_data(link.link_endpoint_ids[-1])
        if link_endpoint_data_Z is None: return None
        abstract_device_Z, endpoint_Z = link_endpoint_data_Z
        if not endpoint_type_is_border(endpoint_Z.endpoint_type): return None

        link_uuid = AbstractLink.compose_uuid(
            abstract_device_A.uuid, endpoint_A.endpoint_id.endpoint_uuid.uuid,
            abstract_device_Z.uuid, endpoint_Z.endpoint_id.endpoint_uuid.uuid
        )

        # sort endpoints lexicographically to prevent duplicities
        link_endpoint_uuids = sorted([
            (abstract_device_A.uuid, endpoint_A.endpoint_id.endpoint_uuid.uuid),
            (abstract_device_Z.uuid, endpoint_Z.endpoint_id.endpoint_uuid.uuid)
        ])

        return link_uuid, link_endpoint_uuids

    def _update_abstract_link(
        self, link : Link, dlt_record_sender : DltRecordSender, abstract_topology_id : TopologyId
    ) -> None:
        abstract_link_specs = self._compute_abstract_link(link)
        if abstract_link_specs is None: return
        abstract_link_uuid, link_endpoint_uuids = abstract_link_specs

        abstract_link = self._get_or_create_abstract_link(abstract_link_uuid, dlt_record_sender, abstract_topology_id)
        link_uuid = link.link_id.link_uuid.uuid
        self.real_to_abstract_link_uuid[link_uuid] = abstract_link_uuid
        changed = abstract_link.update_endpoints(link_endpoint_uuids)
        if changed: dlt_record_sender.add_link(abstract_topology_id, abstract_link.link)

    def _infer_abstract_links(self, device : Device, dlt_record_sender : DltRecordSender) -> None:
        device_uuid = device.device_id.device_uuid.uuid

        interdomain_device_uuids = get_uuids_of_devices_in_topology(
            self.context_client, ADMIN_CONTEXT_ID, INTERDOMAIN_TOPOLOGY_NAME)

        for endpoint in device.device_endpoints:
            if not endpoint_type_is_border(endpoint.endpoint_type): continue
            endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid

            abstract_link_uuid = AbstractLink.compose_uuid(device_uuid, endpoint_uuid, endpoint_uuid, device_uuid)
            if abstract_link_uuid in self.abstract_links: continue

            if endpoint_uuid not in interdomain_device_uuids: continue
            remote_device = self.context_client.GetDevice(DeviceId(**json_device_id(endpoint_uuid)))
            remote_device_border_endpoint_uuids = {
                endpoint.endpoint_id.endpoint_uuid.uuid : endpoint.endpoint_type
                for endpoint in remote_device.device_endpoints
                if endpoint_type_is_border(endpoint.endpoint_type)
            }
            if device_uuid not in remote_device_border_endpoint_uuids: continue

            link_endpoint_uuids = sorted([(device_uuid, endpoint_uuid), (endpoint_uuid, device_uuid)])

            abstract_link = self._get_or_create_abstract_link(
                abstract_link_uuid, dlt_record_sender, INTERDOMAIN_TOPOLOGY_ID)
            changed = abstract_link.update_endpoints(link_endpoint_uuids)
            if changed: dlt_record_sender.add_link(INTERDOMAIN_TOPOLOGY_ID, abstract_link.link)

    def update_abstraction(self, event : EventTypes) -> None:
        env_vars = find_environment_variables([
            get_env_var_name(ServiceNameEnum.DLT, ENVVAR_SUFIX_SERVICE_HOST     ),
            get_env_var_name(ServiceNameEnum.DLT, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
        ])
        if len(env_vars) == 2:
            # DLT available
            dlt_connector_client = DltConnectorClient()
            dlt_connector_client.connect()
        else:
            dlt_connector_client = None

        dlt_record_sender = DltRecordSender(self.context_client, dlt_connector_client)

        if isinstance(event, ContextEvent):
            LOGGER.debug('Processing ContextEvent({:s})'.format(grpc_message_to_json_string(event)))
            LOGGER.warning('Ignoring ContextEvent({:s})'.format(grpc_message_to_json_string(event)))

        elif isinstance(event, TopologyEvent):
            LOGGER.debug('Processing TopologyEvent({:s})'.format(grpc_message_to_json_string(event)))
            topology_id = event.topology_id
            topology_uuid = topology_id.topology_uuid.uuid
            context_id = topology_id.context_id
            context_uuid = context_id.context_uuid.uuid
            topology_uuids = {DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME}

            context = self.context_client.GetContext(context_id)
            context_name = context.name

            topology_details = self.context_client.GetTopologyDetails(topology_id)
            topology_name = topology_details.name

            if ((context_uuid == DEFAULT_CONTEXT_NAME) or (context_name == DEFAULT_CONTEXT_NAME)) and \
                (topology_uuid not in topology_uuids) and (topology_name not in topology_uuids):

                abstract_topology_id = TopologyId(**json_topology_id(topology_uuid, context_id=ADMIN_CONTEXT_ID))
                self._get_or_create_abstract_device(
                    topology_uuid, topology_name, DeviceTypeEnum.NETWORK, dlt_record_sender, abstract_topology_id)

                #devices = get_devices_in_topology(self.context_client, context_id, topology_uuid)
                for device in topology_details.devices:
                    self._update_abstract_device(
                        device, dlt_record_sender, abstract_topology_id, abstract_device_uuid=topology_uuid)

                #links = get_links_in_topology(self.context_client, context_id, topology_uuid)
                for link in topology_details.links:
                    self._update_abstract_link(link, dlt_record_sender, abstract_topology_id)
                
                for device in topology_details.devices:
                    self._infer_abstract_links(device, dlt_record_sender)

            else:
                MSG = 'Ignoring ({:s}/{:s})({:s}/{:s}) TopologyEvent({:s})'
                args = context_uuid, context_name, topology_uuid, topology_name, grpc_message_to_json_string(event)
                LOGGER.warning(MSG.format(*args))

        elif isinstance(event, DeviceEvent):
            LOGGER.debug('Processing DeviceEvent({:s})'.format(grpc_message_to_json_string(event)))
            device_id = event.device_id
            device_uuid = device_id.device_uuid.uuid
            abstract_device_uuid = self.real_to_abstract_device_uuid.get(device_uuid)
            device = self.context_client.GetDevice(device_id)
            if abstract_device_uuid is None:
                LOGGER.warning('Ignoring DeviceEvent({:s})'.format(grpc_message_to_json_string(event)))
            else:
                abstract_topology_id = self.abstract_device_to_topology_id[abstract_device_uuid]
                self._update_abstract_device(
                    device, dlt_record_sender, abstract_topology_id, abstract_device_uuid=abstract_device_uuid)

            self._infer_abstract_links(device, dlt_record_sender)

        elif isinstance(event, LinkEvent):
            LOGGER.debug('Processing LinkEvent({:s})'.format(grpc_message_to_json_string(event)))
            link_id = event.link_id
            link_uuid = link_id.link_uuid.uuid
            abstract_link_uuid = self.real_to_abstract_link_uuid.get(link_uuid)
            if abstract_link_uuid is None:
                LOGGER.warning('Ignoring LinkEvent({:s})'.format(grpc_message_to_json_string(event)))
            else:
                abstract_topology_id = self.abstract_link_to_topology_id[abstract_link_uuid]
                link = self.context_client.GetLink(link_id)
                self._update_abstract_link(link, dlt_record_sender, abstract_topology_id)

        else:
            LOGGER.warning('Unsupported Event({:s})'.format(grpc_message_to_json_string(event)))

        dlt_record_sender.commit()
        if dlt_connector_client is not None: dlt_connector_client.close()
