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

# See usage example below

import grpc, logging, queue, threading, time
from typing import Any, Callable, List, Optional
from common.proto.context_pb2 import Empty
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class CollectorThread(threading.Thread):
    def __init__(
        self, subscription_func : Callable, events_queue = queue.PriorityQueue,
        terminate = threading.Event, log_events_received: bool = False
    ) -> None:
        super().__init__(daemon=False)
        self._subscription_func = subscription_func
        self._events_queue = events_queue
        self._terminate = terminate
        self._log_events_received = log_events_received
        self._stream = None

    def cancel(self) -> None:
        if self._stream is None: return
        self._stream.cancel()

    def run(self) -> None:
        while not self._terminate.is_set():
            self._stream = self._subscription_func()
            try:
                for event in self._stream:
                    if self._log_events_received:
                        str_event = grpc_message_to_json_string(event)
                        LOGGER.info('[_collect] event: {:s}'.format(str_event))
                    object_name = str(event.__class__.__name__).lower().replace('event', '')
                    if object_name == 'any':
                        object_name = event.WhichOneof('event')
                        _event = getattr(event, object_name)
                        timestamp = _event.event.timestamp.timestamp
                    else:
                        timestamp = event.event.timestamp.timestamp
                    self._events_queue.put_nowait((timestamp, event))
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAVAILABLE: # pylint: disable=no-member
                    LOGGER.info('[_collect] UNAVAILABLE... retrying...')
                    time.sleep(0.5)
                    continue
                elif e.code() == grpc.StatusCode.CANCELLED: # pylint: disable=no-member
                    break
                else:
                    raise # pragma: no cover

class BaseEventCollector:
    def __init__(
        self, terminate : Optional[threading.Event] = None
    ) -> None:
        self._events_queue = queue.PriorityQueue()
        self._terminate = threading.Event() if terminate is None else terminate
        self._collector_threads : List[CollectorThread] = list()

    def install_collector(
        self, subscription_method : Callable, request_message : Any,
        log_events_received : bool = False
    ) -> None:
        self._collector_threads.append(CollectorThread(
            lambda: subscription_method(request_message),
            self._events_queue, self._terminate, log_events_received
        ))

    def start(self):
        self._terminate.clear()
        for collector_thread in self._collector_threads:
            collector_thread.start()

    def stop(self):
        self._terminate.set()

        for collector_thread in self._collector_threads:
            collector_thread.cancel()

        for collector_thread in self._collector_threads:
            collector_thread.join()

    def get_events_queue(self) -> queue.PriorityQueue:
        return self._events_queue

    def get_event(self, block : bool = True, timeout : float = 0.1):
        try:
            _,event = self._events_queue.get(block=block, timeout=timeout)
            return event
        except queue.Empty: # pylint: disable=catching-non-exception
            return None

    def get_events(self, block : bool = True, timeout : float = 0.1, count : int = None):
        events = []
        if count is None:
            while not self._terminate.is_set():
                event = self.get_event(block=block, timeout=timeout)
                if event is None: break
                events.append(event)
        else:
            while len(events) < count:
                if self._terminate.is_set(): break
                event = self.get_event(block=block, timeout=timeout)
                if event is None: continue
                events.append(event)
        return sorted(events, key=lambda e: e.event.timestamp.timestamp)

def main() -> None:
    logging.basicConfig(level=logging.INFO)

    context_client = ContextClient()
    context_client.connect()

    event_collector = BaseEventCollector()
    event_collector.install_collector(context_client.GetDeviceEvents,  Empty(), log_events_received=True)
    event_collector.install_collector(context_client.GetLinkEvents,    Empty(), log_events_received=True)
    event_collector.install_collector(context_client.GetServiceEvents, Empty(), log_events_received=True)
    event_collector.start()

    time.sleep(60)

    event_collector.stop()
    context_client.close()

if __name__ == '__main__':
    main()
