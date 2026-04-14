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

import logging, threading
from typing import Dict
from .dispatchers.Dispatchers import Dispatchers
from .Subscription import Subscription
from .TFSControllerSettings import TFSControllerSettings

LOGGER = logging.getLogger(__name__)

class Subscriptions:
    def __init__(self, dispatchers : Dispatchers, terminate : threading.Event) -> None:
        self._dispatchers = dispatchers
        self._terminate   = terminate
        self._lock        = threading.Lock()
        self._subscriptions : Dict[str, Subscription] = dict()

    def add_subscription(self, tfs_ctrl_settings : TFSControllerSettings) -> None:
        device_uuid = tfs_ctrl_settings.device_uuid
        with self._lock:
            subscription = self._subscriptions.get(device_uuid)
            if subscription is not None: return
            subscription = Subscription(tfs_ctrl_settings, self._dispatchers, self._terminate)
            self._subscriptions[device_uuid] = subscription
            subscription.start()

    def remove_subscription(self, device_uuid : str) -> None:
        with self._lock:
            subscription = self._subscriptions.get(device_uuid)
            if subscription is None: return
            if subscription.is_running: subscription.stop()
            self._subscriptions.pop(device_uuid, None)
