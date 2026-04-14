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
from common.Settings import get_setting, is_deployed_forecaster

DEFAULT_PATHCOMP_BACKEND_SCHEME  = 'http'
DEFAULT_PATHCOMP_BACKEND_HOST    = '127.0.0.1'
DEFAULT_PATHCOMP_BACKEND_PORT    = '8081'
DEFAULT_PATHCOMP_BACKEND_BASEURL = '/pathComp/api/v1/compRoute'

PATHCOMP_BACKEND_SCHEME  = str(os.environ.get('PATHCOMP_BACKEND_SCHEME',  DEFAULT_PATHCOMP_BACKEND_SCHEME ))
PATHCOMP_BACKEND_BASEURL = str(os.environ.get('PATHCOMP_BACKEND_BASEURL', DEFAULT_PATHCOMP_BACKEND_BASEURL))

# Find IP:port of backend container as follows:
# - first check env vars PATHCOMP_BACKEND_HOST & PATHCOMP_BACKEND_PORT
# - if not set, check env vars PATHCOMPSERVICE_SERVICE_HOST & PATHCOMPSERVICE_SERVICE_PORT_HTTP
# - if not set, use DEFAULT_PATHCOMP_BACKEND_HOST & DEFAULT_PATHCOMP_BACKEND_PORT

backend_host = DEFAULT_PATHCOMP_BACKEND_HOST
#backend_host = os.environ.get('PATHCOMPSERVICE_SERVICE_HOST', backend_host)
PATHCOMP_BACKEND_HOST = str(os.environ.get('PATHCOMP_BACKEND_HOST', backend_host))

backend_port = DEFAULT_PATHCOMP_BACKEND_PORT
backend_port = os.environ.get('PATHCOMPSERVICE_SERVICE_PORT_HTTP', backend_port)
PATHCOMP_BACKEND_PORT = int(os.environ.get('PATHCOMP_BACKEND_PORT', backend_port))

BACKEND_URL = '{:s}://{:s}:{:d}{:s}'.format(
    PATHCOMP_BACKEND_SCHEME, PATHCOMP_BACKEND_HOST, PATHCOMP_BACKEND_PORT, PATHCOMP_BACKEND_BASEURL)


SETTING_NAME_ENABLE_FORECASTER = 'ENABLE_FORECASTER'
TRUE_VALUES = {'Y', 'YES', 'TRUE', 'T', 'E', 'ENABLE', 'ENABLED'}

def is_forecaster_enabled() -> bool:
    if not is_deployed_forecaster(): return False
    is_enabled = get_setting(SETTING_NAME_ENABLE_FORECASTER, default=None)
    if is_enabled is None: return False
    str_is_enabled = str(is_enabled).upper()
    return str_is_enabled in TRUE_VALUES
