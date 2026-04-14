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

import grpc, logging, queue, threading, time
from typing import Callable
from common.proto.context_pb2 import Empty
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class _Collector(threading.Thread):
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
                    timestamp = event.event.timestamp.timestamp
                    self._events_queue.put_nowait((timestamp, event))
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    LOGGER.info('[_collect] UNAVAILABLE... retrying...')
                    time.sleep(0.5)
                    continue
                elif e.code() == grpc.StatusCode.CANCELLED:
                    break
                else:
                    raise # pragma: no cover

class EventsCollector:
    def __init__(
        self, context_client          : ContextClient,
        log_events_received           : bool = False,
        activate_context_collector    : bool = True,
        activate_topology_collector   : bool = True,
        activate_device_collector     : bool = True,
        activate_link_collector       : bool = True,
        activate_service_collector    : bool = True,
        activate_slice_collector      : bool = True,
        activate_connection_collector : bool = True,
    ) -> None:
        self._events_queue = queue.PriorityQueue()
        self._terminate = threading.Event()
        self._log_events_received = log_events_received

        self._context_thread = _Collector(
                lambda: context_client.GetContextEvents(Empty()),
                self._events_queue, self._terminate, self._log_events_received
            ) if activate_context_collector else None

        self._topology_thread = _Collector(
                lambda: context_client.GetTopologyEvents(Empty()),
                self._events_queue, self._terminate, self._log_events_received
            ) if activate_topology_collector else None

        self._device_thread = _Collector(
                lambda: context_client.GetDeviceEvents(Empty()),
                self._events_queue, self._terminate, self._log_events_received
            ) if activate_device_collector else None

        self._link_thread = _Collector(
                lambda: context_client.GetLinkEvents(Empty()),
                self._events_queue, self._terminate, self._log_events_received
            ) if activate_link_collector else None

        self._service_thread = _Collector(
                lambda: context_client.GetServiceEvents(Empty()),
                self._events_queue, self._terminate, self._log_events_received
            ) if activate_service_collector else None

        self._slice_thread = _Collector(
                lambda: context_client.GetSliceEvents(Empty()),
                self._events_queue, self._terminate, self._log_events_received
            ) if activate_slice_collector else None

        self._connection_thread = _Collector(
                lambda: context_client.GetConnectionEvents(Empty()),
                self._events_queue, self._terminate, self._log_events_received
            ) if activate_connection_collector else None

    def start(self):
        self._terminate.clear()

        if self._context_thread    is not None: self._context_thread.start()
        if self._topology_thread   is not None: self._topology_thread.start()
        if self._device_thread     is not None: self._device_thread.start()
        if self._link_thread       is not None: self._link_thread.start()
        if self._service_thread    is not None: self._service_thread.start()
        if self._slice_thread      is not None: self._slice_thread.start()
        if self._connection_thread is not None: self._connection_thread.start()

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

    def stop(self):
        self._terminate.set()

        if self._context_thread    is not None: self._context_thread.cancel()
        if self._topology_thread   is not None: self._topology_thread.cancel()
        if self._device_thread     is not None: self._device_thread.cancel()
        if self._link_thread       is not None: self._link_thread.cancel()
        if self._service_thread    is not None: self._service_thread.cancel()
        if self._slice_thread      is not None: self._slice_thread.cancel()
        if self._connection_thread is not None: self._connection_thread.cancel()

        if self._context_thread    is not None: self._context_thread.join()
        if self._topology_thread   is not None: self._topology_thread.join()
        if self._device_thread     is not None: self._device_thread.join()
        if self._link_thread       is not None: self._link_thread.join()
        if self._service_thread    is not None: self._service_thread.join()
        if self._slice_thread      is not None: self._slice_thread.join()
        if self._connection_thread is not None: self._connection_thread.join()
