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

# RFC 8466 - L2VPN Service Model (L2SM)
# Ref: https://datatracker.ietf.org/doc/html/rfc8466


import json
from typing import Any, Dict, Tuple
from common.proto.context_pb2 import ConfigActionEnum
from common.tools.grpc.Tools import grpc_message_to_json_string

def update_config_rule_custom(
    config_rules, resource_key : str, fields : Dict[str, Tuple[Any, bool]],
    new_action : ConfigActionEnum = ConfigActionEnum.CONFIGACTION_SET
) -> None:
    # fields: Dict[field_name : str, Tuple[field_value : Any, raise_if_differs : bool]]

    # TODO: add support for ACL config rules

    for config_rule in config_rules:
        kind = config_rule.WhichOneof('config_rule')
        if kind != 'custom': continue
        if config_rule.custom.resource_key != resource_key: continue
        json_resource_value = json.loads(config_rule.custom.resource_value)
        break   # found, end loop
    else:
        # not found, add it
        config_rule = config_rules.add()    # pylint: disable=no-member
        config_rule.custom.resource_key = resource_key
        json_resource_value = {}

    config_rule.action = new_action

    for field_name,(field_value, raise_if_differs) in fields.items():
        if (field_name not in json_resource_value) or not raise_if_differs:
            # missing or raise_if_differs=False, add/update it
            json_resource_value[field_name] = field_value
        elif json_resource_value[field_name] != field_value:
            # exists, differs, and raise_if_differs=True
            msg = 'Specified {:s}({:s}) differs existing value({:s})'
            raise Exception(msg.format(str(field_name), str(field_value), str(json_resource_value[field_name])))

    config_rule.custom.resource_value = json.dumps(json_resource_value, sort_keys=True)

def copy_config_rules(source_config_rules, target_config_rules, raise_if_differs = True):
    for source_config_rule in source_config_rules:
        config_rule_kind = source_config_rule.WhichOneof('config_rule')
        if config_rule_kind == 'custom':
            custom = source_config_rule.custom
            resource_key = custom.resource_key
            resource_value = json.loads(custom.resource_value)
            fields = {name:(value, raise_if_differs) for name,value in resource_value.items()}
            update_config_rule_custom(target_config_rules, resource_key, fields)

        else:
            raise NotImplementedError('ConfigRule({:s})'.format(grpc_message_to_json_string(source_config_rule)))
