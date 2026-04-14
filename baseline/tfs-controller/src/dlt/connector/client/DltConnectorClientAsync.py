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

import grpc, logging, asyncio

from common.Constants import ServiceNameEnum
from common.Settings import get_service_host, get_service_port_grpc
from common.proto.context_pb2 import Empty, TopologyId
from common.proto.dlt_connector_pb2 import DltDeviceId, DltLinkId, DltServiceId, DltSliceId
from common.proto.dlt_connector_pb2_grpc import DltConnectorServiceStub
from common.tools.client.RetryDecorator import retry, delay_exponential
from common.tools.grpc.Tools import grpc_message_to_json_string

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class DltConnectorClientAsync:
    def __init__(self, host=None, port=None):
        if not host: host = get_service_host(ServiceNameEnum.DLT)
        if not port: port = get_service_port_grpc(ServiceNameEnum.DLT)
        self.endpoint = '{:s}:{:s}'.format(str(host), str(port))
        LOGGER.debug('Creating channel to {:s}...'.format(self.endpoint))
        self.channel = None
        self.stub = None
        #self.connect()
        #LOGGER.debug('Channel created')

    async def connect(self):
        self.channel = grpc.aio.insecure_channel(self.endpoint)
        self.stub = DltConnectorServiceStub(self.channel)
        LOGGER.debug('Channel created')

    async def close(self):
        if self.channel is not None:
            await self.channel.close()
        self.channel = None
        self.stub = None

    @RETRY_DECORATOR
    async def RecordAll(self, request: TopologyId) -> Empty:
        LOGGER.debug('RecordAll request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordAll(request)
        LOGGER.debug('RecordAll result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def RecordAllDevices(self, request: TopologyId) -> Empty:
        LOGGER.debug('RecordAllDevices request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordAllDevices(request)
        LOGGER.debug('RecordAllDevices result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def RecordDevice(self, request: DltDeviceId) -> Empty:
        LOGGER.debug('RECORD_DEVICE request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordDevice(request)
        LOGGER.debug('RecordDevice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def RecordAllLinks(self, request: TopologyId) -> Empty:
        LOGGER.debug('RecordAllLinks request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordAllLinks(request)
        LOGGER.debug('RecordAllLinks result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def RecordLink(self, request: DltLinkId) -> Empty:
        LOGGER.debug('RecordLink request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordLink(request)
        LOGGER.debug('RecordLink result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def RecordAllServices(self, request: TopologyId) -> Empty:
        LOGGER.debug('RecordAllServices request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordAllServices(request)
        LOGGER.debug('RecordAllServices result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def RecordService(self, request: DltServiceId) -> Empty:
        LOGGER.debug('RecordService request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordService(request)
        LOGGER.debug('RecordService result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def RecordAllSlices(self, request: TopologyId) -> Empty:
        LOGGER.debug('RecordAllSlices request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordAllSlices(request)
        LOGGER.debug('RecordAllSlices result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    async def RecordSlice(self, request: DltSliceId) -> Empty:
        LOGGER.debug('RecordSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = await self.stub.RecordSlice(request)
        LOGGER.debug('RecordSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
