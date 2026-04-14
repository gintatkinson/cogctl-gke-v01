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
from common.proto.context_pb2 import Empty, Service, ServiceId, ServiceStatusEnum
from common.proto.service_pb2_grpc import ServiceServiceServicer
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

class MockServicerImpl_Service(ServiceServiceServicer):
    def __init__(self):
        LOGGER.info('[__init__] Creating Servicer...')
        self.context_client = ContextClient(
            get_setting('CONTEXTSERVICE_SERVICE_HOST'),
            get_setting('CONTEXTSERVICE_SERVICE_PORT_GRPC'))
        LOGGER.info('[__init__] Servicer Created')

    def CreateService(self, request : Service, context : grpc.ServicerContext) -> ServiceId:
        LOGGER.info('[CreateService] request={:s}'.format(grpc_message_to_json_string(request)))
        return self.context_client.SetService(request)

    def UpdateService(self, request : Service, context : grpc.ServicerContext) -> ServiceId:
        LOGGER.info('[UpdateService] request={:s}'.format(grpc_message_to_json_string(request)))
        service = Service()
        service.CopyFrom(request)
        service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_ACTIVE #pylint: disable=no-member
        return self.context_client.SetService(service)

    def DeleteService(self, request : ServiceId, context : grpc.ServicerContext) -> Empty:
        LOGGER.info('[DeleteService] request={:s}'.format(grpc_message_to_json_string(request)))
        return self.context_client.RemoveService(request)
