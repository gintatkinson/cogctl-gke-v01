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

import asyncio, grpc, logging
from typing import Iterator, List
from common.proto.context_pb2 import Empty, TeraFlowController
from common.proto.dlt_gateway_pb2 import (
    DltPeerStatus, DltPeerStatusList, DltRecord, DltRecordEvent, DltRecordId, DltRecordStatus, DltRecordSubscription
)
from common.proto.dlt_gateway_pb2_grpc import DltGatewayServiceStub
from common.tools.client.RetryDecorator import retry, delay_exponential
from common.tools.grpc.Tools import grpc_message_to_json_string
from dlt.connector.Config import DLT_GATEWAY_HOST, DLT_GATEWAY_PORT

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class DltGatewayClientAsync:
    def __init__(self, host=None, port=None):
        if not host: host = DLT_GATEWAY_HOST
        if not port: port = DLT_GATEWAY_PORT
        self.endpoint = '{:s}:{:s}'.format(str(host), str(port))
        LOGGER.debug('Creating channel to {:s}...'.format(self.endpoint))
        self.channel = None
        self.stub = None
        self.message_queue: List[DltRecord] = []

    async def connect(self):
        self.channel = grpc.aio.insecure_channel(self.endpoint)
        self.stub = DltGatewayServiceStub(self.channel)
        LOGGER.debug('Channel created')

    async def close(self):
        if self.channel is not None:
            await self.channel.close()
        self.channel = None
        self.stub = None

    @RETRY_DECORATOR
    async def RecordToDlt(self, request : DltRecord) -> DltRecordStatus:
        LOGGER.debug('RecordToDlt request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordToDlt(request)
        LOGGER.debug('RecordToDlt result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def GetFromDlt(self, request : DltRecordId) -> DltRecord:
        LOGGER.debug('GetFromDlt request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.GetFromDlt(request)
        LOGGER.debug('GetFromDlt result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SubscribeToDlt(self, request : DltRecordSubscription) -> Iterator[DltRecordEvent]:
        LOGGER.debug('SubscribeToDlt request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SubscribeToDlt(request)
        LOGGER.debug('SubscribeToDlt result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def GetDltStatus(self, request : TeraFlowController) -> DltPeerStatus:
        LOGGER.debug('GetDltStatus request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.GetDltStatus(request)
        LOGGER.debug('GetDltStatus result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def GetDltPeers(self, request : Empty) -> DltPeerStatusList:
        LOGGER.debug('GetDltPeers request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.GetDltPeers(request)
        LOGGER.debug('GetDltPeers result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
