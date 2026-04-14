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

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from nbi.Config import RESTAPI_USERS

HTTP_AUTH = HTTPBasicAuth()

@HTTP_AUTH.verify_password
def verify_password(username, password):
    if username not in RESTAPI_USERS: return None
    if not check_password_hash(RESTAPI_USERS[username], password): return None
    return username
