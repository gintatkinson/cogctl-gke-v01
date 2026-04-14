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

import queue, socketio, threading
from concurrent.futures import Future
from typing import Any, Tuple

class _Dispatcher(threading.Thread):
    def __init__(self, terminate : threading.Event):
        super().__init__(daemon=True)
        self._dispatcher_queue = queue.Queue[Tuple[Any, Future]]()
        self._terminate = terminate

    @property
    def dispatcher_queue(self): return self._dispatcher_queue

    def register(self, sio_client : socketio.Client) -> None:
        raise NotImplementedError('To be implemented in subclass')

    def run(self):
        while not self._terminate.is_set():
            try:
                request,future = self._dispatcher_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue

            try:
                result = self.process_request(request)
            except Exception as e:
                future.set_exception(e)
            else:
                future.set_result(result)

    def process_request(self, request : Any) -> Any:
        raise NotImplementedError('To be implemented in subclass')
