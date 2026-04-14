# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import grpc , logging
from common.proto.automation_pb2 import (
    ZSMCreateRequest, #ZSMService,
    ZSMServiceID, #ZSMServiceState,
)
from common.proto.context_pb2 import ServiceId

LOGGER = logging.getLogger(__name__)

class _ZSMHandler:
    def __init__(self):
        LOGGER.info('Init Scenario')

    def zsmCreate(self, request : ZSMCreateRequest, context : grpc.ServicerContext):
        LOGGER.info('zsmCreate method')

    def zsmDelete(self, request : ZSMServiceID, context : grpc.ServicerContext):
        LOGGER.info('zsmDelete method')

    def zsmGetById(self, request : ZSMServiceID, context : grpc.ServicerContext):
        LOGGER.info('zsmGetById method')

    def zsmGetByService(self, request : ServiceId, context : grpc.ServicerContext):
        LOGGER.info('zsmGetByService method')
