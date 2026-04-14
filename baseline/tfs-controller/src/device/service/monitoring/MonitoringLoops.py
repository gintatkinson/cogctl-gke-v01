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

import copy, logging, queue, threading
from typing import Dict, Optional, Tuple, Union
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.monitoring_pb2 import Kpi
from monitoring.client.MonitoringClient import MonitoringClient
from ..driver_api._Driver import _Driver
from .MonitoringLoop import MonitoringLoop

LOGGER = logging.getLogger(__name__)

QUEUE_GET_WAIT_TIMEOUT = 0.5

def value_to_grpc(value : Union[bool, float, int, str]) -> Dict:
    if isinstance(value, int):
        kpi_value_field_name = 'int64Val'
        kpi_value_field_cast = int
    elif isinstance(value, float):
        kpi_value_field_name = 'floatVal'
        kpi_value_field_cast = float
    elif isinstance(value, bool):
        kpi_value_field_name = 'boolVal'
        kpi_value_field_cast = bool
    else:
        kpi_value_field_name = 'stringVal'
        kpi_value_field_cast = str

    return {kpi_value_field_name: kpi_value_field_cast(value)}

TYPE_TARGET_KEY = Tuple[str, str]               # (device_uuid, monitoring_resource_key)
TYPE_TARGET_KPI = Tuple[str, float, float]      # (kpi_uuid, sampling_duration, sampling_interval)
TYPE_KPI_DETAIL = Tuple[str, str, float, float] # (device_uuid, monitoring_resource_key,
                                                #  sampling_duration, sampling_interval)

class MonitoringLoops:
    def __init__(self) -> None:
        self._monitoring_client = MonitoringClient()
        self._samples_queue = queue.Queue()
        self._running = threading.Event()
        self._terminate = threading.Event()

        self._lock_device_endpoint = threading.Lock()
        self._device_endpoint_sampletype__to__resource_key : Dict[Tuple[str, str, int], str] = dict()

        self._lock_monitoring_loop = threading.Lock()
        self._device_uuid__to__monitoring_loop : Dict[str, MonitoringLoop] = dict()

        self._lock_kpis = threading.Lock()
        self._target_to_kpi : Dict[TYPE_TARGET_KEY, TYPE_TARGET_KPI] = dict()
        self._kpi_to_detail : Dict[str, TYPE_KPI_DETAIL] = dict()
        
        self._exporter_thread = threading.Thread(target=self._export, daemon=True)

    def add_device(self, device_uuid : str, driver : _Driver) -> None:
        with self._lock_monitoring_loop:
            monitoring_loop = self._device_uuid__to__monitoring_loop.get(device_uuid)
            if (monitoring_loop is not None) and monitoring_loop.is_running: return
            monitoring_loop = MonitoringLoop(device_uuid, driver, self._samples_queue)
            self._device_uuid__to__monitoring_loop[device_uuid] = monitoring_loop
            monitoring_loop.start()

    def remove_device(self, device_uuid : str) -> None:
        with self._lock_monitoring_loop:
            monitoring_loop = self._device_uuid__to__monitoring_loop.get(device_uuid)
            if monitoring_loop is None: return
            if monitoring_loop.is_running: monitoring_loop.stop()
            self._device_uuid__to__monitoring_loop.pop(device_uuid, None)

    def add_resource_key(
        self, device_uuid : str, endpoint_uuid : str, kpi_sample_type : KpiSampleType, resource_key : str
    ) -> None:
        with self._lock_device_endpoint:
            key = (device_uuid, endpoint_uuid, kpi_sample_type)
            self._device_endpoint_sampletype__to__resource_key[key] = resource_key

    def get_resource_key(
        self, device_uuid : str, endpoint_uuid : str, kpi_sample_type : KpiSampleType
    ) -> Optional[str]:
        with self._lock_device_endpoint:
            key = (device_uuid, endpoint_uuid, kpi_sample_type)
            return self._device_endpoint_sampletype__to__resource_key.get(key)

    def get_all_resource_keys(self) -> Dict[Tuple[str, str, int], str]:
        with self._lock_device_endpoint:
            return copy.deepcopy(self._device_endpoint_sampletype__to__resource_key)

    def remove_resource_key(
        self, device_uuid : str, endpoint_uuid : str, kpi_sample_type : KpiSampleType
    ) -> None:
        with self._lock_device_endpoint:
            key = (device_uuid, endpoint_uuid, kpi_sample_type)
            self._device_endpoint_sampletype__to__resource_key.pop(key, None)

    def add_kpi(
        self, device_uuid : str, monitoring_resource_key : str, kpi_uuid : str, sampling_duration : float,
        sampling_interval : float
    ) -> None:
        with self._lock_kpis:
            kpi_key = (device_uuid, monitoring_resource_key)
            kpi_values = (kpi_uuid, sampling_duration, sampling_interval)
            self._target_to_kpi[kpi_key] = kpi_values

            kpi_details = (device_uuid, monitoring_resource_key, sampling_duration, sampling_interval)
            self._kpi_to_detail[kpi_uuid] = kpi_details

    def get_kpi_by_uuid(self, kpi_uuid : str) -> Optional[TYPE_KPI_DETAIL]:
        with self._lock_kpis:
            return self._kpi_to_detail.get(kpi_uuid)

    def get_kpi_by_metric(
        self, device_uuid : str, monitoring_resource_key : str
    ) -> Optional[TYPE_TARGET_KPI]:
        with self._lock_kpis:
            kpi_key = (device_uuid, monitoring_resource_key)
            return self._target_to_kpi.get(kpi_key)

    def remove_kpi(self, kpi_uuid : str) -> None:
        with self._lock_kpis:
            kpi_details = self._kpi_to_detail.pop(kpi_uuid, None)
            if kpi_details is None: return
            kpi_key = kpi_details[0:2] # (device_uuid, monitoring_resource_key, _, _)
            self._target_to_kpi.pop(kpi_key, None)

    def start(self):
        self._exporter_thread.start()

    @property
    def is_running(self): return self._running.is_set()

    def stop(self):
        self._terminate.set()
        self._exporter_thread.join()

    def _export(self) -> None:
        self._running.set()
        while not self._terminate.is_set():
            try:
                sample = self._samples_queue.get(block=True, timeout=QUEUE_GET_WAIT_TIMEOUT)
                #LOGGER.debug('[MonitoringLoops:_export] sample={:s}'.format(str(sample)))
            except queue.Empty:
                continue

            device_uuid, timestamp, monitoring_resource_key, value = sample

            kpi_details = self.get_kpi_by_metric(device_uuid, monitoring_resource_key)
            if kpi_details is None:
                MSG = 'Kpi for Device({:s})/MonitoringResourceKey({:s}) not found'
                LOGGER.warning(MSG.format(str(device_uuid), str(monitoring_resource_key)))
                continue
            kpi_uuid,_,_ = kpi_details

            try:
                self._monitoring_client.IncludeKpi(Kpi(**{
                    'kpi_id'   : {'kpi_id': {'uuid': kpi_uuid}},
                    'timestamp': {'timestamp': timestamp},
                    'kpi_value': value_to_grpc(value),
                }))
            except: # pylint: disable=bare-except
                LOGGER.exception('Unable to format/send Kpi')

        self._running.clear()
