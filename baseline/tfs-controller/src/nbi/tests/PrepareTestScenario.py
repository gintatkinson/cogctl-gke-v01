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

import enum, logging, os, pytest, requests, time # subprocess, threading
from typing import Any, Dict, List, Optional, Set, Union
from socketio import Namespace
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    ENVVAR_SUFIX_SERVICE_PORT_HTTP, get_env_var_name
)
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from nbi.service.NbiApplication import NbiApplication
from nbi.service.health_probes.Constants import SIO_NAMESPACE as HEARTBEAT_NAMESPACE
from nbi.service.health_probes.Namespaces import HeartbeatServerNamespace
from service.client.ServiceClient import ServiceClient
from slice.client.SliceClient import SliceClient
from tests.tools.mock_osm.MockOSM import MockOSM
from .Constants import (
    LOCAL_HOST, MOCKSERVICE_PORT, NBI_SERVICE_BASE_URL, NBI_SERVICE_PORT,
    USERNAME, PASSWORD
)
from .OSM_Constants import WIM_MAPPING
from .MockWebServer import MockWebServer


os.environ[get_env_var_name(ServiceNameEnum.NBI, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.NBI, ENVVAR_SUFIX_SERVICE_PORT_HTTP)] = str(NBI_SERVICE_PORT)

MOCK_SERVICES = [
    ServiceNameEnum.CONTEXT,
    ServiceNameEnum.DEVICE,
    ServiceNameEnum.QOSPROFILE,
    ServiceNameEnum.SERVICE,
    ServiceNameEnum.SLICE,
]
for mock_service in MOCK_SERVICES:
    mock_service_host_env_var = get_env_var_name(mock_service, ENVVAR_SUFIX_SERVICE_HOST)
    os.environ[mock_service_host_env_var] = str('mock_tfs_nbi_dependencies')
    mock_service_port_env_var = get_env_var_name(mock_service, ENVVAR_SUFIX_SERVICE_PORT_GRPC)
    os.environ[mock_service_port_env_var] = str(MOCKSERVICE_PORT)


@pytest.fixture(scope='session')
def nbi_application() -> NbiApplication:
    mock_web_server = MockWebServer()
    mock_web_server.start()
    time.sleep(1)   # bring time for the server to start

    nbi_app = mock_web_server.nbi_app
    yield nbi_app

    sio_server = nbi_app.get_socketio_server()
    sio_namespaces : Dict[str, Namespace] = sio_server.namespace_handlers
    heartbeat_namespace : HeartbeatServerNamespace = sio_namespaces.get(HEARTBEAT_NAMESPACE)
    heartbeat_namespace.stop_thread()

    mock_web_server.join(timeout=1)


@pytest.fixture(scope='session')
def osm_wim(
    nbi_application : NbiApplication            # pylint: disable=redefined-outer-name, unused-argument
) -> MockOSM:
    wim_url = 'http://{:s}:{:d}'.format(LOCAL_HOST, NBI_SERVICE_PORT)
    return MockOSM(wim_url, WIM_MAPPING, USERNAME, PASSWORD)

@pytest.fixture(scope='session')
def context_client() -> ContextClient:
    _client = ContextClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def device_client() -> DeviceClient:
    _client = DeviceClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def service_client() -> ServiceClient:
    _client = ServiceClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def slice_client() -> SliceClient:
    _client = SliceClient()
    yield _client
    _client.close()

class RestRequestMethod(enum.Enum):
    GET    = 'get'
    POST   = 'post'
    PUT    = 'put'
    PATCH  = 'patch'
    DELETE = 'delete'

EXPECTED_STATUS_CODES : Set[int] = {
    requests.codes['OK'        ],
    requests.codes['CREATED'   ],
    requests.codes['ACCEPTED'  ],
    requests.codes['NO_CONTENT'],
}

def do_rest_request(
    method : RestRequestMethod, url : str, body : Optional[Any] = None, timeout : int = 10,
    allow_redirects : bool = True, expected_status_codes : Set[int] = EXPECTED_STATUS_CODES,
    logger : Optional[logging.Logger] = None
) -> Optional[Union[Dict, List]]:
    request_url = NBI_SERVICE_BASE_URL + url
    if logger is not None:
        msg = 'Request: {:s} {:s}'.format(str(method.value).upper(), str(request_url))
        if body is not None: msg += ' body={:s}'.format(str(body))
        logger.warning(msg)
    reply = requests.request(method.value, request_url, timeout=timeout, json=body, allow_redirects=allow_redirects)
    if logger is not None:
        logger.warning('Reply: {:s}'.format(str(reply.text)))
    assert reply.status_code in expected_status_codes, 'Reply failed with status code {:d}'.format(reply.status_code)

    if reply.content and len(reply.content) > 0: return reply.json()
    return None

def do_rest_get_request(
    url : str, body : Optional[Any] = None, timeout : int = 10,
    allow_redirects : bool = True, expected_status_codes : Set[int] = EXPECTED_STATUS_CODES,
    logger : Optional[logging.Logger] = None
) -> Optional[Union[Dict, List]]:
    return do_rest_request(
        RestRequestMethod.GET, url, body=body, timeout=timeout, allow_redirects=allow_redirects,
        expected_status_codes=expected_status_codes, logger=logger
    )

def do_rest_post_request(
    url : str, body : Optional[Any] = None, timeout : int = 10,
    allow_redirects : bool = True, expected_status_codes : Set[int] = EXPECTED_STATUS_CODES,
    logger : Optional[logging.Logger] = None
) -> Optional[Union[Dict, List]]:
    return do_rest_request(
        RestRequestMethod.POST, url, body=body, timeout=timeout, allow_redirects=allow_redirects,
        expected_status_codes=expected_status_codes, logger=logger
    )

def do_rest_put_request(
    url : str, body : Optional[Any] = None, timeout : int = 10,
    allow_redirects : bool = True, expected_status_codes : Set[int] = EXPECTED_STATUS_CODES,
    logger : Optional[logging.Logger] = None
) -> Optional[Union[Dict, List]]:
    return do_rest_request(
        RestRequestMethod.PUT, url, body=body, timeout=timeout, allow_redirects=allow_redirects,
        expected_status_codes=expected_status_codes, logger=logger
    )

def do_rest_patch_request(
    url : str, body : Optional[Any] = None, timeout : int = 10,
    allow_redirects : bool = True, expected_status_codes : Set[int] = EXPECTED_STATUS_CODES,
    logger : Optional[logging.Logger] = None
) -> Optional[Union[Dict, List]]:
    return do_rest_request(
        RestRequestMethod.PATCH, url, body=body, timeout=timeout, allow_redirects=allow_redirects,
        expected_status_codes=expected_status_codes, logger=logger
    )

def do_rest_delete_request(
    url : str, body : Optional[Any] = None, timeout : int = 10,
    allow_redirects : bool = True, expected_status_codes : Set[int] = EXPECTED_STATUS_CODES,
    logger : Optional[logging.Logger] = None
) -> Optional[Union[Dict, List]]:
    return do_rest_request(
        RestRequestMethod.DELETE, url, body=body, timeout=timeout, allow_redirects=allow_redirects,
        expected_status_codes=expected_status_codes, logger=logger
    )
