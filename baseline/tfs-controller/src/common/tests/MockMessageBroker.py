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

import json, logging, threading, time
from queue import Queue, Empty
from typing import Dict, Iterator, NamedTuple, Set
from common.proto.context_pb2 import EventTypeEnum

LOGGER = logging.getLogger(__name__)

TOPIC_CONNECTION = 'connection'
TOPIC_CONTEXT    = 'context'
TOPIC_DEVICE     = 'device'
TOPIC_LINK       = 'link'
TOPIC_POLICY     = 'policy'
TOPIC_SERVICE    = 'service'
TOPIC_SLICE      = 'slice'
TOPIC_TOPOLOGY   = 'topology'

CONSUME_TIMEOUT = 0.5 # seconds

class Message(NamedTuple):
    topic: str
    content: str

class MockMessageBroker:
    def __init__(self):
        self._terminate = threading.Event()
        self._topic__to__queues : Dict[str, Set[Queue]] = {}

    def publish(self, message : Message) -> None:
        queues = self._topic__to__queues.get(message.topic, None)
        if queues is None: return
        for queue in queues: queue.put_nowait((message.topic, message.content))

    def consume(
        self, topic_names : Set[str], block : bool = True, consume_timeout : float = CONSUME_TIMEOUT
    ) -> Iterator[Message]:
        queue = Queue()
        for topic_name in topic_names:
            self._topic__to__queues.setdefault(topic_name, set()).add(queue)

        while not self._terminate.is_set():
            try:
                message = queue.get(block=block, timeout=consume_timeout)
            except Empty:
                continue
            if message is None: continue
            yield Message(*message)

        for topic_name in topic_names:
            self._topic__to__queues.get(topic_name, set()).discard(queue)

    def terminate(self):
        self._terminate.set()

def notify_event(
    messagebroker : MockMessageBroker, topic_name : str, event_type : EventTypeEnum, fields : Dict[str, str]
) -> None:
    event = {'event': {'timestamp': {'timestamp': time.time()}, 'event_type': event_type}}
    for field_name, field_value in fields.items():
        event[field_name] = field_value
    messagebroker.publish(Message(topic_name, json.dumps(event)))
