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
from requests.auth import HTTPBasicAuth
from typing import Any, Optional, Set


class RestRequestMethod(enum.Enum):
    GET    = 'get'
    POST   = 'post'
    PUT    = 'put'
    PATCH  = 'patch'
    DELETE = 'delete'


EXPECTED_STATUS_CODES : Set[int] = {
    requests.codes['OK'        ],   # 200 - OK
    requests.codes['CREATED'   ],   # 201 - Created
    requests.codes['ACCEPTED'  ],   # 202 - Accepted
    requests.codes['NO_CONTENT'],   # 204 - No Content
}


def compose_basic_auth(
    username : Optional[str] = None, password : Optional[str] = None
) -> Optional[HTTPBasicAuth]:
    if username is None or password is None: return None
    return HTTPBasicAuth(username, password)


class SchemeEnum(enum.Enum):
    HTTP  = 'http'
    HTTPS = 'https'


def check_scheme(scheme : str) -> str:
    str_scheme = str(scheme).lower()
    enm_scheme = SchemeEnum._value2member_map_[str_scheme]
    return enm_scheme.value


TEMPLATE_URL  = '{:s}://{:s}:{:d}/{:s}'


class RestApiClient:
    def __init__(
        self, address : str, port : int = 8080, scheme : str = 'http', base_url : str = '',
        username : Optional[str] = None, password : Optional[str] = None,
        timeout : int = 30, verify_certs : bool = True, allow_redirects : bool = True,
        logger : Optional[logging.Logger] = None
    ) -> None:
        self._address         = address
        self._port            = int(port)
        self._scheme          = check_scheme(scheme)
        self._base_url        = base_url
        self._auth            = compose_basic_auth(username=username, password=password)
        self._timeout         = int(timeout)
        self._verify_certs    = verify_certs
        self._allow_redirects = allow_redirects
        self._logger          = logger


    def _log_msg_request(
        self, method : RestRequestMethod, request_url : str, body : Optional[Any],
        log_level : int = logging.INFO
    ) -> str:
        msg = 'Request: {:s} {:s}'.format(str(method.value).upper(), str(request_url))
        if body is not None: msg += ' body={:s}'.format(str(body))
        if self._logger is not None: self._logger.log(log_level, msg)
        return msg


    def _log_msg_check_reply(
        self, method : RestRequestMethod, request_url : str, body : Optional[Any],
        reply : requests.Response, expected_status_codes : Set[int],
        log_level : int = logging.INFO
    ) -> str:
        msg = 'Reply: {:s}'.format(str(reply.text))
        if self._logger is not None: self._logger.log(log_level, msg)
        http_status_code = reply.status_code
        if http_status_code in expected_status_codes: return msg
        MSG = 'Request failed. method={:s} url={:s} body={:s} status_code={:s} reply={:s}'
        msg = MSG.format(
            str(method.value).upper(), str(request_url), str(body),
            str(http_status_code), str(reply.text)
        )
        if self._logger is not None: self._logger.error(msg)
        raise Exception(msg)


    def _do_rest_request(
        self, method : RestRequestMethod, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = EXPECTED_STATUS_CODES
    ) -> Optional[Any]:
        candidate_schemes = tuple(['{:s}://'.format(m).lower() for m in SchemeEnum.__members__])
        if endpoint.lower().startswith(candidate_schemes):
            request_url = endpoint.lstrip('/')
        else:
            endpoint = str(self._base_url + '/' + endpoint).replace('//', '/').lstrip('/')
            request_url = TEMPLATE_URL.format(self._scheme, self._address, self._port, endpoint)

        self._log_msg_request(method, request_url, body)

        try:
            headers = {'accept': 'application/json'}
            reply = requests.request(
                method.value, request_url, headers=headers, json=body,
                auth=self._auth, verify=self._verify_certs, timeout=self._timeout,
                allow_redirects=self._allow_redirects
            )
        except Exception as e:
            MSG = 'Request failed. method={:s} url={:s} body={:s}'
            msg = MSG.format(str(method.value).upper(), request_url, str(body))
            if self._logger is not None: self._logger.exception(msg)
            raise Exception(msg) from e

        self._log_msg_check_reply(method, request_url, body, reply, expected_status_codes)

        if reply.content and len(reply.content) > 0: return reply.json()
        return None


    def get(
        self, endpoint : str,
        expected_status_codes : Set[int] = EXPECTED_STATUS_CODES
    ) -> Optional[Any]:
        return self._do_rest_request(
            RestRequestMethod.GET, endpoint,
            expected_status_codes=expected_status_codes
        )


    def post(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = EXPECTED_STATUS_CODES
    ) -> Optional[Any]:
        return self._do_rest_request(
            RestRequestMethod.POST, endpoint, body=body,
            expected_status_codes=expected_status_codes
        )


    def put(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = EXPECTED_STATUS_CODES
    ) -> Optional[Any]:
        return self._do_rest_request(
            RestRequestMethod.PUT, endpoint, body=body,
            expected_status_codes=expected_status_codes
        )


    def patch(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = EXPECTED_STATUS_CODES
    ) -> Optional[Any]:
        return self._do_rest_request(
            RestRequestMethod.PATCH, endpoint, body=body,
            expected_status_codes=expected_status_codes
        )


    def delete(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = EXPECTED_STATUS_CODES
    ) -> Optional[Any]:
        return self._do_rest_request(
            RestRequestMethod.DELETE, endpoint, body=body,
            expected_status_codes=expected_status_codes
        )
