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

import logging
from flask import request
from flask_socketio import Namespace, join_room, leave_room
from .Constants import SIO_NAMESPACE, SIO_ROOM
from .HeartbeatThread import HeartbeatThread

LOGGER = logging.getLogger(__name__)

class HeartbeatServerNamespace(Namespace):
    def __init__(self):
        super().__init__(namespace=SIO_NAMESPACE)
        self._thread = HeartbeatThread(self)
        self._thread.start()

    def stop_thread(self) -> None:
        self._thread.stop()

    def on_connect(self, auth):
        MSG = '[on_connect] Client connect: sid={:s}, auth={:s}'
        LOGGER.info(MSG.format(str(request.sid), str(auth)))
        join_room(SIO_ROOM, namespace=SIO_NAMESPACE)

    def on_disconnect(self, reason):
        MSG = '[on_disconnect] Client disconnect: sid={:s}, reason={:s}'
        LOGGER.info(MSG.format(str(request.sid), str(reason)))
        leave_room(SIO_ROOM, namespace=SIO_NAMESPACE)
