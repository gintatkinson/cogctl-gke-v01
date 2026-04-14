# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, logging
from flask import request
from flask.json import jsonify
from flask_restful import Resource
from common.proto.context_pb2 import Empty
from common.proto.qkd_app_pb2 import App, QKDAppTypesEnum
from common.Constants import DEFAULT_CONTEXT_NAME
from context.client.ContextClient import ContextClient
from nbi.service._tools.HttpStatusCodes import HTTP_OK, HTTP_SERVERERROR
from qkd_app.client.QKDAppClient import QKDAppClient

LOGGER = logging.getLogger(__name__)

class _Resource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.context_client = ContextClient()
        self.qkd_app_client = QKDAppClient()

class Index(_Resource):
    def get(self):
        return {}

class ListDevices(_Resource):
    def get(self):
        """
        List devices and associate the apps with them.
        """
        devices = self.context_client.ListDevices(Empty()).devices
        for device in devices:
            # Fetch apps associated with this device
            device.apps = self.get_apps_for_device(device.device_id.device_uuid.uuid)
        return {'devices': [self.format_device(device) for device in devices]}

    def get_apps_for_device(self, device_uuid):
        """
        Fetch the apps associated with a given device UUID.
        """
        try:
            # Call the AppService to get the list of apps
            apps_list = self.qkd_app_client.ListApps(Empty())
            
            # Filter apps for this specific device
            device_apps = []
            for app in apps_list.apps:
                if app.local_device_id.device_uuid.uuid == device_uuid or \
                   app.remote_device_id.device_uuid.uuid == device_uuid:
                    device_apps.append(app)
            return device_apps
        
        except Exception as e:
            print(f"Error fetching apps for device {device_uuid}: {e}")
            return []

    def format_device(self, device):
        """
        Formats a device object to include the associated apps in the response.
        """
        return {
            'device_uuid': device.device_id.device_uuid.uuid,
            'name': device.name,
            'type': device.device_type,
            'status': device.device_operational_status,
            'apps': [{'app_id': app.app_id.app_uuid.uuid, 'app_status': app.app_status, 'app_type': app.app_type} for app in device.apps]
        }

class CreateQKDApp(_Resource):
    def post(self):
        app = request.get_json()['app']
        devices = self.context_client.ListDevices(Empty()).devices

        local_qkdn_id = app.get('local_qkdn_id')
        if local_qkdn_id is None:
            MSG = 'local_qkdn_id not specified in qkd_app({:s})'
            msg = MSG.format(str(app))
            LOGGER.exception(msg)
            response = jsonify({'error': msg})
            response.status_code = HTTP_SERVERERROR
            return response

        # This for-loop won't be necessary if Device ID is guaranteed to be the same as QKDN Id
        local_device = None
        for device in devices:
            for config_rule in device.device_config.config_rules:
                if config_rule.custom.resource_key != '__node__': continue
                value = json.loads(config_rule.custom.resource_value)
                qkdn_id = value.get('qkdn_id')
                if qkdn_id is None: continue
                if local_qkdn_id != qkdn_id: continue
                local_device = device
                break

        if local_device is None:
            MSG = 'Unable to find device for local_qkdn_id({:s})'
            msg = MSG.format(str(local_qkdn_id))
            LOGGER.exception(msg)
            response = jsonify({'error': msg})
            response.status_code = HTTP_SERVERERROR
            return response

        external_app_src_dst = {
            'app_id': {'context_id': {'context_uuid': {'uuid': DEFAULT_CONTEXT_NAME}}, 'app_uuid': {'uuid': ''}},
            'app_status': 'QKDAPPSTATUS_' + app['app_status'],
            'app_type': QKDAppTypesEnum.QKDAPPTYPES_CLIENT,
            'server_app_id': app['server_app_id'],
            'client_app_id': app['client_app_id'],
            'backing_qkdl_id': [{'qkdl_uuid': {'uuid': qkdl_id}} for qkdl_id in app['backing_qkdl_id']],
            'local_device_id': local_device.device_id,
            'remote_device_id': {'device_uuid': {'uuid': ''}},
        }

        self.qkd_app_client.RegisterApp(App(**external_app_src_dst))

        response = jsonify({'status': 'success'})
        response.status_code = HTTP_OK
        return response
