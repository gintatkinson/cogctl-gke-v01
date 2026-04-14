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


import logging, requests
from typing import Dict, List, Optional, Union
from common.tools.rest_api.client.RestApiClient import RestApiClient


LOGGER = logging.getLogger(__name__)

GET_OPTICAL_LINKS_URL = '/OpticalTFS/GetLinks'
GET_LIGHTPATHS_URL    = '/OpticalTFS/GetLightpaths'
ADD_LIGHTPATH_URL     = '/OpticalTFS/AddLightpath/{src_node:s}/{dst_node:s}/{bitrate:s}'
DEL_LIGHTPATH_URL     = '/OpticalTFS/DelLightpath/{flow_id:s}/{src_node:s}/{dst_node:s}/{bitrate:s}'


class TfsOpticalClient(RestApiClient):
    def __init__(
        self, address : str, port : int, scheme : str = 'http',
        username : Optional[str] = None, password : Optional[str] = None,
        timeout : Optional[int] = 30
    ) -> None:
        super().__init__(
            address, port, scheme=scheme, username=username, password=password,
            timeout=timeout, verify_certs=False, allow_redirects=True, logger=LOGGER
        )

    def check_credentials(self) -> None:
        self.get(GET_LIGHTPATHS_URL, expected_status_codes={requests.codes['OK']})
        LOGGER.info('Credentials checked')

    def get_optical_links(self) -> Union[List[Dict], Exception]:
        try:
            return self.get(GET_OPTICAL_LINKS_URL, expected_status_codes={requests.codes['OK']})
        except Exception as e:
            LOGGER.exception('Exception retrieving optical links')
            return e

    def get_lightpaths(self) -> Union[List[Dict], Exception]:
        try:
            lightpaths : List[Dict] = self.get(
                GET_LIGHTPATHS_URL, expected_status_codes={requests.codes['OK']}
            )
        except Exception as e:
            LOGGER.exception('Exception retrieving lightpaths')
            return e

        result = []
        for lightpath in lightpaths:
            assert 'flow_id' in lightpath
            assert 'src'     in lightpath
            assert 'dst'     in lightpath
            assert 'bitrate' in lightpath
            resource_key = '/lightpaths/lightpath[{:s}]'.format(lightpath['flow_id'])
            result.append((resource_key, lightpath))
        return result

    def add_lightpath(
        self, src_node : str, dst_node : str, bitrate : int
    ) -> Union[List[Dict], Exception]:
        MSG = 'Add Lightpath: {:s} <-> {:s} with {:d} bitrate'
        LOGGER.info(MSG.format(str(src_node), str(dst_node), int(bitrate)))
        request_endpoint = ADD_LIGHTPATH_URL.format(
            src_node=str(src_node), dst_node=str(dst_node), bitrate=int(bitrate)
        )
        expected_status_codes = {requests.codes['CREATED'], requests.codes['NO_CONTENT']}
        try:
            return self.put(request_endpoint, expected_status_codes=expected_status_codes)
        except Exception as e:
            MSG = 'Exception requesting Lightpath: {:s} <-> {:s} with {:s} bitrate'
            LOGGER.exception(MSG.format(str(src_node), str(dst_node), str(bitrate)))
            return e

    def del_lightpath(
        self, flow_id : str, src_node : str, dst_node : str, bitrate : int
    ) -> Union[List[Dict], Exception]:
        MSG = 'Delete Lightpath {:s}: {:s} <-> {:s} with {:d} bitrate'
        LOGGER.info(MSG.format(str(flow_id), str(src_node), str(dst_node), int(bitrate)))
        request_endpoint = DEL_LIGHTPATH_URL.format(
            src_node=str(src_node), dst_node=str(dst_node), bitrate=int(bitrate)
        )
        expected_status_codes = {requests.codes['NO_CONTENT']}
        try:
            return self.delete(request_endpoint, expected_status_codes=expected_status_codes)
        except Exception as e:
            MSG = 'Exception deleting Lightpath {:s}: {:s} <-> {:s} with {:s} bitrate'
            LOGGER.exception(MSG.format(str(flow_id), str(src_node), str(dst_node), str(bitrate)))
            return e
