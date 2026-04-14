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
from typing import Dict, List, Optional
from common.tools.rest_api.client.RestApiClient import RestApiClient
from device.service.driver_api.ImportTopologyEnum import ImportTopologyEnum

GET_CONTEXT_IDS_URL = '/tfs-api/context_ids'
GET_DEVICES_URL     = '/tfs-api/devices'
GET_LINKS_URL       = '/tfs-api/links'

MAPPING_STATUS = {
    'DEVICEOPERATIONALSTATUS_UNDEFINED': 0,
    'DEVICEOPERATIONALSTATUS_DISABLED' : 1,
    'DEVICEOPERATIONALSTATUS_ENABLED'  : 2,
}

MAPPING_DRIVER = {
    'DEVICEDRIVER_UNDEFINED'            : 0,
    'DEVICEDRIVER_OPENCONFIG'           : 1,
    'DEVICEDRIVER_TRANSPORT_API'        : 2,
    'DEVICEDRIVER_P4'                   : 3,
    'DEVICEDRIVER_IETF_NETWORK_TOPOLOGY': 4,
    'DEVICEDRIVER_ONF_TR_532'           : 5,
    'DEVICEDRIVER_XR'                   : 6,
    'DEVICEDRIVER_IETF_L2VPN'           : 7,
    'DEVICEDRIVER_GNMI_OPENCONFIG'      : 8,
    'DEVICEDRIVER_OPTICAL_TFS'          : 9,
    'DEVICEDRIVER_IETF_ACTN'            : 10,
    'DEVICEDRIVER_OC'                   : 11,
    'DEVICEDRIVER_QKD'                  : 12,
    'DEVICEDRIVER_IETF_L3VPN'           : 13,
    'DEVICEDRIVER_IETF_SLICE'           : 14,
    'DEVICEDRIVER_NCE'                  : 15,
    'DEVICEDRIVER_SMARTNIC'             : 16,
    'DEVICEDRIVER_MORPHEUS'             : 17,
    'DEVICEDRIVER_RYU'                  : 18,
    'DEVICEDRIVER_GNMI_NOKIA_SRLINUX'   : 19,
    'DEVICEDRIVER_OPENROADM'            : 20,
    'DEVICEDRIVER_RESTCONF_OPENCONFIG'  : 21,
}

LOGGER = logging.getLogger(__name__)

class TfsApiClient(RestApiClient):
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
        self.get(GET_CONTEXT_IDS_URL, expected_status_codes={requests.codes['OK']})
        LOGGER.info('Credentials checked')

    def get_devices_endpoints(
        self, import_topology : ImportTopologyEnum = ImportTopologyEnum.DEVICES
    ) -> List[Dict]:
        LOGGER.debug('[get_devices_endpoints] begin')
        MSG = '[get_devices_endpoints] import_topology={:s}'
        LOGGER.debug(MSG.format(str(import_topology)))

        if import_topology == ImportTopologyEnum.DISABLED:
            MSG = 'Unsupported import_topology mode: {:s}'
            raise Exception(MSG.format(str(import_topology)))

        devices = self.get(GET_DEVICES_URL, expected_status_codes={requests.codes['OK']})

        result = list()
        for json_device in devices['devices']:
            device_uuid : str = json_device['device_id']['device_uuid']['uuid']
            device_type : str = json_device['device_type']
            #if not device_type.startswith('emu-'): device_type = 'emu-' + device_type
            device_status = json_device['device_operational_status']
            device_url = '/devices/device[{:s}]'.format(device_uuid)
            device_data = {
                'uuid': json_device['device_id']['device_uuid']['uuid'],
                'name': json_device['name'],
                'type': device_type,
                'status': MAPPING_STATUS[device_status],
                'drivers': [
                    MAPPING_DRIVER[driver]
                    for driver in json_device['device_drivers']
                ],
            }
            result.append((device_url, device_data))

            for json_endpoint in json_device['device_endpoints']:
                endpoint_uuid = json_endpoint['endpoint_id']['endpoint_uuid']['uuid']
                endpoint_url = '/endpoints/endpoint[{:s}]'.format(endpoint_uuid)
                endpoint_data = {
                    'device_uuid': device_uuid,
                    'uuid': endpoint_uuid,
                    'name': json_endpoint['name'],
                    'type': json_endpoint['endpoint_type'],
                }
                result.append((endpoint_url, endpoint_data))

        if import_topology == ImportTopologyEnum.DEVICES:
            LOGGER.debug('[get_devices_endpoints] devices only; returning')
            return result

        links = self.get(GET_LINKS_URL, expected_status_codes={requests.codes['OK']})

        for json_link in links['links']:
            link_uuid : str = json_link['link_id']['link_uuid']['uuid']
            link_url = '/links/link[{:s}]'.format(link_uuid)
            link_endpoint_ids = [
                (
                    json_endpoint_id['device_id']['device_uuid']['uuid'],
                    json_endpoint_id['endpoint_uuid']['uuid'],
                )
                for json_endpoint_id in json_link['link_endpoint_ids']
            ]
            link_data = {
                'uuid': json_link['link_id']['link_uuid']['uuid'],
                'name': json_link['name'],
                'endpoints': link_endpoint_ids,
            }
            result.append((link_url, link_data))

        LOGGER.debug('[get_devices_endpoints] topology; returning')
        return result
