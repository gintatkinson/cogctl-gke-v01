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
import os
import random
from unittest.mock import patch

import pytest

from common.proto.dbscanserving_pb2 import (DetectionRequest,
                                            DetectionResponse, Sample)

from dbscanserving.client.DbscanServingClient import DbscanServingClient
from dbscanserving.service.DbscanService import DbscanService

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


@pytest.fixture(scope="session")
def dbscanserving_service():
    _service = DbscanService()
    _service.start()
    yield _service
    _service.stop()


@pytest.fixture(scope="session")
def dbscanserving_client(dbscanserving_service: DbscanService):
    with patch.dict(
        os.environ,
        {
            "DBSCANSERVINGSERVICE_SERVICE_HOST": "127.0.0.1",
            "DBSCANSERVINGSERVICE_SERVICE_PORT_GRPC": str(dbscanserving_service.bind_port),
        },
        clear=True,
    ):
        _client = DbscanServingClient()
        yield _client
    _client.close()


def test_detection_correct(
    dbscanserving_service, dbscanserving_client: DbscanServingClient
):
    request: DetectionRequest = DetectionRequest()

    request.num_samples = 310
    request.num_features = 100
    request.eps = 100.5
    request.min_samples = 50

    for _ in range(200):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(0.0, 10.0))
        request.samples.append(grpc_sample)

    for _ in range(100):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(50.0, 60.0))
        request.samples.append(grpc_sample)

    for _ in range(10):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(5000.0, 6000.0))
        request.samples.append(grpc_sample)

    response: DetectionResponse = dbscanserving_client.Detect(request)
    assert len(response.cluster_indices) == 310


def test_detection_incorrect(
    dbscanserving_service, dbscanserving_client: DbscanServingClient
):
    request: DetectionRequest = DetectionRequest()

    request.num_samples = 210
    request.num_features = 100
    request.eps = 100.5
    request.min_samples = 50

    for _ in range(200):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(0.0, 10.0))
        request.samples.append(grpc_sample)

    for _ in range(100):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(50.0, 60.0))
        request.samples.append(grpc_sample)

    for _ in range(10):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(5000.0, 6000.0))
        request.samples.append(grpc_sample)

    with pytest.raises(Exception):
        _: DetectionResponse = dbscanserving_client.Detect(request)


def test_detection_clusters(
    dbscanserving_service, dbscanserving_client: DbscanServingClient
):
    request: DetectionRequest = DetectionRequest()

    request.num_samples = 310
    request.num_features = 100
    request.eps = 100.5
    request.min_samples = 50

    for _ in range(200):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(0.0, 10.0))
        request.samples.append(grpc_sample)

    for _ in range(100):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(50.0, 60.0))
        request.samples.append(grpc_sample)

    for _ in range(10):
        grpc_sample = Sample()
        for __ in range(100):
            grpc_sample.features.append(random.uniform(5000.0, 6000.0))
        request.samples.append(grpc_sample)

    response: DetectionResponse = dbscanserving_client.Detect(request)
    for v in response.cluster_indices[:200]:
        assert v == 0
    for v in response.cluster_indices[200:300]:
        assert v == 1
    for v in response.cluster_indices[300:]:
        assert v == -1
