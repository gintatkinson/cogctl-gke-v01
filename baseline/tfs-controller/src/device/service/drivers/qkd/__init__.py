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

from device.service.driver_api._Driver import RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES

RESOURCE_LINKS = '__links__'
RESOURCE_APPS = '__apps__'
RESOURCE_CAPABILITES = '__capabilities__'
RESOURCE_NODE = '__node__'


ALL_RESOURCE_KEYS = [
    RESOURCE_ENDPOINTS,
    RESOURCE_INTERFACES,
    RESOURCE_NETWORK_INSTANCES,
    RESOURCE_LINKS,
    RESOURCE_APPS,
    RESOURCE_CAPABILITES,
    RESOURCE_NODE
]

RESOURCE_KEY_MAPPINGS = {
    RESOURCE_ENDPOINTS        : 'component',
    RESOURCE_INTERFACES       : 'interface',
    RESOURCE_NETWORK_INSTANCES: 'network_instance',
    RESOURCE_LINKS            : 'links',
    RESOURCE_APPS             : 'apps',
    RESOURCE_CAPABILITES      : 'capabilities',
    RESOURCE_NODE             : 'node'
}
