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

import os, queue
from typing import Union
from common.Constants import ServiceNameEnum
from common.Settings import ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name
from common.proto.context_pb2_grpc import add_ContextServiceServicer_to_server
from common.proto.monitoring_pb2_grpc import add_MonitoringServiceServicer_to_server
from common.tests.MockServicerImpl_Context import MockServicerImpl_Context
from common.tests.MockServicerImpl_Monitoring import MockServicerImpl_Monitoring
from common.tools.service.GenericGrpcService import GenericGrpcService

LOCAL_HOST = '127.0.0.1'

SERVICE_CONTEXT = ServiceNameEnum.CONTEXT
SERVICE_MONITORING = ServiceNameEnum.MONITORING

class MockService_Dependencies(GenericGrpcService):
    # Mock Service implementing Context and Monitoring to simplify unitary tests of Device

    def __init__(self, bind_port: Union[str, int]) -> None:
        super().__init__(bind_port, LOCAL_HOST, enable_health_servicer=False, cls_name='MockService')

    # pylint: disable=attribute-defined-outside-init
    def install_servicers(self):
        self.context_servicer = MockServicerImpl_Context()
        add_ContextServiceServicer_to_server(self.context_servicer, self.server)

        self.queue_samples = queue.Queue()
        self.monitoring_servicer = MockServicerImpl_Monitoring(queue_samples=self.queue_samples)
        add_MonitoringServiceServicer_to_server(self.monitoring_servicer, self.server)

    def configure_env_vars(self):
        os.environ[get_env_var_name(SERVICE_CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     )] = str(self.bind_address)
        os.environ[get_env_var_name(SERVICE_CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(self.bind_port)

        os.environ[get_env_var_name(SERVICE_MONITORING, ENVVAR_SUFIX_SERVICE_HOST     )] = str(self.bind_address)
        os.environ[get_env_var_name(SERVICE_MONITORING, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(self.bind_port)
