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

from ncclient.manager import Manager, connect_ssh

str_filter = '''<filter>
    <components xmlns="http://openconfig.net/yang/platform">
        <component/>
    </components>
</filter>'''

_manager : Manager = connect_ssh(
    host='10.5.32.3', port=830, username='admin', password='admin',
    device_params={'name': 'huaweiyang'}, manager_params={'timeout': 120},
    key_filename=None, hostkey_verify=False, allow_agent=False,
    look_for_keys=False)
c = _manager.get(filter=str_filter, with_defaults=None).data_xml
with open('data.xml', 'w') as f:
    f.write(c)
_manager.close_session()
