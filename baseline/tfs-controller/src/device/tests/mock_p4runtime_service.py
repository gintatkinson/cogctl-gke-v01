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

"""
A mock P4Runtime server.
"""

import logging
from concurrent import futures
import grpc
from p4.v1 import p4runtime_pb2_grpc

from .device_p4 import(
    DEVICE_P4_IP_ADDR, DEVICE_P4_PORT,
    DEVICE_P4_WORKERS, DEVICE_P4_GRACE_PERIOD)
from .mock_p4runtime_servicer_impl import MockP4RuntimeServicerImpl

LOGGER = logging.getLogger(__name__)


class MockP4RuntimeService:
    """
    P4Runtime server for testing purposes.
    """

    def __init__(
            self, address=DEVICE_P4_IP_ADDR, port=DEVICE_P4_PORT,
            max_workers=DEVICE_P4_WORKERS,
            grace_period=DEVICE_P4_GRACE_PERIOD):
        self.address = address
        self.port = port
        self.endpoint = f'{self.address}:{self.port}'
        self.max_workers = max_workers
        self.grace_period = grace_period
        self.server = None
        self.servicer = None

    def start(self):
        """
        Start the P4Runtime server.
        """

        LOGGER.info(
            'Starting P4Runtime service on %s with max_workers: %s',
            str(self.endpoint), str(self.max_workers))

        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=self.max_workers))

        self.servicer = MockP4RuntimeServicerImpl()
        p4runtime_pb2_grpc.add_P4RuntimeServicer_to_server(
            self.servicer, self.server)

        _ = self.server.add_insecure_port(self.endpoint)
        LOGGER.info('Listening on %s...', str(self.endpoint))

        self.server.start()
        LOGGER.debug('P4Runtime service started')

    def stop(self):
        """
        Stop the P4Runtime server.
        """

        LOGGER.debug(
            'Stopping P4Runtime service (grace period %d seconds...',
            self.grace_period)
        self.server.stop(self.grace_period)
        LOGGER.debug('P4Runtime service stopped')
