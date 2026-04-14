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
from device.service.driver_api._Driver import RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES
from . import RESOURCE_APPS, RESOURCE_LINKS, RESOURCE_CAPABILITES, RESOURCE_NODE


LOGGER = logging.getLogger(__name__)

HTTP_OK_CODES = {
    200,    # OK
    201,    # Created
    202,    # Accepted
    204,    # No Content
}

def find_key(resource, key):
    return json.loads(resource[1])[key]



def config_getter(
    root_url : str, resource_key : str, auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None,
    node_ids : Set[str] = set(), headers={}
):
    # getting endpoints

    url = root_url + '/restconf/data/etsi-qkd-sdn-node:qkd_node/'


    result = []

    try:
        if resource_key in [RESOURCE_ENDPOINTS, RESOURCE_INTERFACES]:
            url += 'qkd_interfaces/'
            r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
            interfaces = r.json()['qkd_interfaces']['qkd_interface']

            # If it's a physical endpoint
            if resource_key == RESOURCE_ENDPOINTS:
                for interface in interfaces:
                    resource_value = interface.get('qkdi_att_point', {})
                    if 'device' in resource_value and 'port' in resource_value:
                        uuid = '{}:{}'.format(resource_value['device'], resource_value['port'])
                        resource_key = '/endpoints/endpoint[{:s}]'.format(uuid)
                        resource_value['uuid'] = uuid

                        sample_types = {}
                        metric_name = 'KPISAMPLETYPE_LINK_TOTAL_CAPACITY_GBPS'
                        metric_id = 301
                        metric_name = metric_name.lower().replace('kpisampletype_', '')
                        monitoring_resource_key = '{:s}/state/{:s}'.format(resource_key, metric_name)
                        sample_types[metric_id] = monitoring_resource_key



                        resource_value['sample_types'] = sample_types



                        result.append((resource_key, resource_value))
            else:
                for interface in interfaces:   
                    resource_key = '/interface[{:s}]'.format(interface['qkdi_id'])
                    endpoint_value = interface.get('qkdi_att_point', {})

                    if 'device' in endpoint_value and 'port' in endpoint_value:
                        name = '{}:{}'.format(endpoint_value['device'], endpoint_value['port'])
                        interface['name'] = name
                        interface['enabled'] = True # For test purpose only

                    result.append((resource_key, interface))
        
        elif resource_key in [RESOURCE_LINKS, RESOURCE_NETWORK_INSTANCES]:
            url += 'qkd_links/'
            r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
            links = r.json()['qkd_links']['qkd_link']

            if resource_key == RESOURCE_LINKS:
                for link in links:
                    link_type = link.get('qkdl_type', 'Direct')

                    if link_type == 'Direct':
                        resource_key = '/link[{:s}]'.format(link['qkdl_id'])
                        result.append((resource_key, link))
            else:
                for link in links:
                    link_type = link.get('qkdl_type', 'Direct')

                    if link_type == 'Virtual':
                        resource_key = '/service[{:s}]'.format(link['qkdl_id'])
                        result.append((resource_key, link))
        
        elif resource_key == RESOURCE_APPS:
            url += 'qkd_applications/'
            r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
            apps = r.json()['qkd_applications']['qkd_app']

            for app in apps:
                resource_key = '/app[{:s}]'.format(app['app_id'])
                result.append((resource_key, app))


        elif resource_key == RESOURCE_CAPABILITES:
            url += 'qkdn_capabilities/'
            r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
            capabilities = r.json()['qkdn_capabilities']

            result.append((resource_key, capabilities))
        
        elif resource_key == RESOURCE_NODE:
            r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
            node = r.json()['qkd_node']

            result.append((resource_key, node))

    except requests.exceptions.Timeout:
        LOGGER.exception('Timeout connecting {:s}'.format(url))
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception retrieving/parsing endpoints for {:s}'.format(resource_key))
        result.append((resource_key, e))


    return result



def create_connectivity_link(
    root_url, link_uuid, node_id_src, interface_id_src, node_id_dst, interface_id_dst,
    virt_prev_hop = None, virt_next_hops = None, virt_bandwidth = None,
    auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None, headers={}
):

    url = root_url + '/restconf/data/etsi-qkd-sdn-node:qkd_node/qkd_links/'
    is_virtual = bool(virt_prev_hop or virt_next_hops)

    qkd_link = {
        'qkdl_id': link_uuid,
        'qkdl_type': 'etsi-qkd-node-types:' + ('VIRT' if is_virtual else 'PHYS'), 
        'qkdl_local': {
            'qkdn_id': node_id_src,
            'qkdi_id': interface_id_src
        },
        'qkdl_remote': {
            'qkdn_id': node_id_dst,
            'qkdi_id': interface_id_dst
        }
    }

    if is_virtual:
        qkd_link['virt_prev_hop'] = virt_prev_hop
        qkd_link['virt_next_hop'] = virt_next_hops or []
        qkd_link['virt_bandwidth'] = virt_bandwidth
        

    data = {'qkd_links': {'qkd_link': [qkd_link]}}

    requests.post(url, json=data, headers=headers)

