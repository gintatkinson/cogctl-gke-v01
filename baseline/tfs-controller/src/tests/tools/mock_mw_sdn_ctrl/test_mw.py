# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, logging, requests
from requests.auth import HTTPBasicAuth
from typing import Optional

LOGGER = logging.getLogger(__name__)

HTTP_OK_CODES = {
    200,    # OK
    201,    # Created
    202,    # Accepted
    204,    # No Content
}

def create_connectivity_service(
    root_url, uuid, node_id_src, tp_id_src, node_id_dst, tp_id_dst, vlan_id,
    auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None
):

    url = '{:s}/nmswebs/restconf/data/ietf-eth-tran-service:etht-svc'.format(root_url)
    headers = {'content-type': 'application/json'}
    data = {
        'etht-svc-instances': [
            {
                'etht-svc-name': uuid,
                'etht-svc-type': 'ietf-eth-tran-types:p2p-svc',
                'etht-svc-end-points': [
                    {
                        'etht-svc-access-points': [
                            {'access-node-id': node_id_src, 'access-ltp-id': tp_id_src, 'access-point-id': '1'}
                        ],
                        'outer-tag': {'vlan-value': vlan_id, 'tag-type': 'ietf-eth-tran-types:classify-c-vlan'},
                        'etht-svc-end-point-name': '{:s}:{:s}'.format(str(node_id_src), str(tp_id_src)),
                        'service-classification-type': 'ietf-eth-tran-types:vlan-classification'
                    },
                    {
                        'etht-svc-access-points': [
                            {'access-node-id': node_id_dst, 'access-ltp-id': tp_id_dst, 'access-point-id': '2'}
                        ],
                        'outer-tag': {'vlan-value': vlan_id, 'tag-type': 'ietf-eth-tran-types:classify-c-vlan'},
                        'etht-svc-end-point-name': '{:s}:{:s}'.format(str(node_id_dst), str(tp_id_dst)),
                        'service-classification-type': 'ietf-eth-tran-types:vlan-classification'
                    }
                ]
            }
        ]
    }
    results = []
    try:
        LOGGER.info('Connectivity service {:s}: {:s}'.format(str(uuid), str(data)))
        response = requests.post(
            url=url, data=json.dumps(data), timeout=timeout, headers=headers, verify=False, auth=auth)
        LOGGER.info('Microwave Driver response: {:s}'.format(str(response)))
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception creating ConnectivityService(uuid={:s}, data={:s})'.format(str(uuid), str(data)))
        results.append(e)
    else:
        if response.status_code not in HTTP_OK_CODES:
            msg = 'Could not create ConnectivityService(uuid={:s}, data={:s}). status_code={:s} reply={:s}'
            LOGGER.error(msg.format(str(uuid), str(data), str(response.status_code), str(response)))
        results.append(response.status_code in HTTP_OK_CODES)
    return results

def delete_connectivity_service(root_url, uuid, auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None):
    url = '{:s}/nmswebs/restconf/data/ietf-eth-tran-service:etht-svc/etht-svc-instances={:s}'
    url = url.format(root_url, uuid)
    results = []
    try:
        response = requests.delete(url=url, timeout=timeout, verify=False, auth=auth)
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception deleting ConnectivityService(uuid={:s})'.format(str(uuid)))
        results.append(e)
    else:
        if response.status_code not in HTTP_OK_CODES:
            msg = 'Could not delete ConnectivityService(uuid={:s}). status_code={:s} reply={:s}'
            LOGGER.error(msg.format(str(uuid), str(response.status_code), str(response)))
        results.append(response.status_code in HTTP_OK_CODES)
    return results

if __name__ == '__main__':
    ROOT_URL = 'https://127.0.0.1:8443'
    SERVICE_UUID = 'my-service'

    create_connectivity_service(ROOT_URL, SERVICE_UUID, '172.18.0.1', '1', '172.18.0.2', '2', 300)
    delete_connectivity_service(ROOT_URL, SERVICE_UUID)
