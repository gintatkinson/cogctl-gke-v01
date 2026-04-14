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

import logging, socketio, threading, time
from .Constants import HEARTHBEAT_INTERVAL, SIO_NAMESPACE, SIO_ROOM, START_TIME

LOGGER = logging.getLogger(__name__)

class HeartbeatThread(threading.Thread):
    def __init__(self, namespace : socketio.Namespace):
        super().__init__(daemon=True)
        self._terminate = threading.Event()
        self._namespace = namespace

    def start(self):
        self._terminate.clear()
        return super().start()

    def stop(self) -> None:
        self._terminate.set()

    def run(self):
        try:
            LOGGER.info('[run] Running...')
            while not self._terminate.is_set():
                time.sleep(HEARTHBEAT_INTERVAL)
                server : socketio.Server = self._namespace.server
                if server is None: continue
                data = {'uptime_seconds': time.time() - START_TIME}
                server.emit('uptime', data, namespace=SIO_NAMESPACE, to=SIO_ROOM)
        except: # pylint: disable=bare-except
            LOGGER.exception('[run] Unexpected Thread Exception')
        LOGGER.info('[run] Terminated')
