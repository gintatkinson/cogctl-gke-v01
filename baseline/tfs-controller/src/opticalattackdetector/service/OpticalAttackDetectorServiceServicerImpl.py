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
import pickle
import random

import grpc
import numpy as np
import redis
from prometheus_client import Histogram

from common.Constants import ServiceNameEnum
from common.method_wrappers.Decorator import (MetricsPool, MetricTypeEnum,
                                              safe_and_metered_rpc_method)
from common.proto import dbscanserving_pb2 as dbscan
from common.proto import optical_attack_detector_pb2 as oad
from common.proto.context_pb2 import Empty
from common.proto.monitoring_pb2 import Kpi
from common.proto.optical_attack_detector_pb2_grpc import \
    OpticalAttackDetectorServiceServicer
from common.proto.optical_attack_mitigator_pb2 import (AttackDescription,
                                                       AttackResponse)
from common.Settings import get_service_host, get_setting
from common.tools.timestamp.Converters import timestamp_utcnow_to_float
from dbscanserving.client.DbscanServingClient import DbscanServingClient
from monitoring.client.MonitoringClient import MonitoringClient
from opticalattackmitigator.client.OpticalAttackMitigatorClient import \
    OpticalAttackMitigatorClient

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool("OpticalAttackDetector", "RPC")

METRICS_POOL_DETAILS = MetricsPool(
    "OpticalAttackDetector",
    "execution",
    labels={
        "operation": "",
        "step": "",
    },
)

METRIC_LABELS = dict(operation="detect")
HISTOGRAM_DURATION: Histogram = METRICS_POOL_DETAILS.get_or_create(
    "details", MetricTypeEnum.HISTOGRAM_DURATION
)

monitoring_client: MonitoringClient = MonitoringClient()
dbscanserving_client: DbscanServingClient = DbscanServingClient()
attack_mitigator_client: OpticalAttackMitigatorClient = OpticalAttackMitigatorClient()

redis_host = get_service_host(ServiceNameEnum.CACHING)
r = None
if redis_host is not None:
    redis_port = int(get_setting("CACHINGSERVICE_SERVICE_PORT_REDIS", default=6379))
    redis_password = get_setting("REDIS_PASSWORD")

    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
    r.ping()

# detecting preloading of the stats
path = get_setting("PATH_OPM_INFORMATION_SUMMARY", default=None)
if path is not None and len(path) > 0:
    with open(path, "rb") as file:
        opm_information_stats = pickle.load(file)
        LOGGER.info("Using provided dataset: {}".format(path))
else:
    opm_information_stats = None

WAD_WINDOW = 20
WAD_SAMPLES = 9


class OpticalAttackDetectorServiceServicerImpl(OpticalAttackDetectorServiceServicer):
    def __init__(self):
        LOGGER.debug("Creating Servicer...")
        LOGGER.debug("Servicer Created")

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DetectAttack(
        self, request: oad.DetectionRequest, context: grpc.ServicerContext
    ) -> Empty:

        s_uuid = request.service_id.service_uuid.uuid

        # detect if specific configuration is required
        # to set the variable on the fly, try:
        # https://stackoverflow.com/questions/45050050/can-i-modify-containers-environment-variables-without-restarting-pod-using-kube
        _temp = r.get("CLASS_SERVICE_{}".format(s_uuid.replace("-", "_")))
        if _temp is not None and len(_temp) > 0:
            _class = int(_temp)
        else:  # if not, assume no attack is present
            _class = 0
        LOGGER.debug("Using class {} for service {}".format(_class, s_uuid))

        _temp = r.get("PREVIOUS_CLASS_SERVICE_{}".format(s_uuid.replace("-", "_")))
        if _temp is not None and int(_temp) != 0 and _class == 0:
            # if value changed to no-attack
            # reset the experiment
            r.delete("opm_{}".format(s_uuid.replace("-", "_")))
        r.set("PREVIOUS_CLASS_SERVICE_{}".format(s_uuid.replace("-", "_")), _class)

        # code used to validate resiliency against failures and timeouts
        # if random.random() > 0.5:
        #     time.sleep(10)

        # run attack detection for every service
        detection_request: dbscan.DetectionRequest = dbscan.DetectionRequest()
        detection_request.num_samples = 310
        detection_request.num_features = 11

        # checking if we have enough samples already for this service
        length = r.llen("opm_{}".format(s_uuid.replace("-", "_")))
        if length < detection_request.num_samples:
            # if the number of samples is not sufficient,
            # we insert new samples
            for _ in range(detection_request.num_samples - length):
                detection_sample = []
                if opm_information_stats is not None:
                    for col in range(1, len(opm_information_stats.columns), 2):
                        name = opm_information_stats.columns[col][0]
                        # [result.columns[x][0] for x in range(1, len(result.columns), 2)]
                        detection_sample.append(
                            np.random.normal(
                                loc=opm_information_stats[name]["mean"][_class],
                                scale=opm_information_stats[name]["std"][_class],
                            )
                        )
                else:
                    for __ in range(detection_request.num_features):
                        detection_sample.append(random.uniform(0.0, 10.0))
                # push the sample into the list
                r.rpush(
                    "opm_{}".format(s_uuid.replace("-", "_")),
                    pickle.dumps(tuple(detection_sample)),
                )

        # remove the oldest sample from the list
        r.lpop("opm_{}".format(s_uuid.replace("-", "_")))

        # generate the latest sample
        detection_sample = []
        if opm_information_stats is not None:

            for col in range(1, len(opm_information_stats.columns), 2):
                name = opm_information_stats.columns[col][0]
                # [result.columns[x][0] for x in range(1, len(result.columns), 2)]
                detection_sample.append(
                    np.random.normal(
                        loc=opm_information_stats[name]["mean"][_class],
                        scale=opm_information_stats[name]["std"][_class],
                    )
                )

            # generate data based on the stats based on the configuration of
            # https://dx.doi.org/10.1109/JLT.2020.2987032
            detection_request.eps = 1.0
            detection_request.min_samples = 5
        else:
            detection_request.eps = 100.5
            detection_request.min_samples = 5

            if _class == 0:
                for __ in range(detection_request.num_features):
                    detection_sample.append(random.uniform(0.0, 10.0))
            else:  # if not, assume no attack is present
                for __ in range(detection_request.num_features):
                    detection_sample.append(random.uniform(5000.0, 6000.0))

        # adding the sample to the cache and recovering the cache
        with HISTOGRAM_DURATION.labels(step="cachefetch", **METRIC_LABELS).time():
            r.rpush(
                "opm_{}".format(s_uuid.replace("-", "_")),
                pickle.dumps(tuple(detection_sample)),
            )
            cached_samples = r.lrange("opm_{}".format(s_uuid.replace("-", "_")), 0, -1)
            LOGGER.info(
                "Recovered {} samples from the cache".format(len(cached_samples))
            )

        for raw_sample in cached_samples:
            sample = pickle.loads(raw_sample)
            detection_sample = dbscan.Sample()
            for feature in sample:
                detection_sample.features.append(feature)
            detection_request.samples.append(detection_sample)

        with HISTOGRAM_DURATION.labels(step="uldetection", **METRIC_LABELS).time():
            response: dbscan.DetectionResponse = dbscanserving_client.Detect(
                detection_request
            )

        # including KPI
        kpi = Kpi()
        kpi.kpi_id.kpi_id.uuid = request.kpi_id.kpi_id.uuid
        kpi.timestamp.timestamp = timestamp_utcnow_to_float()
        # implementing WAD from https://ieeexplore.ieee.org/abstract/document/9064530
        if response.cluster_indices[-WAD_WINDOW:].count(-1) >= WAD_SAMPLES:
            kpi.kpi_value.int32Val = 1
            LOGGER.info(
                "Attack detected for service {}".format(
                    request.service_id.service_uuid.uuid
                )
            )
        else:
            kpi.kpi_value.int32Val = 0

        with HISTOGRAM_DURATION.labels(step="includekpi", **METRIC_LABELS).time():
            monitoring_client.IncludeKpi(kpi)

        # if -1 in response.cluster_indices:  # attack detected
        if kpi.kpi_value.int32Val == 1:
            attack = AttackDescription()
            attack.cs_id.uuid = request.service_id.service_uuid.uuid
            with HISTOGRAM_DURATION.labels(step="mitigation", **METRIC_LABELS).time():
                # with MITIGATION_RESPONSE_TIME.time():
                response: AttackResponse = attack_mitigator_client.NotifyAttack(attack)

        # if attack is detected, run the attack mitigator
        return Empty()
