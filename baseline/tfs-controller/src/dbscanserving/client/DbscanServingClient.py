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

import logging
from typing import Counter

import grpc

from common.Constants import ServiceNameEnum
from common.proto.dbscanserving_pb2 import DetectionRequest, DetectionResponse
from common.proto.dbscanserving_pb2_grpc import DetectorStub
from common.Settings import get_service_host, get_service_port_grpc
from common.tools.client.RetryDecorator import delay_exponential, retry

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(
    max_retries=MAX_RETRIES,
    delay_function=DELAY_FUNCTION,
    prepare_method_name="connect",
)


class DbscanServingClient:
    def __init__(self, host=None, port=None):
        if not host:
            host = get_service_host(ServiceNameEnum.DBSCANSERVING)
        if not port:
            port = get_service_port_grpc(ServiceNameEnum.DBSCANSERVING)

        self.endpoint = "{:s}:{:s}".format(str(host), str(port))
        LOGGER.debug("Creating channel to {:s}...".format(str(self.endpoint)))
        self.channel = None
        self.stub = None
        self.connect()
        LOGGER.debug("Channel created")

    def connect(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = DetectorStub(self.channel)

    def close(self):
        if self.channel is not None:
            self.channel.close()
        self.channel = None
        self.stub = None

    @RETRY_DECORATOR
    def Detect(self, request: DetectionRequest) -> DetectionResponse:
        LOGGER.debug(
            "Detect request with {} samples and {} features".format(
                request.num_samples, request.num_features
            )
        )
        response: DetectionResponse = self.stub.Detect(request)
        LOGGER.debug(
            "Detect result with {} cluster indices [{}]".format(
                len(response.cluster_indices), Counter(response.cluster_indices)
            )
        )
        return response
