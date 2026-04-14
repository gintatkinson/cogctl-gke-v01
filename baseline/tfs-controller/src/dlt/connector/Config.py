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

DEFAULT_DLT_GATEWAY_HOST = '127.0.0.1'
DEFAULT_DLT_GATEWAY_PORT = '50051'

# Find IP:port of gateway container as follows:
# - first check env vars DLT_GATEWAY_HOST & DLT_GATEWAY_PORT
# - if not set, use DEFAULT_DLT_GATEWAY_HOST & DEFAULT_DLT_GATEWAY_PORT
DLT_GATEWAY_HOST = str(os.environ.get('DLT_GATEWAY_HOST', DEFAULT_DLT_GATEWAY_HOST))
DLT_GATEWAY_PORT = int(os.environ.get('DLT_GATEWAY_PORT', DEFAULT_DLT_GATEWAY_PORT))
