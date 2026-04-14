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
from enum import Enum
from typing import Optional


class WorkerTypeEnum(Enum):
    AGGREGATOR  = 'aggregator'
    COLLECTOR   = 'collector'
    SYNTHESIZER = 'synthesizer'


def get_worker_key(worker_type : WorkerTypeEnum, worker_name : str) -> str:
    return '{:s}-{:s}'.format(worker_type.value, worker_name)


class _Worker(threading.Thread):
    def __init__(
        self, worker_type : WorkerTypeEnum, worker_name : str,
        terminate : Optional[threading.Event] = None
    ) -> None:
        self._worker_type = worker_type
        self._worker_name = worker_name
        self._worker_key = get_worker_key(worker_type, worker_name)
        name = 'TelemetryWorker({:s})'.format(self._worker_key)
        super().__init__(name=name, daemon=True)
        self._logger = logging.getLogger(name)
        self._stop_event = threading.Event()
        self._terminate = threading.Event() if terminate is None else terminate

    @property
    def worker_type(self) -> WorkerTypeEnum: return self._worker_type

    @property
    def worker_name(self) -> str: return self._worker_name

    @property
    def worker_key(self) -> str: return self._worker_key

    def stop(self) -> None:
        self._logger.info('[stop] Stopping...')
        self._stop_event.set()
        self.join()
