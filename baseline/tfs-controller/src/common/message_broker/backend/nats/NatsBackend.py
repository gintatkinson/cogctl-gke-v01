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

import queue, threading
from typing import Iterator, Set, Tuple
from common.Settings import get_setting
from common.message_broker.Message import Message
from .._Backend import _Backend
from .NatsBackendThread import NatsBackendThread

NATS_URI_TEMPLATE_AUTH = 'nats://{:s}:{:s}@{:s}.{:s}.svc.cluster.local:{:s}'
NATS_URI_TEMPLATE_NOAUTH = 'nats://{:s}.{:s}.svc.cluster.local:{:s}'

class NatsBackend(_Backend):
    def __init__(self, **settings) -> None: # pylint: disable=super-init-not-called
        nats_uri = get_setting('NATS_URI', settings=settings, default=None)
        if nats_uri is None:
            nats_namespace   = get_setting('NATS_NAMESPACE', settings=settings)
            nats_client_port = get_setting('NATS_CLIENT_PORT', settings=settings)
            nats_username    = get_setting('NATS_USERNAME', settings=settings, default=None)
            nats_password    = get_setting('NATS_PASSWORD', settings=settings, default=None)
            if nats_username is None or nats_password is None:
                nats_uri = NATS_URI_TEMPLATE_NOAUTH.format(
                    nats_namespace, nats_namespace, nats_client_port)
            else:
                nats_uri = NATS_URI_TEMPLATE_AUTH.format(
                    nats_username, nats_password, nats_namespace, nats_namespace, nats_client_port)

        self._terminate = threading.Event()
        self._nats_backend_thread = NatsBackendThread(nats_uri)
        self._nats_backend_thread.start()

    def terminate(self) -> None:
        self._terminate.set()
        self._nats_backend_thread.terminate()
        self._nats_backend_thread.join()

    def publish(self, topic_name : str, message_content : str) -> None:
        self._nats_backend_thread.publish(topic_name, message_content)

    def consume(self, topic_names : Set[str], consume_timeout : float) -> Iterator[Tuple[str, str]]:
        out_queue = queue.Queue[Message]()
        unsubscribe = threading.Event()
        tasks = []
        for topic_name in topic_names:
            tasks.append(self._nats_backend_thread.subscribe(topic_name, consume_timeout, out_queue, unsubscribe))
        while not self._terminate.is_set():
            try:
                yield out_queue.get(block=True, timeout=consume_timeout)
            except queue.Empty:
                continue
        unsubscribe.set()
        for task in tasks: task.cancel()
