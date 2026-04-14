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
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    get_env_var_name, get_log_level, get_setting
)

LOCAL_HOST = '127.0.0.1'
MOCK_PORT  = 10000

BIND_ADDRESS = str(get_setting('BIND_ADDRESS', default='0.0.0.0'))
BIND_PORT    = int(get_setting('BIND_PORT',    default=MOCK_PORT))
LOG_LEVEL    = str(get_log_level())

MOCKED_SERVICES = [
    ServiceNameEnum.CONTEXT,
    ServiceNameEnum.DEVICE,
    ServiceNameEnum.QOSPROFILE,
    ServiceNameEnum.SERVICE,
    ServiceNameEnum.SLICE,
]
for mocked_service in MOCKED_SERVICES:
    os.environ[get_env_var_name(mocked_service, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
    os.environ[get_env_var_name(mocked_service, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(BIND_PORT )
