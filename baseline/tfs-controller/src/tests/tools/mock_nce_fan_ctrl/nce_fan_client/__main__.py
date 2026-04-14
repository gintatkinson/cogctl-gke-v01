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
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from .Requests import (
    URL_QOS_PROFILE_ITEM, REQUEST_QOS_PROFILE,
    URL_APPLICATION_ITEM, REQUEST_APPLICATION,
    URL_APP_FLOW_ITEM,    REQUEST_APP_FLOW,
)

logging.basicConfig(level=logging.INFO)
logging.getLogger('RestConfClient').setLevel(logging.DEBUG)
LOGGER = logging.getLogger(__name__)

def main() -> None:
    restconf_client = RestConfClient(
        '172.17.0.1', port=8081,
        logger=logging.getLogger('RestConfClient')
    )

    LOGGER.info('Creating QoS Profile: {:s}'.format(str(REQUEST_QOS_PROFILE)))
    restconf_client.post(URL_QOS_PROFILE_ITEM, body=REQUEST_QOS_PROFILE)

    LOGGER.info('Creating Application: {:s}'.format(str(REQUEST_APPLICATION)))
    restconf_client.post(URL_APPLICATION_ITEM, body=REQUEST_APPLICATION)

    LOGGER.info('Creating App Flow: {:s}'.format(str(REQUEST_APP_FLOW)))
    restconf_client.post(URL_APP_FLOW_ITEM, body=REQUEST_APP_FLOW)


if __name__ == '__main__':
    main()
