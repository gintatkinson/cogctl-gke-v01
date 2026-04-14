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

import grpc, logging
from typing import Optional
from apscheduler.schedulers.background import BackgroundScheduler
from common.proto.context_pb2 import Empty
from common.proto.load_generator_pb2 import Parameters, Status
from common.proto.load_generator_pb2_grpc import LoadGeneratorServiceServicer
from load_generator.load_gen.Parameters import Parameters as LoadGen_Parameters
from load_generator.load_gen.RequestGenerator import RequestGenerator
from load_generator.load_gen.RequestScheduler import RequestScheduler
from load_generator.tools.ListScalarRange import list_scalar_range__grpc_to_list, list_scalar_range__list_to_grpc
from .Constants import REQUEST_TYPE_MAP, REQUEST_TYPE_REVERSE_MAP

LOGGER = logging.getLogger(__name__)

class LoadGeneratorServiceServicerImpl(LoadGeneratorServiceServicer):
    def __init__(self):
        LOGGER.debug('Creating Servicer...')
        self._generator : Optional[RequestGenerator] = None
        self._scheduler : Optional[RequestScheduler] = None
        LOGGER.debug('Servicer Created')

    def Start(self, request : Parameters, context : grpc.ServicerContext) -> Empty:
        self._parameters = LoadGen_Parameters(
            num_requests          = request.num_requests,
            request_types         = [REQUEST_TYPE_MAP[rt] for rt in request.request_types],
            device_regex          = request.device_regex,
            endpoint_regex        = request.endpoint_regex,
            offered_load          = request.offered_load if request.offered_load > 1.e-12 else None,
            holding_time          = request.holding_time if request.holding_time > 1.e-12 else None,
            inter_arrival_time    = request.inter_arrival_time if request.inter_arrival_time > 1.e-12 else None,
            availability_ranges   = list_scalar_range__grpc_to_list(request.availability  ),
            capacity_gbps_ranges  = list_scalar_range__grpc_to_list(request.capacity_gbps ),
            e2e_latency_ms_ranges = list_scalar_range__grpc_to_list(request.e2e_latency_ms),
            max_workers           = request.max_workers,
            do_teardown           = request.do_teardown,   # if set, schedule tear down of requests
            dry_mode              = request.dry_mode,      # in dry mode, no request is sent to TeraFlowSDN
            record_to_dlt         = request.record_to_dlt, # if set, upload changes to DLT
            dlt_domain_id         = request.dlt_domain_id, # domain used to uploaded entities (when record_to_dlt = True)
        )

        LOGGER.info('Initializing Generator...')
        self._generator = RequestGenerator(self._parameters)
        self._generator.initialize()

        LOGGER.info('Running Schedule...')
        self._scheduler = RequestScheduler(self._parameters, self._generator, scheduler_class=BackgroundScheduler)
        self._scheduler.start()
        return Empty()

    def GetStatus(self, request : Empty, context : grpc.ServicerContext) -> Status:
        if self._scheduler is None:
            # not started
            status = Status()
            status.num_generated = 0
            status.infinite_loop = False
            status.running       = False
            return status

        params = self._scheduler._parameters
        request_types = [REQUEST_TYPE_REVERSE_MAP[rt] for rt in params.request_types]

        status = Status()
        status.num_generated = self._scheduler.num_generated
        status.num_released  = self._scheduler.num_released
        status.infinite_loop = self._scheduler.infinite_loop
        status.running       = self._scheduler.running

        stat_pars = status.parameters                               # pylint: disable=no-member
        stat_pars.num_requests       = params.num_requests          # pylint: disable=no-member
        stat_pars.device_regex       = params.device_regex          # pylint: disable=no-member
        stat_pars.endpoint_regex     = params.endpoint_regex        # pylint: disable=no-member
        stat_pars.offered_load       = params.offered_load          # pylint: disable=no-member
        stat_pars.holding_time       = params.holding_time          # pylint: disable=no-member
        stat_pars.inter_arrival_time = params.inter_arrival_time    # pylint: disable=no-member
        stat_pars.max_workers        = params.max_workers           # pylint: disable=no-member
        stat_pars.do_teardown        = params.do_teardown           # pylint: disable=no-member
        stat_pars.dry_mode           = params.dry_mode              # pylint: disable=no-member
        stat_pars.record_to_dlt      = params.record_to_dlt         # pylint: disable=no-member
        stat_pars.dlt_domain_id      = params.dlt_domain_id         # pylint: disable=no-member
        stat_pars.request_types.extend(request_types)               # pylint: disable=no-member

        list_scalar_range__list_to_grpc(params.availability_ranges,   stat_pars.availability  ) # pylint: disable=no-member
        list_scalar_range__list_to_grpc(params.capacity_gbps_ranges,  stat_pars.capacity_gbps ) # pylint: disable=no-member
        list_scalar_range__list_to_grpc(params.e2e_latency_ms_ranges, stat_pars.e2e_latency_ms) # pylint: disable=no-member

        return status

    def Stop(self, request : Empty, context : grpc.ServicerContext) -> Empty:
        if self._scheduler is not None:
            self._scheduler.stop()
        return Empty()
