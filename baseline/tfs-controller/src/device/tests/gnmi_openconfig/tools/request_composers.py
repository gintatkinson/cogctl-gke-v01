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

from typing import Dict, Tuple

def interface(if_name, sif_index, ipv4_address, ipv4_prefix, enabled) -> Tuple[str, Dict]:
    str_path = '/interface[{:s}]'.format(if_name)
    str_data = {
        'name': if_name, 'enabled': enabled, 'sub_if_index': sif_index, 'sub_if_enabled': enabled,
        'sub_if_ipv4_enabled': enabled, 'sub_if_ipv4_address': ipv4_address, 'sub_if_ipv4_prefix': ipv4_prefix
    }
    return str_path, str_data

def network_instance(ni_name, ni_type) -> Tuple[str, Dict]:
    str_path = '/network_instance[{:s}]'.format(ni_name)
    str_data = {
        'name': ni_name, 'type': ni_type
    }
    return str_path, str_data

def network_instance_static_route(ni_name, prefix, next_hop_index, next_hop, metric=1) -> Tuple[str, Dict]:
    str_path = '/network_instance[{:s}]/static_route[{:s}]'.format(ni_name, prefix)
    str_data = {
        'name': ni_name, 'prefix': prefix, 'next_hop_index': next_hop_index, 'next_hop': next_hop, 'metric': metric
    }
    return str_path, str_data

def network_instance_interface(ni_name, if_name, sif_index) -> Tuple[str, Dict]:
    str_path = '/network_instance[{:s}]/interface[{:s}.{:d}]'.format(ni_name, if_name, sif_index)
    str_data = {
        'name': ni_name, 'if_name': if_name, 'sif_index': sif_index
    }
    return str_path, str_data
