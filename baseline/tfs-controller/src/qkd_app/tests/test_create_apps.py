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

import requests

QKD_ADDRESS = '127.0.0.1'
QKD_URL     = 'http://{:s}/qkd_app/create_qkd_app'.format(QKD_ADDRESS)

QKD_REQUEST_1 = {
    'app': {
        'server_app_id': '1',
        'client_app_id': [],
        'app_status': 'ON',
        'local_qkdn_id': '00000001-0000-0000-0000-000000000000',
        'backing_qkdl_id': ['00000003-0002-0000-0000-000000000000'],
    }
}
reply = requests.post(QKD_URL, json=QKD_REQUEST_1)
print(reply.status_code, reply.text)

QKD_REQUEST_2 = {
    'app': {
        'server_app_id': '1',
        'client_app_id': [],
        'app_status': 'ON',
        'local_qkdn_id': '00000003-0000-0000-0000-000000000000',
        'backing_qkdl_id': ['00000003-0002-0000-0000-000000000000'],
    }
}
reply = requests.post(QKD_URL, json=QKD_REQUEST_2)
print(reply.status_code, reply.text)
