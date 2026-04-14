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

import logging, queue, threading, time
from typing import Any, Callable, Optional
from common.proto.context_pb2 import DeviceEvent, Empty, EventTypeEnum, LinkEvent
from common.tools.grpc.BaseEventCollector import BaseEventCollector
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

class BaseEventDispatcher(threading.Thread):
    def __init__(
        self, events_queue : queue.PriorityQueue,
        terminate : Optional[threading.Event] = None
    ) -> None:
        super().__init__(daemon=True)
        self._events_queue = events_queue
        self._terminate = threading.Event() if terminate is None else terminate

    def stop(self):
        self._terminate.set()

    def _get_event(self, block : bool = True, timeout : Optional[float] = 0.5) -> Optional[Any]:
        try:
            _, event = self._events_queue.get(block=block, timeout=timeout)
            return event
        except queue.Empty:
            return None

    def _get_dispatcher(self, event : Any) -> Optional[Callable]:
        object_name = str(event.__class__.__name__).lower().replace('event', '')
        event_type  = event.event.event_type
        event_type  = EventTypeEnum.Name(event_type)
        event_type  = event_type.lower().replace('eventtype_', '')

        method_name = 'dispatch_{:s}_{:s}'.format(object_name, event_type)
        dispatcher  = getattr(self, method_name, None)
        if dispatcher is not None: return dispatcher

        method_name = 'dispatch_{:s}'.format(object_name)
        dispatcher  = getattr(self, method_name, None)
        if dispatcher is not None: return dispatcher

        method_name = 'dispatch'
        dispatcher  = getattr(self, method_name, None)
        if dispatcher is not None: return dispatcher

        return None

    def run(self) -> None:
        while not self._terminate.is_set():
            event = self._get_event()
            if event is None: continue

            object_name = str(event.__class__.__name__)
            object_name = object_name.lower().replace('event', '')
            if object_name == 'any':
                field_name = event.WhichOneof('event')
                event = getattr(event, field_name)

            event_type = event.event.event_type
            event_type = EventTypeEnum.Name(event_type)
            event_type = event_type.lower().replace('eventtype_', '')

            dispatcher = self._get_dispatcher(event)
            if dispatcher is None:
                MSG = 'No dispatcher available for Event({:s})'
                LOGGER.warning(MSG.format(grpc_message_to_json_string(event)))
                continue

            dispatcher(event)

class MyEventDispatcher(BaseEventDispatcher):
    def dispatch_device_create(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Create: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))

    def dispatch_device_update(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Update: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))

    def dispatch_device_remove(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Remove: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))

    def dispatch_link(self, link_event : LinkEvent) -> None:
        MSG = 'Processing Link Create/Update/Remove: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(link_event)))

    def dispatch(self, event : Any) -> None:
        MSG = 'Processing any other Event: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(event)))

def main() -> None:
    logging.basicConfig(level=logging.INFO)

    context_client = ContextClient()
    context_client.connect()

    event_collector = BaseEventCollector()
    event_collector.install_collector(context_client.GetDeviceEvents,  Empty(), log_events_received=True)
    event_collector.install_collector(context_client.GetLinkEvents,    Empty(), log_events_received=True)
    event_collector.install_collector(context_client.GetServiceEvents, Empty(), log_events_received=True)
    event_collector.start()

    event_dispatcher = MyEventDispatcher(event_collector.get_events_queue())
    event_dispatcher.start()

    time.sleep(60)

    event_dispatcher.stop()
    event_collector.stop()
    context_client.close()

if __name__ == '__main__':
    main()
