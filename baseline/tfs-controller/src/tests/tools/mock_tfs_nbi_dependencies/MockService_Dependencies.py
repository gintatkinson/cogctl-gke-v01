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

from typing import Optional, Union
from common.proto.context_pb2_grpc import add_ContextServiceServicer_to_server
from common.proto.device_pb2_grpc import add_DeviceServiceServicer_to_server
from common.proto.qos_profile_pb2_grpc import add_QoSProfileServiceServicer_to_server
from common.proto.service_pb2_grpc import add_ServiceServiceServicer_to_server
from common.proto.slice_pb2_grpc import add_SliceServiceServicer_to_server
from common.tests.MockServicerImpl_Context import MockServicerImpl_Context
from common.tests.MockServicerImpl_Device import MockServicerImpl_Device
from common.tests.MockServicerImpl_QoSProfile import MockServicerImpl_QoSProfile
from common.tests.MockServicerImpl_Service import MockServicerImpl_Service
from common.tests.MockServicerImpl_Slice import MockServicerImpl_Slice
from common.tools.service.GenericGrpcService import GenericGrpcService


class MockService_Dependencies(GenericGrpcService):
    # Mock Service implementing multiple mock components to simplify
    # unitary tests of the NBI component.
    # Mocks implemented: Context, Device, QoS Profile, Service and Slice

    def __init__(
        self, bind_port : Union[str, int], bind_address : Optional[str] = None,
        max_workers : Optional[int] = None, grace_period : Optional[int] = None,
        enable_health_servicer : bool = True, enable_reflection : bool = False,
        cls_name : str = 'MockService'
    ) -> None:
        super().__init__(
            bind_port, bind_address=bind_address, max_workers=max_workers,
            grace_period=grace_period, enable_health_servicer=enable_health_servicer,
            enable_reflection=enable_reflection, cls_name=cls_name
        )

    # pylint: disable=attribute-defined-outside-init
    def install_servicers(self):
        self.context_servicer = MockServicerImpl_Context()
        add_ContextServiceServicer_to_server(self.context_servicer, self.server)

        self.device_servicer = MockServicerImpl_Device()
        add_DeviceServiceServicer_to_server(self.device_servicer, self.server)

        self.service_servicer = MockServicerImpl_Service()
        add_ServiceServiceServicer_to_server(self.service_servicer, self.server)

        self.slice_servicer = MockServicerImpl_Slice()
        add_SliceServiceServicer_to_server(self.slice_servicer, self.server)

        self.qos_profile_servicer = MockServicerImpl_QoSProfile()
        add_QoSProfileServiceServicer_to_server(self.qos_profile_servicer, self.server)
