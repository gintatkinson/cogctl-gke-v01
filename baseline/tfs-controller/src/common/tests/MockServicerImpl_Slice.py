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
from common.proto.context_pb2 import Empty, Slice, SliceId, SliceStatusEnum
from common.proto.slice_pb2_grpc import SliceServiceServicer
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

class MockServicerImpl_Slice(SliceServiceServicer):
    def __init__(self):
        LOGGER.info('[__init__] Creating Servicer...')
        self.context_client = ContextClient(
            get_setting('CONTEXTSERVICE_SERVICE_HOST'),
            get_setting('CONTEXTSERVICE_SERVICE_PORT_GRPC'))
        LOGGER.info('[__init__] Servicer Created')

    def CreateSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        LOGGER.info('[CreateSlice] request={:s}'.format(grpc_message_to_json_string(request)))
        return self.context_client.SetSlice(request)

    def UpdateSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        LOGGER.info('[UpdateSlice] request={:s}'.format(grpc_message_to_json_string(request)))
        slice_ = Slice()
        slice_.CopyFrom(request)
        slice_.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_ACTIVE # pylint: disable=no-member
        return self.context_client.SetSlice(slice_)

    def DeleteSlice(self, request : SliceId, context : grpc.ServicerContext) -> Empty:
        LOGGER.info('[DeleteSlice] request={:s}'.format(grpc_message_to_json_string(request)))
        return self.context_client.RemoveSlice(request)
