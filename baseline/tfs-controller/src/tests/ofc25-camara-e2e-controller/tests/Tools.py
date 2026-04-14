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

import enum, logging, requests
from typing import Any, Dict, List, Optional, Set, Union
from common.Constants import ServiceNameEnum
from common.Settings import get_service_host, get_service_port_http

NBI_ADDRESS  = get_service_host(ServiceNameEnum.NBI)
NBI_PORT     = get_service_port_http(ServiceNameEnum.NBI)
NBI_USERNAME = 'admin'
NBI_PASSWORD = 'admin'
NBI_BASE_URL = ''

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
    request_url = 'http://{:s}:{:s}@{:s}:{:d}{:s}{:s}'.format(
        NBI_USERNAME, NBI_PASSWORD, NBI_ADDRESS, NBI_PORT, str(NBI_BASE_URL), url
    )

    if logger is not None:
        msg = 'Request: {:s} {:s}'.format(str(method.value).upper(), str(request_url))
        if body is not None: msg += ' body={:s}'.format(str(body))
        logger.warning(msg)
    reply = requests.request(method.value, request_url, headers={'Content-Type': 'application/json'}, timeout=timeout, json=body, allow_redirects=allow_redirects)
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
