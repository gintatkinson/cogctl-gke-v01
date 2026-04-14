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

import pytest, logging
from common.Settings import get_setting
from tests.tools.mock_osm.Constants import WIM_PASSWORD, WIM_USERNAME
from tests.tools.mock_osm.MockOSM import MockOSM
from .Objects import WIM_MAPPING

LOGGER = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def osm_wim():
    wim_url = 'http://{:s}:{:s}'.format(
        get_setting('NBISERVICE_SERVICE_HOST'), str(get_setting('NBISERVICE_SERVICE_PORT_HTTP')))
    LOGGER.info('WIM_MAPPING = {:s}'.format(str(WIM_MAPPING)))
    return MockOSM(wim_url, WIM_MAPPING, WIM_USERNAME, WIM_PASSWORD)
