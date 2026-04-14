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
    URL_OSU_TUNNEL_ITEM, REQUEST_OSU_TUNNEL,
    URL_ETHT_SERVICE_ITEM, REQUEST_ETHT_SERVICE,
)

logging.basicConfig(level=logging.INFO)
logging.getLogger('RestConfClient').setLevel(logging.DEBUG)
LOGGER = logging.getLogger(__name__)

def main() -> None:
    restconf_client = RestConfClient(
        '172.17.0.1', port=8081, restconf_version='v2',
        logger=logging.getLogger('RestConfClient')
    )

    LOGGER.info('Creating OSU Tunnel: {:s}'.format(str(REQUEST_OSU_TUNNEL)))
    restconf_client.post(URL_OSU_TUNNEL_ITEM, body=REQUEST_OSU_TUNNEL)

    LOGGER.info('Creating ETH-T Service: {:s}'.format(str(REQUEST_ETHT_SERVICE)))
    restconf_client.post(URL_ETHT_SERVICE_ITEM, body=REQUEST_ETHT_SERVICE)


if __name__ == '__main__':
    main()
