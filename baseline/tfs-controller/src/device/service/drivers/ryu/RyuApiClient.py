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
from requests.auth import HTTPBasicAuth
from typing import Dict, List, Optional, Union
from common.proto.context_pb2 import DeviceDriverEnum, DeviceOperationalStatusEnum


CHECK_CRED_URL     = '{:s}://{:s}:{:d}'
GET_DEVICES_URL    = '{:s}://{:s}:{:d}/v1.0/topology/switches'
GET_LINKS_URL      = '{:s}://{:s}:{:d}/v1.0/topology/links'
ADD_FLOW_ENTRY_URL = '{:s}://{:s}:{:d}/stats/flowentry/add'
DEL_FLOW_ENTRY_URL = '{:s}://{:s}:{:d}/stats/flowentry/delete_strict'

TIMEOUT = 30

HTTP_OK_CODES = {
    200,    # OK
    201,    # Created
    202,    # Accepted
    204,    # No Content
}

MSG_ERROR = 'Could not retrieve devices in remote Ryu instance({:s}). status_code={:s} reply={:s}'

LOGGER = logging.getLogger(__name__)

class RyuApiClient:
    def __init__(
        self, address : str, port : int, scheme : str = 'http',
        username : Optional[str] = None, password : Optional[str] = None,
        timeout : int = TIMEOUT
    ) -> None:
        self._check_cred_url     = CHECK_CRED_URL    .format(scheme, address, port)
        self._get_devices_url    = GET_DEVICES_URL   .format(scheme, address, port)
        self._get_links_url      = GET_LINKS_URL     .format(scheme, address, port)
        self._add_flow_entry_url = ADD_FLOW_ENTRY_URL.format(scheme, address, port)
        self._del_flow_entry_url = DEL_FLOW_ENTRY_URL.format(scheme, address, port)
        self._auth = None if username is None or password is None else HTTPBasicAuth(username, password)
        self._timeout = timeout

    def check_credentials(self) -> bool:
        try:
            response = requests.get(self._check_cred_url, timeout=self._timeout, verify=False, auth=self._auth)
            response.raise_for_status()
            return True
        except requests.exceptions.Timeout:
            LOGGER.exception('Timeout connecting to {:s}'.format(str(self._check_cred_url)))
            return False
        except requests.exceptions.RequestException as e:
            LOGGER.exception('Exception connecting to {:s}'.format(str(self._check_cred_url)))
            return False

    def get_devices_endpoints(self) -> List[Dict]:
        LOGGER.debug('[get_devices_endpoints] begin')

        reply_switches = requests.get(self._get_devices_url, timeout=self._timeout, verify=False, auth=self._auth)
        if reply_switches.status_code not in HTTP_OK_CODES:
            msg = MSG_ERROR.format(str(self._get_devices_url), str(reply_switches.status_code), str(reply_switches))
            LOGGER.error(msg)
            raise Exception(msg)

        json_reply_switches = reply_switches.json()
        LOGGER.debug('[get_devices_endpoints] json_reply_switches={:s}'.format(json.dumps(json_reply_switches)))

        result = list()
        for json_switch in json_reply_switches:
            device_uuid : str = json_switch['dpid']
            device_url = '/devices/device[{:s}]'.format(device_uuid)
            device_data = {
                'uuid': device_uuid,
                'name': device_uuid,
                'type': 'packet-switch', 
                'status': DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED,
                'drivers': DeviceDriverEnum.DEVICEDRIVER_RYU,
            }
            result.append((device_url, device_data))

            device_ports = json_switch.get('ports', [])
            for port in device_ports: 
                port_name = port.get('name', '')
                #device_name = port_name.split('-')[0]
                #port_no = port.get('port_no', '')
                #hw_address = port.get('hw_addr', '')
                #port_no   = port.get('port_no','')
                endpoint_uuid = port_name
                endpoint_url = '/endpoints/endpoint[{:s}]'.format(endpoint_uuid)
                endpoint_data = {
                    'device_uuid': device_uuid,
                    'uuid': port_name,
                    'name': port_name,
                    'type': 'copper',
                }
                result.append((endpoint_url, endpoint_data))

        reply_links = requests.get(self._get_links_url, timeout=self._timeout, verify=False, auth=self._auth)
        if reply_links.status_code not in HTTP_OK_CODES:
            msg = MSG_ERROR.format(str(self._get_links_url), str(reply_links.status_code), str(reply_links))
            LOGGER.error(msg)
            raise Exception(msg)

        json_reply_links = reply_links.json()
        LOGGER.debug('[get_devices_endpoints] json_reply_links={:s}'.format(json.dumps(json_reply_links)))

        for json_link in json_reply_links:
            dpid_src = json_link.get('src', {}).get('dpid', '')
            dpid_dst = json_link.get('dst', {}).get('dpid', '')
            port_src_name = json_link.get('src', {}).get('name', '')
            #port_name_secondpart = port_src_name.split('-')[1]
            port_dst_name = json_link.get('dst', {}).get('name', '')
            #port_name_second = port_dst_name.split('-')[1]
            #switch_name_src = port_src_name.split('-')[0]
            #switch_name_dest = port_dst_name.split('-')[0]
            link_name = f"{dpid_src}/{port_src_name}=={dpid_dst}/{port_dst_name}"
            link_uuid = f"{port_src_name}=={port_dst_name}" 
            link_endpoint_ids = [
                (dpid_src, port_src_name),
                (dpid_dst, port_dst_name),
            ]

            LOGGER.debug('link_endpoint_ids = {:s}'.format(str(link_endpoint_ids)))
            link_url = '/links/link[{:s}]'.format(link_uuid)
            link_data = {
                'uuid': link_uuid,
                'name': link_name,
                'endpoints': link_endpoint_ids,
            }
            result.append((link_url, link_data))

        LOGGER.debug('[get_devices_endpoints] topology; returning')
        return result

    def add_flow_rule(
        self, dpid : int, in_port : int, out_port : int,
        eth_type : int, ip_src_addr : str, ip_dst_addr : str,
        priority : int = 65535,
    ) -> Union[bool, Exception]:
        flow_entry = {
            "dpid"    : dpid,
            "priority": priority,
            "match"   : {
                "in_port" : in_port,
                "eth_type": eth_type,
                "ipv4_src": ip_src_addr,
                "ipv4_dst": ip_dst_addr,
            },
            "instructions": [
                {
                    "type": "APPLY_ACTIONS",
                    "actions": [
                        {
                            "max_len": 65535,
                            "type": "OUTPUT",
                            "port": out_port
                        }
                    ]
                }
            ]
        }

        LOGGER.debug("[add_flow_rule] flow_entry = {:s}".format(str(flow_entry)))

        try:
            response = requests.post(
                self._add_flow_entry_url, json=flow_entry,
                timeout=self._timeout, verify=False, auth=self._auth
            )
            response.raise_for_status()
            LOGGER.info("Successfully posted flow entry: {:s}".format(str(flow_entry)))
            return True
        except requests.exceptions.Timeout as e:
            MSG = "Timeout adding flow rule {:s} {:s}"
            LOGGER.exception(MSG.format(str(self._add_flow_entry_url), str(flow_entry)))
            return e
        except requests.exceptions.RequestException as e:
            MSG = "Error adding flow rule {:s} {:s}"
            LOGGER.exception(MSG.format(str(self._add_flow_entry_url), str(flow_entry)))
            return e


    def del_flow_rule(
        self, dpid : int, in_port : int, out_port : int,
        eth_type : int, ip_src_addr : str, ip_dst_addr : str,
        priority : int = 65535,
    ) -> Union[bool, Exception]:
        flow_entry = {
            "dpid"    : dpid,
            "priority": priority,
            "match"   : {
                "in_port" : in_port,
                "eth_type": eth_type,
                "ipv4_src": ip_src_addr,
                "ipv4_dst": ip_dst_addr,
                "table_id"   : 0,
                "cookie"     : 0,
                "cookie_mask": 0,
            },
            "instructions": [
                {
                    "type": "APPLY_ACTIONS",
                    "actions": [
                        {
                            "max_len": 65535,
                            "type": "OUTPUT",
                            "port": out_port
                        }
                    ]
                }
            ]
        }

        LOGGER.debug("[del_flow_rule] flow_entry = {:s}".format(str(flow_entry)))

        try:
            response = requests.post(
                self._del_flow_entry_url, json=flow_entry,
                timeout=self._timeout, verify=False, auth=self._auth
            )
            response.raise_for_status()
            LOGGER.info("Successfully posted flow entry: {:s}".format(str(flow_entry)))
            return True
        except requests.exceptions.Timeout as e:
            MSG = "Timeout deleting flow rule {:s} {:s}"
            LOGGER.exception(MSG.format(str(self._del_flow_entry_url), str(flow_entry)))
            return e
        except requests.exceptions.RequestException as e:
            MSG = "Error deleting flow rule {:s} {:s}"
            LOGGER.exception(MSG.format(str(self._del_flow_entry_url), str(flow_entry)))
            return e
