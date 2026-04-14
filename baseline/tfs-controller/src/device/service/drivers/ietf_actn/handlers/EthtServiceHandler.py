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

import enum, logging
from typing import Dict, List, Optional, Tuple, Union
from common.tools.rest_conf.client.RestConfClient import RestConfClient


LOGGER = logging.getLogger(__name__)


class BandwidthProfileTypeEnum(enum.Enum):
    MEF_10_BWP = 'ietf-eth-tran-types:mef-10-bwp'

class EndpointLayerSpecificAccessTypeEnum(enum.Enum):
    PORT = 'port'

class EndpointProtectionRoleEnum(enum.Enum):
    WORK = 'work'

class OptimizationMetricRole(enum.Enum):
    WORK = 'work'

class OptimizationMetricType(enum.Enum):
    PATH_METRIC_TE = 'ietf-te-types:path-metric-te'

class OuterTagTypeEnum(enum.Enum):
    CLASSIFY_C_VLAN = 'ietf-eth-tran-types:classify-c-vlan'

class ServiceClassificationTypeEnum(enum.Enum):
    VLAN_CLASSIFICATION = 'ietf-eth-tran-type:vlan-classification'

class ServiceTypeEnum(enum.Enum):
    MP2MP = 'op-mp2mp-svc'
    P2MP  = 'op-p2mp-svc'

def compose_outer_tag(tag_type : OuterTagTypeEnum, vlan_value : int) -> Dict:
    return {'tag-type': tag_type.value, 'vlan-value': vlan_value}

def compose_ingress_egress_bandwidth_profile() -> Dict:
    return {
        'bandwidth-profile-type': BandwidthProfileTypeEnum.MEF_10_BWP.value,
        'CIR': 10_000_000,
        'EIR': 10_000_000,
    }

def compose_layer_specific_access_type() -> Dict:
    return {'access-type': EndpointLayerSpecificAccessTypeEnum.PORT.value}

def compose_static_route(prefix : str, mask : int, next_hop : str) -> Dict:
    return {'destination': prefix, 'destination-mask': mask, 'next-hop': next_hop}

def compose_static_route_list(static_routes : List[Tuple[str, int, str]]) -> List[Dict]:
    return [
        compose_static_route(prefix, mask, next_hop)
        for prefix, mask, next_hop in static_routes
    ]

def compose_etht_service_endpoint(
    node_id : str, tp_id : str, vlan_value : int, static_routes : List[Tuple[str, int, str]] = list()
) -> Dict:
    return {
        'node-id'           : node_id,
        'tp-id'             : tp_id,
        'protection-role'   : EndpointProtectionRoleEnum.WORK.value,
        'layer-specific'    : compose_layer_specific_access_type(),
        'is-extendable'     : False,
        'is-terminal'       : True,
        'static-route-list' : compose_static_route_list(static_routes),
        'outer-tag'         : compose_outer_tag(OuterTagTypeEnum.CLASSIFY_C_VLAN, vlan_value),
        'service-classification-type'     : ServiceClassificationTypeEnum.VLAN_CLASSIFICATION.value,
        'ingress-egress-bandwidth-profile': compose_ingress_egress_bandwidth_profile(),
    }

def compose_optimizations() -> Dict:
    return {'optimization-metric': [{
        'metric-role': OptimizationMetricRole.WORK.value,
        'metric-type': OptimizationMetricType.PATH_METRIC_TE.value,
    }]}

def compose_etht_service(
    name : str, service_type : ServiceTypeEnum, osu_tunnel_name : str,
    src_node_id : str, src_tp_id : str, src_vlan_tag : int, dst_node_id : str, dst_tp_id : str, dst_vlan_tag : int,
    src_static_routes : List[Tuple[str, int, str]] = list(), dst_static_routes : List[Tuple[str, int, str]] = list()
) -> Dict:
    return {'ietf-eth-tran-service:etht-svc': {'etht-svc-instances': [{
        'etht-svc-name' : name,
        'etht-svc-title': name.upper(),
        'etht-svc-type' : service_type.value,
        'source-endpoints': {'source-endpoint': [
            compose_etht_service_endpoint(src_node_id, src_tp_id, src_vlan_tag, src_static_routes),
        ]},
        'destination-endpoints': {'destination-endpoint': [
            compose_etht_service_endpoint(dst_node_id, dst_tp_id, dst_vlan_tag, dst_static_routes),
        ]},
        'svc-tunnel': [{'tunnel-name': osu_tunnel_name}],
        'optimizations': compose_optimizations(),
    }]}}


class EthtServiceHandler:
    def __init__(self, rest_conf_client : RestConfClient) -> None:
        self._rest_conf_client = rest_conf_client
        self._subpath_root = '/ietf-eth-tran-service:etht-svc'
        self._subpath_item = self._subpath_root + '/etht-svc-instances={etht_service_name:s}'


    def get(self, etht_service_name : Optional[str] = None) -> Union[Dict, List]:
        if etht_service_name is None:
            subpath_url = self._subpath_root
        else:
            subpath_url = self._subpath_item.format(etht_service_name=etht_service_name)

        data = self._rest_conf_client.get(subpath_url)

        if not isinstance(data, dict): raise ValueError('data should be a dict')
        if 'ietf-eth-tran-service:etht-svc' not in data: return list()
        data = data['ietf-eth-tran-service:etht-svc']
        if 'etht-svc-instances' not in data:
            raise ValueError('data["ietf-eth-tran-service:etht-svc"] does not contain key "etht-svc-instances"')
        data = data['etht-svc-instances']
        if not isinstance(data, list):
            raise ValueError('data["ietf-eth-tran-service:etht-svc"]["etht-svc-instances"] should be a list')

        etht_services : List[Dict] = list()
        for item in data:
            src_endpoints = item['source-endpoints']['source-endpoint']
            if len(src_endpoints) != 1:
                MSG = 'EthtService({:s}) has zero/multiple source endpoints'
                raise Exception(MSG.format(str(item)))
            src_endpoint = src_endpoints[0]

            dst_endpoints = item['destination-endpoints']['destination-endpoint']
            if len(dst_endpoints) != 1:
                MSG = 'EthtService({:s}) has zero/multiple destination endpoints'
                raise Exception(MSG.format(str(item)))
            dst_endpoint = dst_endpoints[0]

            svc_tunnels = item['svc-tunnel']
            if len(svc_tunnels) != 1:
                MSG = 'EthtService({:s}) has zero/multiple service tunnels'
                raise Exception(MSG.format(str(item)))
            svc_tunnel = svc_tunnels[0]

            etht_service = {
                'name'             : item['etht-svc-name'],
                'service_type'     : item['etht-svc-type'],
                'osu_tunnel_name'  : svc_tunnel['tunnel-name'],

                'src_node_id'      : src_endpoint['node-id'],
                'src_tp_id'        : src_endpoint['tp-id'],
                'src_vlan_tag'     : src_endpoint['outer-tag']['vlan-value'],
                'src_static_routes': [
                    [static_route['destination'], static_route['destination-mask'], static_route['next-hop']]
                    for static_route in src_endpoint.get('static-route-list', list())
                ],

                'dst_node_id'      : dst_endpoint['node-id'],
                'dst_tp_id'        : dst_endpoint['tp-id'],
                'dst_vlan_tag'     : dst_endpoint['outer-tag']['vlan-value'],
                'dst_static_routes': [
                    [static_route['destination'], static_route['destination-mask'], static_route['next-hop']]
                    for static_route in dst_endpoint.get('static-route-list', list())
                ],
            }
            etht_services.append(etht_service)

        return etht_services


    def update(self, parameters : Dict) -> bool:
        name              = parameters['name'           ]
        service_type      = parameters['service_type'   ]
        osu_tunnel_name   = parameters['osu_tunnel_name']

        src_node_id       = parameters['src_node_id'    ]
        src_tp_id         = parameters['src_tp_id'      ]
        src_vlan_tag      = parameters['src_vlan_tag'   ]
        src_static_routes = parameters.get('src_static_routes', [])

        dst_node_id       = parameters['dst_node_id'    ]
        dst_tp_id         = parameters['dst_tp_id'      ]
        dst_vlan_tag      = parameters['dst_vlan_tag'   ]
        dst_static_routes = parameters.get('dst_static_routes', [])

        service_type = ServiceTypeEnum._value2member_map_[service_type]

        data = compose_etht_service(
            name, service_type, osu_tunnel_name,
            src_node_id, src_tp_id, src_vlan_tag, dst_node_id, dst_tp_id, dst_vlan_tag,
            src_static_routes=src_static_routes, dst_static_routes=dst_static_routes
        )
        return self._rest_conf_client.post(self._subpath_root, body=data) is not None


    def delete(self, etht_service_name : str) -> None:
        if etht_service_name is None: raise Exception('etht_service_name is None')
        subpath_url = self._subpath_item.format(etht_service_name=etht_service_name)
        return self._rest_conf_client.delete(subpath_url)
