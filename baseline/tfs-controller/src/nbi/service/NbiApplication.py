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


import logging, socketio, time
from typing import Any, List, Optional, Tuple
from flask import Flask, request
from flask_restful import Api, Resource
from flask_socketio import Namespace, SocketIO
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from nbi.Config import SECRET_KEY


LOGGER = logging.getLogger(__name__)

def log_request(response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    LOGGER.info(
        '%s %s %s %s %s', timestamp, request.remote_addr, request.method,
        request.full_path, response.status
    )
    return response

class NbiApplication:
    def __init__(self, base_url : Optional[str] = None) -> None:
        if base_url is None: base_url = ''
        self.base_url = base_url

        self._app = Flask(__name__)
        self._app.config['SECRET_KEY'] = SECRET_KEY
        self._app.after_request(log_request)
        self._api = Api(self._app, prefix=base_url)

        # Configure KafkaManager to enable SocketIO Servers running in different
        # gunicorn workers to self-coordinate and share sessions.
        #self._sio_client_manager = socketio.KafkaManager(
        #    url='kafka://{:s}'.format(KafkaConfig.get_kafka_address()),
        #    channel=KafkaTopic.NBI_SOCKETIO_WORKERS.value
        #)
        self._sio = SocketIO(
            self._app, cors_allowed_origins='*', async_mode='eventlet',
            #client_manager=self._sio_client_manager,
            logger=True, engineio_logger=True
        )

    def add_rest_api_resource(self, resource_class : Resource, *urls, **kwargs) -> None:
        self._api.add_resource(resource_class, *urls, **kwargs)

    def add_rest_api_resources(self, resources : List[Tuple[Resource, str, str]]) -> None:
        for endpoint_name, resource_class, resource_url in resources:
            self.add_rest_api_resource(resource_class, resource_url, endpoint=endpoint_name)

    def add_websocket_namespace(self, namespace : Namespace) -> None:
        self._sio.on_namespace(namespace)

    def websocket_emit_message(
        self, event : str, *args : Any, namespace : str = '/', to : Optional[str] = None
    ) -> None:
        self._sio.emit(event, *args, namespace=namespace, to=to)

    def get_flask_app(self) -> Flask:
        return self._app

    def get_flask_api(self) -> Api:
        return self._api

    def get_socketio_server(self) -> Optional[socketio.Server]:
        return self._sio.server

    def dump_configuration(self) -> None:
        LOGGER.debug('Configured REST-API Resources:')
        for resource in self._api.resources:
            LOGGER.debug(' - {:s}'.format(str(resource)))

        LOGGER.debug('Configured Flask Rules:')
        for rule in self._app.url_map.iter_rules():
            LOGGER.debug(' - {:s}'.format(str(rule)))

        LOGGER.debug('Configured SocketIO/WebSocket Namespaces:')
        for handler in self._sio.handlers:
            LOGGER.debug(' - {:s}'.format(str(handler)))
        for namespace in self._sio.namespace_handlers:
            LOGGER.debug(' - {:s}'.format(str(namespace)))
        for namespace in self._sio.server.handlers:
            LOGGER.debug(' - {:s}'.format(str(namespace)))
        for namespace in self._sio.server.namespace_handlers:
            LOGGER.debug(' - {:s}'.format(str(namespace)))
