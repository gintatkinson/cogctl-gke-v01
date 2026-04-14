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

import json, logging
from flask import request
from flask_socketio import Namespace, join_room, leave_room
from kafka import KafkaProducer
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from .Constants import SIO_NAMESPACE, SIO_ROOM
from .VntRecommThread import VntRecommThread

LOGGER = logging.getLogger(__name__)

class VntRecommServerNamespace(Namespace):
    def __init__(self):
        super().__init__(namespace=SIO_NAMESPACE)
        self._thread = VntRecommThread(self)
        self._thread.start()

        self.kafka_producer = KafkaProducer(
            bootstrap_servers = KafkaConfig.get_kafka_address(),
        )

    def stop_thread(self) -> None:
        self._thread.stop()

    def on_connect(self, auth):
        MSG = '[on_connect] Client connect: sid={:s}, auth={:s}'
        LOGGER.debug(MSG.format(str(request.sid), str(auth)))
        join_room(SIO_ROOM, namespace=SIO_NAMESPACE)

    def on_disconnect(self, reason):
        MSG = '[on_disconnect] Client disconnect: sid={:s}, reason={:s}'
        LOGGER.debug(MSG.format(str(request.sid), str(reason)))
        leave_room(SIO_ROOM, namespace=SIO_NAMESPACE)

    def on_vlink_created(self, data):
        MSG = '[on_vlink_created] begin: sid={:s}, data={:s}'
        LOGGER.debug(MSG.format(str(request.sid), str(data)))

        data = json.loads(data)
        request_key = str(data.pop('_request_key')).encode('utf-8')
        vntm_reply = json.dumps({'event': 'vlink_created', 'data': data}).encode('utf-8')
        LOGGER.debug('[on_vlink_created] request_key={:s}/{:s}'.format(str(type(request_key)), str(request_key)))
        LOGGER.debug('[on_vlink_created] vntm_reply={:s}/{:s}'.format(str(type(vntm_reply)), str(vntm_reply)))

        self.kafka_producer.send(
            KafkaTopic.VNTMANAGER_RESPONSE.value, key=request_key, value=vntm_reply
        )
        self.kafka_producer.flush()

    def on_vlink_removed(self, data):
        MSG = '[on_vlink_removed] begin: sid={:s}, data={:s}'
        LOGGER.debug(MSG.format(str(request.sid), str(data)))

        data = json.loads(data)
        request_key = str(data.pop('_request_key')).encode('utf-8')
        vntm_reply = json.dumps({'event': 'vlink_removed', 'data': data}).encode('utf-8')
        LOGGER.debug('[on_vlink_removed] request_key={:s}/{:s}'.format(str(type(request_key)), str(request_key)))
        LOGGER.debug('[on_vlink_removed] vntm_reply={:s}/{:s}'.format(str(type(vntm_reply)), str(vntm_reply)))

        self.kafka_producer.send(
            KafkaTopic.VNTMANAGER_RESPONSE.value, key=request_key, value=vntm_reply
        )
        self.kafka_producer.flush()
