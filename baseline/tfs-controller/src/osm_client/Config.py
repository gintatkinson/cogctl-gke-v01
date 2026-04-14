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

from common.Settings import get_setting

DEFAULT_OSM_ADDRESS = '127.0.0.1'
OSM_ADDRESS = get_setting('OSM_ADDRESS', default=DEFAULT_OSM_ADDRESS)

DEFAULT_OSM_PORT = 80
OSM_PORT = int(get_setting('OSM_PORT', default=DEFAULT_OSM_PORT))

DEFAULT_OSM_USERNAME = 'admin'
OSM_USERNAME = get_setting('OSM_USERNAME', default=DEFAULT_OSM_USERNAME)

DEFAULT_OSM_PASSWORD = 'admin'
OSM_PASSWORD = get_setting('OSM_PASSWORD', default=DEFAULT_OSM_PASSWORD)

DEFAULT_OSM_PROJECT = 'admin'
OSM_PROJECT = get_setting('OSM_PROJECT', default=DEFAULT_OSM_PROJECT)

DEFAULT_OSM_VERIFY_TLS = True
OSM_VERIFY_TLS = get_setting('OSM_VERIFY_TLS', default=None)
TRUE_VALUES = {'Y', 'YES', 'TRUE', 'T', 'E', 'ENABLE', 'ENABLED', '1'}
if OSM_VERIFY_TLS is None:
    OSM_VERIFY_TLS = DEFAULT_OSM_VERIFY_TLS
else:
    OSM_VERIFY_TLS = str(OSM_VERIFY_TLS).upper() in TRUE_VALUES
