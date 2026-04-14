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

import logging, socketio, threading
from typing import List, Type
from ._Dispatcher import _Dispatcher

LOGGER = logging.getLogger(__name__)

class Dispatchers:
    def __init__(self, terminate : threading.Event) -> None:
        self._terminate = terminate
        self._dispatchers : List[_Dispatcher] = list()

    def add_dispatcher(self, dispatcher_class : Type[_Dispatcher]) -> None:
        dispatcher = dispatcher_class(self._terminate)
        self._dispatchers.append(dispatcher)
        dispatcher.start()

    def register(self, sio_client : socketio.Client) -> None:
        for dispatcher in self._dispatchers:
            dispatcher.register(sio_client)
