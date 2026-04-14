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

import logging
from ..service.AutomationServiceServicerImpl import AutomationServiceServicerImpl
from common.proto.context_pb2 import ServiceTypeEnum
from ..service.zsm_handler_api.ZSMFilterFields import ZSMFilterFieldEnum
from ..service.zsm_handlers import Poc1 , Poc2

LOGGER = logging.getLogger(__name__)

ZSM_SERVICE_HANDLERS = [
    (Poc1, [
        {
            ZSMFilterFieldEnum.TARGET_SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
            ZSMFilterFieldEnum.TELEMETRY_SERVICE_TYPE : ServiceTypeEnum.SERVICETYPE_INT,
        }
    ]),
    (Poc2, [
        {
            ZSMFilterFieldEnum.TARGET_SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_INT,
            ZSMFilterFieldEnum.TELEMETRY_SERVICE_TYPE : ServiceTypeEnum.SERVICETYPE_L2NM,
        }
    ])
]

def test_get_service_handler_based_on_service_types():
    automation = AutomationServiceServicerImpl()

    handler_cls = automation.get_service_handler_based_on_service_types(ServiceTypeEnum.SERVICETYPE_INT, ServiceTypeEnum.SERVICETYPE_L2NM , ZSM_SERVICE_HANDLERS)
    if handler_cls:
        assert True
    else:
        assert False


def test_get_service_handler_based_on_service_types_error():
    automation = AutomationServiceServicerImpl()

    handler_cls = automation.get_service_handler_based_on_service_types(ServiceTypeEnum.SERVICETYPE_INT , ServiceTypeEnum.SERVICETYPE_L2NM , ZSM_SERVICE_HANDLERS)
    if handler_cls:
        assert True
    else:
        assert False

def test_check_if_requested_services_pass_filter_criteria():
    filter = {
            ZSMFilterFieldEnum.TARGET_SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
            ZSMFilterFieldEnum.TELEMETRY_SERVICE_TYPE : ServiceTypeEnum.SERVICETYPE_INT,
        }

    automation = AutomationServiceServicerImpl()
    flag = automation.check_if_requested_services_pass_filter_criteria(filter , ServiceTypeEnum.SERVICETYPE_L2NM , ServiceTypeEnum.SERVICETYPE_INT)

    if flag:
        assert True
    else:
        assert False

def test_check_if_requested_services_pass_filter_criteria_error():
    filter = {
            ZSMFilterFieldEnum.TARGET_SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
            ZSMFilterFieldEnum.TELEMETRY_SERVICE_TYPE : ServiceTypeEnum.SERVICETYPE_INT,
        }

    automation = AutomationServiceServicerImpl()
    flag = automation.check_if_requested_services_pass_filter_criteria(filter , ServiceTypeEnum.SERVICETYPE_INT , ServiceTypeEnum.SERVICETYPE_L2NM)

    if flag:
        assert False
    else:
        assert True
