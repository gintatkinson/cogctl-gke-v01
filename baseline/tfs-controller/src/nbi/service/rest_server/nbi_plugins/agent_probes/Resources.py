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

from flask_restful import Resource, request
from common.proto.context_pb2 import Empty
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from .Tools import format_grpc_to_json, grpc_device, grpc_device_id

class _Resource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.client = ContextClient()
        self.device_client = DeviceClient()

class DeviceIds(_Resource):
    def get(self):
        return format_grpc_to_json(self.client.ListDeviceIds(Empty()))

class Devices(_Resource):
    def get(self):
        return format_grpc_to_json(self.client.ListDevices(Empty()))

class Device(_Resource):
    def get(self, device_uuid : str):
        return format_grpc_to_json(self.client.GetDevice(grpc_device_id(device_uuid)))

    def post(self, device_uuid : str): # pylint: disable=unused-argument
        device = request.get_json()['devices'][0]
        return format_grpc_to_json(self.device_client.AddDevice(grpc_device(
            device_uuid = device['device_id']['device_uuid']['uuid'],
            device_type = device['device_type'],
            status = device['device_operational_status'],
            endpoints = device['device_endpoints'],            
            config_rules = device['device_config']['config_rules'],
            drivers = device['device_drivers']
        )))

    def put(self, device_uuid : str):  # pylint: disable=unused-argument
        device = request.get_json()['devices'][0]
        return format_grpc_to_json(self.device_client.ConfigureDevice(grpc_device(
            device_uuid = device['device_id']['device_uuid']['uuid'],
            device_type = device['device_type'],
            status = device['device_operational_status'],
            endpoints = device['device_endpoints'],      
            config_rules = device['device_config']['config_rules'],
            drivers = device['device_drivers']
        )))
    
    def delete(self, device_uuid : str):
        device = request.get_json()['devices'][0]
        return format_grpc_to_json(self.device_client.DeleteDevice(grpc_device(
            device_uuid = device['device_id']['device_uuid']['uuid'],
            device_type = device['device_type'],
            status = device['device_operational_status'],
            endpoints = device['device_endpoints'],      
            config_rules = device['device_config']['config_rules'],
            drivers = device['device_drivers']
        )))
