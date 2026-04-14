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

import pytest, os

from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    ENVVAR_SUFIX_SERVICE_PORT_HTTP, get_env_var_name, get_service_port_grpc
)

from common.Constants import ServiceNameEnum
from osm_client.client.OsmClient import OsmClient
from osm_client.service.OsmClientService import OsmClientService

LOCAL_HOST = '127.0.0.1'
GRPC_PORT = 10000 + int(get_service_port_grpc(ServiceNameEnum.OSMCLIENT))

os.environ[get_env_var_name(ServiceNameEnum.OSMCLIENT, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.OSMCLIENT, ENVVAR_SUFIX_SERVICE_PORT_HTTP)] = str(GRPC_PORT)

@pytest.fixture(scope='session')
def osm_client_service(): # pylint: disable=redefined-outer-name
    _service = OsmClientService()
    _service.start()
    yield _service
    _service.stop()

@pytest.fixture(scope='session')
def osm_client(osm_client_service : OsmClientService):    # pylint: disable=redefined-outer-name
    _client = OsmClient()
    yield _client
    _client.close()
