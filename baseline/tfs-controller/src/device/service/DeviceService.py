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

from common.Constants import ServiceNameEnum
from common.Settings import get_service_port_grpc
from common.proto.device_pb2 import DESCRIPTOR as DEVICE_DESCRIPTOR
from common.proto.device_pb2_grpc import add_DeviceServiceServicer_to_server
from common.proto.optical_device_pb2 import DESCRIPTOR as OPTICAL_DEVICE_DESCRIPTOR
from common.proto.optical_device_pb2_grpc import add_OpenConfigServiceServicer_to_server
from common.tools.service.GenericGrpcService import GenericGrpcService
from device.Config import LOAD_ALL_DEVICE_DRIVERS
from .driver_api.DriverInstanceCache import DriverInstanceCache
from .DeviceServiceServicerImpl import DeviceServiceServicerImpl
from .monitoring.MonitoringLoops import MonitoringLoops
from .OpenConfigServicer import OpenConfigServicer

# Custom gRPC settings
# Multiple clients might keep connections alive waiting for RPC methods to be executed.
# Requests needs to be serialized to ensure correct device configurations
GRPC_MAX_WORKERS = 200

class DeviceService(GenericGrpcService):
    def __init__(self, driver_instance_cache : DriverInstanceCache, cls_name: str = __name__) -> None:
        port = get_service_port_grpc(ServiceNameEnum.DEVICE)
        super().__init__(port, max_workers=GRPC_MAX_WORKERS, cls_name=cls_name)
        self.monitoring_loops = MonitoringLoops()
        self.device_servicer = DeviceServiceServicerImpl(driver_instance_cache, self.monitoring_loops)
        if LOAD_ALL_DEVICE_DRIVERS:
            self.openconfig_device_servicer = OpenConfigServicer(driver_instance_cache,self.monitoring_loops)

    def install_servicers(self):
        self.monitoring_loops.start()
        add_DeviceServiceServicer_to_server(self.device_servicer, self.server)
        self.add_reflection_service_name(DEVICE_DESCRIPTOR, 'DeviceService')

        if LOAD_ALL_DEVICE_DRIVERS:
            add_OpenConfigServiceServicer_to_server(self.openconfig_device_servicer,self.server)
            self.add_reflection_service_name(OPTICAL_DEVICE_DESCRIPTOR, 'OpenConfigService')

    def stop(self):
        super().stop()
        self.monitoring_loops.stop()
