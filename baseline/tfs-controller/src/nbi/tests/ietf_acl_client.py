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

import requests, time
from typing import Optional
from requests.auth import HTTPBasicAuth

BASE_URL = '{:s}://{:s}:{:d}/restconf/data'
ACLS_URL = '{:s}/device={:s}/ietf-access-control-list:acls'
ACL_URL  = '{:s}/device={:s}/ietf-access-control-list:acl={:s}'

CSG1_DEVICE_UUID = '118295c8-318a-52ec-a394-529fc4b70f2f' # router: 128.32.10.1
ACL_NAME         = 'sample-ipv4-acl'
ACL_RULE         = {"ietf-access-control-list:acls": {
    "acl": [{
        "name": "sample-ipv4-acl", "type": "ipv4-acl-type",
        "aces": {"ace": [{
            "name": "rule1",
            "matches": {
                "ipv4": {
                    "source-ipv4-network": "128.32.10.6/24",
                    "destination-ipv4-network": "172.10.33.0/24",
                    "dscp": 18
                },
                "tcp": {
                    "source-port": {"operator": "eq", "port": 1444},
                    "destination-port": {"operator": "eq", "port": 1333},
                    "flags": "syn"
                }
            },
            "actions": {"forwarding": "drop"}
        }]}
    }],
    "attachment-points": {"interface": [{
        "interface-id": "200",
        "ingress": {"acl-sets": {"acl-set": [{"name": "sample-ipv4-acl"}]}}
    }]
}}}

class TfsIetfAclClient:
    def __init__(
        self, host : str = 'localhost', port : int = 80, schema : str = 'http',
        username : Optional[str] = 'admin', password : Optional[str] = 'admin',
        timeout : int = 10, allow_redirects : bool = True, verify : bool = False
    ) -> None:
        self._base_url = BASE_URL.format(schema, host, port)
        auth = HTTPBasicAuth(username, password) if username is not None and password is not None else None
        self._settings = dict(auth=auth, timeout=timeout, allow_redirects=allow_redirects, verify=verify)

    def post(self, device_uuid : str, ietf_acl_data : dict) -> str:
        request_url = ACLS_URL.format(self._base_url, device_uuid)
        reply = requests.post(request_url, json=ietf_acl_data, **(self._settings))
        return reply.text

    def get(self, device_uuid : str, acl_name : str) -> str:
        request_url = ACL_URL.format(self._base_url, device_uuid, acl_name)
        reply = requests.get(request_url, **(self._settings))
        return reply.text

    def delete(self, device_uuid : str, acl_name : str) -> str:
        request_url = ACL_URL.format(self._base_url, device_uuid, acl_name)
        reply = requests.delete(request_url, **(self._settings))
        return reply.text

def main():
    client = TfsIetfAclClient()
    print(f'ACL rule: {ACL_RULE}')
    post_response = client.post(CSG1_DEVICE_UUID, ACL_RULE)
    print(f'post response: {post_response}')
    time.sleep(.5)
    get_response = client.get(CSG1_DEVICE_UUID, ACL_NAME)
    print(f'get response: {get_response}')
    time.sleep(.5)
    delete_response = client.delete(CSG1_DEVICE_UUID, ACL_NAME)
    print(f'delete response: {delete_response}')

if __name__ == '__main__':
    main()
