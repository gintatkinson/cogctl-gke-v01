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

from common.proto.context_pb2 import ConnectionId, DeviceId, ServiceId
from common.proto.qkd_app_pb2 import AppId

def get_connection_key(connection_id : ConnectionId) -> str:
    return connection_id.connection_uuid.uuid

def get_device_key(device_id : DeviceId) -> str:
    return device_id.device_uuid.uuid

def get_service_key(service_id : ServiceId) -> str:
    context_uuid = service_id.context_id.context_uuid.uuid
    service_uuid = service_id.service_uuid.uuid
    return '{:s}/{:s}'.format(context_uuid, service_uuid)

def get_qkd_app_key(app_id: AppId) -> str:
    return app_id.app_uuid.uuid

