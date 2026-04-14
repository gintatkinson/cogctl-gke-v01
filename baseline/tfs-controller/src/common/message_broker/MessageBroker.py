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

import logging
from typing import Iterator, Set
from .backend._Backend import _Backend
from .Constants import CONSUME_TIMEOUT
from .Message import Message

LOGGER = logging.getLogger(__name__)

class MessageBroker:
    def __init__(self, backend : _Backend):
        if not isinstance(backend, _Backend):
            str_class_path = '{}.{}'.format(_Backend.__module__, _Backend.__name__)
            raise AttributeError('backend must inherit from {}'.format(str_class_path))
        self._backend = backend

    @property
    def backend(self) -> _Backend: return self._backend

    def publish(self, message : Message) -> None:
        self._backend.publish(message.topic, message.content)

    def consume(self, topic_names : Set[str], consume_timeout : float = CONSUME_TIMEOUT) -> Iterator[Message]:
        for pair in self._backend.consume(topic_names, consume_timeout=consume_timeout):
            yield Message(*pair)

    def terminate(self):
        self._backend.terminate()
