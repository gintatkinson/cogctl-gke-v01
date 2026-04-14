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

import pytest
from common.Settings import get_setting
from common.proto.monitoring_pb2 import AlarmDescriptor, AlarmSubscription
from nbi.tests.mock_osm.MockOSM import MockOSM
from .Objects import WIM_MAPPING, WIM_PASSWORD, WIM_USERNAME


@pytest.fixture(scope='session')
def osm_wim():
    wim_url = 'http://{:s}:{:s}'.format(
        get_setting('NBISERVICE_SERVICE_HOST'), str(get_setting('NBISERVICE_SERVICE_PORT_HTTP')))
    return MockOSM(wim_url, WIM_MAPPING, WIM_USERNAME, WIM_PASSWORD)

@pytest.fixture(scope='session')
def alarm_descriptor():

    alarm_descriptor = AlarmDescriptor()

    alarm_descriptor.alarm_description                      = "Default Alarm Description"
    alarm_descriptor.name                                   = "Default Alarm Name"
    alarm_descriptor.kpi_value_range.kpiMinValue.floatVal   = 0.0
    alarm_descriptor.kpi_value_range.kpiMaxValue.floatVal   = 250.0
    alarm_descriptor.kpi_value_range.inRange                = True
    alarm_descriptor.kpi_value_range.includeMinValue        = False
    alarm_descriptor.kpi_value_range.includeMaxValue        = True

    return alarm_descriptor

@pytest.fixture(scope='session')
def alarm_subscription():

    alarm_subscription = AlarmSubscription()

    alarm_subscription.subscription_timeout_s      = 10
    alarm_subscription.subscription_frequency_ms   = 2000

    return alarm_subscription