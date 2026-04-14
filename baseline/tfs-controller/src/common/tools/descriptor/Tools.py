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

import collections
import copy, json
from typing import Dict, List, Optional, Tuple, Union
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import DeviceDriverEnum, LinkTypeEnum

def get_descriptors_add_contexts(contexts : List[Dict]) -> List[Dict]:
    contexts_add = copy.deepcopy(contexts)
    for context in contexts_add:
        context['topology_ids'] = []
        context['service_ids'] = []
        context['slice_ids'] = []
    return contexts_add

def get_descriptors_add_topologies(topologies : List[Dict]) -> List[Dict]:
    topologies_add = copy.deepcopy(topologies)
    for topology in topologies_add:
        topology['device_ids'] = []
        topology['link_ids'] = []
        topology['optical_link_ids'] = []
    return topologies_add

def get_descriptors_add_services(services : List[Dict]) -> List[Dict]:
    services_add = []
    for service in services:
        service_copy = copy.deepcopy(service)
        service_copy['service_endpoint_ids'] = []
        service_copy['service_constraints'] = []
        service_copy['service_config'] = {'config_rules': []}
        services_add.append(service_copy)
    return services_add

def get_descriptors_add_slices(slices : List[Dict]) -> List[Dict]:
    slices_add = []
    for slice_ in slices:
        slice_copy = copy.deepcopy(slice_)
        slice_copy['slice_endpoint_ids'] = []
        slice_copy['slice_constraints'] = []
        slice_copy['slice_config'] = {'config_rules': []}
        slices_add.append(slice_copy)
    return slices_add

TypeResourceValue = Union[str, int, bool, float, dict, list]
def format_custom_config_rules(config_rules : List[Dict]) -> List[Dict]:
    for config_rule in config_rules:
        if 'custom' not in config_rule: continue
        custom_resource_value : TypeResourceValue = config_rule['custom']['resource_value']
        if isinstance(custom_resource_value, (dict, list)):
            custom_resource_value = json.dumps(custom_resource_value, sort_keys=True, indent=0)
            config_rule['custom']['resource_value'] = custom_resource_value
        elif not isinstance(custom_resource_value, str):
            config_rule['custom']['resource_value'] = str(custom_resource_value)
    return config_rules

def format_device_custom_config_rules(device : Dict) -> Dict:
    config_rules = device.get('device_config', {}).get('config_rules', [])
    config_rules = format_custom_config_rules(config_rules)
    device.setdefault('device_config', {})['config_rules'] = config_rules
    return device

def format_service_custom_config_rules(service : Dict) -> Dict:
    config_rules = service.get('service_config', {}).get('config_rules', [])
    config_rules = format_custom_config_rules(config_rules)
    service.setdefault('service_config', {})['config_rules'] = config_rules
    return service

def format_slice_custom_config_rules(slice_ : Dict) -> Dict:
    config_rules = slice_.get('slice_config', {}).get('config_rules', [])
    config_rules = format_custom_config_rules(config_rules)
    slice_.setdefault('slice_config', {})['config_rules'] = config_rules
    return slice_

def split_devices_by_rules(devices : List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    devices_add = []
    devices_config = []
    for device in devices:
        connect_rules = []
        config_rules = []
        for config_rule in device.get('device_config', {}).get('config_rules', []):
            custom_resource_key : Optional[str] = config_rule.get('custom', {}).get('resource_key')
            if custom_resource_key is not None and custom_resource_key.startswith('_connect/'):
                connect_rules.append(config_rule)
            else:
                config_rules.append(config_rule)

        if len(connect_rules) > 0:
            device_add = copy.deepcopy(device)
            if (device['device_drivers'][0] != DeviceDriverEnum.DEVICEDRIVER_OC):
                device_add['device_endpoints'] = []
            device_add['device_config'] = {'config_rules': connect_rules}
            devices_add.append(device_add)

        if len(config_rules) > 0:
            device['device_config'] = {'config_rules': config_rules}
            devices_config.append(device)

    return devices_add, devices_config

CONTROLLER_DEVICE_TYPES = {
    DeviceTypeEnum.EMULATED_IP_SDN_CONTROLLER.value,
    DeviceTypeEnum.EMULATED_MICROWAVE_RADIO_SYSTEM.value,
    DeviceTypeEnum.EMULATED_OPEN_LINE_SYSTEM.value,
    DeviceTypeEnum.IP_SDN_CONTROLLER.value,
    DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM.value,
    DeviceTypeEnum.OPEN_LINE_SYSTEM.value,
    DeviceTypeEnum.TERAFLOWSDN_CONTROLLER.value,
    DeviceTypeEnum.IETF_SLICE.value,
    DeviceTypeEnum.NCE.value,
}

def split_controllers_and_network_devices(devices : List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    controllers     : List[Dict] = list()
    network_devices : List[Dict] = list()
    for device in devices:
        device_type = device.get('device_type')
        if device_type in CONTROLLER_DEVICE_TYPES:
            controllers.append(device)
        else:
            network_devices.append(device)
    return controllers, network_devices

def link_type_to_str(link_type : Union[int, str]) -> Optional[str]:
    if isinstance(link_type, int): return LinkTypeEnum.Name(link_type)
    if isinstance(link_type, str): return LinkTypeEnum.Name(LinkTypeEnum.Value(link_type))
    return None

LINK_TYPES_NORMAL = {
    LinkTypeEnum.LINKTYPE_UNKNOWN,
    LinkTypeEnum.LINKTYPE_COPPER,
    LinkTypeEnum.LINKTYPE_RADIO,
    LinkTypeEnum.LINKTYPE_MANAGEMENT,
}
LINK_TYPES_OPTICAL = {
    LinkTypeEnum.LINKTYPE_FIBER,
}
LINK_TYPES_VIRTUAL = {
    LinkTypeEnum.LINKTYPE_VIRTUAL,
}

def split_links_by_type(links : List[Dict]) -> Dict[str, List[Dict]]:
    typed_links = collections.defaultdict(list)
    for link in links:
        link_type = link.get('link_type', LinkTypeEnum.LINKTYPE_UNKNOWN)
        str_link_type = link_type_to_str(link_type)
        if str_link_type is None:
            MSG = 'Unsupported LinkType in Link({:s})'
            raise Exception(MSG.format(str(link)))

        link_type = LinkTypeEnum.Value(str_link_type)
        if link_type in LINK_TYPES_NORMAL:
            typed_links['normal'].append(link)
        elif link_type in LINK_TYPES_OPTICAL:
            typed_links['optical'].append(link)
        elif link_type in LINK_TYPES_VIRTUAL:
            typed_links['virtual'].append(link)
        else:
            MSG = 'Unsupported LinkType({:s}) in Link({:s})'
            raise Exception(MSG.format(str_link_type, str(link)))

    return typed_links
