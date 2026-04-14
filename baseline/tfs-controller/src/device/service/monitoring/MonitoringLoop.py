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

import queue, threading
from device.service.driver_api._Driver import _Driver

class MonitoringLoop:
    def __init__(self, device_uuid : str, driver : _Driver, samples_queue : queue.Queue) -> None:
        self._device_uuid = device_uuid
        self._driver = driver
        self._samples_queue = samples_queue
        self._running = threading.Event()
        self._terminate = threading.Event()
        self._samples_stream = self._driver.GetState(blocking=True, terminate=self._terminate)
        self._collector_thread = threading.Thread(target=self._collect, daemon=True)

    def _collect(self) -> None:
        for sample in self._samples_stream:
            if self._terminate.is_set(): break
            sample = (self._device_uuid, *sample)
            self._samples_queue.put_nowait(sample)

    def start(self):
        self._collector_thread.start()
        self._running.set()

    @property
    def is_running(self): return self._running.is_set()

    def stop(self):
        self._terminate.set()
        self._collector_thread.join()
