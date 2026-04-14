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

import logging, requests
from typing import Any, Dict, Optional, Set
from common.tools.rest_api.client.RestApiClient import RestApiClient


HOST_META_URL = '{:s}://{:s}:{:d}/.well-known/host-meta'


class RestConfClient(RestApiClient):
    def __init__(
        self, address : str, port : int = 8080, scheme : str = 'http',
        username : Optional[str] = None, password : Optional[str] = None,
        restconf_version : Optional[str] = None,
        timeout : int = 30, verify_certs : bool = True, allow_redirects : bool = True,
        logger : Optional[logging.Logger] = None
    ) -> None:
        super().__init__(
            address, port=port, scheme=scheme, username=username, password=password,
            timeout=timeout, verify_certs=verify_certs, allow_redirects=allow_redirects,
            logger=logger
        )
        self._restconf_version = restconf_version
        self._discover_base_url()


    def _discover_base_url(self) -> None:
        host_meta_url = HOST_META_URL.format(self._scheme, self._address, self._port)
        host_meta : Dict = super().get(host_meta_url, expected_status_codes={requests.codes['OK']})

        links = host_meta.get('links')
        if links is None: raise AttributeError('Missing attribute "links" in host-meta reply')
        if not isinstance(links, list): raise AttributeError('Attribute "links" must be a list')
        if len(links) != 1: raise AttributeError('Attribute "links" is expected to have exactly 1 item')

        link = links[0]
        if not isinstance(link, dict): raise AttributeError('Attribute "links[0]" must be a dict')

        rel = link.get('rel')
        if rel is None: raise AttributeError('Missing attribute "links[0].rel" in host-meta reply')
        if not isinstance(rel, str): raise AttributeError('Attribute "links[0].rel" must be a str')
        if rel != 'restconf': raise AttributeError('Attribute "links[0].rel" != "restconf"')

        href = link.get('href')
        if href is None: raise AttributeError('Missing attribute "links[0]" in host-meta reply')
        if not isinstance(href, str): raise AttributeError('Attribute "links[0].href" must be a str')

        self._base_url = str(href).replace('//', '/')
        if self._restconf_version is not None:
            self._base_url += '/{:s}'.format(self._restconf_version)
        if self._base_url.endswith('/data/'):
            self._base_url = self._base_url.split('/data/')[0]
        elif self._base_url.endswith('/data'):
            self._base_url = self._base_url.split('/data')[0]


    def get(
        self, endpoint : str,
        expected_status_codes : Set[int] = {requests.codes['OK']}
    ) -> Optional[Any]:
        return super().get(
            ('/data/{:s}'.format(endpoint)).replace('//', '/'),
            expected_status_codes=expected_status_codes
        )


    def post(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = {requests.codes['CREATED']}
    ) -> Optional[Any]:
        return super().post(
            ('/data/{:s}'.format(endpoint)).replace('//', '/'), body=body,
            expected_status_codes=expected_status_codes
        )


    def put(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = {requests.codes['CREATED'], requests.codes['NO_CONTENT']}
    ) -> Optional[Any]:
        return super().put(
            ('/data/{:s}'.format(endpoint)).replace('//', '/'), body=body,
            expected_status_codes=expected_status_codes
        )


    def patch(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = {requests.codes['NO_CONTENT']}
    ) -> Optional[Any]:
        return super().patch(
            ('/data/{:s}'.format(endpoint)).replace('//', '/'), body=body,
            expected_status_codes=expected_status_codes
        )


    def delete(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = {requests.codes['NO_CONTENT']}
    ) -> Optional[Any]:
        return super().delete(
            ('/data/{:s}'.format(endpoint)).replace('//', '/'), body=body,
            expected_status_codes=expected_status_codes
        )


    def rpc(
        self, endpoint : str, body : Optional[Any] = None,
        expected_status_codes : Set[int] = {requests.codes['OK'], requests.codes['NO_CONTENT']}
    ) -> Optional[Any]:
        return super().post(
            ('/operations/{:s}'.format(endpoint)).replace('//', '/'), body=body,
            expected_status_codes=expected_status_codes
        )
