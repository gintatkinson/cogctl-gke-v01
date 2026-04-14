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

import os, threading
from typing import Any, Dict, Iterator, Set, Tuple
from redis.client import Redis

from common.message_broker.Message import Message
from .._Backend import _Backend

DEFAULT_SERVICE_HOST = '127.0.0.1'
DEFAULT_SERVICE_PORT = 6379
DEFAULT_DATABASE_ID  = 0

def get_setting(settings : Dict[str, Any], name : str, default : Any) -> Any:
    value = settings.get(name, os.environ.get(name))
    return default if value is None else value

class RedisBackend(_Backend):
    def __init__(self, **settings) -> None: # pylint: disable=super-init-not-called
        host = get_setting(settings, 'REDIS_SERVICE_HOST', DEFAULT_SERVICE_HOST)
        port = get_setting(settings, 'REDIS_SERVICE_PORT', DEFAULT_SERVICE_PORT)
        dbid = get_setting(settings, 'REDIS_DATABASE_ID',  DEFAULT_DATABASE_ID )
        self._client = Redis.from_url('redis://{host}:{port}/{dbid}'.format(host=host, port=port, dbid=dbid))
        self._terminate = threading.Event()

    def terminate(self) -> None:
        self._terminate.set()

    def publish(self, topic_name : str, message_content : str) -> None:
        self._client.publish(topic_name, message_content)

    def consume(self, topic_names : Set[str], consume_timeout : float) -> Iterator[Tuple[str, str]]:
        pubsub = self._client.pubsub(ignore_subscribe_messages=True)
        for topic_name in topic_names: pubsub.subscribe(topic_name)

        while not self._terminate.is_set():
            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=consume_timeout)
            if message is None: continue
            if message['type'] not in {'message', 'pmessage'}: continue
            topic = message['channel'].decode('UTF-8')
            content = message['data'].decode('UTF-8')
            yield Message(topic, content)

        pubsub.unsubscribe()
        while pubsub.get_message() is not None: pass
        pubsub.close()
