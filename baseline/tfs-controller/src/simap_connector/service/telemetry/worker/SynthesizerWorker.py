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


import math, threading, time
from typing import Optional
from simap_connector.service.simap_updater.SimapClient import SimapClient
from .data.Resources import Resources
from ._Worker import _Worker, WorkerTypeEnum


WAIT_LOOP_GRANULARITY = 0.5


class SynthesizerWorker(_Worker):
    def __init__(
        self, worker_name : str, simap_client : SimapClient, resources : Resources,
        sampling_interval : float, terminate : Optional[threading.Event] = None
    ) -> None:
        super().__init__(WorkerTypeEnum.SYNTHESIZER, worker_name, terminate=terminate)
        self._lock = threading.Lock()
        self._simap_client = simap_client
        self._resources = resources
        self._sampling_interval = sampling_interval

    def change_resources(self, bandwidth_factor : float, latency_factor : float) -> None:
        with self._lock:
            for link in self._resources.links:
                link.bandwidth_utilization_sampler.offset *= bandwidth_factor
                link.latency_sampler.offset *= latency_factor

    def run(self) -> None:
        self._logger.info('[run] Starting...')

        try:
            while not self._stop_event.is_set() and not self._terminate.is_set():
                #self._logger.debug('[run] Sampling...')

                with self._lock:
                    self._resources.generate_samples(self._simap_client)

                # Make wait responsible to terminations
                iterations = int(math.ceil(self._sampling_interval / WAIT_LOOP_GRANULARITY))
                for _ in range(iterations):
                    if self._stop_event.is_set(): break
                    if self._terminate.is_set() : break
                    time.sleep(WAIT_LOOP_GRANULARITY)

        except Exception:
            self._logger.exception('[run] Unhandled Exception')
        finally:
            self._logger.info('[run] Terminated')
