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
from common.proto.forecaster_pb2 import (
    ForecastLinkCapacityReply, ForecastLinkCapacityRequest,
    ForecastTopologyCapacityReply, ForecastTopologyCapacityRequest
)
from common.proto.forecaster_pb2_grpc import ForecasterServiceStub
from common.tools.client.RetryDecorator import retry, delay_exponential
from common.tools.grpc.Tools import grpc_message_to_json_string

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class ForecasterClient:
    def __init__(self, host=None, port=None):
        if not host: host = get_service_host(ServiceNameEnum.FORECASTER)
        if not port: port = get_service_port_grpc(ServiceNameEnum.FORECASTER)
        self.endpoint = '{:s}:{:s}'.format(str(host), str(port))
        LOGGER.debug('Creating channel to {:s}...'.format(str(self.endpoint)))
        self.channel = None
        self.stub = None
        self.connect()
        LOGGER.debug('Channel created')

    def connect(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = ForecasterServiceStub(self.channel)

    def close(self):
        if self.channel is not None: self.channel.close()
        self.channel = None
        self.stub = None

    @RETRY_DECORATOR
    def ForecastLinkCapacity(self, request : ForecastLinkCapacityRequest) -> ForecastLinkCapacityReply:
        LOGGER.debug('ForecastLinkCapacity request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ForecastLinkCapacity(request)
        LOGGER.debug('ForecastLinkCapacity result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ForecastTopologyCapacity(self, request : ForecastTopologyCapacityRequest) -> ForecastTopologyCapacityReply:
        LOGGER.debug('ForecastTopologyCapacity request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ForecastTopologyCapacity(request)
        LOGGER.debug('ForecastTopologyCapacity result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
