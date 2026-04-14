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


from .app import app

BIND_ADDRESS = '0.0.0.0'
BIND_PORT    = 8080

if __name__ == '__main__':
    # Only used to run it locally during development stage;
    # otherwise, app is directly launched by gunicorn.
    app.run(
        host=BIND_ADDRESS, port=BIND_PORT, debug=True, use_reloader=False
    )
