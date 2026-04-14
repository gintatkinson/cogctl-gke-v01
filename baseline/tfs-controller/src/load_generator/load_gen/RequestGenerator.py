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

import logging, json, random, re, threading, uuid
from typing import Dict, Optional, Set, Tuple
from common.proto.context_pb2 import Empty, IsolationLevelEnum, TopologyId
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.Constraint import (
    json_constraint_sla_availability, json_constraint_sla_capacity, json_constraint_sla_isolation,
    json_constraint_sla_latency)
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from common.tools.object_factory.Service import (
    json_service_l2nm_planned, json_service_l3nm_planned, json_service_tapi_planned)
from common.tools.object_factory.Slice import json_slice
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from dlt.connector.client.DltConnectorClient import DltConnectorClient
from load_generator.tools.ListScalarRange import generate_value
from .Constants import ENDPOINT_COMPATIBILITY, RequestType
from .DltTools import record_device_to_dlt, record_link_to_dlt
from .Parameters import Parameters

LOGGER = logging.getLogger(__name__)

ROUTER_ID = {
    'R149': '5.5.5.5',
    'R155': '5.5.5.1',
    'R199': '5.5.5.6',
}

class RequestGenerator:
    def __init__(self, parameters : Parameters) -> None:
        self._parameters = parameters
        self._lock = threading.Lock()
        self._num_generated = 0
        self._num_released = 0
        self._available_device_endpoints : Dict[str, Set[str]] = dict()
        self._used_device_endpoints : Dict[str, Dict[str, str]] = dict()
        self._endpoint_ids_to_types : Dict[Tuple[str, str], str] = dict()
        self._endpoint_types_to_ids : Dict[str, Set[Tuple[str, str]]] = dict()

        self._device_data : Dict[str, Dict] = dict()
        self._device_endpoint_data : Dict[str, Dict[str, Dict]] = dict()

    @property
    def num_generated(self): return self._num_generated

    @property
    def num_released(self): return self._num_released

    @property
    def infinite_loop(self): return self._parameters.num_requests == 0

    def initialize(self) -> None:
        with self._lock:
            self._available_device_endpoints.clear()
            self._used_device_endpoints.clear()

            context_client = ContextClient()
            dlt_connector_client = DltConnectorClient()

            if self._parameters.record_to_dlt:
                dlt_domain_id = TopologyId(**json_topology_id('dlt-perf-eval'))

            re_device = re.compile(r'^{:s}$'.format(self._parameters.device_regex))
            re_endpoint = re.compile(r'^{:s}$'.format(self._parameters.endpoint_regex))

            devices = context_client.ListDevices(Empty())
            for device in devices.devices:
                if self._parameters.record_to_dlt:
                    record_device_to_dlt(dlt_connector_client, dlt_domain_id, device.device_id)

                if re_device.match(device.name) is None: continue
                device_uuid = device.device_id.device_uuid.uuid
                self._device_data[device_uuid] = grpc_message_to_json(device)

                _endpoints = self._available_device_endpoints.setdefault(device_uuid, set())
                for endpoint in device.device_endpoints:
                    if re_endpoint.match(endpoint.name) is None: continue
                    endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
                    endpoints = self._device_endpoint_data.setdefault(device_uuid, dict())
                    endpoints[endpoint_uuid] = grpc_message_to_json(endpoint)

                    endpoint_type = endpoint.endpoint_type
                    _endpoints.add(endpoint_uuid)
                    self._endpoint_ids_to_types.setdefault((device_uuid, endpoint_uuid), endpoint_type)
                    self._endpoint_types_to_ids.setdefault(endpoint_type, set()).add((device_uuid, endpoint_uuid))

            links = context_client.ListLinks(Empty())
            for link in links.links:
                if self._parameters.record_to_dlt:
                    record_link_to_dlt(dlt_connector_client, dlt_domain_id, link.link_id)

                for endpoint_id in link.link_endpoint_ids:
                    device_uuid = endpoint_id.device_id.device_uuid.uuid
                    endpoint_uuid = endpoint_id.endpoint_uuid.uuid
                    _endpoints = self._available_device_endpoints.get(device_uuid, set())
                    _endpoints.discard(endpoint_uuid)
                    if len(_endpoints) == 0: self._available_device_endpoints.pop(device_uuid, None)

                    endpoint_type = self._endpoint_ids_to_types.pop((device_uuid, endpoint_uuid), None)
                    if endpoint_type is None: continue

                    if endpoint_type not in self._endpoint_types_to_ids: continue
                    endpoints_for_type = self._endpoint_types_to_ids[endpoint_type]
                    endpoint_key = (device_uuid, endpoint_uuid)
                    if endpoint_key not in endpoints_for_type: continue
                    endpoints_for_type.discard(endpoint_key)

    def dump_state(self) -> None:
        with self._lock:
            _endpoints = {
                device_uuid:[endpoint_uuid for endpoint_uuid in endpoint_uuids]
                for device_uuid,endpoint_uuids in self._available_device_endpoints.items()
            }
            LOGGER.debug('[dump_state] available_device_endpoints = {:s}'.format(json.dumps(_endpoints)))
            LOGGER.debug('[dump_state] used_device_endpoints = {:s}'.format(json.dumps(self._used_device_endpoints)))

    def _use_device_endpoint(
        self, service_uuid : str, request_type : RequestType, endpoint_types : Optional[Set[str]] = None,
        exclude_device_uuids : Set[str] = set(), exclude_endpoint_uuids : Set[Tuple[str, str]] = set(), 
    ) -> Optional[Tuple[str, str]]:
        with self._lock:
            compatible_endpoints : Set[Tuple[str, str]] = set()
            elegible_device_endpoints : Dict[str, Set[str]] = {}

            if endpoint_types is None:
                # allow all
                elegible_device_endpoints : Dict[str, Set[str]] = {
                    device_uuid:[
                        endpoint_uuid for endpoint_uuid in device_endpoint_uuids
                        if (len(exclude_endpoint_uuids) == 0) or \
                            ((device_uuid,endpoint_uuid) not in exclude_endpoint_uuids)
                    ]
                    for device_uuid,device_endpoint_uuids in self._available_device_endpoints.items()
                    if (device_uuid not in exclude_device_uuids) and \
                        (len(device_endpoint_uuids) > 0)
                }
            else:
                # allow only compatible endpoints
                for endpoint_type in endpoint_types:
                    if endpoint_type not in self._endpoint_types_to_ids: continue
                    compatible_endpoints.update(self._endpoint_types_to_ids[endpoint_type])

                for device_uuid,device_endpoint_uuids in self._available_device_endpoints.items():
                    if device_uuid in exclude_device_uuids or len(device_endpoint_uuids) == 0: continue
                    for endpoint_uuid in device_endpoint_uuids:
                        endpoint_key = (device_uuid,endpoint_uuid)
                        if endpoint_key in exclude_endpoint_uuids: continue
                        if endpoint_key not in compatible_endpoints: continue
                        elegible_device_endpoints.setdefault(device_uuid, set()).add(endpoint_uuid)

            if len(elegible_device_endpoints) == 0:
                LOGGER.warning(' '.join([
                    '>> No endpoint is available:',
                    'endpoint_types={:s}'.format(str(endpoint_types)),
                    'exclude_device_uuids={:s}'.format(str(exclude_device_uuids)),
                    'self._endpoint_types_to_ids={:s}'.format(str(self._endpoint_types_to_ids)),
                    'self._available_device_endpoints={:s}'.format(str(self._available_device_endpoints)),
                    'compatible_endpoints={:s}'.format(str(compatible_endpoints)),
                ]))
                return None

            device_uuid = random.choice(list(elegible_device_endpoints.keys()))
            device_endpoint_uuids = elegible_device_endpoints.get(device_uuid)
            endpoint_uuid = random.choice(list(device_endpoint_uuids))
            if request_type not in {RequestType.SERVICE_MW}:
                # reserve the resources
                self._available_device_endpoints.setdefault(device_uuid, set()).discard(endpoint_uuid)
                self._used_device_endpoints.setdefault(device_uuid, dict())[endpoint_uuid] = service_uuid
            return device_uuid, endpoint_uuid

    def _release_device_endpoint(self, device_uuid : str, endpoint_uuid : str) -> None:
        with self._lock:
            self._used_device_endpoints.setdefault(device_uuid, dict()).pop(endpoint_uuid, None)
            self._available_device_endpoints.setdefault(device_uuid, set()).add(endpoint_uuid)

    def compose_request(self) -> Tuple[bool, Optional[Dict], str]: # completed, request
        with self._lock:
            if not self.infinite_loop and (self._num_generated >= self._parameters.num_requests):
                LOGGER.info('Generation Done!')
                return True, None, None # completed

        request_uuid = str(uuid.uuid4())
        request_type = random.choice(self._parameters.request_types)

        if request_type in {
            RequestType.SERVICE_L2NM, RequestType.SERVICE_L3NM, RequestType.SERVICE_TAPI, RequestType.SERVICE_MW
        }:
            return False, self._compose_service(request_uuid, request_type), request_type
        elif request_type in {RequestType.SLICE_L2NM, RequestType.SLICE_L3NM}:
            return False, self._compose_slice(request_uuid, request_type), request_type

    def _compose_service(self, request_uuid : str, request_type : str) -> Optional[Dict]:
        # choose source endpoint
        src_endpoint_types = set(ENDPOINT_COMPATIBILITY.keys()) if request_type in {RequestType.SERVICE_TAPI} else None
        src = self._use_device_endpoint(request_uuid, request_type, endpoint_types=src_endpoint_types)
        if src is None:
            LOGGER.warning('>> No source endpoint is available')
            return None
        src_device_uuid,src_endpoint_uuid = src

        # identify compatible destination endpoint types
        src_endpoint_type = self._endpoint_ids_to_types.get((src_device_uuid,src_endpoint_uuid))
        dst_endpoint_type = ENDPOINT_COMPATIBILITY.get(src_endpoint_type)
        dst_endpoint_types = {dst_endpoint_type} if request_type in {RequestType.SERVICE_TAPI} else None

        # identify excluded destination devices
        REQUESTTYPES_REUSING_DEVICES = {RequestType.SERVICE_TAPI, RequestType.SERVICE_MW}
        exclude_device_uuids = {} if request_type in REQUESTTYPES_REUSING_DEVICES else {src_device_uuid}

        # choose feasible destination endpoint
        dst = self._use_device_endpoint(
            request_uuid, request_type, endpoint_types=dst_endpoint_types, exclude_device_uuids=exclude_device_uuids,
            exclude_endpoint_uuids={src})
        
        # if destination endpoint not found, release source, and terminate current service generation
        if dst is None:
            LOGGER.warning('>> No destination endpoint is available')
            self._release_device_endpoint(src_device_uuid, src_endpoint_uuid)
            return None

        with self._lock:
            self._num_generated += 1
            num_request = self._num_generated

        # compose endpoints
        dst_device_uuid,dst_endpoint_uuid = dst
        endpoint_ids = [
            json_endpoint_id(json_device_id(src_device_uuid), src_endpoint_uuid),
            json_endpoint_id(json_device_id(dst_device_uuid), dst_endpoint_uuid),
        ]

        if request_type == RequestType.SERVICE_L2NM:
            availability   = generate_value(self._parameters.availability_ranges,   ndigits=5)
            capacity_gbps  = generate_value(self._parameters.capacity_gbps_ranges,  ndigits=2)
            e2e_latency_ms = generate_value(self._parameters.e2e_latency_ms_ranges, ndigits=2)

            constraints = [
                json_constraint_sla_availability(1, True, availability),
                json_constraint_sla_capacity(capacity_gbps),
                json_constraint_sla_isolation([IsolationLevelEnum.NO_ISOLATION]),
                json_constraint_sla_latency(e2e_latency_ms),
            ]

            vlan_id = 300 + num_request % 1000
            circuit_id = '{:03d}'.format(vlan_id)

            src_device_name = self._device_data[src_device_uuid]['name']
            src_endpoint_name = self._device_endpoint_data[src_device_uuid][src_endpoint_uuid]['name']
            src_router_num = int(re.findall(r'^\D*(\d+)', src_device_name)[0])
            src_router_id = ROUTER_ID.get(src_device_name)
            if src_router_id is None: src_router_id = '10.0.0.{:d}'.format(src_router_num)

            dst_device_name = self._device_data[dst_device_uuid]['name']
            dst_endpoint_name = self._device_endpoint_data[dst_device_uuid][dst_endpoint_uuid]['name']
            dst_router_num = int(re.findall(r'^\D*(\d+)', dst_device_name)[0])
            dst_router_id = ROUTER_ID.get(dst_device_name)
            if dst_router_id is None: dst_router_id = '10.0.0.{:d}'.format(dst_router_num)

            config_rules = [
                json_config_rule_set('/settings', {
                    'mtu': 1512
                }),
                json_config_rule_set(
                    '/device[{:s}]/endpoint[{:s}]/settings'.format(src_device_name, src_endpoint_name), {
                        'sub_interface_index': 0,
                        'vlan_id': vlan_id,
                        'remote_router': dst_router_id,
                        'circuit_id': circuit_id,
                }),
                json_config_rule_set(
                    '/device[{:s}]/endpoint[{:s}]/settings'.format(dst_device_name, dst_endpoint_name), {
                        'sub_interface_index': 0,
                        'vlan_id': vlan_id,
                        'remote_router': src_router_id,
                        'circuit_id': circuit_id,
                }),
            ]
            return json_service_l2nm_planned(
                request_uuid, endpoint_ids=endpoint_ids, constraints=constraints, config_rules=config_rules)

        elif request_type == RequestType.SERVICE_L3NM:
            availability   = generate_value(self._parameters.availability_ranges,   ndigits=5)
            capacity_gbps  = generate_value(self._parameters.capacity_gbps_ranges,  ndigits=2)
            e2e_latency_ms = generate_value(self._parameters.e2e_latency_ms_ranges, ndigits=2)

            constraints = [
                json_constraint_sla_availability(1, True, availability),
                json_constraint_sla_capacity(capacity_gbps),
                json_constraint_sla_isolation([IsolationLevelEnum.NO_ISOLATION]),
                json_constraint_sla_latency(e2e_latency_ms),
            ]

            bgp_as = 65000 + (num_request % 10000)

            vlan_id = 300 + num_request % 1000
            x = num_request % 255
            y = num_request % 25 * num_request % 10
            route_distinguisher = '{:5d}:{:03d}'.format(bgp_as, vlan_id)

            src_device_name = self._device_data[src_device_uuid]['name']
            src_endpoint_name = self._device_endpoint_data[src_device_uuid][src_endpoint_uuid]['name']
            src_router_num = int(re.findall(r'^\D*(\d+)', src_device_name)[0])
            src_router_id = ROUTER_ID.get(src_device_name)
            if src_router_id is None: src_router_id = '10.0.0.{:d}'.format(src_router_num)
            src_address_ip = '10.{:d}.{:d}.{:d}'.format(x, y, src_router_num)

            dst_device_name = self._device_data[dst_device_uuid]['name']
            dst_endpoint_name = self._device_endpoint_data[dst_device_uuid][dst_endpoint_uuid]['name']
            dst_router_num = int(re.findall(r'^\D*(\d+)', dst_device_name)[0])
            dst_router_id = ROUTER_ID.get(dst_device_name)
            if dst_router_id is None: dst_router_id = '10.0.0.{:d}'.format(dst_router_num)
            dst_address_ip = '10.{:d}.{:d}.{:d}'.format(y, x, dst_router_num)

            policy_AZ = 'srv_{:d}_a'.format(vlan_id)
            policy_ZA = 'srv_{:d}_b'.format(vlan_id)

            config_rules = [
                json_config_rule_set('/settings', {
                    'bgp_as'          : bgp_as,
                    'route_distinguisher': route_distinguisher,
                }),
                json_config_rule_set(
                    '/device[{:s}]/endpoint[{:s}]/settings'.format(src_device_name, src_endpoint_name), {
                        'router_id'          : src_router_id,
                        'route_distinguisher': route_distinguisher,
                        'sub_interface_index': 0,
                        'vlan_id'            : vlan_id,
                        'address_ip'         : src_address_ip,
                        'address_prefix'     : 16,
                        'policy_AZ'           : policy_AZ,
                        'policy_ZA'           : policy_ZA,
                    }),
                json_config_rule_set(
                    '/device[{:s}]/endpoint[{:s}]/settings'.format(dst_device_name, dst_endpoint_name), {
                        'router_id'          : dst_router_id,
                        'route_distinguisher': route_distinguisher,
                        'sub_interface_index': 0,
                        'vlan_id'            : vlan_id,
                        'address_ip'         : dst_address_ip,
                        'address_prefix'     : 16,
                        'policy_ZA'           : policy_AZ,
                        'policy_AZ'           : policy_ZA,
                    }),
            ]
            return json_service_l3nm_planned(
                request_uuid, endpoint_ids=endpoint_ids, constraints=constraints, config_rules=config_rules)

        elif request_type == RequestType.SERVICE_TAPI:
            config_rules = [
                json_config_rule_set('/settings', {
                    'capacity_value'  : 50.0,
                    'capacity_unit'   : 'GHz',
                    'layer_proto_name': 'PHOTONIC_MEDIA',
                    'layer_proto_qual': 'tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC',
                    'direction'       : 'UNIDIRECTIONAL',
                }),
            ]
            return json_service_tapi_planned(
                request_uuid, endpoint_ids=endpoint_ids, constraints=[], config_rules=config_rules)

        elif request_type == RequestType.SERVICE_MW:
            vlan_id = 1000 + num_request % 1000
            config_rules = [
                json_config_rule_set('/settings', {
                    'vlan_id': vlan_id,
                }),
            ]
            return json_service_l2nm_planned(
                request_uuid, endpoint_ids=endpoint_ids, constraints=[], config_rules=config_rules)

    def _compose_slice(self, request_uuid : str, request_type : str) -> Optional[Dict]:
        # choose source endpoint
        src = self._use_device_endpoint(request_uuid, request_type)
        if src is None:
            LOGGER.warning('>> No source endpoint is available')
            return None
        src_device_uuid,src_endpoint_uuid = src

        # identify excluded destination devices
        REQUESTTYPES_REUSING_DEVICES = {RequestType.SERVICE_TAPI, RequestType.SERVICE_MW}
        exclude_device_uuids = {} if request_type in REQUESTTYPES_REUSING_DEVICES else {src_device_uuid}

        # choose feasible destination endpoint
        dst = self._use_device_endpoint(request_uuid, request_type, exclude_device_uuids=exclude_device_uuids)
        
        # if destination endpoint not found, release source, and terminate current service generation
        if dst is None:
            LOGGER.warning('>> No destination endpoint is available')
            self._release_device_endpoint(src_device_uuid, src_endpoint_uuid)
            return None

        with self._lock:
            self._num_generated += 1
            num_request = self._num_generated

        # compose endpoints
        dst_device_uuid,dst_endpoint_uuid = dst
        endpoint_ids = [
            json_endpoint_id(json_device_id(src_device_uuid), src_endpoint_uuid),
            json_endpoint_id(json_device_id(dst_device_uuid), dst_endpoint_uuid),
        ]

        availability   = generate_value(self._parameters.availability_ranges,   ndigits=5)
        capacity_gbps  = generate_value(self._parameters.capacity_gbps_ranges,  ndigits=2)
        e2e_latency_ms = generate_value(self._parameters.e2e_latency_ms_ranges, ndigits=2)

        constraints = [
            json_constraint_sla_availability(1, True, availability),
            json_constraint_sla_capacity(capacity_gbps),
            json_constraint_sla_isolation([IsolationLevelEnum.NO_ISOLATION]),
            json_constraint_sla_latency(e2e_latency_ms),
        ]

        if request_type == RequestType.SLICE_L2NM:
            vlan_id = 300 + num_request % 1000
            circuit_id = '{:03d}'.format(vlan_id)

            src_device_name = self._device_data[src_device_uuid]['name']
            src_router_id = '10.0.0.{:d}'.format(int(re.findall(r'^\D*(\d+)', src_device_name)[0]))

            dst_device_name = self._device_data[dst_device_uuid]['name']
            dst_router_id = '10.0.0.{:d}'.format(int(re.findall(r'^\D*(\d+)', dst_device_name)[0]))

            config_rules = [
                json_config_rule_set('/settings', {
                    'mtu': 1512
                }),
                json_config_rule_set(
                    '/device[{:s}]/endpoint[{:s}]/settings'.format(src_device_uuid, src_endpoint_uuid), {
                        'router_id': src_router_id,
                        'sub_interface_index': vlan_id,
                        'vlan_id': vlan_id,
                        'remote_router': dst_router_id,
                        'circuit_id': circuit_id,
                    }),
                json_config_rule_set(
                    '/device[{:s}]/endpoint[{:s}]/settings'.format(dst_device_uuid, dst_endpoint_uuid), {
                        'router_id': dst_router_id,
                        'sub_interface_index': vlan_id,
                        'vlan_id': vlan_id,
                        'remote_router': src_router_id,
                        'circuit_id': circuit_id,
                    }),
            ]

        elif request_type == RequestType.SLICE_L3NM:
            vlan_id = 300 + num_request % 1000
            circuit_id = '{:03d}'.format(vlan_id)
            bgp_as = 60000 + (num_request % 10000)
            bgp_route_target = '{:5d}:{:03d}'.format(bgp_as, 333)
            route_distinguisher = '{:5d}:{:03d}'.format(bgp_as, vlan_id)

            src_device_name = self._device_data[src_device_uuid]['name']
            src_endpoint_name = self._device_endpoint_data[src_device_uuid][src_endpoint_uuid]['name']
            src_router_id = '10.0.0.{:d}'.format(int(re.findall(r'^\D*(\d+)', src_device_name)[0]))
            src_address_ip = '.'.join([re.findall(r'^\D*(\d+)', src_device_name)[0], '0'] + src_endpoint_name.split('/'))

            dst_device_name = self._device_data[dst_device_uuid]['name']
            dst_endpoint_name = self._device_endpoint_data[dst_device_uuid][dst_endpoint_uuid]['name']
            dst_router_id = '10.0.0.{:d}'.format(int(re.findall(r'^\D*(\d+)', dst_device_name)[0]))
            dst_address_ip = '.'.join([re.findall(r'^\D*(\d+)', dst_device_name)[0], '0'] + dst_endpoint_name.split('/'))

            config_rules = [
                json_config_rule_set('/settings', {
                    'mtu'             : 1512,
                    'bgp_as'          : bgp_as,
                    'bgp_route_target': bgp_route_target,
                }),
                json_config_rule_set(
                    '/device[{:s}]/endpoint[{:s}]/settings'.format(src_device_uuid, src_endpoint_uuid), {
                        'router_id'          : src_router_id,
                        'route_distinguisher': route_distinguisher,
                        'sub_interface_index': vlan_id,
                        'vlan_id'            : vlan_id,
                        'address_ip'         : src_address_ip,
                        'address_prefix'     : 16,
                    }),
                json_config_rule_set(
                    '/device[{:s}]/endpoint[{:s}]/settings'.format(dst_device_uuid, dst_endpoint_uuid), {
                        'router_id'          : dst_router_id,
                        'route_distinguisher': route_distinguisher,
                        'sub_interface_index': vlan_id,
                        'vlan_id'            : vlan_id,
                        'address_ip'         : dst_address_ip,
                        'address_prefix'     : 16,
                    }),
            ]

        return json_slice(
            request_uuid, endpoint_ids=endpoint_ids, constraints=constraints, config_rules=config_rules)

    def release_request(self, json_request : Dict) -> None:
        if 'service_id' in json_request:
            for endpoint_id in json_request['service_endpoint_ids']:
                device_uuid = endpoint_id['device_id']['device_uuid']['uuid']
                endpoint_uuid = endpoint_id['endpoint_uuid']['uuid']
                self._release_device_endpoint(device_uuid, endpoint_uuid)

            with self._lock:
                self._num_released += 1

        elif 'slice_id' in json_request:
            for endpoint_id in json_request['slice_endpoint_ids']:
                device_uuid = endpoint_id['device_id']['device_uuid']['uuid']
                endpoint_uuid = endpoint_id['endpoint_uuid']['uuid']
                self._release_device_endpoint(device_uuid, endpoint_uuid)

            with self._lock:
                self._num_released += 1
