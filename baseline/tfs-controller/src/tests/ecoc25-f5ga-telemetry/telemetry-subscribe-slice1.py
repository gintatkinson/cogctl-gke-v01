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
TARGET_SIMAP_NAME = 'e2e'
TARGET_LINK_NAME  = 'E2E-L1'
SAMPLING_INTERVAL = 10.0


SUBSCRIBE_URI = '/restconf/operations/subscriptions:establish-subscription'
SUBSCRIBE_URL = 'http://{:s}:{:d}{:s}'.format(RESTCONF_ADDRESS, RESTCONF_PORT, SUBSCRIBE_URI)
XPATH_FILTER = '/ietf-network:networks/network={:s}/ietf-network-topology:link={:s}/simap-telemetry:simap-telemetry'
REQUEST = {
    'ietf-subscribed-notifications:input': {
        'datastore': 'operational',
        'ietf-yang-push:datastore-xpath-filter': XPATH_FILTER.format(TARGET_SIMAP_NAME, TARGET_LINK_NAME),
        'ietf-yang-push:periodic': {
            'ietf-yang-push:period': SAMPLING_INTERVAL
        }
    }
}


def main() -> None:
    print('[E2E] Subscribe Telemetry slice1...')
    headers = {'accept': 'application/json'}
    auth = HTTPBasicAuth('admin', 'admin')
    print(SUBSCRIBE_URL)
    print(REQUEST)
    reply = requests.post(
        SUBSCRIBE_URL, headers=headers, json=REQUEST, auth=auth,
        verify=False, allow_redirects=True, timeout=30
    )
    content_type = reply.headers.get('Content-Type', '')
    if 'application/json' not in content_type:
        raise Exception('Not JSON:', reply.content.decode('UTF-8'))
    try:
        reply_data = reply.json()
    except ValueError as e:
        str_error = 'Invalid JSON: {:s}'.format(str(reply.content.decode('UTF-8')))
        raise Exception(str_error) from e

    if 'uri' not in reply_data:
        raise Exception('Unexpected Reply: {:s}'.format(str(reply_data)))
    subscription_uri = reply_data['uri']

    stream_url = 'http://{:s}:{:d}{:s}'.format(RESTCONF_ADDRESS, RESTCONF_PORT, subscription_uri)
    print('Opening stream "{:s}" (press Ctrl+C to stop)...'.format(stream_url))

    with requests.get(stream_url, stream=True) as resp:
        for line in resp.iter_lines(decode_unicode=True):
            print(line)

if __name__ == '__main__':
    main()
