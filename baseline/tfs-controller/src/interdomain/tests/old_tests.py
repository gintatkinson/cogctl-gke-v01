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

#import logging, grpc
#import os
#import sqlite3
#
#import pytest
#from typing import Tuple
#
#from interdomain.proto import context_pb2, kpi_sample_types_pb2, monitoring_pb2
#from interdomain.client.interdomain_client import InterdomainClient
#from interdomain.Config import GRPC_SERVICE_PORT, GRPC_MAX_WORKERS, GRPC_GRACE_PERIOD
#from interdomain.service.InterdomainService import InterdomainService
#
#from common.orm.Database import Database
#from common.orm.Factory import get_database_backend, BackendEnum as DatabaseBackendEnum
#from common.message_broker.Factory import get_messagebroker_backend, BackendEnum as MessageBrokerBackendEnum
#from common.message_broker.MessageBroker import MessageBroker
#
#LOGGER = logging.getLogger(__name__)
#LOGGER.setLevel(logging.DEBUG)
#
############################
## Tests Setup
############################
#
#SERVER_ADDRESS = '127.0.0.1'
#LISTEN_ADDRESS = '[::]'
#GRPC_PORT_MONITORING = 9090
#
#GRPC_PORT_CONTEXT    = 10000 + grpc_port_context    # avoid privileged ports
#
#SCENARIOS = [ # comment/uncomment scenarios to activate/deactivate them in the test unit
#    ('all_inmemory', DatabaseBackendEnum.INMEMORY, {},           MessageBrokerBackendEnum.INMEMORY, {}          ),
#]
#
#
## This fixture will be requested by test cases and last during testing session
#@pytest.fixture(scope='session')
#def interdomain_service():
#    LOGGER.warning('interdomain_service begin')
#
#    interdomain_port    = GRPC_INTERDOMAIN_PORT
#    max_workers     = GRPC_MAX_WORKERS
#    grace_period    = GRPC_GRACE_PERIOD
#
#    LOGGER.info('Initializing InterdomainService...')
#    grpc_service = InterdomainService(port=interdomain_port, max_workers=max_workers, grace_period=grace_period)
#    server = grpc_service.start()
#
#    # yield the server, when test finishes, execution will resume to stop it
#    LOGGER.warning('interdomain_service yielding')
#    yield server
#
#    LOGGER.info('Terminating InterdomainService...')
#    grpc_service.stop()
#
## This fixture will be requested by test cases and last during testing session.
## The client requires the server, so client fixture has the server as dependency.
#@pytest.fixture(scope='session')
#def interdomain_client(interdomain_service):
#    LOGGER.warning('interdomain_client begin')
#    client = InterdomainClient(server=SERVER_ADDRESS, port=GRPC_PORT_INTERDOMAIN)  # instantiate the client
#    LOGGER.warning('interdomain_client returning')
#    return client
#
## This fixture will be requested by test cases and last during testing session.
#@pytest.fixture(scope='session')
#def create_TeraFlowController():
#    LOGGER.warning('create_TeraFlowController begin')
#    # form request
#    tf_ctl                  = context_pb2.TeraFlowController()
#    tf_ctl.context_id       = context_pb2.ContextId()
#    tf_ctl.context_id.context_uuid = context_pb2.Uuid()
#    tf_ctl.context_id.context_uuid.uuid = str(1) 
#    tf_ctl.ip_address       = "127.0.0.1"
#    tf_ctl.port      	    = 9090
#    return tf_ctl
#
#@pytest.fixture(scope='session')
#def create_TransportSlice():
#    LOGGER.warning('create_TransportSlice begin')
#
#    # form request
#    slice_req              = slice_pb2.TransportSlice()
#    slice_req.contextId    = context_pb2.ContextId()
#    slice_req.contextId.context_uuid = context_pb2.Uuid()
#    slice_req.contextId.context_uuid.uuid = str(1) 
#    slice_req.slice_id     = context_pb2.Uuid()
#    slice_req.slice_id.context_uuid.uuid = str(1) 
#
#    return slice_req
#
#
############################
## Tests Implementation
############################
#
#
## Test case that makes use of client fixture to test server's CreateKpi method
#def test_Authenticate(interdomain_client,create_TeraFlowController):
#    # make call to server
#    LOGGER.warning('test_Authenticate requesting')
#    response = interdomain_client.Authenticate(create_TeraFlowController)
#    LOGGER.debug(str(response))
#    assert isinstance(response, context.AuthenticationResult)
#
## Test case that makes use of client fixture to test server's MonitorKpi method
#def test_LookUpSlice(interdomain_client,create_TransportSlice):
#    LOGGER.warning('test_LookUpSlice begin')
#
#    response = interdomain_client.LookUpSlice(create_TransportSlice)
#    LOGGER.debug(str(response))
#    assert isinstance(response, slice.SliceId)
#
## Test case that makes use of client fixture to test server's GetStreamKpi method
#def test_CreateSliceAndAddToCatalog(interdomain_client,create_TransportSlice):
#    LOGGER.warning('test_CreateSliceAndAddToCatalog begin')
#    response = interdomain_client.CreateSliceAndAddToCatalog(create_TransportSlice)
#    LOGGER.debug(str(response))
#    assert isinstance(response, slice.SliceId)
#
## Test case that makes use of client fixture to test server's IncludeKpi method
#def test_OrderSliceFromCatalog(interdomain_client,create_TransportSlice):
#    # make call to server
#    LOGGER.warning('test_OrderSliceFromCatalog requesting')
#    response = interdomain_client.OrderSliceFromCatalog(create_TransportSlice)
#    LOGGER.debug(str(response))
#    assert isinstance(response, slice.SliceId)
#
