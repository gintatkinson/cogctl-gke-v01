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

import grpc
from sklearn.cluster import DBSCAN

from common.method_wrappers.Decorator import (MetricsPool,
                                              safe_and_metered_rpc_method)
from common.proto.dbscanserving_pb2 import DetectionRequest, DetectionResponse
from common.proto.dbscanserving_pb2_grpc import DetectorServicer

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool("DBSCANServing", "RPC")


class DbscanServiceServicerImpl(DetectorServicer):
    def __init__(self):
        LOGGER.debug("Creating Servicer...")
        LOGGER.debug("Servicer Created")

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def Detect(
        self, request: DetectionRequest, context: grpc.ServicerContext
    ) -> DetectionResponse:
        if request.num_samples != len(request.samples):
            context.set_details(
                f"The sample dimension declared ({request.num_samples}) does not match with the number of samples received ({len(request.samples)})."
            )
            LOGGER.debug(
                f"The sample dimension declared does not match with the number of samples received. Declared: {request.num_samples} - Received: {len(request.samples)}"
            )
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return DetectionResponse()
        # TODO: implement the validation of the features dimension
        clusters = DBSCAN(eps=request.eps, min_samples=request.min_samples).fit_predict(
            [[x for x in sample.features] for sample in request.samples]
        )
        response = DetectionResponse()
        for cluster in clusters:
            response.cluster_indices.append(cluster)
        return response
