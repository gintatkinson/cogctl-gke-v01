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

import json
import logging
import requests
from typing import Dict, Optional, Set, List, Tuple, Union, Any
from device.service.driver_api._Driver import RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES
from . import RESOURCE_APPS, RESOURCE_LINKS, RESOURCE_CAPABILITES, RESOURCE_NODE

LOGGER = logging.getLogger(__name__)

HTTP_OK_CODES = {200, 201, 202, 204}

def find_key(resource: Tuple[str, str], key: str) -> Any:
    """
    Extracts a specific key from a JSON resource.
    """
    return json.loads(resource[1]).get(key)


def config_getter(
    root_url: str, resource_key: str, auth: Optional[Any] = None, timeout: Optional[int] = None,
    node_ids: Set[str] = set(), headers: Dict[str, str] = {}
) -> List[Tuple[str, Union[Dict[str, Any], Exception]]]:
    """
    Fetches configuration data from a QKD node for a specified resource key.
    Returns a list of tuples containing the resource key and the corresponding data or exception.
    The function is agnostic to authentication: headers and auth are passed from external sources.
    """
    url = f"{root_url}/restconf/data/etsi-qkd-sdn-node:qkd_node/"
    LOGGER.info(f"Fetching configuration for {resource_key} from {root_url}")

    try:
        if resource_key in [RESOURCE_ENDPOINTS, RESOURCE_INTERFACES]:
            return fetch_interfaces(url, resource_key, headers, auth, timeout)

        elif resource_key in [RESOURCE_LINKS, RESOURCE_NETWORK_INSTANCES]:
            return fetch_links(url, resource_key, headers, auth, timeout)

        elif resource_key in [RESOURCE_APPS]:
            return fetch_apps(url, resource_key, headers, auth, timeout)

        elif resource_key in [RESOURCE_CAPABILITES]:
            return fetch_capabilities(url, resource_key, headers, auth, timeout)

        elif resource_key in [RESOURCE_NODE]:
            return fetch_node(url, resource_key, headers, auth, timeout)

        else:
            LOGGER.warning(f"Unknown resource key: {resource_key}")
            return [(resource_key, ValueError(f"Unknown resource key: {resource_key}"))]

    except requests.exceptions.RequestException as e:
        LOGGER.error(f'Error retrieving/parsing {resource_key} from {url}: {e}')
        return [(resource_key, e)]


def fetch_interfaces(url: str, resource_key: str, headers: Dict[str, str], auth: Optional[Any], timeout: Optional[int]) -> List[Tuple[str, Union[Dict[str, Any], Exception]]]:
    """
    Fetches interface data from the QKD node. Adapts to both mocked and real QKD data structures.
    """
    result = []
    url += 'qkd_interfaces/'
    
    try:
        r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
        r.raise_for_status()

        # Handle both real and mocked QKD response structures
        response_data = r.json()

        if isinstance(response_data.get('qkd_interfaces'), dict):
            interfaces = response_data.get('qkd_interfaces', {}).get('qkd_interface', [])
        else:
            interfaces = response_data.get('qkd_interface', [])

        for interface in interfaces:
            if resource_key in [RESOURCE_ENDPOINTS]:
                # Handle real QKD data format
                resource_value = interface.get('qkdi_att_point', {})
                if 'device' in resource_value and 'port' in resource_value:
                    uuid = f"{resource_value['device']}:{resource_value['port']}"
                    resource_key_with_uuid = f"/endpoints/endpoint[{uuid}]"
                    resource_value['uuid'] = uuid

                    # Add sample types (for demonstration purposes)
                    sample_types = {}
                    metric_name = 'KPISAMPLETYPE_LINK_TOTAL_CAPACITY_GBPS'
                    metric_id = 301
                    metric_name = metric_name.lower().replace('kpisampletype_', '')
                    monitoring_resource_key = '{:s}/state/{:s}'.format(resource_key, metric_name)
                    sample_types[metric_id] = monitoring_resource_key
                    resource_value['sample_types'] = sample_types

                    result.append((resource_key_with_uuid, resource_value))

            else:
                # Handle both real and mocked QKD formats
                endpoint_value = interface.get('qkdi_att_point', {})
                if 'device' in endpoint_value and 'port' in endpoint_value:
                    # Real QKD data format
                    interface_uuid = f"{endpoint_value['device']}:{endpoint_value['port']}"
                    interface['uuid'] = interface_uuid
                    interface['name'] = interface_uuid
                    interface['enabled'] = True  # Assume enabled for real data
                else:
                    # Mocked QKD data format
                    interface_uuid = interface.get('uuid', f"/interface[{interface['qkdi_id']}]")
                    interface['uuid'] = interface_uuid
                    interface['name'] = interface.get('name', interface_uuid)
                    interface['enabled'] = interface.get('enabled', False)  # Mocked enabled status

                result.append((f"/interface[{interface['qkdi_id']}]", interface))

    except requests.RequestException as e:
        LOGGER.error(f"Error fetching interfaces from {url}: {e}")
        result.append((resource_key, e))
    
    return result

def fetch_links(url: str, resource_key: str, headers: Dict[str, str], auth: Optional[Any], timeout: Optional[int]) -> List[Tuple[str, Union[Dict[str, Any], Exception]]]:
    """
    Fetches link data from the QKD node. Adapts to both mocked and real QKD data structures.
    """
    result = []
    
    if resource_key in [RESOURCE_LINKS, RESOURCE_NETWORK_INSTANCES]:
        url += 'qkd_links/'
        
        try:
            r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
            r.raise_for_status()
            
            # Handle real and mocked QKD data structures
            links = r.json().get('qkd_links', [])
            
            for link in links:
                # For real QKD format (QKD links returned as dictionary objects)
                if isinstance(link, dict):
                    qkdl_id = link.get('qkdl_id')
                    link_type = link.get('qkdl_type', 'Direct')
                    
                    # Handle both real (PHYS, VIRT) and mocked (DIRECT) link types
                    if link_type == 'PHYS' or link_type == 'VIRT':
                        resource_key_direct = f"/link[{qkdl_id}]"
                        result.append((resource_key_direct, link))
                    elif link_type == 'DIRECT':
                        # Mocked QKD format has a slightly different structure
                        result.append((f"/link/link[{qkdl_id}]", link))

                # For mocked QKD format (QKD links returned as lists)
                elif isinstance(link, list):
                    for l in link:
                        qkdl_id = l.get('uuid')
                        link_type = l.get('type', 'Direct')
                        
                        if link_type == 'DIRECT':
                            resource_key_direct = f"/link/link[{qkdl_id}]"
                            result.append((resource_key_direct, l))
        
        except requests.RequestException as e:
            LOGGER.error(f"Error fetching links from {url}: {e}")
            result.append((resource_key, e))
    
    return result

def fetch_apps(url: str, resource_key: str, headers: Dict[str, str], auth: Optional[Any], timeout: Optional[int]) -> List[Tuple[str, Union[Dict[str, Any], Exception]]]:
    """
    Fetches application data from the QKD node.
    """
    result = []
    url += 'qkd_applications/'
    
    try:
        r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
        r.raise_for_status()
        
        apps = r.json().get('qkd_applications', {}).get('qkd_app', [])
        for app in apps:
            result.append((f"/app[{app['app_id']}]", app))
    except requests.RequestException as e:
        LOGGER.error(f"Error fetching applications from {url}: {e}")
        result.append((resource_key, e))
    
    return result


def fetch_capabilities(url: str, resource_key: str, headers: Dict[str, str], auth: Optional[Any], timeout: Optional[int]) -> List[Tuple[str, Union[Dict[str, Any], Exception]]]:
    """
    Fetches capabilities data from the QKD node.
    """
    result = []
    url += 'qkdn_capabilities/'
    
    try:
        r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
        r.raise_for_status()
        result.append((resource_key, r.json()))
    except requests.RequestException as e:
        LOGGER.error(f"Error fetching capabilities from {url}: {e}")
        result.append((resource_key, e))
    
    return result


def fetch_node(url: str, resource_key: str, headers: Dict[str, str], auth: Optional[Any], timeout: Optional[int]) -> List[Tuple[str, Union[Dict[str, Any], Exception]]]:
    """
    Fetches node data from the QKD node.
    """
    result = []
    
    try:
        r = requests.get(url, timeout=timeout, verify=False, auth=auth, headers=headers)
        r.raise_for_status()
        data = r.json()
        data.pop('qkdn_capabilities', None)
        data.pop('qkd_applications', None)
        data.pop('qkd_interfaces', None)
        data.pop('qkd_links', None)
        result.append((resource_key, data))
    except requests.RequestException as e:
        LOGGER.error(f"Error fetching node from {url}: {e}")
        result.append((resource_key, e))

    return result


def create_connectivity_link(
    root_url: str, link_uuid: str, node_id_src: str, interface_id_src: str, node_id_dst: str, interface_id_dst: str,
    virt_prev_hop: Optional[str] = None, virt_next_hops: Optional[List[str]] = None, virt_bandwidth: Optional[int] = None,
    auth: Optional[Any] = None, timeout: Optional[int] = None, headers: Dict[str, str] = {}
) -> Union[bool, Exception]:
    """
    Creates a connectivity link between QKD nodes using the provided parameters.
    """
    url = f"{root_url}/restconf/data/etsi-qkd-sdn-node:qkd_node/qkd_links/"
    
    qkd_link = {
        'qkdl_id': link_uuid,
        'qkdl_type': 'etsi-qkd-node-types:' + ('VIRT' if virt_prev_hop or virt_next_hops else 'PHYS'),
        'qkdl_local': {'qkdn_id': node_id_src, 'qkdi_id': interface_id_src},
        'qkdl_remote': {'qkdn_id': node_id_dst, 'qkdi_id': interface_id_dst}
    }

    if virt_prev_hop or virt_next_hops:
        qkd_link['virt_prev_hop'] = virt_prev_hop
        qkd_link['virt_next_hop'] = virt_next_hops or []
        qkd_link['virt_bandwidth'] = virt_bandwidth

    data = {'qkd_links': {'qkd_link': [qkd_link]}}

    LOGGER.info(f"Creating connectivity link with payload: {json.dumps(data)}")

    try:
        r = requests.post(url, json=data, timeout=timeout, verify=False, auth=auth, headers=headers)
        r.raise_for_status()
        if r.status_code in HTTP_OK_CODES:
            LOGGER.info(f"Link {link_uuid} created successfully.")
            return True
        else:
            LOGGER.error(f"Failed to create link {link_uuid}, status code: {r.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        LOGGER.error(f"Exception creating link {link_uuid} with payload {json.dumps(data)}: {e}")
        return e
