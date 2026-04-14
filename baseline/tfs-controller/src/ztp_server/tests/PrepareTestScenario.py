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

from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    ENVVAR_SUFIX_SERVICE_PORT_HTTP, get_env_var_name
)

from common.tools.rest_api.server.GenericRestServer import GenericRestServer
from ztp_server.service.rest_server.ztpServer_plugins.ztp_provisioning_api import register_ztp_provisioning
from ztp_server.client.ZtpClient import ZtpClient

from .Constants import (
    LOCAL_HOST, MOCKSERVICE_PORT, ZTP_SERVICE_BASE_URL, ZTP_SERVICE_PORT,
    USERNAME, PASSWORD
)

os.environ[get_env_var_name(ServiceNameEnum.ZTP_SERVER, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.ZTP_SERVER, ENVVAR_SUFIX_SERVICE_PORT_HTTP)] = str(ZTP_SERVICE_PORT)

@pytest.fixture(scope='session')
def ztp_server_application():
    _rest_server = GenericRestServer(ZTP_SERVICE_PORT, bind_address='127.0.0.1')
    register_ztp_provisioning(_rest_server)
    _rest_server.start()
    time.sleep(1)   # bring time for the server to start
    yield _rest_server
    _rest_server.shutdown()
    _rest_server.join()

@pytest.fixture(scope='session')
def ztp_client():    # pylint: disable=redefined-outer-name
    _client = ZtpClient()
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
    request_url = ZTP_SERVICE_BASE_URL + url
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
