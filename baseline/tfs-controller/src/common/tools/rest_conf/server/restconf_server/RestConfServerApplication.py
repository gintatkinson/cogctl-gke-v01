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


import json, logging, time
from typing import Any, Dict, Tuple, Type
from flask import Flask, request
from flask_restful import Api, Resource
from .Callbacks import CallbackDispatcher
from .Config import RESTCONF_PREFIX, SECRET_KEY, STARTUP_FILE, YANG_SEARCH_PATH
from .DispatchData import RestConfDispatchData
from .DispatchOperations import RestConfDispatchOperations
from .HostMeta import HostMeta
from .YangHandler import YangHandler
from .YangModelDiscoverer import YangModuleDiscoverer


logging.basicConfig(
    level=logging.INFO,
    format='[Worker-%(process)d][%(asctime)s] %(levelname)s:%(name)s:%(message)s',
)


LOGGER = logging.getLogger(__name__)


def log_request(response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    LOGGER.info(
        '%s %s %s %s %s', timestamp, request.remote_addr, request.method,
        request.full_path, response.status
    )
    return response


class RestConfServerApplication:
    def __init__(self) -> None:
        self._ymd = YangModuleDiscoverer(YANG_SEARCH_PATH)
        self._yang_module_names = self._ymd.run(do_log_order=True)

        with open(STARTUP_FILE, mode='r', encoding='UTF-8') as fp:
            self._yang_startup_data = json.loads(fp.read())

        self._yang_handler = YangHandler(
            YANG_SEARCH_PATH, self._yang_module_names, self._yang_startup_data
        )

        self._callback_dispatcher = CallbackDispatcher()

        self._app = Flask(__name__)
        self._app.config['SECRET_KEY'] = SECRET_KEY
        self._app.after_request(log_request)
        self._api = Api(self._app)

    @property
    def yang_handler(self): return self._yang_handler

    @property
    def callback_dispatcher(self): return self._callback_dispatcher

    def get_startup_data(self) -> None:
        return self._yang_startup_data

    def register_host_meta(self) -> None:
        self._api.add_resource(
            HostMeta,
            '/.well-known/host-meta',
            resource_class_args=(RESTCONF_PREFIX,)
        )

    def register_restconf(self) -> None:
        self._api.add_resource(
            RestConfDispatchData,
            RESTCONF_PREFIX + '/data/<path:subpath>',
            RESTCONF_PREFIX + '/data/<path:subpath>/',
            resource_class_args=(self._yang_handler, self._callback_dispatcher)
        )
        self._api.add_resource(
            RestConfDispatchOperations,
            RESTCONF_PREFIX + '/operations/<path:subpath>',
            RESTCONF_PREFIX + '/operations/<path:subpath>/',
            resource_class_args=(self._yang_handler, self._callback_dispatcher)
        )

    def register_custom(
        self, resource_class : Type[Resource],
        *urls : str, add_prefix_to_urls : bool = True,
        resource_class_args : Tuple[Any, ...] = tuple(),
        resource_class_kwargs : Dict[str, Any] = dict()
    ) -> None:
        if add_prefix_to_urls:
            urls = [RESTCONF_PREFIX + u for u in urls]
        self._api.add_resource(
            resource_class, *urls,
            resource_class_args=resource_class_args,
            resource_class_kwargs=resource_class_kwargs
        )

    def get_flask_app(self) -> Flask:
        return self._app

    def get_flask_api(self) -> Api:
        return self._api

    def dump_configuration(self) -> None:
        LOGGER.info('Available RESTCONF paths:')
        restconf_paths = self._yang_handler.get_schema_paths()
        for restconf_path in sorted(restconf_paths):
            LOGGER.info('- {:s}'.format(str(restconf_path)))
