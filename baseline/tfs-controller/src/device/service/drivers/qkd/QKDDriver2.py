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

import os
import json
import logging
import requests
import threading
from requests.auth import HTTPBasicAuth
from typing import Any, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.type_checkers.Checkers import chk_string, chk_type
from device.service.driver_api._Driver import _Driver
from .Tools2 import config_getter, create_connectivity_link
from device.service.driver_api._Driver import _Driver
from . import ALL_RESOURCE_KEYS

LOGGER = logging.getLogger(__name__)

DRIVER_NAME = 'qkd'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})


class QKDDriver(_Driver):
    def __init__(self, address: str, port: int, **settings) -> None:
        LOGGER.info(f"Initializing QKDDriver with address={address}, port={port}, settings={settings}")
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        self.__auth = None
        self.__headers = {}
        self.__qkd_root = os.getenv('QKD_API_URL', f"http://{self.address}:{self.port}")  # Simplified URL management
        self.__timeout = int(self.settings.get('timeout', 120))
        self.__node_ids = set(self.settings.get('node_ids', []))
        self.__initial_data = None

        # Optionally pass headers for authentication (e.g., JWT)
        self.__headers = settings.get('headers', {})
        self.__auth = settings.get('auth', None)

        LOGGER.info(f"QKDDriver initialized with QKD root URL: {self.__qkd_root}")

    def Connect(self) -> bool:
        url = self.__qkd_root + '/restconf/data/etsi-qkd-sdn-node:qkd_node'
        with self.__lock:
            LOGGER.info(f"Starting connection to {url}")
            if self.__started.is_set():
                LOGGER.info("Already connected, skipping re-connection.")
                return True

            try:
                LOGGER.info(f'Attempting to connect to {url} with headers {self.__headers} and timeout {self.__timeout}')
                response = requests.get(url, timeout=self.__timeout, verify=False, headers=self.__headers, auth=self.__auth)
                LOGGER.info(f'Received response: {response.status_code}, content: {response.text}')
                response.raise_for_status()
                self.__initial_data = response.json()
                self.__started.set()
                LOGGER.info('Connection successful')
                return True
            except requests.exceptions.RequestException as e:
                LOGGER.error(f'Connection failed: {e}')
                return False

    def Disconnect(self) -> bool:
        LOGGER.info("Disconnecting QKDDriver")
        with self.__lock:
            self.__terminate.set()
            LOGGER.info("QKDDriver disconnected successfully")
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        LOGGER.info("Getting initial configuration")
        with self.__lock:
            if isinstance(self.__initial_data, dict):
                initial_config = [('qkd_node', self.__initial_data.get('qkd_node', {}))]
                LOGGER.info(f"Initial configuration: {initial_config}")
                return initial_config
            LOGGER.warning("Initial data is not a dictionary")
            return []

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys: List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        LOGGER.info(f"Getting configuration for resource_keys: {resource_keys}")
        results = []
        with self.__lock:
            if not resource_keys:
                resource_keys = ALL_RESOURCE_KEYS
            for i, resource_key in enumerate(resource_keys):
                chk_string(f'resource_key[{i}]', resource_key, allow_empty=False)
                LOGGER.info(f"Retrieving resource key: {resource_key}")
                resource_results = config_getter(
                    self.__qkd_root, resource_key, timeout=self.__timeout, headers=self.__headers, auth=self.__auth)
                results.extend(resource_results)
                LOGGER.info(f"Resource results for {resource_key}: {resource_results}")
        LOGGER.info(f"Final configuration results: {results}")
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0:
            return results

        with self.__lock:
            for resource_key, resource_value in resources:
                LOGGER.info('Processing resource_key = {:s}'.format(str(resource_key)))

                # Only process '/link' keys
                if resource_key.startswith('/link'):
                    try:
                        # Ensure resource_value is deserialized
                        if isinstance(resource_value, str):
                            resource_value = json.loads(resource_value)
                        
                        # Extract values from resource_value dictionary
                        link_uuid = resource_value['uuid']
                        node_id_src = resource_value['src_qkdn_id']
                        interface_id_src = resource_value['src_interface_id']
                        node_id_dst = resource_value['dst_qkdn_id']
                        interface_id_dst = resource_value['dst_interface_id']
                        virt_prev_hop = resource_value.get('virt_prev_hop')
                        virt_next_hops = resource_value.get('virt_next_hops')
                        virt_bandwidth = resource_value.get('virt_bandwidth')

                        # Call create_connectivity_link with the extracted values
                        LOGGER.info(f"Creating connectivity link with UUID: {link_uuid}")
                        data = create_connectivity_link(
                            self.__qkd_root, link_uuid, node_id_src, interface_id_src, node_id_dst, interface_id_dst,
                            virt_prev_hop, virt_next_hops, virt_bandwidth,
                            timeout=self.__timeout, auth=self.__auth
                        )

                        # Append success result
                        results.append(True)
                        LOGGER.info(f"Connectivity link {link_uuid} created successfully")

                    except Exception as e:
                        # Catch and log any unhandled exceptions
                        LOGGER.exception(f'Unhandled error processing resource_key({resource_key})')
                        results.append(e)
                else:
                    # Skip unsupported resource keys and append success
                    results.append(True)

        # Logging test results
        LOGGER.info('Test keys: ' + str([x for x,y in resources]))
        LOGGER.info('Test values: ' + str(results))

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        LOGGER.info(f"Deleting configuration for resources: {resources}")
        results = []
        if not resources:
            LOGGER.warning("No resources provided for DeleteConfig")
            return results
        with self.__lock:
            for resource in resources:
                LOGGER.info(f'Resource to delete: {resource}')
                uuid = resource[1].get('uuid')
                if uuid:
                    LOGGER.info(f'Resource with UUID {uuid} deleted successfully')
                    results.append(True)
                else:
                    LOGGER.warning(f"UUID not found in resource: {resource}")
                    results.append(False)
        LOGGER.info(f"DeleteConfig results: {results}")
        return results

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions: List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        LOGGER.info(f"Subscribing to state updates: {subscriptions}")
        results = [True for _ in subscriptions]
        LOGGER.info(f"Subscription results: {results}")
        return results

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions: List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        LOGGER.info(f"Unsubscribing from state updates: {subscriptions}")
        results = [True for _ in subscriptions]
        LOGGER.info(f"Unsubscription results: {results}")
        return results

    @metered_subclass_method(METRICS_POOL)
    def GetState(self, blocking=False, terminate: Optional[threading.Event] = None) -> Union[dict, list]:
        LOGGER.info(f"GetState called with blocking={blocking}, terminate={terminate}")
        url = self.__qkd_root + '/restconf/data/etsi-qkd-sdn-node:qkd_node'
        try:
            LOGGER.info(f"Making GET request to {url} to retrieve state")
            response = requests.get(url, timeout=self.__timeout, verify=False, headers=self.__headers, auth=self.__auth)
            LOGGER.info(f"Received state response: {response.status_code}, content: {response.text}")
            response.raise_for_status()
            state_data = response.json()
            LOGGER.info(f"State data retrieved: {state_data}")
            return state_data
        except requests.exceptions.Timeout:
            LOGGER.error(f'Timeout getting state from {self.__qkd_root}')
            return []
        except Exception as e:
            LOGGER.error(f'Exception getting state from {self.__qkd_root}: {e}')
            return []
