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

import json, logging
from typing import Dict, List, Set
from flask import jsonify, request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, NotFound, UnsupportedMediaType
from common.proto.context_pb2 import ConfigRule
from common.tools.context_queries.Device import get_device
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from nbi.service._tools.Authentication import HTTP_AUTH
from .ietf_acl_parser import AclDirectionEnum, config_rule_from_ietf_acl
from .YangValidator import YangValidator

LOGGER = logging.getLogger(__name__)


def compose_interface_direction_acl_rules(
    device_name : str, interface_name : str, interface_data : Dict,
    acl_direction : AclDirectionEnum, acl_name__to__acl_data : Dict[str, Dict]
) -> List[ConfigRule]:
    acl_direction_name  = acl_direction.value
    acl_direction_title = str(acl_direction_name).title()
    direction_data : Dict[str, Dict] = interface_data.get(acl_direction_name, {})
    acl_sets       : Dict[str, Dict] = direction_data.get('acl-sets',         {})
    acl_set_list   : List[Dict]      = acl_sets      .get('acl-set',          [])
    acl_set_names  : Set[str]        = {acl_set['name'] for acl_set in acl_set_list}

    acl_config_rules : List[ConfigRule] = list()
    for acl_set_name in acl_set_names:
        acl_set = acl_name__to__acl_data.get(acl_set_name)
        if acl_set is None:
            MSG = 'Interface({:s})/{:s}/AclSet({:s}) not found'
            raise NotFound(MSG.format(
                str(interface_name), acl_direction_title, str(acl_set_name)
            ))

        acl_config_rule = config_rule_from_ietf_acl(
            device_name, interface_name, acl_direction, acl_set
        )
        MSG = 'Adding {:s} ACL Config Rule: {:s}'
        LOGGER.info(MSG.format(
            acl_direction_title, grpc_message_to_json_string(acl_config_rule)
        ))
        acl_config_rules.append(acl_config_rule)

    return acl_config_rules

class Acls(Resource):
    @HTTP_AUTH.login_required
    def get(self):
        return {}

    @HTTP_AUTH.login_required
    def post(self, device_uuid : str):
        if not request.is_json:
            LOGGER.warning('POST device_uuid={:s}, body={:s}'.format(str(device_uuid), str(request.data)))
            raise UnsupportedMediaType('JSON payload is required')
        request_data : Dict = request.json
        LOGGER.debug('POST device_uuid={:s}, body={:s}'.format(str(device_uuid), json.dumps(request_data)))

        context_client = ContextClient()
        device = get_device(
            context_client, device_uuid, rw_copy=True, include_config_rules=False, include_components=False
        )
        if device is None:
            raise NotFound('Device({:s}) not found'.format(str(device_uuid)))

        device_name = device.name
        interface_names : Set[str] = set()
        for endpoint in device.device_endpoints:
            interface_names.add(endpoint.endpoint_id.endpoint_uuid.uuid)
            interface_names.add(endpoint.name)

        yang_validator = YangValidator()
        request_data = yang_validator.parse_to_dict(request_data, list(interface_names))
        yang_validator.destroy()

        acls          : Dict = request_data.get('acls', {})
        acl_list      : List = acls.get('acl', [])
        acl_name__to__acl_data = {
            acl['name'] : acl
            for acl in acl_list
        }

        if len(acl_name__to__acl_data) == 0:
            raise BadRequest('No ACLs defined in the request')

        interface_list : List = acls.get('attachment-points', {}).get('interface', [])
        interface_name__to__interface_data = {
            interface['interface-id'] : interface
            for interface in interface_list
        }

        if len(interface_name__to__interface_data) == 0:
            raise BadRequest('No interfaces defined in the request')

        for interface_name in interface_names:
            interface_data = interface_name__to__interface_data.get(interface_name)
            if interface_data is None: continue

            if 'ingress' in interface_data:
                ingress_acl_config_rules = compose_interface_direction_acl_rules(
                    device_name, interface_name, interface_data, AclDirectionEnum.INGRESS,
                    acl_name__to__acl_data
                )
                device.device_config.config_rules.extend(ingress_acl_config_rules)

            if 'egress' in interface_data:
                egress_acl_config_rules = compose_interface_direction_acl_rules(
                    device_name, interface_name, interface_data, AclDirectionEnum.EGRESS,
                    acl_name__to__acl_data
                )
                device.device_config.config_rules.extend(egress_acl_config_rules)

        device_client = DeviceClient()
        device_client.ConfigureDevice(device)
        return jsonify({})
