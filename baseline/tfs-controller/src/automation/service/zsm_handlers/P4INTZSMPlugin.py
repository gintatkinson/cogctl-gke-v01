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
from common.proto.analytics_frontend_pb2 import AnalyzerId
from common.proto.policy_pb2 import PolicyRuleState
from common.proto.automation_pb2 import ZSMCreateRequest, ZSMService

from analytics.frontend.client.AnalyticsFrontendClient import AnalyticsFrontendClient
from automation.client.PolicyClient import PolicyClient
from context.client.ContextClient import ContextClient
from automation.service.zsm_handler_api._ZSMHandler import _ZSMHandler
from common.proto.policy_condition_pb2 import PolicyRuleCondition

LOGGER = logging.getLogger(__name__)

class P4INTZSMPlugin(_ZSMHandler):
    def __init__(self):
        LOGGER.info('Init P4INTZSMPlugin')

    def zsmCreate(self,request : ZSMCreateRequest, context : grpc.ServicerContext):
        # check that service does not exist
        context_client = ContextClient()
        policy_client = PolicyClient()
        analytics_frontend_client = AnalyticsFrontendClient()

        # Verify the input target service ID
        try:
            target_service_id = context_client.GetService(request.target_service_id)
        except grpc.RpcError as ex:
            if ex.code() != grpc.StatusCode.NOT_FOUND: raise  # pylint: disable=no-member
            LOGGER.exception('Unable to get target service({:s})'.format(str(target_service_id)))
            context_client.close()
            return None

        # Verify the input telemetry service ID
        try:
            telemetry_service_id = context_client.GetService(request.telemetry_service_id)
        except grpc.RpcError as ex:
            if ex.code() != grpc.StatusCode.NOT_FOUND: raise  # pylint: disable=no-member
            LOGGER.exception('Unable to get telemetry service({:s})'.format(str(telemetry_service_id)))
            context_client.close()
            return None

        # Start an analyzer
        try:
            analyzer_id_lat: AnalyzerId = analytics_frontend_client.StartAnalyzer(request.analyzer) # type: ignore
            LOGGER.info('analyzer_id_lat({:s})'.format(str(analyzer_id_lat)))
        except grpc.RpcError as ex:
            if ex.code() != grpc.StatusCode.NOT_FOUND: raise  # pylint: disable=no-member
            LOGGER.exception('Unable to start analyzer({:s})'.format(str(request.analyzer)))
            context_client.close()
            analytics_frontend_client.close()
            return None

        # Create a policy
        try:
            LOGGER.info('policy({:s})'.format(str(request.policy)))
            # PolicyRuleCondition
            policyRuleCondition = PolicyRuleCondition()
            # policyRuleCondition.kpiId.kpi_id.uuid = request.analyzer.output_kpi_ids[0].kpi_id.uuid
            # policyRuleCondition.numericalOperator = 5
            # policyRuleCondition.kpiValue.floatVal = 300
            # request.policy.policyRuleBasic.conditionList.append(policyRuleCondition)
            LOGGER.info('policy after({:s})'.format(str(request.policy)))

            policy_rule_state: PolicyRuleState = policy_client.PolicyAddService(request.policy) # type: ignore
            LOGGER.info('policy_rule_state({:s})'.format(str(policy_rule_state)))
        except grpc.RpcError as ex:
            if ex.code() != grpc.StatusCode.NOT_FOUND: raise  # pylint: disable=no-member
            LOGGER.exception('Unable to create policy({:s})'.format(str(request.policy)))
            context_client.close()
            policy_client.close()
            return None

        context_client.close()
        analytics_frontend_client.close()
        policy_client.close()
        return ZSMService()

    def zsmDelete(self):
        LOGGER.info('zsmDelete method')

    def zsmGetById(self):
        LOGGER.info('zsmGetById method')

    def zsmGetByService(self):
        LOGGER.info('zsmGetByService method')
