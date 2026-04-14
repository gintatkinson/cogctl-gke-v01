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
from common.proto.context_pb2 import Empty, QoSProfileId
from common.proto.qos_profile_pb2 import ConstraintList, QoSProfile, QoDConstraintsRequest, QoSProfileList
from common.proto.qos_profile_pb2_grpc import QoSProfileServiceStub
from common.tools.client.RetryDecorator import retry, delay_exponential
from common.tools.grpc.Tools import grpc_message_to_json_string

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class QoSProfileClient:
    def __init__(self, host=None, port=None):
        if not host: host = get_service_host(ServiceNameEnum.QOSPROFILE)
        if not port: port = get_service_port_grpc(ServiceNameEnum.QOSPROFILE)
        self.endpoint = '{:s}:{:s}'.format(str(host), str(port))
        LOGGER.debug('Creating channel to {:s}...'.format(str(self.endpoint)))
        self.channel = None
        self.stub = None
        self.connect()
        LOGGER.debug('Channel created')

    def connect(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = QoSProfileServiceStub(self.channel)

    def close(self):
        if self.channel is not None: self.channel.close()
        self.channel = None
        self.stub = None

    @RETRY_DECORATOR
    def CreateQoSProfile(self, request: QoSProfile) -> QoSProfile:
        LOGGER.debug('CreateQoSProfile request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.CreateQoSProfile(request)
        LOGGER.debug('CreateQoSProfile result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def UpdateQoSProfile(self, request: QoSProfile) -> QoSProfile:
        LOGGER.debug('UpdateQoSProfile request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.UpdateQoSProfile(request)
        LOGGER.debug('UpdateQoSProfile result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def DeleteQoSProfile(self, request: QoSProfileId) -> Empty:
        LOGGER.debug('DeleteQoSProfile request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteQoSProfile(request)
        LOGGER.debug('DeleteQoSProfile result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetQoSProfile(self, request: QoSProfileId) -> QoSProfile:
        LOGGER.debug('GetQoSProfile request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetQoSProfile(request)
        LOGGER.debug('GetQoSProfile result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetQoSProfiles(self, request: Empty) -> QoSProfileList:
        LOGGER.debug('GetQoSProfiles request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetQoSProfiles(request)
        LOGGER.debug('GetQoSProfiles result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetConstraintsFromQoSProfile(self, request: QoDConstraintsRequest) -> ConstraintList:
        LOGGER.debug('GetConstraintsFromQoSProfile request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetConstraintsFromQoSProfile(request)
        #LOGGER.debug('GetConstraintsFromQoSProfile result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
