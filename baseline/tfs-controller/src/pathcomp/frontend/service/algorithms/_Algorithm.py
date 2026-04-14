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

import json, logging, re, requests, uuid
from typing import Dict, List, Optional, Tuple, Union
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import (
    ConfigActionEnum, ConfigRule, Connection, Device, DeviceList, EndPointId,
    Link, LinkList, Service, ServiceStatusEnum, ServiceTypeEnum,
)
from common.proto.pathcomp_pb2 import PathCompReply, PathCompRequest
from common.tools.context_queries.Device import get_device
from common.tools.grpc.ConfigRules import update_config_rule_custom
from common.tools.grpc.Tools import grpc_message_list_to_json
from context.client.ContextClient import ContextClient
from pathcomp.frontend.Config import BACKEND_URL
from .tools.EroPathToHops import eropath_to_hops
from .tools.ComposeConfigRules import (
    compose_device_config_rules, compose_l2nm_config_rules, compose_l3nm_config_rules, compose_tapi_config_rules,
    generate_neighbor_endpoint_config_rules, compose_ipowdm_config_rules, compose_tapi_lsp_config_rules,
    compose_iplink_config_rules
)
from .tools.ComposeRequest import compose_device, compose_link, compose_service
from .tools.ComputeSubServices import (
    convert_explicit_path_hops_to_connections,
    convert_explicit_path_hops_to_plain_connection,
)

SRC_END = 'src'
DST_END = 'dst'
SENSE = [SRC_END, DST_END]

class _Algorithm:
    def __init__(self, algorithm_id : str, sync_paths : bool, class_name=__name__) -> None:
        # algorithm_id: algorithm to be executed
        # sync_paths: if multiple services are included in the request, tunes how to prevent contention. If true,
        #             services are computed one after the other and resources assigned to service i, are considered as
        #             used when computing services i+1..n; otherwise, resources are never marked as used during the
        #             path computation.

        self.logger = logging.getLogger(class_name)
        self.algorithm_id = algorithm_id
        self.sync_paths = sync_paths

        self.device_list : List[Dict] = list()
        self.device_dict : Dict[str, Tuple[Dict, Device]] = dict()
        self.device_uuid_mapping : Dict[str, str] = dict()
        self.device_name_mapping : Dict[str, str] = dict()
        self.endpoint_dict : Dict[str, Dict[str, Tuple[Dict, EndPointId]]] = dict()
        self.endpoint_uuid_mapping : Dict[Tuple[str, str], str] = dict()
        self.endpoint_name_mapping : Dict[Tuple[str, str], str] = dict()
        self.link_list : List[Dict] = list()
        self.link_dict : Dict[str, Tuple[Dict, Link]] = dict()
        self.endpoint_to_link_dict : Dict[Tuple[str, str, str], Tuple[Dict, Link]] = dict()
        self.service_list : List[Dict] = list()
        self.service_dict : Dict[Tuple[str, str], Tuple[Dict, Service]] = dict()

    def add_devices(self, grpc_devices : Union[List[Device], DeviceList]) -> None:
        if isinstance(grpc_devices, DeviceList): grpc_devices = grpc_devices.devices
        for grpc_device in grpc_devices:
            json_device = compose_device(grpc_device)
            self.device_list.append(json_device)

            device_uuid = json_device['device_Id']
            self.device_dict[device_uuid] = (json_device, grpc_device)

            _device_uuid = grpc_device.device_id.device_uuid.uuid
            _device_name = grpc_device.name
            self.device_uuid_mapping[_device_name] = _device_uuid
            self.device_uuid_mapping[_device_uuid] = _device_uuid
            self.device_name_mapping[_device_name] = _device_name
            self.device_name_mapping[_device_uuid] = _device_name

            device_endpoint_dict : Dict[str, Tuple[Dict, EndPointId]] = dict()
            for json_endpoint,grpc_endpoint in zip(json_device['device_endpoints'], grpc_device.device_endpoints):
                endpoint_uuid = json_endpoint['endpoint_id']['endpoint_uuid']
                endpoint_tuple = (json_endpoint['endpoint_id'], grpc_endpoint.endpoint_id)
                device_endpoint_dict[endpoint_uuid] = endpoint_tuple

                _endpoint_uuid = grpc_endpoint.endpoint_id.endpoint_uuid.uuid
                _endpoint_name = grpc_endpoint.name
                self.endpoint_uuid_mapping[(_device_uuid, _endpoint_name)] = _endpoint_uuid
                self.endpoint_uuid_mapping[(_device_name, _endpoint_name)] = _endpoint_uuid
                self.endpoint_uuid_mapping[(_device_uuid, _endpoint_uuid)] = _endpoint_uuid
                self.endpoint_uuid_mapping[(_device_name, _endpoint_uuid)] = _endpoint_uuid
                self.endpoint_name_mapping[(_device_uuid, _endpoint_name)] = _endpoint_name
                self.endpoint_name_mapping[(_device_name, _endpoint_name)] = _endpoint_name
                self.endpoint_name_mapping[(_device_uuid, _endpoint_uuid)] = _endpoint_name
                self.endpoint_name_mapping[(_device_name, _endpoint_uuid)] = _endpoint_name

            self.endpoint_dict[device_uuid] = device_endpoint_dict

    def add_links(self, grpc_links : Union[List[Link], LinkList]) -> None:
        if isinstance(grpc_links, LinkList): grpc_links = grpc_links.links
        for grpc_link in grpc_links:
            if 'mgmt' in grpc_link.name.lower(): continue

            json_link = compose_link(grpc_link)
            if len(json_link['link_endpoint_ids']) != 2: continue
            self.link_list.append(json_link)

            link_uuid = json_link['link_Id']
            self.link_dict[link_uuid] = (json_link, grpc_link)

            for i,link_endpoint_id in enumerate(json_link['link_endpoint_ids']):
                link_endpoint_id = link_endpoint_id['endpoint_id']
                device_uuid = link_endpoint_id['device_id']
                endpoint_uuid = link_endpoint_id['endpoint_uuid']
                endpoint_key = (device_uuid, endpoint_uuid, SENSE[i])
                link_tuple = (json_link, grpc_link)
                self.endpoint_to_link_dict[endpoint_key] = link_tuple

    def add_service_requests(self, request : PathCompRequest) -> None:
        for grpc_service in request.services:
            json_service = compose_service(grpc_service)
            self.service_list.append(json_service)
            service_id = json_service['serviceId']
            service_key = (service_id['contextId'], service_id['service_uuid'])
            service_tuple = (json_service, grpc_service)
            self.service_dict[service_key] = service_tuple

    def execute(self, dump_request_filename : Optional[str] = None, dump_reply_filename : Optional[str] = None) -> None:
        request = {'serviceList': self.service_list, 'deviceList': self.device_list, 'linkList': self.link_list}

        self.logger.debug('[execute] request={:s}'.format(json.dumps(request, sort_keys=True, indent=4)))
        if dump_request_filename is not None:
            with open(dump_request_filename, 'w', encoding='UTF-8') as f:
                f.write(json.dumps(request, sort_keys=True, indent=4))

        self.logger.debug('[execute] BACKEND_URL: {:s}'.format(str(BACKEND_URL)))
        reply = requests.post(BACKEND_URL, json=request)
        self.status_code = reply.status_code
        self.raw_reply = reply.content.decode('UTF-8')

        self.logger.debug('[execute] status_code={:s} reply={:s}'.format(str(reply.status_code), str(self.raw_reply)))
        if dump_reply_filename is not None:
            with open(dump_reply_filename, 'w', encoding='UTF-8') as f:
                f.write('status_code={:s} reply={:s}'.format(str(self.status_code), str(self.raw_reply)))

        if reply.status_code not in {requests.codes.ok}: # pylint: disable=no-member
            raise Exception('Backend error({:s}) for request({:s})'.format(
                str(self.raw_reply), json.dumps(request, sort_keys=True)))

        self.json_reply = reply.json()

    def add_connection_to_reply(
        self, reply : PathCompReply, connection_uuid : str, service : Service, path_hops : List[Dict]
    ) -> Connection:
        connection = reply.connections.add()

        connection.connection_id.connection_uuid.uuid = connection_uuid
        connection.service_id.CopyFrom(service.service_id)

        for path_hop in path_hops:
            device_uuid = path_hop['device']

            ingress_endpoint_uuid = path_hop['ingress_ep']
            endpoint_id = connection.path_hops_endpoint_ids.add()
            endpoint_id.CopyFrom(self.endpoint_dict[device_uuid][ingress_endpoint_uuid][1])

            egress_endpoint_uuid = path_hop['egress_ep']
            endpoint_id = connection.path_hops_endpoint_ids.add()
            endpoint_id.CopyFrom(self.endpoint_dict[device_uuid][egress_endpoint_uuid][1])

        return connection

    def add_service_to_reply(
        self, reply : PathCompReply, context_uuid : str, service_uuid : str, service_type : ServiceTypeEnum,
        path_hops : List[Dict] = [], config_rules : List = []
    ) -> Service:
        # TODO: implement support for multi-point services
        # Control deactivated to enable disjoint paths with multiple redundant endpoints on each side
        #service_endpoint_ids = service.service_endpoint_ids
        #if len(service_endpoint_ids) != 2: raise NotImplementedError('Service must have 2 endpoints')

        service_key = (context_uuid, service_uuid)
        tuple_service = self.service_dict.get(service_key)

        service = reply.services.add()
        service.service_id.context_id.context_uuid.uuid = context_uuid
        service.service_id.service_uuid.uuid = service_uuid
        service.service_type = service_type

        #rules_nb = len(config_rules)
        rules_nb = 0 # NOTE: do we need to skip default rules if there are other rules?

        if service_type == ServiceTypeEnum.SERVICETYPE_L2NM and rules_nb == 0:
            compose_l2nm_config_rules(config_rules, service.service_config.config_rules)
            self.logger.info("Installing default rules for L2NM service")
        elif service_type == ServiceTypeEnum.SERVICETYPE_L3NM and rules_nb == 0:
            compose_l3nm_config_rules(config_rules, service.service_config.config_rules)
            self.logger.info("Installing default rules for L3NM service")
        elif service_type == ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE and rules_nb == 0:
            compose_tapi_config_rules(config_rules, service.service_config.config_rules)
            self.logger.info("Installing default rules for TAPI service")
        elif service_type == ServiceTypeEnum.SERVICETYPE_IP_LINK:
            compose_iplink_config_rules(config_rules, service.service_config.config_rules)
            self.logger.info("Installing default rules for IP-LINK service")
        elif service_type == ServiceTypeEnum.SERVICETYPE_IPOWDM and rules_nb == 0:
            compose_ipowdm_config_rules(config_rules, service.service_config.config_rules)
            self.logger.info("Installing default rules for IPOWDM service")
        elif service_type == ServiceTypeEnum.SERVICETYPE_TAPI_LSP:
            compose_tapi_lsp_config_rules(config_rules, service.service_config.config_rules)
            self.logger.info("Installing default rules for TAPI LSP service")

        else:
            MSG = 'Unhandled generic Config Rules for service {:s} {:s}'
            self.logger.warning(MSG.format(str(service_uuid), str(ServiceTypeEnum.Name(service_type))))

        compose_device_config_rules(
            config_rules, service.service_config.config_rules, path_hops,
            self.device_uuid_mapping, self.endpoint_uuid_mapping)

        context_client = ContextClient()
        device_cache : Dict[str, Device] = dict()
        for path_hop in path_hops:
            path_hop_device_id     = path_hop['device']
            path_hop_ingress_ep_id = path_hop['ingress_ep']
            path_hop_egress_ep_id  = path_hop['egress_ep']

            path_hop_device_uuid = self.device_uuid_mapping[path_hop_device_id]
            if path_hop_device_uuid in device_cache:
                path_hop_device = device_cache[path_hop_device_uuid]
            else:
                path_hop_device = get_device(
                    context_client, path_hop_device_uuid, include_components=False,
                    include_endpoints=False, include_config_rules=True
                )
                device_cache[path_hop_device_uuid] = path_hop_device

            target_endpoint_ids = {
                self.endpoint_uuid_mapping[(path_hop_device_id, path_hop_ingress_ep_id)],
                self.endpoint_uuid_mapping[(path_hop_device_id, path_hop_egress_ep_id )],
                self.endpoint_name_mapping[(path_hop_device_id, path_hop_ingress_ep_id)],
                self.endpoint_name_mapping[(path_hop_device_id, path_hop_egress_ep_id )],
            }

            path_hop_device_name = path_hop_device.name

            RE_ENDPOINT_SETTINGS = re.compile(r'\/endpoints\/endpoint\[([^\]]+)\](\/settings)?')
            for config_rule in path_hop_device.device_config.config_rules:
                if config_rule.WhichOneof('config_rule') != 'custom': continue
                resource_key = str(config_rule.custom.resource_key)
                ep_match = RE_ENDPOINT_SETTINGS.match(resource_key)
                if ep_match is None: continue
                endpoint_id = ep_match.group(1)
                if endpoint_id not in target_endpoint_ids: continue
                endpoint_name = self.endpoint_name_mapping[(path_hop_device_id, endpoint_id)]

                resource_value : Dict = json.loads(config_rule.custom.resource_value)
                address_ip = resource_value.pop('address_ip', '0.0.0.0')
                if address_ip != '0.0.0.0': resource_value['address_ip'] = address_ip

                if len(resource_value) == 0: continue
                field_updates = {name:(value, False) for name,value in resource_value.items()}

                resource_key = '/device[{:s}]/endpoint[{:s}]/settings'.format(
                    path_hop_device_name, endpoint_name
                )
                update_config_rule_custom(
                    service.service_config.config_rules, resource_key, field_updates,
                    new_action=ConfigActionEnum.CONFIGACTION_SET
                )

        if path_hops is not None and len(path_hops) > 0:
            ingress_endpoint_id = service.service_endpoint_ids.add()
            ingress_endpoint_id.device_id.device_uuid.uuid = path_hops[0]['device']
            ingress_endpoint_id.endpoint_uuid.uuid = path_hops[0]['ingress_ep']

            egress_endpoint_id = service.service_endpoint_ids.add()
            egress_endpoint_id.device_id.device_uuid.uuid = path_hops[-1]['device']
            egress_endpoint_id.endpoint_uuid.uuid = path_hops[-1]['egress_ep']

        if tuple_service is None:
            service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED
        else:
            service.name = tuple_service[1].name
            service.service_status.CopyFrom(tuple_service[1].service_status)
            service.timestamp.CopyFrom(tuple_service[1].timestamp)
            for constraint in tuple_service[1].service_constraints:
                service.service_constraints.add().CopyFrom(constraint)
            for config_rule in config_rules:
                service.service_config.config_rules.add().CopyFrom(config_rule)

        return service

    def get_reply(self) -> PathCompReply:
        response_list = self.json_reply.get('response-list', [])
        reply = PathCompReply()
        grpc_services : Dict[Tuple[str, str], Service] = {}
        #grpc_connections : Dict[str, Connection] = {}
        for response in response_list:
            orig_service_id = response['serviceId']
            context_uuid = orig_service_id['contextId']
            main_service_uuid = orig_service_id['service_uuid']
            orig_service_key = (context_uuid, main_service_uuid)
            _,grpc_orig_service = self.service_dict[orig_service_key]
            main_service_type = grpc_orig_service.service_type

            no_path_issue = response.get('noPath', {}).get('issue')
            if no_path_issue is not None:
                # no path found: leave connection with no endpoints
                # no_path_issue == 1 => no path due to a constraint
                grpc_services[orig_service_key] = grpc_orig_service
                continue

            orig_config_rules = grpc_orig_service.service_config.config_rules
            json_orig_config_rules = grpc_message_list_to_json(orig_config_rules)

            for service_path_ero in response['path']:
                self.logger.debug('service_path_ero["devices"] = {:s}'.format(str(service_path_ero['devices'])))
                _endpoint_to_link_dict = {k:v[0] for k,v in self.endpoint_to_link_dict.items()}
                self.logger.debug('self.endpoint_to_link_dict = {:s}'.format(str(_endpoint_to_link_dict)))
                path_hops = eropath_to_hops(service_path_ero['devices'], self.endpoint_to_link_dict)

                json_generated_config_rules = generate_neighbor_endpoint_config_rules(
                    json_orig_config_rules, path_hops, self.device_uuid_mapping, self.endpoint_uuid_mapping
                )
                json_extended_config_rules = list()
                json_extended_config_rules.extend(json_orig_config_rules)
                json_extended_config_rules.extend(json_generated_config_rules)
                extended_config_rules = [
                    ConfigRule(**json_extended_config_rule)
                    for json_extended_config_rule in json_extended_config_rules
                ]

                self.logger.debug('path_hops = {:s}'.format(str(path_hops)))
                device_types = {v[0]['device_type'] for k,v in self.device_dict.items()}
                DEVICES_BASIC_CONNECTION = {
                    DeviceTypeEnum.EMULATED_CLIENT.value,
                    DeviceTypeEnum.EMULATED_COMPUTER.value,
                    DeviceTypeEnum.EMULATED_DATACENTER.value,
                    DeviceTypeEnum.EMULATED_VIRTUAL_MACHINE.value,
                    DeviceTypeEnum.EMULATED_PACKET_ROUTER.value,
                    DeviceTypeEnum.PACKET_POP.value,
                    DeviceTypeEnum.PACKET_ROUTER.value,
                }
                self.logger.debug('device_types = {:s}'.format(str(device_types)))
                self.logger.debug('DEVICES_BASIC_CONNECTION = {:s}'.format(str(DEVICES_BASIC_CONNECTION)))
                is_basic_connection = device_types.issubset(DEVICES_BASIC_CONNECTION)
                self.logger.debug('is_basic_connection = {:s}'.format(str(is_basic_connection)))
                if is_basic_connection:
                    self.logger.info('Assuming basic connections...')
                    connections = convert_explicit_path_hops_to_plain_connection(
                        path_hops, main_service_uuid, main_service_type)
                    self.logger.debug('BASIC connections = {:s}'.format(str(connections)))
                else:
                    try:
                        _device_dict = {k:v[0] for k,v in self.device_dict.items()}
                        self.logger.debug('self.device_dict = {:s}'.format(str(_device_dict)))
                        connections = convert_explicit_path_hops_to_connections(
                            path_hops, self.device_dict, main_service_uuid, main_service_type)
                        self.logger.debug('EXTRAPOLATED connections = {:s}'.format(str(connections)))
                    except: # pylint: disable=bare-except
                        MSG = ' '.join([
                            'Unable to Extrapolate sub-services and sub-connections.',
                            'Assuming single-service and single-connection.',
                        ])
                        self.logger.exception(MSG)
                        connections = convert_explicit_path_hops_to_plain_connection(
                            path_hops, main_service_uuid, main_service_type)
                        self.logger.debug('BASIC connections = {:s}'.format(str(connections)))

                for connection in connections:
                    service_uuid,service_type,path_hops,_ = connection
                    service_key = (context_uuid, service_uuid)
                    if service_key in grpc_services: continue
                    grpc_service = self.add_service_to_reply(
                        reply, context_uuid, service_uuid, service_type, path_hops=path_hops,
                        config_rules=extended_config_rules)
                    grpc_services[service_key] = grpc_service

                for connection in connections:
                    service_uuid,_,path_hops,dependencies = connection

                    service_key = (context_uuid, service_uuid)
                    grpc_service = grpc_services.get(service_key)
                    if grpc_service is None: raise Exception('Service({:s}) not found'.format(str(service_key)))

                    #if connection_uuid in grpc_connections: continue
                    grpc_connection = self.add_connection_to_reply(reply, str(uuid.uuid4()), grpc_service, path_hops)
                    #grpc_connections[connection_uuid] = grpc_connection

                    for sub_service_uuid in dependencies:
                        sub_service_key = (context_uuid, sub_service_uuid)
                        grpc_sub_service = grpc_services.get(sub_service_key)
                        if grpc_sub_service is None:
                            raise Exception('Service({:s}) not found'.format(str(sub_service_key)))
                        grpc_sub_service_id = grpc_connection.sub_service_ids.add()
                        grpc_sub_service_id.CopyFrom(grpc_sub_service.service_id)

                # ... "path-capacity": {"total-size": {"value": 200, "unit": 0}},
                # ... "path-latency": {"fixed-latency-characteristic": "10.000000"},
                # ... "path-cost": {"cost-name": "", "cost-value": "5.000000", "cost-algorithm": "0.000000"},
                #path_capacity = service_path_ero['path-capacity']['total-size']
                #path_capacity_value = path_capacity['value']
                #path_capacity_unit = CapacityUnit(path_capacity['unit'])
                #path_latency = service_path_ero['path-latency']['fixed-latency-characteristic']
                #path_cost = service_path_ero['path-cost']
                #path_cost_name = path_cost['cost-name']
                #path_cost_value = path_cost['cost-value']
                #path_cost_algorithm = path_cost['cost-algorithm']

        return reply
