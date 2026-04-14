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

import json, logging, queue, socketio
from concurrent.futures import Future
from .Constants import SIO_NAMESPACE
from .Recommendation import Recommendation, RecommendationAction

LOGGER = logging.getLogger(__name__)

class ClientNamespace(socketio.ClientNamespace):
    def __init__(self, dispatcher_queue : queue.Queue[Recommendation]):
        self._dispatcher_queue = dispatcher_queue
        super().__init__(namespace=SIO_NAMESPACE)

    def on_connect(self):
        LOGGER.info('[on_connect] Connected')

    def on_disconnect(self, reason):
        MSG = '[on_disconnect] Disconnected!, reason: {:s}'
        LOGGER.info(MSG.format(str(reason)))

    def on_vlink_create(self, data):
        MSG = '[on_vlink_create] begin data={:s}'
        LOGGER.info(MSG.format(str(data)))

        json_data = json.loads(data)
        request_key = json_data.pop('_request_key')

        recommendation = Recommendation(
            action = RecommendationAction.VLINK_CREATE,
            data   = json_data,
        )
        result = Future()

        MSG = '[on_vlink_create] Recommendation ({:s}): {:s}'
        LOGGER.info(MSG.format(str(request_key), str(recommendation)))

        LOGGER.debug('[on_vlink_create] Queuing recommendation...')
        self._dispatcher_queue.put_nowait((recommendation, result))
        
        reply = dict()
        reply['_request_key'] = request_key
        try:
            reply['result'] = result.result()
            event = reply['result'].pop('event')
        except Exception as e:
            reply['error'] = str(e)
            #reply['stacktrace'] = str(e)
            event = 'error'

        LOGGER.debug('[on_vlink_create] Replying...')
        self.emit(event, json.dumps(reply))
        LOGGER.debug('[on_vlink_create] end')

    def on_vlink_remove(self, data):
        MSG = '[on_vlink_remove] begin data={:s}'
        LOGGER.info(MSG.format(str(data)))

        json_data = json.loads(data)
        request_key = json_data.pop('_request_key')

        recommendation = Recommendation(
            action = RecommendationAction.VLINK_REMOVE,
            data   = json_data,
        )
        result = Future()

        MSG = '[on_vlink_remove] Recommendation ({:s}): {:s}'
        LOGGER.info(MSG.format(str(request_key), str(recommendation)))

        LOGGER.debug('[on_vlink_remove] Queuing recommendation...')
        self._dispatcher_queue.put_nowait((recommendation, result))
        
        reply = dict()
        reply['_request_key'] = request_key
        try:
            reply['result'] = result.result()
            event = reply['result'].pop('event')
        except Exception as e:
            reply['error'] = str(e)
            #reply['stacktrace'] = str(e)
            event = 'error'

        LOGGER.debug('[on_vlink_remove] Replying...')
        self.emit(event, json.dumps(reply))
        LOGGER.debug('[on_vlink_remove] end')
