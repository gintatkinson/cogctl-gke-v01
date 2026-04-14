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


import os, secrets


RESTCONF_PREFIX  = os.environ.get('RESTCONF_PREFIX',  '/restconf'     )
YANG_SEARCH_PATH = os.environ.get('YANG_SEARCH_PATH', './yang'        )
STARTUP_FILE     = os.environ.get('STARTUP_FILE',     './startup.json')
SECRET_KEY       = os.environ.get('SECRET_KEY',       secrets.token_hex(64))
