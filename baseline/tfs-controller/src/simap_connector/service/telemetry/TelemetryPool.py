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
from typing import Dict, Optional
from simap_connector.service.simap_updater.SimapClient import SimapClient
from .worker.data.Resources import Resources
from .worker.data.AggregationCache import AggregationCache
from .worker._Worker import _Worker, WorkerTypeEnum, get_worker_key
from .worker.AggregatorWorker import AggregatorWorker
from .worker.CollectorWorker import CollectorWorker
from .worker.SynthesizerWorker import SynthesizerWorker


LOGGER = logging.getLogger(__name__)


WORKER_CLASSES = {
    WorkerTypeEnum.AGGREGATOR : AggregatorWorker,
    WorkerTypeEnum.COLLECTOR  : CollectorWorker,
    WorkerTypeEnum.SYNTHESIZER: SynthesizerWorker,
}


class TelemetryPool:
    def __init__(
        self, simap_client : SimapClient, terminate : Optional[threading.Event] = None
    ) -> None:
        self._simap_client = simap_client
        self._workers  : Dict[str, _Worker] = dict()
        self._lock = threading.Lock()
        self._terminate = threading.Event() if terminate is None else terminate


    def has_worker(self, worker_type : WorkerTypeEnum, worker_name : str) -> bool:
        worker_key = get_worker_key(worker_type, worker_name)
        return self.has_worker_by_key(worker_key)


    def has_worker_by_key(self, worker_key : str) -> bool:
        with self._lock:
            return worker_key in self._workers


    def get_worker(self, worker_type : WorkerTypeEnum, worker_name : str) -> Optional[_Worker]:
        worker_key = get_worker_key(worker_type, worker_name)
        return self.get_worker_by_key(worker_key)


    def get_worker_by_key(self, worker_key : str) -> Optional[_Worker]:
        with self._lock:
            return self._workers.get(worker_key)


    def start_aggregator(
        self, worker_name : str, network_id : str, link_id : str, parent_subscription_id : int,
        aggregation_cache : AggregationCache, topic : str, sampling_interval : float
    ) -> None:
        self._start_worker(
            WorkerTypeEnum.AGGREGATOR, worker_name, self._simap_client, network_id, link_id,
            parent_subscription_id, aggregation_cache, topic, sampling_interval
        )


    def start_collector(
        self, worker_name : str, controller_uuid : Optional[str], network_id : str, link_id : str,
        target_uri : str, aggregation_cache : AggregationCache, sampling_interval : float
    ) -> None:
        self._start_worker(
            WorkerTypeEnum.COLLECTOR, worker_name, controller_uuid, network_id, link_id,
            target_uri, aggregation_cache, sampling_interval
        )


    def start_synthesizer(
        self, worker_name : str, resources : Resources, sampling_interval : float
    ) -> None:
        self._start_worker(
            WorkerTypeEnum.SYNTHESIZER, worker_name, self._simap_client, resources,
            sampling_interval
        )


    def _start_worker(
        self, worker_type : WorkerTypeEnum, worker_name : str, *args, **kwargs
    ) -> None:
        worker_key = get_worker_key(worker_type, worker_name)
        with self._lock:
            if worker_key in self._workers:
                MSG = '[start_worker] Worker({:s}) already exists'
                LOGGER.debug(MSG.format(str(worker_key)))
                return

            worker_class = WORKER_CLASSES.get(worker_type)
            if worker_class is None:
                MSG = 'Unsupported WorkerType({:s})'
                raise Exception(MSG.format(str(worker_type)))

            worker : _Worker = worker_class(
                worker_name, *args, terminate=self._terminate, **kwargs
            )
            worker.start()

            MSG = '[start_worker] Started Worker({:s})'
            LOGGER.info(MSG.format(str(worker_key)))

            self._workers[worker_key] = worker


    def stop_worker(self, worker_type : WorkerTypeEnum, worker_name : str) -> None:
        worker_key = get_worker_key(worker_type, worker_name)
        self.stop_worker_by_key(worker_key)


    def stop_worker_by_key(self, worker_key : str) -> None:
        with self._lock:
            worker = self._workers.pop(worker_key, None)

        if worker is None:
            MSG = '[stop_worker] Worker({:s}) not found'
            LOGGER.debug(MSG.format(str(worker_key)))
            return

        worker.stop()

        MSG = '[stop_worker] Stopped Worker({:s})'
        LOGGER.info(MSG.format(str(worker_key)))


    def stop_all(self) -> None:
        LOGGER.info('[stop_all] Stopping all workers')

        with self._lock:
            worker_keys = list(self._workers.keys())

        for worker_key in worker_keys:
            try:
                self.stop_worker_by_key(worker_key)
            except Exception:
                MSG = '[stop_all] Unhandled Exception stopping Worker({:s})'
                LOGGER.exception(MSG.format(str(worker_key)))
