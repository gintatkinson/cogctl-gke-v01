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
from common.proto.context_pb2 import Device, DeviceId, EndPoint, EndPointId

class NameMappings:
    def __init__(self) -> None:
        self._device_uuid_to_name   : Dict[str,             str] = dict()
        self._endpoint_uuid_to_name : Dict[Tuple[str, str], str] = dict()

    def store_device_name(self, device : Device) -> None:
        device_uuid = device.device_id.device_uuid.uuid
        device_name = device.name
        self._device_uuid_to_name[device_uuid] = device_name
        self._device_uuid_to_name[device_name] = device_name

    def store_endpoint_name(self, device : Device, endpoint : EndPoint) -> None:
        device_uuid = device.device_id.device_uuid.uuid
        device_name = device.name
        endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
        endpoint_name = endpoint.name
        self._endpoint_uuid_to_name[(device_uuid, endpoint_uuid)] = endpoint_name
        self._endpoint_uuid_to_name[(device_name, endpoint_uuid)] = endpoint_name
        self._endpoint_uuid_to_name[(device_uuid, endpoint_name)] = endpoint_name
        self._endpoint_uuid_to_name[(device_name, endpoint_name)] = endpoint_name

    def get_device_name(self, device_id : DeviceId) -> str:
        device_uuid = device_id.device_uuid.uuid
        return self._device_uuid_to_name.get(device_uuid, device_uuid)

    def get_endpoint_name(self, endpoint_id : EndPointId) -> str:
        device_uuid = endpoint_id.device_id.device_uuid.uuid
        endpoint_uuid = endpoint_id.endpoint_uuid.uuid
        return self._endpoint_uuid_to_name.get((device_uuid, endpoint_uuid), endpoint_uuid)
