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

import json, logging, re
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from common.proto.context_pb2 import ConfigActionEnum, ConfigRule
from common.tools.context_queries.Device import get_device
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from nbi.service._tools.Authentication import HTTP_AUTH
from .ietf_acl_parser import ietf_acl_from_config_rule_resource_value

LOGGER = logging.getLogger(__name__)

ACL_CONIG_RULE_KEY = r'\/device\[.+\]\/endpoint\[(.+)\]/acl_ruleset\[{}\]'

class Acl(Resource):
    @HTTP_AUTH.login_required
    def get(self, device_uuid : str, acl_name : str):
        LOGGER.debug('GET device_uuid={:s}, acl_name={:s}'.format(str(device_uuid), str(acl_name)))
        RE_ACL_CONIG_RULE_KEY = re.compile(ACL_CONIG_RULE_KEY.format(acl_name))

        context_client = ContextClient()
        device = get_device(context_client, device_uuid, rw_copy=False, include_config_rules=True)
        if device is None: raise NotFound('Device({:s}) not found'.format(str(device_uuid)))

        for config_rule in device.device_config.config_rules:
            if config_rule.WhichOneof('config_rule') != 'custom': continue
            ep_uuid_match = RE_ACL_CONIG_RULE_KEY.match(config_rule.custom.resource_key)
            if ep_uuid_match is None: continue
            resource_value_dict = json.loads(config_rule.custom.resource_value)
            return ietf_acl_from_config_rule_resource_value(resource_value_dict)

        raise NotFound('Acl({:s}) not found in Device({:s})'.format(str(acl_name), str(device_uuid)))

    @HTTP_AUTH.login_required
    def delete(self, device_uuid : str, acl_name : str):
        LOGGER.debug('DELETE device_uuid={:s}, acl_name={:s}'.format(str(device_uuid), str(acl_name)))
        RE_ACL_CONIG_RULE_KEY = re.compile(ACL_CONIG_RULE_KEY.format(acl_name))

        context_client = ContextClient()
        device = get_device(context_client, device_uuid, rw_copy=True, include_config_rules=True)
        if device is None: raise NotFound('Device({:s}) not found'.format(str(device_uuid)))

        delete_config_rules = list()
        for config_rule in device.device_config.config_rules:
            if config_rule.WhichOneof('config_rule') != 'custom': continue
            ep_uuid_match = RE_ACL_CONIG_RULE_KEY.match(config_rule.custom.resource_key)
            if ep_uuid_match is None: continue

            _config_rule = ConfigRule()
            _config_rule.CopyFrom(config_rule)
            _config_rule.action = ConfigActionEnum.CONFIGACTION_DELETE
            delete_config_rules.append(_config_rule)

        if not delete_config_rules:
            raise NotFound('Acl({:s}) not found in Device({:s})'.format(str(acl_name), str(device_uuid)))

        device_client = DeviceClient()
        del device.device_config.config_rules[:]
        device.device_config.config_rules.extend(delete_config_rules)
        device_client.ConfigureDevice(device)
        return None
