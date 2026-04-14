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
import json

from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    ztp_server_application, do_rest_get_request
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

BASE_URL = '/provisioning'

def test_get_config_file(ztp_server_application,   # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    URL = BASE_URL + '/config/ztp.json'
    data = {
    "ztp": {
      "01-provisioning-script": {
        "plugin": {
          "url": "http://localhost:9001/provisioning/provisioning_script_sonic.sh"
        },
        "reboot-on-success": True
      }}
    }
    retrieved_data = do_rest_get_request(URL, body=data, logger=LOGGER, expected_status_codes={200})
    LOGGER.debug('retrieved_data={:s}'.format(json.dumps(retrieved_data, sort_keys=True)))
