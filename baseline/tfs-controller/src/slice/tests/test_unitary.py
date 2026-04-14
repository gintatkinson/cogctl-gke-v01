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

#import logging, os, pytest
#from common.Constants import ServiceNameEnum
#from common.Settings import (
#    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name, get_service_port_grpc)
#from slice.client.SliceClient import SliceClient
#from slice.service.SliceService import SliceService

#LOCAL_HOST = '127.0.0.1'
#MOCKSERVICE_PORT = 10000
#SLICE_SERVICE_PORT = MOCKSERVICE_PORT + get_service_port_grpc(ServiceNameEnum.SLICE) # avoid privileged ports
#os.environ[get_env_var_name(ServiceNameEnum.SLICE, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
#os.environ[get_env_var_name(ServiceNameEnum.SLICE, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(SLICE_SERVICE_PORT)

#LOGGER = logging.getLogger(__name__)
#LOGGER.setLevel(logging.DEBUG)

#@pytest.fixture(scope='session')
#def slice_service():
#    _service = SliceService()
#    _service.start()
#    yield _service
#    _service.stop()

#@pytest.fixture(scope='session')
#def slice_client(slice_service : SliceService): # pylint: disable=redefined-outer-name
#    _client = SliceClient()
#    yield _client
#    _client.close()

#def test_add_device_wrong_attributes(slice_client : SliceClient):
#    # should fail with slice uuid is empty
#    with pytest.raises(grpc._channel._InactiveRpcError) as e:
#        slice_client.CreateUpdateSlice(TransportSlice())
#    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
#    assert e.value.details() == 'slice.slice_id.slice_id.uuid() string is empty.'
