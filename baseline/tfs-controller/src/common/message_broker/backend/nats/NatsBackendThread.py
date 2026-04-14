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

import asyncio, logging, nats, nats.errors, queue, threading
from typing import List
from common.message_broker.Message import Message

LOGGER = logging.getLogger(__name__)

class NatsBackendThread(threading.Thread):
    def __init__(self, nats_uri : str) -> None:
        self._nats_uri = nats_uri
        self._event_loop = asyncio.get_event_loop()
        self._terminate = asyncio.Event()
        self._tasks_terminated = asyncio.Event()
        self._publish_queue = asyncio.Queue[Message]()
        self._tasks : List[asyncio.Task] = list()
        super().__init__()

    def terminate(self) -> None:
        self._terminate.set()
        for task in self._tasks: task.cancel()
        self._tasks_terminated.set()

    async def _run_publisher(self) -> None:
        LOGGER.info('[_run_publisher] NATS URI: {:s}'.format(str(self._nats_uri)))
        client = await nats.connect(servers=[self._nats_uri])
        LOGGER.info('[_run_publisher] Connected!')
        while not self._terminate.is_set():
            try:
                message : Message = await self._publish_queue.get()
            except asyncio.CancelledError:
                break
            await client.publish(message.topic, message.content.encode('UTF-8'))
        await client.drain()

    def publish(self, topic_name : str, message_content : str) -> None:
        self._publish_queue.put_nowait(Message(topic_name, message_content))

    async def _run_subscriber(
        self, topic_name : str, timeout : float, out_queue : queue.Queue[Message], unsubscribe : threading.Event,
        ready_event : threading.Event
    ) -> None:
        try:
            LOGGER.info('[_run_subscriber] NATS URI: {:s}'.format(str(self._nats_uri)))
            client = await nats.connect(servers=[self._nats_uri])
            server_version = client.connected_server_version
            LOGGER.info('[_run_subscriber] Connected! NATS Server version: {:s}'.format(str(repr(server_version))))
            subscription = await client.subscribe(topic_name)
            LOGGER.info('[_run_subscriber] Subscribed!')
            ready_event.set()
            while not self._terminate.is_set() and not unsubscribe.is_set():
                try:
                    message = await subscription.next_msg(timeout)
                except nats.errors.TimeoutError:
                    continue
                except asyncio.CancelledError:
                    break
                out_queue.put(Message(message.subject, message.data.decode('UTF-8')))
            await subscription.unsubscribe()
            await client.drain()
        except Exception:   # pylint: disable=broad-exception-caught
            LOGGER.exception('[_run_subscriber] Unhandled Exception')

    def subscribe(
        self, topic_name : str, timeout : float, out_queue : queue.Queue[Message], unsubscribe : threading.Event
    ) -> None:
        ready_event = threading.Event()
        task = self._event_loop.create_task(
            self._run_subscriber(topic_name, timeout, out_queue, unsubscribe, ready_event)
        )
        self._tasks.append(task)
        LOGGER.info('[subscribe] Waiting for subscriber to be ready...')
        is_ready = ready_event.wait(timeout=120)
        LOGGER.info('[subscribe] Subscriber is Ready? {:s}'.format(str(is_ready)))

    def run(self) -> None:
        asyncio.set_event_loop(self._event_loop)
        task = self._event_loop.create_task(self._run_publisher())
        self._tasks.append(task)
        self._event_loop.run_until_complete(self._terminate.wait())
        self._tasks.remove(task)
        self._event_loop.run_until_complete(self._tasks_terminated.wait())
