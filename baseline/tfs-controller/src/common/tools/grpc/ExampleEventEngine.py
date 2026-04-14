# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging, threading, time
from typing import Optional
from common.proto.context_pb2 import DeviceEvent, Empty, ServiceEvent
from common.tools.grpc.BaseEventCollector import BaseEventCollector
from common.tools.grpc.BaseEventDispatcher import BaseEventDispatcher
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

class EventCollector(BaseEventCollector):
    pass

class EventDispatcher(BaseEventDispatcher):
    def dispatch_device_create(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Create: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))

    def dispatch_device_update(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Update: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))

    def dispatch_device_remove(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Remove: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))

    def dispatch_service_create(self, service_event : ServiceEvent) -> None:
        MSG = 'Processing Service Create: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(service_event)))

    def dispatch_service_update(self, service_event : ServiceEvent) -> None:
        MSG = 'Processing Service Update: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(service_event)))

    def dispatch_service_remove(self, service_event : ServiceEvent) -> None:
        MSG = 'Processing Service Remove: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(service_event)))

class ExampleEventEngine:
    def __init__(
        self, terminate : Optional[threading.Event] = None
    ) -> None:
        self._terminate = threading.Event() if terminate is None else terminate

        self._context_client = ContextClient()
        self._event_collector = EventCollector(terminate=self._terminate)
        self._event_collector.install_collector(
            self._context_client.GetDeviceEvents, Empty(),
            log_events_received=True
        )
        self._event_collector.install_collector(
            self._context_client.GetLinkEvents, Empty(),
            log_events_received=True
        )
        self._event_collector.install_collector(
            self._context_client.GetServiceEvents, Empty(),
            log_events_received=True
        )

        self._event_dispatcher = EventDispatcher(
            self._event_collector.get_events_queue(),
            terminate=self._terminate
        )

    def start(self) -> None:
        self._context_client.connect()
        self._event_collector.start()
        self._event_dispatcher.start()

    def stop(self) -> None:
        self._terminate.set()
        self._event_dispatcher.stop()
        self._event_collector.stop()
        self._context_client.close()

def main() -> None:
    logging.basicConfig(level=logging.INFO)

    event_engine = ExampleEventEngine()
    event_engine.start()

    time.sleep(60)

    event_engine.stop()

if __name__ == '__main__':
    main()
