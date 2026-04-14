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

SIMAP_SERVER_SCHEME   = str(get_setting('SIMAP_SERVER_SCHEME',    default='http'     ))
SIMAP_SERVER_ADDRESS  = str(get_setting('SIMAP_SERVER_ADDRESS',   default='127.0.0.1'))
SIMAP_SERVER_PORT     = int(get_setting('SIMAP_SERVER_PORT',      default='80'       ))
SIMAP_SERVER_USERNAME = str(get_setting('SIMAP_SERVER_USERNAME',  default='admin'    ))
SIMAP_SERVER_PASSWORD = str(get_setting('SIMAP_SERVER_PASSWORD',  default='admin'    ))
