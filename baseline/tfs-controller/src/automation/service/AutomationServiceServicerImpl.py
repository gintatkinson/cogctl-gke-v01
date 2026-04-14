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

import grpc, logging
from uuid import uuid4
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.automation_pb2_grpc import AutomationServiceServicer
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.proto.automation_pb2 import ZSMCreateRequest, ZSMService, ZSMServiceID, ZSMServiceState
from common.proto.context_pb2 import ServiceId
from automation.service.database.AutomationDB import AutomationDB
from automation.service.database.AutomationModel import AutomationModel
from automation.service.zsm_handlers import ZSM_SERVICE_HANDLERS
from automation.service.zsm_handler_api.ZSMFilterFields import (
    ZSMFilterFieldEnum, #TELEMETRY_SERVICE_TYPE_VALUES, TARGET_SERVICE_TYPE_VALUES,
    ZSM_FILTER_FIELD_ALLOWED_VALUES
)
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)
METRICS_POOL = MetricsPool('Automation', 'RPC')

class AutomationServiceServicerImpl(AutomationServiceServicer):
    def __init__(self):
        self.automation_db_obj = AutomationDB(AutomationModel)
        LOGGER.info('Init AutomationService')

    @safe_and_metered_rpc_method(METRICS_POOL,LOGGER)
    def ZSMCreate(self, request : ZSMCreateRequest, context : grpc.ServicerContext) -> ZSMService:
        LOGGER.info("Received gRPC message object: {:}".format(request))
        context_client = ContextClient()

        targetService = context_client.GetService(request.target_service_id)
        telemetryService = context_client.GetService(request.telemetry_service_id)

        handler_cls = self.get_service_handler_based_on_service_types(
            targetService.service_type, telemetryService.service_type, ZSM_SERVICE_HANDLERS
        )

        if handler_cls:
            handler_obj = handler_cls()  # instantiate it
            handler_obj.zsmCreate(request, context)
        else:
            LOGGER.info("No matching handler found.")

        response = ZSMService()
        automation_id = str(uuid4())
        zsm_to_insert = AutomationModel.convert_Automation_to_row(automation_id , "Test Description")
        if self.automation_db_obj.add_row_to_db(zsm_to_insert):
            response.zsmServiceId.uuid.uuid = automation_id

        return response

    @safe_and_metered_rpc_method(METRICS_POOL,LOGGER)
    def ZSMDelete(self, request : ZSMServiceID, context : grpc.ServicerContext) -> ZSMServiceState:
        LOGGER.info("Received gRPC message object: {:}".format(request))
        zsm_id_to_search = request.uuid.uuid

        row = self.automation_db_obj.search_db_row_by_id(AutomationModel, 'zsm_id', zsm_id_to_search)
        if row is None:
            LOGGER.info('No matching row found zsm id: {:}'.format(zsm_id_to_search))
            raise NotFoundException('ZsmID', zsm_id_to_search)
        
        self.automation_db_obj.delete_db_row_by_id(AutomationModel, 'zsm_id', zsm_id_to_search)

        zsmServiceState  = ZSMServiceState()
        zsmServiceState.zsmServiceState = 5
        zsmServiceState.zsmServiceStateMessage = "Removed id: {:}".format(request)

        return zsmServiceState

    @safe_and_metered_rpc_method(METRICS_POOL,LOGGER)
    def ZSMGetById(self, request : ZSMServiceID, context : grpc.ServicerContext) -> ZSMService:
        LOGGER.info("Received gRPC message object: {:}".format(request))
        zsm_id_to_search = request.uuid.uuid
        row = self.automation_db_obj.search_db_row_by_id(AutomationModel, 'zsm_id', zsm_id_to_search)
        if row is None:
            LOGGER.info('No matching row found zsm id: {:}'.format(zsm_id_to_search))
            raise NotFoundException('ZsmID', zsm_id_to_search)
        response = AutomationModel.convert_row_to_Automation(row)
        return response

    @safe_and_metered_rpc_method(METRICS_POOL,LOGGER)
    def ZSMGetByService(self, request : ServiceId, context : grpc.ServicerContext) -> ZSMService:
        LOGGER.info('NOT IMPLEMENTED ZSMGetByService')
        return ZSMService()

    def get_service_handler_based_on_service_types(
        self, targetServiceType ,telemetryServiceType , ZSM_SERVICE_HANDLERS
    ):
        flag = True
        for handler_cls, filters in ZSM_SERVICE_HANDLERS:
            for filter in filters:
                flag = self.check_if_requested_services_pass_filter_criteria(
                    filter, targetServiceType, telemetryServiceType
                )
            if flag:
                return handler_cls
        return None

    def check_if_requested_services_pass_filter_criteria(
        self ,filter , targetServiceType , telemetryServiceType
    ):
        flag = True
        for filter_key, filter_value in filter.items():
            if filter_value in ZSM_FILTER_FIELD_ALLOWED_VALUES[filter_key.value]:
                if filter_key.value == ZSMFilterFieldEnum.TARGET_SERVICE_TYPE.value:
                    if filter_value != targetServiceType:
                        flag = False
                elif filter_key.value == ZSMFilterFieldEnum.TELEMETRY_SERVICE_TYPE.value:
                    if filter_value != telemetryServiceType:
                        flag = False
            else:
                flag = False
        return flag
