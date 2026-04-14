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

import operator
from typing import Dict, List, Optional, Set, Tuple
from common.proto.context_pb2 import Link
from common.proto.pathcomp_pb2 import Algorithm_KDisjointPath, Algorithm_KShortestPath, PathCompRequest
from common.tools.grpc.Tools import grpc_message_to_json_string
from ._Algorithm import _Algorithm, SRC_END
from .KShortestPathAlgorithm import KShortestPathAlgorithm

Service_Id          = Tuple[str, str]   # (context_uuid, service_uuid)
Service_Constraints = Dict[str, str]    # {constraint_type => constraint_value}
Endpoint_Id         = Tuple[str, str]   # (device_uuid, endpoint_uuid)
Endpoint_Details    = Tuple[str, int]   # (site_id, priority)
Service_Endpoints   = Dict[Endpoint_Id, Endpoint_Details]
Service_Details     = Tuple[int, Service_Constraints, Service_Endpoints]
Services_Details    = Dict[Service_Id, Service_Details]

CUSTOM_CONSTRAINTS = {'bandwidth[gbps]', 'latency[ms]', 'jitter[us]'}

DUMP_EXECUTION_STEPS = False

class KDisjointPathAlgorithm(_Algorithm):
    def __init__(self, algorithm : Algorithm_KDisjointPath, class_name=__name__) -> None:
        super().__init__('KDP', False, class_name=class_name)
        self.num_disjoint = algorithm.num_disjoint
        self.services_details : Services_Details = dict()

    def add_service_requests(self, request: PathCompRequest) -> None:
        super().add_service_requests(request)
        for service in request.services:
            service_id = service.service_id
            context_uuid = service_id.context_id.context_uuid.uuid
            service_uuid = service_id.service_uuid.uuid
            service_key = (context_uuid, service_uuid)

            constraints = dict()
            endpoints = dict()
            service_details = (int(service.service_type), constraints, endpoints)
            self.services_details.setdefault(service_key, service_details)

            for constraint in service.service_constraints:
                kind = constraint.WhichOneof('constraint')

                if kind == 'custom':
                    constraint_type = constraint.custom.constraint_type
                    if constraint_type not in CUSTOM_CONSTRAINTS: continue
                    constraint_value = constraint.custom.constraint_value
                    constraints[constraint_type] = constraint_value

                elif kind == 'endpoint_location':
                    endpoint_id = constraint.endpoint_location.endpoint_id
                    device_uuid = endpoint_id.device_id.device_uuid.uuid
                    device_uuid = self.device_uuid_mapping.get(device_uuid, device_uuid)
                    endpoint_uuid = endpoint_id.endpoint_uuid.uuid
                    endpoint_uuid = self.endpoint_uuid_mapping.get((device_uuid, endpoint_uuid), endpoint_uuid)
                    location_kind = constraint.endpoint_location.location.WhichOneof('location')
                    if location_kind != 'region':
                        MSG = 'Unsupported LocationType({:s}) in Constraint({:s})'
                        raise Exception(MSG.format(location_kind, grpc_message_to_json_string(constraint)))
                    site_id = constraint.endpoint_location.location.region
                    endpoints.setdefault((device_uuid, endpoint_uuid), dict())['site_id'] = site_id

                elif kind == 'endpoint_priority':
                    endpoint_id = constraint.endpoint_priority.endpoint_id
                    device_uuid = endpoint_id.device_id.device_uuid.uuid
                    device_uuid = self.device_uuid_mapping.get(device_uuid, device_uuid)
                    endpoint_uuid = endpoint_id.endpoint_uuid.uuid
                    endpoint_uuid = self.endpoint_uuid_mapping.get((device_uuid, endpoint_uuid), endpoint_uuid)
                    priority = constraint.endpoint_priority.priority
                    endpoints.setdefault((device_uuid, endpoint_uuid), dict())['priority'] = priority

                elif kind == 'sla_capacity':
                    capacity_gbps = constraint.sla_capacity.capacity_gbps
                    constraints['bandwidth[gbps]'] = str(capacity_gbps)

                elif kind == 'sla_latency':
                    e2e_latency_ms = constraint.sla_latency.e2e_latency_ms
                    constraints['latency[ms]'] = str(e2e_latency_ms)

            # TODO: ensure these constraints are provided in the request
            if 'bandwidth[gbps]' not in constraints: constraints['bandwidth[gbps]'] = '20.0'
            if 'latency[ms]' not in constraints: constraints['latency[ms]'] = '20.0'
            #if 'jitter[us]' not in constraints: constraints['jitter[us]'] = '50.0'

    def get_link_from_endpoint(self, endpoint : Dict) -> Tuple[Dict, Link]:
        device_uuid = endpoint['device_id']
        endpoint_uuid = endpoint['endpoint_uuid']
        item = self.endpoint_to_link_dict.get((device_uuid, endpoint_uuid, SRC_END))
        if item is None:
            MSG = 'Link for Endpoint({:s}, {:s}) not found'
            self.logger.warning(MSG.format(device_uuid, endpoint_uuid))
            return None
        return item

    def path_to_links(self, path_endpoints : List[Dict]) -> Tuple[List[Dict], Set[str]]:
        path_links = list()
        path_link_ids = set()
        for endpoint in path_endpoints:
            link_tuple = self.get_link_from_endpoint(endpoint)
            if link_tuple is None: continue
            json_link,_ = link_tuple
            json_link_id = json_link['link_Id']
            if len(path_links) == 0 or path_links[-1]['link_Id'] != json_link_id:
                path_links.append(json_link)
                path_link_ids.add(json_link_id)
        return path_links, path_link_ids

    def remove_traversed_links(self, link_list : List[Dict], path_endpoints : List[Dict]):
        _, path_link_ids = self.path_to_links(path_endpoints)
        new_link_list = list(filter(lambda l: l['link_Id'] not in path_link_ids, link_list))
        #self.logger.info('cur_link_list = {:s}'.format(str(link_list)))
        #self.logger.info('new_link_list = {:s}'.format(str(new_link_list)))
        return new_link_list

    def execute(self, dump_request_filename: Optional[str] = None, dump_reply_filename: Optional[str] = None) -> None:
        algorithm = KShortestPathAlgorithm(Algorithm_KShortestPath(k_inspection=0, k_return=1))
        algorithm.sync_paths = True
        algorithm.device_list = self.device_list
        algorithm.device_name_mapping = self.device_name_mapping
        algorithm.device_uuid_mapping = self.device_uuid_mapping
        algorithm.device_dict = self.device_dict
        algorithm.endpoint_dict = self.endpoint_dict
        algorithm.endpoint_name_mapping = self.endpoint_name_mapping
        algorithm.endpoint_uuid_mapping = self.endpoint_uuid_mapping
        algorithm.link_list = self.link_list
        algorithm.link_dict = self.link_dict
        algorithm.endpoint_to_link_dict = self.endpoint_to_link_dict

        Path = List[Dict]
        Path_NoPath = Optional[Path] # None = no path, list = path
        service_to_paths : Dict[Tuple[str, str], List[Path_NoPath]] = dict()

        for num_path in range(self.num_disjoint):
            algorithm.service_list = list()
            algorithm.service_dict = dict()

            #self.logger.warning('services_details = {:s}'.format(str(self.services_details)))

            _request = PathCompRequest()
            for service_key, service_details in self.services_details.items():
                service_type, constraints, endpoints = service_details
                _service = _request.services.add()  # pylint: disable=no-member
                _service.service_id.context_id.context_uuid.uuid = service_key[0]
                _service.service_id.service_uuid.uuid = service_key[1]
                _service.service_type = service_type

                for constraint_type, constraint_value in constraints.items():
                    constraint = _service.service_constraints.add()
                    constraint.custom.constraint_type = constraint_type
                    constraint.custom.constraint_value = constraint_value

                site_to_endpoints : Dict[str, List[Tuple[Endpoint_Id, int]]] = {}
                for endpoint_key,endpoint_details in endpoints.items():
                    site_id = endpoint_details.get('site_id')
                    if site_id is None: continue
                    priority = endpoint_details.get('priority', 999)
                    site_to_endpoints.setdefault(site_id, list()).append((endpoint_key, priority))

                for site_id,site_endpoints in site_to_endpoints.items():
                    pending_endpoints = sorted(site_endpoints, key=operator.itemgetter(1))
                    if len(pending_endpoints) == 0: continue
                    endpoint_key, _ = pending_endpoints[0]
                    device_uuid, endpoint_uuid = endpoint_key
                    endpoint_id = _service.service_endpoint_ids.add()
                    endpoint_id.device_id.device_uuid.uuid = device_uuid
                    endpoint_id.endpoint_uuid.uuid = endpoint_uuid
                    endpoints.pop(endpoint_key)

            algorithm.add_service_requests(_request)

            dump_request_filename = 'ksp-{:d}-request.json'.format(num_path) if DUMP_EXECUTION_STEPS else None
            dump_reply_filename   = 'ksp-{:d}-reply.txt'.format(num_path)    if DUMP_EXECUTION_STEPS else None
            algorithm.execute(dump_request_filename, dump_reply_filename)

            response_list = algorithm.json_reply.get('response-list', [])
            for response in response_list:
                service_id = response['serviceId']
                service_key = (service_id['contextId'], service_id['service_uuid'])
                json_reply_service = service_to_paths.setdefault(service_key, list())

                no_path_issue = response.get('noPath', {}).get('issue')
                if no_path_issue is not None: continue

                path_endpoints = response['path'][0]
                json_reply_service.append(path_endpoints)
                algorithm.link_list = self.remove_traversed_links(algorithm.link_list, path_endpoints['devices'])

        self.json_reply = dict()
        response_list = self.json_reply.setdefault('response-list', [])
        for service_key,paths in service_to_paths.items():
            response = {'serviceId': {
                'contextId': service_key[0],
                'service_uuid': service_key[1],
            }}
            response['path'] = paths
            if len(paths) < self.num_disjoint:
                response['noPath'] = {'issue': 1}
            response_list.append(response)

        self.logger.debug('self.json_reply = {:s}'.format(str(self.json_reply)))
