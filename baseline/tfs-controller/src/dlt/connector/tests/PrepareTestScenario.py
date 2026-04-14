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

#import os, pytest
#from typing import Tuple
#from common.Constants import ServiceNameEnum
#from common.Settings import (
#    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name, get_service_port_grpc)
#from common.orm.Database import Database
#from common.orm.Factory import get_database_backend, BackendEnum as DatabaseBackendEnum
#from common.message_broker.Factory import get_messagebroker_backend, BackendEnum as MessageBrokerBackendEnum
#from common.message_broker.MessageBroker import MessageBroker
#from context.client.ContextClient import ContextClient
#from context.service.grpc_server.ContextService import ContextService
#from dlt.connector.client.DltConnectorClient import DltConnectorClient
#from dlt.connector.service.DltConnectorService import DltConnectorService
#from .MockService_Dependencies import MockService_Dependencies
#
#LOCAL_HOST = '127.0.0.1'
#MOCKSERVICE_PORT = 10000
##GRPC_PORT = 10000 + get_service_port_grpc(ServiceNameEnum.CONTEXT) # avoid privileged ports
##os.environ[get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
##os.environ[get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(GRPC_PORT)
#
## ===== BlockChain Emulator (Mock DLT Gateway) =========================================================================
## A single gateway is used for all the domains
#
#@pytest.fixture(scope='session')
#def dltgateway_service():
#    _service = MockService_Dependencies(MOCKSERVICE_PORT)
#    _service.configure_env_vars()
#    _service.start()
#    yield _service
#    _service.stop()
#
## ===== Domain A (Real Context + Real DLT Connector) ===================================================================
#
#@pytest.fixture(scope='session')
#def context_service_a(): # pylint: disable=redefined-outer-name
#    _database = Database(get_database_backend(backend=DatabaseBackendEnum.INMEMORY))
#    _message_broker = MessageBroker(get_messagebroker_backend(backend=MessageBrokerBackendEnum.INMEMORY))
#    _service = ContextService(_database, _message_broker)
#    _service.start()
#    yield _service
#    _service.stop()
#    _message_broker.terminate()
#
#@pytest.fixture(scope='session')
#def context_client_a(context_service_a : ContextService): # pylint: disable=redefined-outer-name
#    _client = ContextClient(host=context_service_a.bind_address, port=context_service_a.bind_port)
#    yield _client
#    _client.close()
#
#@pytest.fixture(scope='session')
#def dltconnector_service_a():
#    _service = DltConnectorService()
#    _service.bind_port += 1
#    _service.start()
#    yield _service
#    _service.stop()
#
#@pytest.fixture(scope='session')
#def dltconnector_client_a(dltconnector_service_a : DltConnectorService): # pylint: disable=redefined-outer-name
#    _client = DltConnectorClient(host=dltconnector_service_a.bind_address, port=dltconnector_service_a.bind_port)
#    yield _client
#    _client.close()
#
## ===== Domain B (Real Context + Real DLT Connector) ===================================================================
#
#@pytest.fixture(scope='session')
#def context_service_b(): # pylint: disable=redefined-outer-name
#    _database = Database(get_database_backend(backend=DatabaseBackendEnum.INMEMORY))
#    _message_broker = MessageBroker(get_messagebroker_backend(backend=MessageBrokerBackendEnum.INMEMORY))
#    _service = ContextService(_database, _message_broker)
#    _service.start()
#    yield _service
#    _service.stop()
#    _message_broker.terminate()
#
#@pytest.fixture(scope='session')
#def context_client_b(context_service_b : ContextService): # pylint: disable=redefined-outer-name
#    _client = ContextClient(host=context_service_b.bind_address, port=context_service_b.bind_port)
#    yield _client
#    _client.close()
#
#@pytest.fixture(scope='session')
#def dltconnector_service_b():
#    _service = DltConnectorService()
#    _service.bind_port += 2
#    _service.start()
#    yield _service
#    _service.stop()
#
#@pytest.fixture(scope='session')
#def dltconnector_client_b(dltconnector_service_b : DltConnectorService): # pylint: disable=redefined-outer-name
#    _client = DltConnectorClient(host=dltconnector_service_b.bind_address, port=dltconnector_service_b.bind_port)
#    yield _client
#    _client.close()
