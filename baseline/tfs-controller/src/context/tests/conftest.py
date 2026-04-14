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

import os, pytest, sqlalchemy
from _pytest.config import Config
from _pytest.terminal import TerminalReporter
from typing import Tuple
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    get_env_var_name, get_service_port_grpc
)
from common.message_broker.Factory import get_messagebroker_backend
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.Decorator import MetricsPool
from context.client.ContextClient import ContextClient
from context.service.ContextService import ContextService
from context.service.database.Engine import Engine
from context.service.database.models._Base import rebuild_database

LOCAL_HOST = '127.0.0.1'
GRPC_PORT = 10000 + int(get_service_port_grpc(ServiceNameEnum.CONTEXT))   # avoid privileged ports

os.environ[get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(GRPC_PORT)

@pytest.fixture(scope='session')
def context_db_mb(request) -> Tuple[sqlalchemy.engine.Engine, MessageBroker]:   # pylint: disable=unused-argument
    _db_engine = Engine.get_engine()
    Engine.drop_database(_db_engine)
    Engine.create_database(_db_engine)
    rebuild_database(_db_engine)

    _msg_broker = MessageBroker(get_messagebroker_backend())
    yield _db_engine, _msg_broker
    _msg_broker.terminate()

RAW_METRICS : MetricsPool = None

@pytest.fixture(scope='session')
def context_service(
    context_db_mb : Tuple[sqlalchemy.engine.Engine, MessageBroker]  # pylint: disable=redefined-outer-name
):
    global RAW_METRICS # pylint: disable=global-statement
    _service = ContextService(context_db_mb[0], context_db_mb[1])
    RAW_METRICS = _service.context_servicer._get_metrics()
    _service.start()
    yield _service
    _service.stop()

@pytest.fixture(scope='session')
def context_client(context_service : ContextService): # pylint: disable=redefined-outer-name,unused-argument
    _client = ContextClient()
    yield _client
    _client.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(
    terminalreporter : TerminalReporter, exitstatus : int, config : Config  # pylint: disable=unused-argument
):
    yield

    if RAW_METRICS is not None:
        print('')
        print('Performance Results:')
        print(RAW_METRICS.get_pretty_table().get_string())
