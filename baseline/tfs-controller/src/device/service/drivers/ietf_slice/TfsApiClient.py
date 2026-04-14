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

import json, logging, requests
from typing import Dict, List, Optional
from common.tools.rest_api.client.RestApiClient import RestApiClient
from device.service.driver_api.ImportTopologyEnum import ImportTopologyEnum


GET_CONTEXT_IDS_URL = '/tfs-api/context_ids'
GET_DEVICES_URL     = '/tfs-api/devices'
GET_LINKS_URL       = '/tfs-api/links'


IETF_SLICE_ALL_URL  = '/restconf/data/ietf-network-slice-service:network-slice-services'
IETF_SLICE_ONE_URL  = IETF_SLICE_ALL_URL + '/slice-service={:s}'
IETF_SLICE_CG_URL   = IETF_SLICE_ONE_URL + '/connection-groups/connection-group={:s}'


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


    def check_credentials(self, raise_if_fail : bool = True) -> None:
        try:
            LOGGER.info('Checking credentials...')
            self.get(GET_CONTEXT_IDS_URL, expected_status_codes={requests.codes['OK']})
            LOGGER.info('Credentials checked')
            return True
        except requests.exceptions.Timeout as e:
            MSG = 'Timeout connecting {:s}'
            msg = MSG.format(GET_CONTEXT_IDS_URL)
            LOGGER.exception(msg)
            if raise_if_fail: raise Exception(msg) from e
            return False
        except Exception as e:
            MSG = 'Exception connecting credentials: {:s}'
            msg = MSG.format(GET_CONTEXT_IDS_URL)
            LOGGER.exception(msg)
            if raise_if_fail: raise Exception(msg) from e
            return False


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

            ctrl_id : Dict[str, Dict] = json_device.get('controller_id', dict())
            ctrl_uuid : Optional[str] = ctrl_id.get('device_uuid', dict()).get('uuid')

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
            if ctrl_uuid is not None and len(ctrl_uuid) > 0:
                device_data['ctrl_uuid'] = ctrl_uuid
            result.append((device_url, device_data))

            config_rule_list : List[Dict] = (
                json_device
                .get('device_config', dict())
                .get('config_rules', list())
            )
            config_rule_dict = dict()
            for cr in config_rule_list:
                if cr['action'] != 'CONFIGACTION_SET': continue
                if 'custom' not in cr: continue
                cr_rk : str = cr['custom']['resource_key']
                if not cr_rk.startswith('/endpoints/endpoint['): continue
                settings = json.loads(cr['custom']['resource_value'])
                ep_name = settings['name']
                config_rule_dict[ep_name] = settings

            for json_endpoint in json_device['device_endpoints']:
                endpoint_uuid = json_endpoint['endpoint_id']['endpoint_uuid']['uuid']
                endpoint_name = json_endpoint['name']
                endpoint_url = '/endpoints/endpoint[{:s}]'.format(endpoint_uuid)
                endpoint_data = {
                    'device_uuid': device_uuid,
                    'uuid': endpoint_uuid,
                    'name': endpoint_name,
                    'type': json_endpoint['endpoint_type'],
                }
                endpoint_settings = config_rule_dict.get(endpoint_name)
                if endpoint_settings is not None:
                    endpoint_data['settings'] = endpoint_settings
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


    def create_slice(self, data : Dict) -> None:
        MSG = '[create_slice] data={:s}'
        LOGGER.debug(MSG.format(str(data)))
        try:
            MSG = '[create_slice] POST {:s}: {:s}'
            LOGGER.info(MSG.format(str(IETF_SLICE_ALL_URL), str(data)))
            self.post(IETF_SLICE_ALL_URL, body=data)
        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send POST request to TFS IETF Slice NBI'
            raise Exception(MSG) from e


    def list_slices(self) -> Dict:
        try:
            MSG = '[list_slices] GET {:s}'
            LOGGER.info(MSG.format(str(IETF_SLICE_ALL_URL)))
            return self.get(IETF_SLICE_ALL_URL)
        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send GET request to TFS IETF Slice NBI'
            raise Exception(MSG) from e


    def retrieve_slice(self, slice_name : str) -> Dict:
        MSG = '[retrieve_slice] slice_name={:s}'
        LOGGER.debug(MSG.format(str(slice_name)))
        url = IETF_SLICE_ONE_URL.format(slice_name)
        try:
            MSG = '[retrieve_slice] GET {:s}'
            LOGGER.info(MSG.format(str(url)))
            return self.get(url)
        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send GET request to TFS IETF Slice NBI'
            raise Exception(MSG) from e


    def update_slice(
        self, slice_name : str, connection_group_id : str,
        updated_connection_group_data : Dict
    ) -> None:
        MSG = '[update_slice] slice_name={:s} connection_group_id={:s} updated_connection_group_data={:s}'
        LOGGER.debug(MSG.format(str(slice_name), str(connection_group_id), str(updated_connection_group_data)))
        url = IETF_SLICE_CG_URL.format(slice_name, connection_group_id)
        try:
            MSG = '[update_slice] PUT {:s}: {:s}'
            LOGGER.info(MSG.format(str(url), str(updated_connection_group_data)))
            self.put(url, body=updated_connection_group_data)
        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send PUT request to TFS IETF Slice NBI'
            raise Exception(MSG) from e


    def delete_slice(self, slice_name : str) -> None:
        MSG = '[delete_slice] slice_name={:s}'
        LOGGER.debug(MSG.format(str(slice_name)))
        url = IETF_SLICE_ONE_URL.format(slice_name)
        try:
            MSG = '[delete_slice] DELETE {:s}'
            LOGGER.info(MSG.format(str(url)))
            self.delete(url)
        except requests.exceptions.ConnectionError as e:
            MSG = 'Failed to send DELETE request to TFS IETF Slice NBI'
            raise Exception(MSG) from e
