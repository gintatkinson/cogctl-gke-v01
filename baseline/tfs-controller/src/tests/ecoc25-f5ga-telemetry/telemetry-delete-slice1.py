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
from requests.auth import HTTPBasicAuth


RESTCONF_ADDRESS = '127.0.0.1'
RESTCONF_PORT = 80
TELEMETRY_ID = 1109405947767160833

UNSUBSCRIBE_URI = '/restconf/operations/subscriptions:delete-subscription'
UNSUBSCRIBE_URL = 'http://{:s}:{:d}{:s}'.format(RESTCONF_ADDRESS, RESTCONF_PORT, UNSUBSCRIBE_URI)
REQUEST = {
    'ietf-subscribed-notifications:input': {
        'id': TELEMETRY_ID,
    }
}


def main() -> None:
    print('[E2E] Delete Telemetry slice1...')
    headers = {'accept': 'application/json'}
    auth = HTTPBasicAuth('admin', 'admin')
    print(UNSUBSCRIBE_URL)
    print(REQUEST)
    reply = requests.post(
        UNSUBSCRIBE_URL, headers=headers, json=REQUEST, auth=auth,
        verify=False, allow_redirects=True, timeout=30
    )
    reply.raise_for_status()

if __name__ == '__main__':
    main()
