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

# InMemeory MessageBroker Backend
# -------------------------------
# - WARNING: DESIGNED AND BUILT FOR UNIT TESTING AND INTEGRATION TESTING PURPOSES ONLY !!!
#            USE ANOTHER BACKEND IN PRODUCTION ENVIRONMENTS.

import logging, threading
from queue import Queue, Empty
from typing import Dict, Iterator, Set, Tuple
from .._Backend import _Backend

LOGGER = logging.getLogger(__name__)

class InMemoryBackend(_Backend):
    def __init__(self, **settings) -> None: # pylint: disable=super-init-not-called
        self._lock = threading.Lock()
        self._terminate = threading.Event()
        self._topic__to__queues : Dict[str, Set[Queue]] = {}

    def terminate(self) -> None:
        self._terminate.set()

    def publish(self, topic_name : str, message_content : str) -> None:
        queues = self._topic__to__queues.get(topic_name, None)
        if queues is None: return
        for queue in queues: queue.put_nowait((topic_name, message_content))

    def consume(self, topic_names : Set[str], consume_timeout : float) -> Iterator[Tuple[str, str]]:
        queue = Queue()
        for topic_name in topic_names:
            self._topic__to__queues.setdefault(topic_name, set()).add(queue)

        while not self._terminate.is_set():
            try:
                message = queue.get(block=True, timeout=consume_timeout)
            except Empty:
                continue
            if message is None: continue
            yield message

        for topic_name in topic_names:
            self._topic__to__queues.get(topic_name, set()).discard(queue)
