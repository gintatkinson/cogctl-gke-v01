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

from typing import Dict, Optional

def compose_service_endpoint_id(site_id : str, endpoint_id : Dict):
    device_uuid = endpoint_id['device_id']['device_uuid']['uuid']
    endpoint_uuid = endpoint_id['endpoint_uuid']['uuid']
    return ':'.join([site_id, device_uuid, endpoint_uuid])

def wim_mapping(site_id, ce_endpoint_id, pe_device_id : Optional[Dict] = None, priority=None, redundant=[]):
    ce_device_uuid = ce_endpoint_id['device_id']['device_uuid']['uuid']
    ce_endpoint_uuid = ce_endpoint_id['endpoint_uuid']['uuid']
    service_endpoint_id = compose_service_endpoint_id(site_id, ce_endpoint_id)
    if pe_device_id is None:
        bearer = '{:s}:{:s}'.format(ce_device_uuid, ce_endpoint_uuid)
    else:
        pe_device_uuid = pe_device_id['device_uuid']['uuid']
        bearer = '{:s}:{:s}'.format(ce_device_uuid, pe_device_uuid)
    mapping = {
        'service_endpoint_id': service_endpoint_id,
        'datacenter_id': site_id, 'device_id': ce_device_uuid, 'device_interface_id': ce_endpoint_uuid,
        'service_mapping_info': {
            'site-id': site_id,
            'bearer': {'bearer-reference': bearer},
        }
    }
    if priority is not None: mapping['service_mapping_info']['priority'] = priority
    if len(redundant) > 0: mapping['service_mapping_info']['redundant'] = redundant
    return service_endpoint_id, mapping

def connection_point(service_endpoint_id : str, encapsulation_type : str, vlan_id : int):
    return {
        'service_endpoint_id': service_endpoint_id,
        'service_endpoint_encapsulation_type': encapsulation_type,
        'service_endpoint_encapsulation_info': {'vlan': vlan_id}
    }
