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

import copy, logging, pytz, random, threading
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from typing import Dict, Optional
from common.method_wrappers.Decorator import MetricsPool
from common.proto.context_pb2 import Service, ServiceId, Slice, SliceId
from common.tools.grpc.Tools import grpc_message_to_json_string
from service.client.ServiceClient import ServiceClient
from slice.client.SliceClient import SliceClient
from .DltTools import explore_entities_to_record, record_entities
from .Parameters import Parameters
from .RequestGenerator import RequestGenerator

logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
logging.getLogger('apscheduler.scheduler').setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('LoadGen', 'Requests', labels={
    'request_type': ''
})

class RequestScheduler:
    def __init__(
        self, parameters : Parameters, generator : RequestGenerator, scheduler_class=BlockingScheduler
    ) -> None:
        self._scheduler = scheduler_class()
        self._scheduler.configure(
            jobstores = {'default': MemoryJobStore()},
            executors = {'default': ThreadPoolExecutor(max_workers=parameters.max_workers)},
            job_defaults = {
                'coalesce': False,
                'max_instances': 100,
                'misfire_grace_time': 120,
            },
            timezone=pytz.utc)
        self._parameters = parameters
        self._generator = generator
        self._running = threading.Event()

    @property
    def num_generated(self): return min(self._generator.num_generated, self._parameters.num_requests)

    @property
    def num_released(self): return min(self._generator.num_released, self._parameters.num_requests)

    @property
    def infinite_loop(self): return self._generator.infinite_loop

    @property
    def running(self): return self._running.is_set()

    def _schedule_request_setup(self) -> None:
        iat = random.expovariate(1.0 / self._parameters.inter_arrival_time)
        run_date = datetime.utcnow() + timedelta(seconds=iat)
        self._scheduler.add_job(
            self._request_setup, trigger='date', run_date=run_date, timezone=pytz.utc)

    def _schedule_request_teardown(self, request : Dict, request_type : str) -> None:
        ht  = random.expovariate(1.0 / self._parameters.holding_time)
        run_date = datetime.utcnow() + timedelta(seconds=ht)
        args = (request, request_type)
        self._scheduler.add_job(
            self._request_teardown, args=args, trigger='date', run_date=run_date, timezone=pytz.utc)

    def start(self):
        self._running.set()
        self._schedule_request_setup()
        self._scheduler.start()

    def stop(self):
        self._scheduler.shutdown()
        self._running.clear()

    def _request_setup(self) -> None:
        completed, request, request_type = self._generator.compose_request()
        if completed:
            LOGGER.info('Generation Done!')
            #self._scheduler.shutdown()
            self._running.clear()
            return
        else:
            self._schedule_request_setup()

        if request is None:
            LOGGER.warning('No resources available to compose new request')
            metrics = METRICS_POOL.get_metrics_loadgen('setup', labels={'request_type': request_type})
            _, _, _, _, counter_blocked = metrics
            counter_blocked.inc()
            return

        if 'service_id' in request:
            service_uuid = request['service_id']['service_uuid']['uuid']
            src_device_uuid = request['service_endpoint_ids'][0]['device_id']['device_uuid']['uuid']
            src_endpoint_uuid = request['service_endpoint_ids'][0]['endpoint_uuid']['uuid']
            dst_device_uuid = request['service_endpoint_ids'][1]['device_id']['device_uuid']['uuid']
            dst_endpoint_uuid = request['service_endpoint_ids'][1]['endpoint_uuid']['uuid']
            LOGGER.info('Setup Service: uuid=%s src=%s:%s dst=%s:%s',
                service_uuid, src_device_uuid, src_endpoint_uuid, dst_device_uuid, dst_endpoint_uuid)
            self._create_update(request_type, service=request)

        elif 'slice_id' in request:
            slice_uuid = request['slice_id']['slice_uuid']['uuid']
            src_device_uuid = request['slice_endpoint_ids'][0]['device_id']['device_uuid']['uuid']
            src_endpoint_uuid = request['slice_endpoint_ids'][0]['endpoint_uuid']['uuid']
            dst_device_uuid = request['slice_endpoint_ids'][1]['device_id']['device_uuid']['uuid']
            dst_endpoint_uuid = request['slice_endpoint_ids'][1]['endpoint_uuid']['uuid']
            LOGGER.info('Setup Slice: uuid=%s src=%s:%s dst=%s:%s',
                slice_uuid, src_device_uuid, src_endpoint_uuid, dst_device_uuid, dst_endpoint_uuid)
            self._create_update(request_type, slice_=request)

        if self._parameters.do_teardown:
            self._schedule_request_teardown(request, request_type)

    def _request_teardown(self, request : Dict, request_type : str) -> None:
        if 'service_id' in request:
            service_uuid = request['service_id']['service_uuid']['uuid']
            src_device_uuid = request['service_endpoint_ids'][0]['device_id']['device_uuid']['uuid']
            src_endpoint_uuid = request['service_endpoint_ids'][0]['endpoint_uuid']['uuid']
            dst_device_uuid = request['service_endpoint_ids'][1]['device_id']['device_uuid']['uuid']
            dst_endpoint_uuid = request['service_endpoint_ids'][1]['endpoint_uuid']['uuid']
            LOGGER.info('Teardown Service: uuid=%s src=%s:%s dst=%s:%s',
                service_uuid, src_device_uuid, src_endpoint_uuid, dst_device_uuid, dst_endpoint_uuid)
            self._delete(request_type, service_id=ServiceId(**(request['service_id'])))

        elif 'slice_id' in request:
            slice_uuid = request['slice_id']['slice_uuid']['uuid']
            src_device_uuid = request['slice_endpoint_ids'][0]['device_id']['device_uuid']['uuid']
            src_endpoint_uuid = request['slice_endpoint_ids'][0]['endpoint_uuid']['uuid']
            dst_device_uuid = request['slice_endpoint_ids'][1]['device_id']['device_uuid']['uuid']
            dst_endpoint_uuid = request['slice_endpoint_ids'][1]['endpoint_uuid']['uuid']
            LOGGER.info('Teardown Slice: uuid=%s src=%s:%s dst=%s:%s',
                slice_uuid, src_device_uuid, src_endpoint_uuid, dst_device_uuid, dst_endpoint_uuid)
            self._delete(request_type, slice_id=SliceId(**(request['slice_id'])))

        self._generator.release_request(request)

    def _create_update(
        self, request_type : str, service : Optional[Dict] = None, slice_ : Optional[Dict] = None
    ) -> None:
        if self._parameters.dry_mode: return

        metrics = METRICS_POOL.get_metrics_loadgen('setup', labels={'request_type': request_type})
        histogram_duration, counter_started, counter_completed, counter_failed, _ = metrics

        service_id = None
        if service is not None:
            service_client = ServiceClient()

            service_add = copy.deepcopy(service)
            service_add['service_endpoint_ids'] = []
            service_add['service_constraints'] = []
            service_add['service_config'] = {'config_rules': []}
            service_add = Service(**service_add)
            service = Service(**service)

            with histogram_duration.time():
                try:
                    counter_started.inc()
                    service_id = service_client.CreateService(service_add)
                    service_id = service_client.UpdateService(service)
                    counter_completed.inc()
                except: # pylint: disable=bare-except
                    counter_failed.inc()
                    MSG = 'Exception Setting Up Service {:s}'
                    LOGGER.exception(MSG.format(grpc_message_to_json_string(service)))

            service_client.close()

        slice_id = None
        if slice_ is not None:
            slice_client = SliceClient()

            slice_add = copy.deepcopy(slice_)
            slice_add['slice_endpoint_ids'] = []
            slice_add['slice_constraints'] = []
            slice_add['slice_config'] = {'config_rules': []}
            slice_add = Slice(**slice_add)
            slice_ = Slice(**slice_)

            with histogram_duration.time():
                try:
                    counter_started.inc()
                    slice_id = slice_client.CreateSlice(slice_add)
                    slice_id = slice_client.UpdateSlice(slice_)
                    counter_completed.inc()
                except: # pylint: disable=bare-except
                    counter_failed.inc()
                    MSG = 'Exception Setting Up Slice {:s}'
                    LOGGER.exception(MSG.format(grpc_message_to_json_string(slice_)))

            slice_client.close()

        if self._parameters.record_to_dlt:
            entities_to_record = explore_entities_to_record(slice_id=slice_id, service_id=service_id)
            slices_to_record, services_to_record, devices_to_record = entities_to_record
            record_entities(
                slices_to_record=slices_to_record, services_to_record=services_to_record,
                devices_to_record=devices_to_record, delete=False)

    def _delete(
        self, request_type : str, service_id : Optional[ServiceId] = None, slice_id : Optional[SliceId] = None
    ) -> None:
        if self._parameters.dry_mode: return

        metrics = METRICS_POOL.get_metrics_loadgen('teardown', labels={'request_type': request_type})
        histogram_duration, counter_started, counter_completed, counter_failed, _ = metrics

        if self._parameters.record_to_dlt:
            entities_to_record = explore_entities_to_record(slice_id=slice_id, service_id=service_id)
            slices_to_record, services_to_record, devices_to_record = entities_to_record

        if service_id is not None:
            service_client = ServiceClient()

            with histogram_duration.time():
                try:
                    counter_started.inc()
                    service_client.DeleteService(service_id)
                    counter_completed.inc()
                except: # pylint: disable=bare-except
                    counter_failed.inc()
                    MSG = 'Exception Tearing Down Service {:s}'
                    LOGGER.exception(MSG.format(grpc_message_to_json_string(service_id)))

            service_client.close()

        if slice_id is not None:
            slice_client = SliceClient()

            with histogram_duration.time():
                try:
                    counter_started.inc()
                    slice_client.DeleteSlice(slice_id)
                    counter_completed.inc()
                except: # pylint: disable=bare-except
                    counter_failed.inc()
                    MSG = 'Exception Tearing Down Slice {:s}'
                    LOGGER.exception(MSG.format(grpc_message_to_json_string(slice_id)))

            slice_client.close()

        if self._parameters.record_to_dlt:
            record_entities(
                slices_to_record=slices_to_record, services_to_record=services_to_record,
                devices_to_record=devices_to_record, delete=True)
