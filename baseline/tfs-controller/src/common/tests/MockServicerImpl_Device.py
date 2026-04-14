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

import grpc, logging
from common.Settings import get_setting
from common.proto.context_pb2 import Device, DeviceConfig, DeviceId, Empty
from common.proto.device_pb2 import MonitoringSettings
from common.proto.device_pb2_grpc import DeviceServiceServicer
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

class MockServicerImpl_Device(DeviceServiceServicer):
    def __init__(self):
        LOGGER.info('[__init__] Creating Servicer...')
        self.context_client = ContextClient(
            get_setting('CONTEXTSERVICE_SERVICE_HOST'),
            get_setting('CONTEXTSERVICE_SERVICE_PORT_GRPC'))
        LOGGER.info('[__init__] Servicer Created')

    def AddDevice(self, request : Device, context : grpc.ServicerContext) -> DeviceId:
        LOGGER.info('[AddDevice] request={:s}'.format(grpc_message_to_json_string(request)))
        return self.context_client.SetDevice(request)

    def ConfigureDevice(self, request : Device, context : grpc.ServicerContext) -> DeviceId:
        LOGGER.info('[ConfigureDevice] request={:s}'.format(grpc_message_to_json_string(request)))
        return self.context_client.SetDevice(request)

    def DeleteDevice(self, request : DeviceId, context : grpc.ServicerContext) -> Empty:
        LOGGER.info('[DeleteDevice] request={:s}'.format(grpc_message_to_json_string(request)))
        return self.context_client.RemoveDevice(request)

    def GetInitialConfig(self, request : DeviceId, context : grpc.ServicerContext) -> DeviceConfig:
        LOGGER.info('[GetInitialConfig] request={:s}'.format(grpc_message_to_json_string(request)))
        return DeviceConfig()

    def MonitorDeviceKpi(self, request : MonitoringSettings, context : grpc.ServicerContext) -> Empty:
        LOGGER.info('[MonitorDeviceKpi] request={:s}'.format(grpc_message_to_json_string(request)))
        return Empty()
