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
from common.Constants import ServiceNameEnum
from common.Settings import get_service_host, get_service_port_grpc
from common.proto.context_pb2 import AuthenticationResult, Empty, Slice, SliceId, SliceStatus, TeraFlowController
from common.proto.interdomain_pb2_grpc import InterdomainServiceStub
from common.tools.client.RetryDecorator import retry, delay_exponential
from common.tools.grpc.Tools import grpc_message_to_json_string

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class InterdomainClient:
    def __init__(self, host=None, port=None):
        if not host: host = get_service_host(ServiceNameEnum.INTERDOMAIN)
        if not port: port = get_service_port_grpc(ServiceNameEnum.INTERDOMAIN)
        self.endpoint = '{:s}:{:s}'.format(str(host), str(port))
        LOGGER.debug('Creating channel to {:s}...'.format(self.endpoint))
        self.channel = None
        self.stub = None
        self.connect()
        LOGGER.debug('Channel created')

    def connect(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = InterdomainServiceStub(self.channel)

    def close(self):
        if self.channel is not None: self.channel.close()
        self.channel = None
        self.stub = None

    @RETRY_DECORATOR
    def Authenticate(self, request : TeraFlowController) -> AuthenticationResult:
        LOGGER.debug('Authenticate request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.Authenticate(request)
        LOGGER.debug('Authenticate result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RequestSlice(self, request : Slice) -> SliceId:
        LOGGER.debug('RequestSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.RequestSlice(request)
        LOGGER.debug('RequestSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def LookUpSlice(self, request : Slice) -> SliceId:
        LOGGER.debug('LookUpSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.LookUpSlice(request)
        LOGGER.debug('LookUpSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def OrderSliceFromCatalog(self, request : Slice) -> SliceStatus:
        LOGGER.debug('OrderSliceFromCatalog request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.OrderSliceFromCatalog(request)
        LOGGER.debug('OrderSliceFromCatalog result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def CreateSliceAndAddToCatalog(self, request : Slice) -> SliceStatus:
        LOGGER.debug('CreateSliceAndAddToCatalog request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.CreateSliceAndAddToCatalog(request)
        LOGGER.debug('CreateSliceAndAddToCatalog result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def OrderSliceWithSLA(self, request : Slice) -> SliceId:
        LOGGER.debug('OrderSliceWithSLA request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.OrderSliceWithSLA(request)
        LOGGER.debug('OrderSliceWithSLA result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def UpdateSlice(self, request : Slice) -> Slice:
        LOGGER.debug('UpdateSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.UpdateSlice(request)
        LOGGER.debug('UpdateSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def DeleteSlice(self, request : SliceId) -> Empty:
        LOGGER.debug('DeleteSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteSlice(request)
        LOGGER.debug('DeleteSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
