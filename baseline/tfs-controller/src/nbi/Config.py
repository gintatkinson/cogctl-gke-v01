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

from werkzeug.security import generate_password_hash

# REST-API users
RESTAPI_USERS = {   # TODO: implement a database of credentials and permissions
    'admin': generate_password_hash('admin'),
}

# Rebuild using: "python -c 'import secrets; print(secrets.token_hex())'"
SECRET_KEY = '2b8ab76763d81f7bced786de8ba40bd67eea6ff79217a711eb5f8d1f19c145c1'
