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

import copy, itertools, json, logging, re
from typing import Dict, Iterable, List, Optional, Set, Tuple
from common.proto.context_pb2 import ConfigRule
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.ConfigRule import json_config_rule_set

LOGGER = logging.getLogger(__name__)

SETTINGS_RULE_NAME = '/settings'
STATIC_ROUTING_RULE_NAME = '/static_routing'
RUNNING_RESOURCE_KEY = "running_ietf_slice"
CANDIDATE_RESOURCE_KEY = "candidate_ietf_slice"

RE_UUID = re.compile(r'([0-9a-fA-F]{8})\-([0-9a-fA-F]{4})\-([0-9a-fA-F]{4})\-([0-9a-fA-F]{4})\-([0-9a-fA-F]{12})')

RE_DEVICE_SETTINGS        = re.compile(r'\/device\[([^\]]+)\]\/settings')
RE_ENDPOINT_SETTINGS      = re.compile(r'\/device\[([^\]]+)\]\/endpoint\[([^\]]+)\]\/settings')
RE_ENDPOINT_VLAN_SETTINGS = re.compile(r'\/device\[([^\]]+)\]\/endpoint\[([^\]]+)\]\/vlan\[([^\]]+)\]\/settings')

TMPL_ENDPOINT_SETTINGS      = '/device[{:s}]/endpoint[{:s}]/settings'
TMPL_ENDPOINT_VLAN_SETTINGS = '/device[{:s}]/endpoint[{:s}]/vlan[{:s}]/settings'

L2NM_SETTINGS_FIELD_DEFAULTS = {
    #'encapsulation_type': 'dot1q',
    #'vlan_id'           : 100,
    'mtu'               : 1450,
}

L3NM_SETTINGS_FIELD_DEFAULTS = {
    #'encapsulation_type': 'dot1q',
    #'vlan_id'           : 100,
    'mtu'               : 1450,
}

TAPI_SETTINGS_FIELD_DEFAULTS = {
    'capacity_value'  : 50.0,
    'capacity_unit'   : 'GHz',
    'layer_proto_name': 'PHOTONIC_MEDIA',
    'layer_proto_qual': 'tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC',
    'direction'       : 'UNIDIRECTIONAL',
}

IPLINK_SETTINGS_FIELD_DEFAULTS = {
    'mtu'               : 1450,
}

def find_custom_config_rule(config_rules : List, resource_name : str) -> Optional[Dict]:
    resource_value : Optional[Dict] = None
    for config_rule in config_rules:
        if config_rule.WhichOneof('config_rule') != 'custom': continue
        if config_rule.custom.resource_key != resource_name: continue
        resource_value = json.loads(config_rule.custom.resource_value)
    return resource_value

def compose_config_rules(
    main_service_config_rules : List, subservice_config_rules : List, settings_rule_name : str, field_defaults : Dict
) -> None:
    settings = find_custom_config_rule(main_service_config_rules, settings_rule_name)
    if settings is None: return

    json_settings = {}

    if len(field_defaults) == 0:
        for field_name,field_value in settings.items():
            json_settings[field_name] = field_value
    else:
        for field_name,default_value in field_defaults.items():
            field_value = settings.get(field_name, default_value)
            if field_value is None: continue
            json_settings[field_name] = field_value

    if len(json_settings) == 0: return

    config_rule = ConfigRule(**json_config_rule_set(settings_rule_name, json_settings))
    subservice_config_rules.append(config_rule)

def compose_l2nm_config_rules(main_service_config_rules : List, subservice_config_rules : List) -> None:
    CONFIG_RULES = [
        (SETTINGS_RULE_NAME, L2NM_SETTINGS_FIELD_DEFAULTS),
    ]
    for rule_name, defaults in CONFIG_RULES:
        compose_config_rules(main_service_config_rules, subservice_config_rules, rule_name, defaults)

def compose_l3nm_config_rules(main_service_config_rules : List, subservice_config_rules : List) -> None:
    CONFIG_RULES = [
        (SETTINGS_RULE_NAME, L3NM_SETTINGS_FIELD_DEFAULTS),
        (STATIC_ROUTING_RULE_NAME, {}),
        (RUNNING_RESOURCE_KEY, {}),
        (CANDIDATE_RESOURCE_KEY, {}),
    ]
    for rule_name, defaults in CONFIG_RULES:
        compose_config_rules(main_service_config_rules, subservice_config_rules, rule_name, defaults)

def compose_tapi_config_rules(main_service_config_rules : List, subservice_config_rules : List) -> None:
    CONFIG_RULES = [
        (SETTINGS_RULE_NAME, TAPI_SETTINGS_FIELD_DEFAULTS),
    ]
    for rule_name, defaults in CONFIG_RULES:
        compose_config_rules(main_service_config_rules, subservice_config_rules, rule_name, defaults)

def compose_iplink_config_rules(main_service_config_rules : List, subservice_config_rules : List) -> None:
    CONFIG_RULES: List[Tuple[str, dict]] = [(SETTINGS_RULE_NAME, IPLINK_SETTINGS_FIELD_DEFAULTS)]
    for rule_name, defaults in CONFIG_RULES:
        compose_config_rules(main_service_config_rules, subservice_config_rules, rule_name, defaults)

def compose_device_config_rules(
    config_rules : List, subservice_config_rules : List, path_hops : List,
    device_name_mapping : Dict[str, str], endpoint_name_mapping : Dict[Tuple[str, str], str]
) -> None:
    LOGGER.debug('[compose_device_config_rules] begin')

    LOGGER.debug('[compose_device_config_rules] device_name_mapping={:s}'.format(str(device_name_mapping)))
    LOGGER.debug('[compose_device_config_rules] endpoint_name_mapping={:s}'.format(str(endpoint_name_mapping)))

    devices_traversed = set()
    endpoints_traversed = set()
    for path_hop in path_hops:
        device_uuid_or_name = path_hop['device']
        devices_traversed.add(device_uuid_or_name)
        endpoints_traversed.add((device_uuid_or_name, path_hop['ingress_ep']))
        endpoints_traversed.add((device_uuid_or_name, path_hop['egress_ep']))

    LOGGER.debug('[compose_device_config_rules] devices_traversed={:s}'.format(str(devices_traversed)))
    LOGGER.debug('[compose_device_config_rules] endpoints_traversed={:s}'.format(str(endpoints_traversed)))

    for config_rule in config_rules:
        LOGGER.debug('[compose_device_config_rules] processing config_rule: {:s}'.format(
            grpc_message_to_json_string(config_rule)))

        if config_rule.WhichOneof('config_rule') == 'acl':
            LOGGER.debug('[compose_device_config_rules]   is acl')
            endpoint_id = config_rule.acl.endpoint_id
            device_uuid_or_name = endpoint_id.device_id.device_uuid.uuid
            LOGGER.debug('[compose_device_config_rules]   device_uuid_or_name={:s}'.format(str(device_uuid_or_name)))
            device_name_or_uuid = device_name_mapping.get(device_uuid_or_name, device_uuid_or_name)
            LOGGER.debug('[compose_device_config_rules]   device_name_or_uuid={:s}'.format(str(device_name_or_uuid)))
            device_keys = {device_uuid_or_name, device_name_or_uuid}
            if len(device_keys.intersection(devices_traversed)) == 0: continue

            endpoint_uuid = endpoint_id.endpoint_uuid.uuid
            LOGGER.debug('[compose_device_config_rules]   endpoint_uuid={:s}'.format(str(endpoint_uuid)))
            # given endpoint uuids link 'eth-1/0/20.533', remove last part after the '.'
            endpoint_uuid_or_name = (endpoint_uuid[::-1].split('.', maxsplit=1)[-1])[::-1]
            LOGGER.debug('[compose_device_config_rules]   endpoint_uuid_or_name={:s}'.format(str(endpoint_uuid_or_name)))
            endpoint_name_or_uuid_1 = endpoint_name_mapping[(device_uuid_or_name, endpoint_uuid_or_name)]
            endpoint_name_or_uuid_2 = endpoint_name_mapping[(device_name_or_uuid, endpoint_uuid_or_name)]
            endpoint_keys = {endpoint_uuid_or_name, endpoint_name_or_uuid_1, endpoint_name_or_uuid_2}

            device_endpoint_keys = set(itertools.product(device_keys, endpoint_keys))
            if len(device_endpoint_keys.intersection(endpoints_traversed)) == 0: continue

            LOGGER.debug('[compose_device_config_rules]   adding acl config rule')
            subservice_config_rules.append(config_rule)

        elif config_rule.WhichOneof('config_rule') == 'ip_link':
            LOGGER.debug('[compose_device_config_rules]   is ip_link')
            endpoint_id = config_rule.ip_link.endpoint_id
            device_uuid_or_name = endpoint_id.device_id.device_uuid.uuid
            LOGGER.debug('[compose_device_config_rules]   device_uuid_or_name={:s}'.format(str(device_uuid_or_name)))
            device_name_or_uuid = device_name_mapping.get(device_uuid_or_name, device_uuid_or_name)
            LOGGER.debug('[compose_device_config_rules]   device_name_or_uuid={:s}'.format(str(device_name_or_uuid)))
            device_keys = {device_uuid_or_name, device_name_or_uuid}
            if len(device_keys.intersection(devices_traversed)) == 0: continue

            endpoint_uuid = endpoint_id.endpoint_uuid.uuid
            LOGGER.debug('[compose_device_config_rules]   endpoint_uuid={:s}'.format(str(endpoint_uuid)))
            endpoint_uuid_or_name = (endpoint_uuid[::-1].split('.', maxsplit=1)[-1])[::-1]
            LOGGER.debug('[compose_device_config_rules]   endpoint_uuid_or_name={:s}'.format(str(endpoint_uuid_or_name)))
            endpoint_name_or_uuid_1 = endpoint_name_mapping[(device_uuid_or_name, endpoint_uuid_or_name)]
            endpoint_name_or_uuid_2 = endpoint_name_mapping[(device_name_or_uuid, endpoint_uuid_or_name)]
            endpoint_keys = {endpoint_uuid_or_name, endpoint_name_or_uuid_1, endpoint_name_or_uuid_2}

            device_endpoint_keys = set(itertools.product(device_keys, endpoint_keys))
            if len(device_endpoint_keys.intersection(endpoints_traversed)) == 0: continue

            LOGGER.debug('[compose_device_config_rules]   adding ip_link config rule')
            subservice_config_rules.append(config_rule)

        elif config_rule.WhichOneof('config_rule') == 'custom':
            LOGGER.debug('[compose_device_config_rules]   is custom')

            match = RE_DEVICE_SETTINGS.match(config_rule.custom.resource_key)
            if match is not None:
                device_uuid_or_name = match.group(1)
                device_keys = {device_uuid_or_name}
                device_name_or_uuid = device_name_mapping.get(device_uuid_or_name)
                if device_name_or_uuid is not None: device_keys.add(device_name_or_uuid)

                if len(device_keys.intersection(devices_traversed)) == 0: continue
                subservice_config_rules.append(config_rule)

            match = RE_ENDPOINT_SETTINGS.match(config_rule.custom.resource_key)
            if match is None:
                match = RE_ENDPOINT_VLAN_SETTINGS.match(config_rule.custom.resource_key)
            if match is not None:
                device_uuid_or_name = match.group(1)
                device_keys = {device_uuid_or_name}
                device_name_or_uuid = device_name_mapping.get(device_uuid_or_name)
                if device_name_or_uuid is not None: device_keys.add(device_name_or_uuid)

                endpoint_uuid_or_name = match.group(2)
                endpoint_keys = {endpoint_uuid_or_name}
                endpoint_name_or_uuid_1 = endpoint_name_mapping.get((device_uuid_or_name, endpoint_uuid_or_name))
                if endpoint_name_or_uuid_1 is not None: endpoint_keys.add(endpoint_name_or_uuid_1)
                endpoint_name_or_uuid_2 = endpoint_name_mapping.get((device_name_or_uuid, endpoint_uuid_or_name))
                if endpoint_name_or_uuid_2 is not None: endpoint_keys.add(endpoint_name_or_uuid_2)

                device_endpoint_keys = set(itertools.product(device_keys, endpoint_keys))
                if len(device_endpoint_keys.intersection(endpoints_traversed)) == 0: continue

                # TODO: check if vlan needs to be removed from config_rule
                #config_rule.custom.resource_key = re.sub('\/vlan\[[^\]]+\]', '', config_rule.custom.resource_key)

                subservice_config_rules.append(config_rule)
        else:
            continue

    for config_rule in subservice_config_rules:
        LOGGER.debug('[compose_device_config_rules] result config_rule: {:s}'.format(
            grpc_message_to_json_string(config_rule)))

    LOGGER.debug('[compose_device_config_rules] end')

def compose_ipowdm_config_rules(main_service_config_rules : List, subservice_config_rules : List) -> None:
    CONFIG_RULES: List[Tuple[str, dict]] = [(SETTINGS_RULE_NAME, L3NM_SETTINGS_FIELD_DEFAULTS)]
    for rule_name, defaults in CONFIG_RULES:
        compose_config_rules(main_service_config_rules, subservice_config_rules, rule_name, defaults)

def compose_tapi_lsp_config_rules(main_service_config_rules : List, subservice_config_rules : List) -> None:
    CONFIG_RULES: List[Tuple[str, dict]] = [(SETTINGS_RULE_NAME, TAPI_SETTINGS_FIELD_DEFAULTS)]
    for rule_name, defaults in CONFIG_RULES:
        compose_config_rules(main_service_config_rules, subservice_config_rules, rule_name, defaults)

def pairwise(iterable : Iterable) -> Tuple[Iterable, Iterable]:
    # TODO: To be replaced by itertools.pairwise() when we move to Python 3.10
    # Python 3.10 introduced method itertools.pairwise()
    # Standalone method extracted from:
    # - https://docs.python.org/3/library/itertools.html#itertools.pairwise
    a, b = itertools.tee(iterable, 2)
    next(b, None)
    return zip(a, b)

def compute_device_keys(
    device_uuid_or_name : str, device_name_mapping : Dict[str, str]
) -> Set[str]:
    LOGGER.debug('[compute_device_keys] begin')
    LOGGER.debug('[compute_device_keys] device_uuid_or_name={:s}'.format(str(device_uuid_or_name)))
    #LOGGER.debug('[compute_device_keys] device_name_mapping={:s}'.format(str(device_name_mapping)))

    device_keys = {device_uuid_or_name}
    for k,v in device_name_mapping.items():
        if device_uuid_or_name not in {k, v}: continue
        device_keys.add(k)
        device_keys.add(v)

    LOGGER.debug('[compute_device_keys] device_keys={:s}'.format(str(device_keys)))
    LOGGER.debug('[compute_device_keys] end')
    return device_keys

def compute_endpoint_keys(
    device_keys : Set[str], endpoint_uuid_or_name : str, endpoint_name_mapping : Dict[str, str]
) -> Set[str]:
    LOGGER.debug('[compute_endpoint_keys] begin')
    LOGGER.debug('[compute_endpoint_keys] device_keys={:s}'.format(str(device_keys)))
    LOGGER.debug('[compute_endpoint_keys] endpoint_uuid_or_name={:s}'.format(str(endpoint_uuid_or_name)))
    #LOGGER.debug('[compute_device_endpoint_keys] endpoint_name_mapping={:s}'.format(str(endpoint_name_mapping)))

    endpoint_keys = {endpoint_uuid_or_name}
    for k,v in endpoint_name_mapping.items():
        if (k[0] in device_keys or v in device_keys) and (endpoint_uuid_or_name in {k[1], v}):
            endpoint_keys.add(k[1])
            endpoint_keys.add(v)

    LOGGER.debug('[compute_endpoint_keys] endpoint_keys={:s}'.format(str(endpoint_keys)))
    LOGGER.debug('[compute_endpoint_keys] end')
    return endpoint_keys

def compute_device_endpoint_keys(
    device_uuid_or_name : str, endpoint_uuid_or_name : str,
    device_name_mapping : Dict[str, str], endpoint_name_mapping : Dict[Tuple[str, str], str]
) -> Set[Tuple[str, str]]:
    LOGGER.debug('[compute_device_endpoint_keys] begin')
    LOGGER.debug('[compute_device_endpoint_keys] device_uuid_or_name={:s}'.format(str(device_uuid_or_name)))
    LOGGER.debug('[compute_device_endpoint_keys] endpoint_uuid_or_name={:s}'.format(str(endpoint_uuid_or_name)))
    #LOGGER.debug('[compute_device_endpoint_keys] device_name_mapping={:s}'.format(str(device_name_mapping)))
    #LOGGER.debug('[compute_device_endpoint_keys] endpoint_name_mapping={:s}'.format(str(endpoint_name_mapping)))

    device_keys = compute_device_keys(device_uuid_or_name, device_name_mapping)
    endpoint_keys = compute_endpoint_keys(device_keys, endpoint_uuid_or_name, endpoint_name_mapping)
    device_endpoint_keys = set(itertools.product(device_keys, endpoint_keys))

    LOGGER.debug('[compute_device_endpoint_keys] device_endpoint_keys={:s}'.format(str(device_endpoint_keys)))
    LOGGER.debug('[compute_device_endpoint_keys] end')
    return device_endpoint_keys

def generate_neighbor_endpoint_config_rules(
    config_rules : List[Dict], path_hops : List[Dict],
    device_name_mapping : Dict[str, str], endpoint_name_mapping : Dict[Tuple[str, str], str]
) -> List[Dict]:
    LOGGER.debug('[generate_neighbor_endpoint_config_rules] begin')
    LOGGER.debug('[generate_neighbor_endpoint_config_rules] config_rules={:s}'.format(str(config_rules)))
    LOGGER.debug('[generate_neighbor_endpoint_config_rules] path_hops={:s}'.format(str(path_hops)))
    LOGGER.debug('[generate_neighbor_endpoint_config_rules] device_name_mapping={:s}'.format(str(device_name_mapping)))
    LOGGER.debug('[generate_neighbor_endpoint_config_rules] endpoint_name_mapping={:s}'.format(str(endpoint_name_mapping)))

    generated_config_rules = list()
    for link_endpoint_a, link_endpoint_b in pairwise(path_hops):
        LOGGER.debug('[generate_neighbor_endpoint_config_rules] loop begin')
        LOGGER.debug('[generate_neighbor_endpoint_config_rules] link_endpoint_a={:s}'.format(str(link_endpoint_a)))
        LOGGER.debug('[generate_neighbor_endpoint_config_rules] link_endpoint_b={:s}'.format(str(link_endpoint_b)))

        device_endpoint_keys_a = compute_device_endpoint_keys(
            link_endpoint_a['device'], link_endpoint_a['egress_ep'],
            device_name_mapping, endpoint_name_mapping
        )

        device_endpoint_keys_b = compute_device_endpoint_keys(
            link_endpoint_b['device'], link_endpoint_b['ingress_ep'],
            device_name_mapping, endpoint_name_mapping
        )

        for config_rule in config_rules:
            # Only applicable, by now, to Custom Config Rules for endpoint settings
            if 'custom' not in config_rule or 'ip_link' not in config_rule: continue
            if 'custom'  in config_rule:
                match = RE_ENDPOINT_SETTINGS.match(config_rule['custom']['resource_key'])
                if match is None:
                    match = RE_ENDPOINT_VLAN_SETTINGS.match(config_rule['custom']['resource_key'])
                if match is None: continue
                resource_key_values = match.groups()
                if resource_key_values[0:2] in device_endpoint_keys_a:
                    resource_key_values = list(resource_key_values)
                    resource_key_values[0] = link_endpoint_b['device']
                    resource_key_values[1] = link_endpoint_b['ingress_ep']
                elif resource_key_values[0:2] in device_endpoint_keys_b:
                    resource_key_values = list(resource_key_values)
                    resource_key_values[0] = link_endpoint_a['device']
                    resource_key_values[1] = link_endpoint_a['egress_ep']
                else:
                    continue

                device_keys = compute_device_keys(resource_key_values[0], device_name_mapping)
                device_names = {device_key for device_key in device_keys if RE_UUID.match(device_key) is None}
                if len(device_names) != 1:
                    MSG = 'Unable to identify name for Device({:s}): device_keys({:s})'
                    raise Exception(MSG.format(str(resource_key_values[0]), str(device_keys)))
                resource_key_values[0] = device_names.pop()

                endpoint_keys = compute_endpoint_keys(device_keys, resource_key_values[1], endpoint_name_mapping)
                endpoint_names = {endpoint_key for endpoint_key in endpoint_keys if RE_UUID.match(endpoint_key) is None}
                if len(endpoint_names) != 1:
                    MSG = 'Unable to identify name for Endpoint({:s}): endpoint_keys({:s})'
                    raise Exception(MSG.format(str(resource_key_values[1]), str(endpoint_keys)))
                resource_key_values[1] = endpoint_names.pop()

                resource_value : Dict = json.loads(config_rule['custom']['resource_value'])
                if 'neighbor_address' not in resource_value: continue
                resource_value['ip_address'] = resource_value.pop('neighbor_address')

                # remove neighbor_address also from original rule as it is already consumed

                resource_key_template = TMPL_ENDPOINT_VLAN_SETTINGS if len(match.groups()) == 3 else TMPL_ENDPOINT_SETTINGS
                generated_config_rule = copy.deepcopy(config_rule)
                generated_config_rule['custom']['resource_key'] = resource_key_template.format(*resource_key_values)
                generated_config_rule['custom']['resource_value'] = json.dumps(resource_value)
                generated_config_rules.append(generated_config_rule)
            else:
                LOGGER.debug('[generate_neighbor_endpoint_config_rules] IP_LINK: {:s}'.format(str(config_rule)))
                resource_value : Dict = config_rule['ip_link']
                generated_config_rule = copy.deepcopy(config_rule)
                generated_config_rule['ip_link'] = resource_value
                generated_config_rules.append(generated_config_rule)

    LOGGER.debug('[generate_neighbor_endpoint_config_rules] generated_config_rules={:s}'.format(str(generated_config_rules)))
    LOGGER.debug('[generate_neighbor_endpoint_config_rules] end')
    return generated_config_rules
