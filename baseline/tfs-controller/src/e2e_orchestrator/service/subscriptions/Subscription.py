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


import socketio, threading
from common.Constants import ServiceNameEnum
from common.Settings import get_service_baseurl_http
from .dispatchers.Dispatchers import Dispatchers
from .TFSControllerSettings import TFSControllerSettings


NBI_SERVICE_PREFIX_URL = get_service_baseurl_http(ServiceNameEnum.NBI) or ''
CHILD_SOCKETIO_URL = 'http://{:s}:{:s}@{:s}:{:d}' + NBI_SERVICE_PREFIX_URL


class Subscription(threading.Thread):
    def __init__(
        self, tfs_ctrl_settings : TFSControllerSettings, dispatchers : Dispatchers,
        terminate : threading.Event
    ) -> None:
        super().__init__(daemon=True)
        self._settings    = tfs_ctrl_settings
        self._dispatchers = dispatchers
        self._terminate   = terminate
        self._is_running  = threading.Event()

    @property
    def is_running(self): return self._is_running.is_set()

    def run(self) -> None:
        child_socketio_url = CHILD_SOCKETIO_URL.format(
            self._settings.nbi_username,
            self._settings.nbi_password,
            self._settings.nbi_address,
            self._settings.nbi_port,
        )

        sio = socketio.Client(logger=True, engineio_logger=True)
        self._dispatchers.register(sio)
        sio.connect(child_socketio_url)

        while not self._terminate.is_set():
            sio.sleep(seconds=0.5)

        sio.shutdown()

    def stop(self):
        self._terminate.set()
