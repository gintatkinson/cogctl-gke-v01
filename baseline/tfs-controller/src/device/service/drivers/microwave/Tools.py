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

import json, logging, requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Optional, Set
from device.service.driver_api._Driver import RESOURCE_ENDPOINTS

LOGGER = logging.getLogger(__name__)

HTTP_OK_CODES = {
    200,    # OK
    201,    # Created
    202,    # Accepted
    204,    # No Content
}

def find_key(resource, key):
    return json.loads(resource[1])[key]

# this function exports only the endpoints which are not already involved in a microwave physical link
# TODO: improvement: create a Set[Tuple[node_id:str, tp_id:str]] containing the endpoints involved in links
# TODO: exportable endpoints are those not in this set. That will prevent looping through links for every endpoint
def is_exportable_endpoint(node, termination_point_id, links):
    # for each link we check if the endpoint (termination_point_id) is already used by an existing link
    for link in links:
        src = link['source']
        dest = link['destination']
        if dest['dest-node'] == node and dest['dest-tp'] == termination_point_id:
            return False
        if src['source-node'] == node and src['source-tp'] == termination_point_id:
            return False
    return True

VLAN_CLASSIFICATION_TYPES = {'ietf-eth-tran-types:vlan-classification', 'vlan-classification'}
OUTER_TAG_C_TYPE = {'ietf-eth-tran-types:classify-c-vlan', 'classify-c-vlan'}
def get_vlan_outer_tag(endpoint : Dict) -> Optional[int]:
    if endpoint.get('service-classification-type', '') not in VLAN_CLASSIFICATION_TYPES: return None
    outer_tag = endpoint.get('outer-tag', {})
    if outer_tag.get('tag-type', '') not in OUTER_TAG_C_TYPE: return None
    return outer_tag.get('vlan-value')

def config_getter(
    root_url : str, resource_key : str, auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None,
    node_ids : Set[str] = set()
):
    # getting endpoints
    network_name = 'SIAE-ETH-TOPOLOGY'
    FIELDS = ''.join([
        'ietf-network-topology:',
        'link(link-id;destination(dest-node;dest-tp);source(source-node;source-tp));',
        'node(node-id;ietf-network-topology:termination-point(tp-id;ietf-te-topology:te/name)))',
    ])
    URL_TEMPLATE = '{:s}/nmswebs/restconf/data/ietf-network:networks/network={:s}?fields={:s}'
    url = URL_TEMPLATE.format(root_url, network_name, FIELDS)

    result = []
    if resource_key == RESOURCE_ENDPOINTS:
        # getting existing endpoints
        try:
            response = requests.get(url, timeout=timeout, verify=False, auth=auth)
            context = json.loads(response.content)
            network_instance = context.get('ietf-network:network', {})
            links = network_instance.get('ietf-network-topology:link', [])
            for node in network_instance['node']:
                node_id = node['node-id']
                if len(node_ids) > 0 and node_id not in node_ids: continue
                tp_list = node['ietf-network-topology:termination-point']
                for tp in tp_list:
                    tp_id = tp['tp-id']
                    if not is_exportable_endpoint(node_id, tp_id, links): continue
                    tp_uuid = '{:s}:{:s}'.format(node_id,tp_id)
                    resource_key = '/endpoints/endpoint[{:s}]'.format(tp_uuid)
                    resource_value = {'uuid': tp_uuid, 'type': tp['ietf-te-topology:te']['name']}
                    result.append((resource_key, resource_value))
        except requests.exceptions.Timeout:
            LOGGER.exception('Timeout connecting {:s}'.format(url))
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.exception('Exception retrieving/parsing endpoints for {:s}'.format(resource_key))
            result.append((resource_key, e))
    else:
        # getting created services
        url = '{:s}/nmswebs/restconf/data/ietf-eth-tran-service:etht-svc'.format(root_url)
        try:
            response = requests.get(url, timeout=timeout, verify=False, auth=auth)
            context = json.loads(response.content)
            etht_service = context.get('ietf-eth-tran-service:etht-svc', {})
            service_instances = etht_service.get('etht-svc-instances', [])
            for service in service_instances:
                service_name = service['etht-svc-name']
                resource_key = '/services/service[{:s}]'.format(service_name)
                resource_value = {'uuid': service.get('etht-svc-name', '<UNDEFINED>')}

                for endpoint in service.get('etht-svc-end-points', []):
                    _vlan_id = get_vlan_outer_tag(endpoint)
                    if _vlan_id is not None:
                        vlan_id = resource_value.get('vlan_id')
                        if vlan_id is None:
                            resource_value['vlan_id'] = _vlan_id
                        elif vlan_id != _vlan_id:
                            raise Exception('Incompatible VLAN Ids: {:s}'.format(str(service)))
                    access_points = endpoint.get('etht-svc-access-points', [])
                    for access_point in access_points:
                        if access_point['access-point-id'] == '1':
                            resource_value['node_id_src'] = access_point['access-node-id']
                            resource_value['tp_id_src']   = access_point['access-ltp-id']
                        elif access_point['access-point-id'] == '2':
                            resource_value['node_id_dst'] = access_point['access-node-id']
                            resource_value['tp_id_dst']   = access_point['access-ltp-id']

                if len(node_ids) > 0:
                    node_id_src = resource_value.get('node_id_src')
                    if node_id_src is None: continue
                    if node_id_src not in node_ids: continue

                    node_id_dst = resource_value.get('node_id_dst')
                    if node_id_dst is None: continue
                    if node_id_dst not in node_ids: continue

                result.append((resource_key, resource_value))
        except requests.exceptions.Timeout:
            LOGGER.exception('Timeout connecting {:s}'.format(url))
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.exception('Exception retrieving/parsing services for {:s}'.format(resource_key))
            result.append((resource_key, e))

    return result

def create_connectivity_service(
    root_url, uuid, node_id_src, tp_id_src, node_id_dst, tp_id_dst, vlan_id,
    auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None
):

    url = '{:s}/nmswebs/restconf/data/ietf-eth-tran-service:etht-svc'.format(root_url)
    headers = {'content-type': 'application/json'}
    data = {
        'etht-svc-instances': [
            {
                'etht-svc-name': uuid,
                'etht-svc-type': 'ietf-eth-tran-types:p2p-svc',
                'etht-svc-end-points': [
                    {
                        'etht-svc-access-points': [
                            {'access-node-id': node_id_src, 'access-ltp-id': tp_id_src, 'access-point-id': '1'}
                        ],
                        'outer-tag': {'vlan-value': vlan_id, 'tag-type': 'ietf-eth-tran-types:classify-c-vlan'},
                        'etht-svc-end-point-name': '{:s}:{:s}'.format(str(node_id_src), str(tp_id_src)),
                        'service-classification-type': 'ietf-eth-tran-types:vlan-classification'
                    },
                    {
                        'etht-svc-access-points': [
                            {'access-node-id': node_id_dst, 'access-ltp-id': tp_id_dst, 'access-point-id': '2'}
                        ],
                        'outer-tag': {'vlan-value': vlan_id, 'tag-type': 'ietf-eth-tran-types:classify-c-vlan'},
                        'etht-svc-end-point-name': '{:s}:{:s}'.format(str(node_id_dst), str(tp_id_dst)),
                        'service-classification-type': 'ietf-eth-tran-types:vlan-classification'
                    }
                ]
            }
        ]
    }
    results = []
    try:
        LOGGER.info('Connectivity service {:s}: {:s}'.format(str(uuid), str(data)))
        response = requests.post(
            url=url, data=json.dumps(data), timeout=timeout, headers=headers, verify=False, auth=auth)
        LOGGER.info('Microwave Driver response: {:s}'.format(str(response)))
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception creating ConnectivityService(uuid={:s}, data={:s})'.format(str(uuid), str(data)))
        results.append(e)
    else:
        if response.status_code not in HTTP_OK_CODES:
            msg = 'Could not create ConnectivityService(uuid={:s}, data={:s}). status_code={:s} reply={:s}'
            LOGGER.error(msg.format(str(uuid), str(data), str(response.status_code), str(response)))
        results.append(response.status_code in HTTP_OK_CODES)
    return results

def delete_connectivity_service(root_url, uuid, auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None):
    url = '{:s}/nmswebs/restconf/data/ietf-eth-tran-service:etht-svc/etht-svc-instances={:s}'
    url = url.format(root_url, uuid)
    results = []
    try:
        response = requests.delete(url=url, timeout=timeout, verify=False, auth=auth)
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception deleting ConnectivityService(uuid={:s})'.format(str(uuid)))
        results.append(e)
    else:
        if response.status_code not in HTTP_OK_CODES:
            msg = 'Could not delete ConnectivityService(uuid={:s}). status_code={:s} reply={:s}'
            LOGGER.error(msg.format(str(uuid), str(response.status_code), str(response)))
        results.append(response.status_code in HTTP_OK_CODES)
    return results
