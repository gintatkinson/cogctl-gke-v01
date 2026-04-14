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

import ast
import json
import logging
import requests
from flask_restful import Resource
from common.Constants import DEFAULT_CONTEXT_NAME
from service.client.ServiceClient import ServiceClient
from .Tools import grpc_service_id
from concurrent.futures import ThreadPoolExecutor
import requests
import threading

LOGGER = logging.getLogger(__name__)


HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

headers = {
    "Content-Type": "application/json",
    "Expect": ""
}

class E2EInfoDelete(Resource):
    def __init__(self):
        super().__init__()
        self.service_client = ServiceClient()

    def delete(self, allocationId: str):
        service_id = ""
        if 'ipowdm' in allocationId:
            service_id    = allocationId.split('=')[1].split(':')[0].split('[[')[0]
            nodes_str      = allocationId.split('[[')[1].split(']]')[0]
            nodes_list_str = nodes_str + ']'
            nodes      = ast.literal_eval(nodes_list_str)
            data_str   = allocationId.split(':', 1)[1]
            data       = json.loads(data_str)
            components = data.get("components", [])

            src = nodes[0]
            dst_list = nodes[1:]
            services = [f"L3VPN_{src}_{dst}" for dst in dst_list]
            for service in services:
                url = f"http://192.168.202.254:80/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service={service}"
                response = requests.delete(url=url)
                LOGGER.debug(f"RESPONSE :\n {response}")

            for i, device in enumerate(components):
                if i >= len(nodes):
                    LOGGER.warning(f"Index {i} exceeds nodes list length {len(nodes)}")
                    break
                name = nodes[i]
                if name == "T2.1":device["frequency"]= 195000000
                if name == "T1.1":device["frequency"]= 195006250
                if name == "T1.2":device["frequency"]= 195018750
                if name == "T1.3":device["frequency"]= 195031250

                LOGGER.debug(f"NODE TO DELETE: \n{name}:{device}")
                response = test_patch_optical_channel_frequency(device, name)
                LOGGER.debug(f"RESPONSE :\n {response}")
        elif 'tapi_lsp' in allocationId:
            service_id = str(allocationId.split('=')[1])
            service_id_list = [s.strip() for s in service_id.split(',')]
            service_id = service_id_list[0]

            LOGGER.info("Service ID list: %s", service_id_list)

            executor = ThreadPoolExecutor(max_workers=len(service_id_list))
            for key in service_id_list:
                executor.submit(delete_slice, key, headers)

            threading.Thread(target=executor.shutdown, kwargs={'wait': True}).start()
        else:
            LOGGER.error("Unknown service type for allocationId: %s", allocationId)
            return {
                'status': 'Error',
                'message': 'Unknown service type',
            }, 400

        service_id = grpc_service_id(DEFAULT_CONTEXT_NAME, service_id)
        self.service_client.DeleteService(service_id)

        return {
            'status': 'Service deleted',
            'allocationId': allocationId,
        }, 200

def delete_slice(key, headers):
    url_delete_slice = f'http://172.24.36.54:4900/restconf/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={key}'
    try:
        response = requests.delete(url=url_delete_slice, headers=headers, timeout=300)
        LOGGER.info("Key: %s", key)
        LOGGER.info("Response Status code: %s", response.status_code)
        LOGGER.info("Response Text: %s", response.text)
    except requests.exceptions.RequestException as e:
        LOGGER.info(f"ERROR request to delete slice {key} failed: {e}")

def test_patch_optical_channel_frequency(data, DEVICE_ID):
    """Test PATCH to update optical channel frequency."""
    # Use simple path with / and encode manually for component name
    encoded_path = f"http://192.168.202.254:80/restconf/data/device={DEVICE_ID}/openconfig-platform:components/component=channel-1/optical-channel/config"

    # Update frequency
    patch_data = data

    response = requests.patch(f"{encoded_path}",
                            json=patch_data,
                            headers=HEADERS)
    assert response.status_code == 200

    # Validate restoration
    return response
