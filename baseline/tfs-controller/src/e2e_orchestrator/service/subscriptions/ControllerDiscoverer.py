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


import logging, queue, threading
from typing import Any, Optional
from common.proto.context_pb2 import DeviceEvent, Empty
from common.tools.grpc.BaseEventCollector import BaseEventCollector
from common.tools.grpc.BaseEventDispatcher import BaseEventDispatcher
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from .Subscriptions import Subscriptions
from .TFSControllerSettings import get_tfs_controller_settings


LOGGER = logging.getLogger(__name__)


class EventDispatcher(BaseEventDispatcher):
    def __init__(
        self, events_queue : queue.PriorityQueue,
        context_client : ContextClient,
        subscriptions : Subscriptions,
        terminate : Optional[threading.Event] = None
    ) -> None:
        super().__init__(events_queue, terminate)
        self._context_client = context_client
        self._subscriptions  = subscriptions

    def dispatch_device_create(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Create: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))
        tfs_ctrl_settings = get_tfs_controller_settings(
            self._context_client, device_event
        )
        if tfs_ctrl_settings is None: return
        self._subscriptions.add_subscription(tfs_ctrl_settings)

    def dispatch_device_update(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Update: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))
        tfs_ctrl_settings = get_tfs_controller_settings(
            self._context_client, device_event
        )
        if tfs_ctrl_settings is None: return
        self._subscriptions.add_subscription(tfs_ctrl_settings)

    def dispatch_device_remove(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Remove: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))
        device_uuid = device_event.device_id.device_uuid.uuid
        self._subscriptions.remove_subscription(device_uuid)

    def dispatch(self, event : Any) -> None:
        MSG = 'Unexpected Event: {:s}'
        LOGGER.warning(MSG.format(grpc_message_to_json_string(event)))

class ControllerDiscoverer:
    def __init__(
        self, subscriptions : Subscriptions, terminate : threading.Event
    ) -> None:
        self._context_client = ContextClient()

        self._event_collector = BaseEventCollector(terminate=terminate)
        self._event_collector.install_collector(
            self._context_client.GetDeviceEvents, Empty(), log_events_received=True
        )
        self._event_dispatcher = EventDispatcher(
            self._event_collector.get_events_queue(), self._context_client, subscriptions,
            terminate=terminate
        )

    def start(self) -> None:
        self._context_client.connect()
        self._event_dispatcher.start()
        self._event_collector.start()

    def stop(self):
        self._event_collector.stop()
        self._event_dispatcher.stop()
        self._context_client.close()
