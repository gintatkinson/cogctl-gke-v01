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

import grpc
import logging
from concurrent import futures
from grpc_health.v1.health import HealthServicer, OVERALL_HEALTH
from grpc_health.v1.health_pb2 import HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import add_HealthServicer_to_server
from common.proto.l3_attackmitigator_pb2_grpc import (
    add_L3AttackmitigatorServicer_to_server,
)
from l3_attackmitigator.service.l3_attackmitigatorServiceServicerImpl import (
    l3_attackmitigatorServiceServicerImpl,
)
from l3_attackmitigator.Config import (
    GRPC_SERVICE_PORT,
    GRPC_MAX_WORKERS,
    GRPC_GRACE_PERIOD,
)

BIND_ADDRESS = "0.0.0.0"
LOGGER = logging.getLogger(__name__)


class l3_attackmitigatorService:
    def __init__(
        self,
        address=BIND_ADDRESS,
        port=GRPC_SERVICE_PORT,
        max_workers=GRPC_MAX_WORKERS,
        grace_period=GRPC_GRACE_PERIOD,
    ):
        self.address = address
        self.port = port
        self.endpoint = None
        self.max_workers = max_workers
        self.grace_period = grace_period
        self.l3_attackmitigator_servicer = None
        self.health_servicer = None
        self.pool = None
        self.server = None

    def start(self):
        self.endpoint = "{}:{}".format(self.address, self.port)
        LOGGER.debug(
            "Starting Service (tentative endpoint: {}, max_workers: {})...".format(
                self.endpoint, self.max_workers
            )
        )

        self.pool = futures.ThreadPoolExecutor(max_workers=self.max_workers)
        self.server = grpc.server(self.pool)  # , interceptors=(tracer_interceptor,))

        self.l3_attackmitigator_servicer = (
            l3_attackmitigatorServiceServicerImpl()
        )
        add_L3AttackmitigatorServicer_to_server(
            self.l3_attackmitigator_servicer, self.server
        )

        self.health_servicer = HealthServicer(
            experimental_non_blocking=True,
            experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=1),
        )
        add_HealthServicer_to_server(self.health_servicer, self.server)

        port = self.server.add_insecure_port(self.endpoint)
        self.endpoint = "{}:{}".format(self.address, port)
        LOGGER.info("Listening on {}...".format(self.endpoint))
        self.server.start()
        self.health_servicer.set(
            OVERALL_HEALTH, HealthCheckResponse.SERVING
        )  # pylint: disable=maybe-no-member

        LOGGER.debug("Service started")
        #print('Setting up')
        #self.l3_attackmitigator_servicer.setupl3_attackmitigator()

    def stop(self):
        LOGGER.debug(
            "Stopping service (grace period {} seconds)...".format(self.grace_period)
        )
        self.health_servicer.enter_graceful_shutdown()
        self.server.stop(self.grace_period)
        LOGGER.debug("Service stopped")
