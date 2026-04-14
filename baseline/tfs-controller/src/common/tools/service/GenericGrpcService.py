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
from concurrent import futures
from typing import Any, List, Optional, Union
from grpc_health.v1.health import HealthServicer, OVERALL_HEALTH
from grpc_health.v1.health_pb2 import HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import add_HealthServicer_to_server
from grpc_reflection.v1alpha import reflection
from common.Settings import get_grpc_bind_address, get_grpc_grace_period, get_grpc_max_workers

class GenericGrpcService:
    def __init__(
        self, bind_port : Union[str, int], bind_address : Optional[str] = None,
        max_workers : Optional[int] = None, grace_period : Optional[int] = None,
        enable_health_servicer : bool = True, enable_reflection : bool = True,
        cls_name : str = __name__
    ) -> None:
        self.logger = logging.getLogger(cls_name)
        self.bind_port = bind_port
        self.bind_address = get_grpc_bind_address() if bind_address is None else bind_address
        self.max_workers = get_grpc_max_workers() if max_workers is None else max_workers
        self.grace_period = get_grpc_grace_period() if grace_period is None else grace_period
        self.enable_health_servicer = enable_health_servicer
        self.enable_reflection = enable_reflection
        self.reflection_service_names : List[str] = [reflection.SERVICE_NAME]
        self.endpoint = None
        self.health_servicer = None
        self.pool = None
        self.server = None

    def install_servicers(self):
        pass

    def add_reflection_service_name(self, service_descriptor : Any, service_name : str):
        self.reflection_service_names.append(
            service_descriptor.services_by_name[service_name].full_name
        )

    def start(self):
        self.endpoint = '{:s}:{:s}'.format(str(self.bind_address), str(self.bind_port))
        self.logger.info('Starting Service (tentative endpoint: {:s}, max_workers: {:s})...'.format(
            str(self.endpoint), str(self.max_workers)))

        self.pool = futures.ThreadPoolExecutor(max_workers=self.max_workers)
        self.server = grpc.server(self.pool) # , interceptors=(tracer_interceptor,))

        self.install_servicers()

        if self.enable_health_servicer:
            self.health_servicer = HealthServicer(
                experimental_non_blocking=True, experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=1))
            add_HealthServicer_to_server(self.health_servicer, self.server)

        if self.enable_reflection:
            reflection.enable_server_reflection(self.reflection_service_names, self.server)

        self.bind_port = self.server.add_insecure_port(self.endpoint)
        self.endpoint = '{:s}:{:s}'.format(str(self.bind_address), str(self.bind_port))
        self.logger.info('Listening on {:s}...'.format(str(self.endpoint)))
        self.server.start()
        if self.enable_health_servicer:
            self.health_servicer.set(OVERALL_HEALTH, HealthCheckResponse.SERVING) # pylint: disable=maybe-no-member

        self.logger.debug('Service started')

    def stop(self):
        self.logger.debug('Stopping service (grace period {:s} seconds)...'.format(str(self.grace_period)))
        if self.enable_health_servicer:
            self.health_servicer.enter_graceful_shutdown()
        self.server.stop(self.grace_period)
        self.logger.debug('Service stopped')
