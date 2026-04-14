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
from common.proto.context_pb2 import Empty
from common.proto.l3_centralizedattackdetector_pb2_grpc import L3CentralizedattackdetectorStub
from common.proto.l3_centralizedattackdetector_pb2 import (
    AttackIPs,
    AutoFeatures,
    L3CentralizedattackdetectorBatchInput,
    L3CentralizedattackdetectorMetrics,
    StatusMessage
)
from common.tools.client.RetryDecorator import retry, delay_exponential
from common.tools.grpc.Tools import grpc_message_to_json_string

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class l3_centralizedattackdetectorClient:
    def __init__(self, address, port):
        self.endpoint = "{}:{}".format(address, port)
        LOGGER.debug("Creating channel to {:s}...".format(self.endpoint))
        self.channel = None
        self.stub = None
        self.connect()
        LOGGER.debug("Channel created")

    def connect(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = L3CentralizedattackdetectorStub(self.channel)

    def close(self):
        if self.channel is not None:
            self.channel.close()
        self.channel = None
        self.stub = None

    @RETRY_DECORATOR
    def AnalyzeConnectionStatistics(self, request : L3CentralizedattackdetectorMetrics) -> StatusMessage:
        LOGGER.debug('AnalyzeConnectionStatistics request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.AnalyzeConnectionStatistics(request)
        LOGGER.debug('AnalyzeConnectionStatistics result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def AnalyzeBatchConnectionStatistics(self, request: L3CentralizedattackdetectorBatchInput) -> StatusMessage:
        LOGGER.debug('AnalyzeBatchConnectionStatistics request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.AnalyzeBatchConnectionStatistics(request)
        LOGGER.debug('AnalyzeBatchConnectionStatistics result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetFeaturesIds(self, request : Empty) -> AutoFeatures:
        LOGGER.debug('GetFeaturesIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetFeaturesIds(request)
        LOGGER.debug('GetFeaturesIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetAttackIPs(self, request : AttackIPs) -> Empty:
        LOGGER.debug('SetAttackIPs request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetAttackIPs(request)
        LOGGER.debug('SetAttackIPs result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
