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

from common.proto.context_pb2 import Empty
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.client.RetryDecorator import retry, delay_exponential

from common.proto.pluggables_pb2_grpc import PluggablesServiceStub
from common.proto.pluggables_pb2 import (
    Pluggable, CreatePluggableRequest, ListPluggablesRequest, ListPluggablesResponse,
    GetPluggableRequest, DeletePluggableRequest, ConfigurePluggableRequest)

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 10
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class PluggablesClient:
    def __init__(self, host=None, port=None):
        if not host: host = get_service_host(ServiceNameEnum.PLUGGABLES) 
        if not port: port = get_service_port_grpc(ServiceNameEnum.PLUGGABLES) 
        self.endpoint     = '{:s}:{:s}'.format(str(host), str(port))
        LOGGER.debug('Creating channel to {:s}...'.format(str(self.endpoint)))

        self.channel      = None
        self.stub         = None
        self.connect()
        LOGGER.debug('Channel created')

    def connect(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub   = PluggablesServiceStub(self.channel)

    def close(self):
        if self.channel is not None: self.channel.close()
        self.channel = None
        self.stub    = None

    @RETRY_DECORATOR
    def CreatePluggable(self, request : CreatePluggableRequest) -> Pluggable: # pyright: ignore[reportInvalidTypeForm]
        LOGGER.debug('CreatePluggable: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.CreatePluggable(request)
        LOGGER.debug('CreatePluggable result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    @RETRY_DECORATOR
    def ListPluggables(self, request : ListPluggablesRequest) -> ListPluggablesResponse:        # pyright: ignore[reportInvalidTypeForm]
        LOGGER.debug('ListPluggables: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListPluggables(request)
        LOGGER.debug('ListPluggables result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    @RETRY_DECORATOR
    def GetPluggable(self, request : GetPluggableRequest) -> Pluggable:     # pyright: ignore[reportInvalidTypeForm]
        LOGGER.debug('GetPluggable: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetPluggable(request)
        LOGGER.debug('GetPluggable result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    @RETRY_DECORATOR
    def DeletePluggable(self, request : DeletePluggableRequest) -> Empty:       # pyright: ignore[reportInvalidTypeForm]
        LOGGER.debug('DeletePluggable: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeletePluggable(request)
        LOGGER.debug('DeletePluggable result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    @RETRY_DECORATOR
    def ConfigurePluggable(self, request : ConfigurePluggableRequest) -> Pluggable:     # pyright: ignore[reportInvalidTypeForm]
        LOGGER.debug('ConfigurePluggable: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ConfigurePluggable(request)
        LOGGER.debug('ConfigurePluggable result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
