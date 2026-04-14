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
from enum import Enum

# Default logging level
DEFAULT_LOG_LEVEL = logging.WARNING

# Default gRPC server settings
DEFAULT_GRPC_BIND_ADDRESS = '0.0.0.0'
DEFAULT_GRPC_MAX_WORKERS  = 200
DEFAULT_GRPC_GRACE_PERIOD = 10

# Default HTTP server settings
DEFAULT_HTTP_BIND_ADDRESS = '0.0.0.0'

# Default Prometheus settings
DEFAULT_METRICS_PORT = 9192

# Default context and topology UUIDs
DEFAULT_CONTEXT_NAME      = 'admin'
DEFAULT_TOPOLOGY_NAME     = 'admin'     # contains the detailed local topology
INTERDOMAIN_TOPOLOGY_NAME = 'inter'     # contains the abstract inter-domain topology

# Default service names
class ServiceNameEnum(Enum):
    AUTOMATION             = 'automation'
    CONTEXT                = 'context'
    DEVICE                 = 'device'
    SERVICE                = 'service'
    SLICE                  = 'slice'
    ZTP                    = 'ztp'
    ZTP_SERVER             = 'ztp-server'
    POLICY                 = 'policy'
    MONITORING             = 'monitoring'
    DLT                    = 'dlt'
    NBI                    = 'nbi'
    SIMAP_CONNECTOR        = 'simap-connector'
    CYBERSECURITY          = 'cybersecurity'
    INTERDOMAIN            = 'interdomain'
    PATHCOMP               = 'pathcomp'
    L3_AM                  = 'l3-attackmitigator'
    L3_CAD                 = 'l3-centralizedattackdetector'
    WEBUI                  = 'webui'
    DBSCANSERVING          = 'dbscanserving'
    OPTICALATTACKMANAGER   = 'opticalattackmanager'
    OPTICALATTACKDETECTOR  = 'opticalattackdetector'
    OPTICALATTACKMITIGATOR = 'opticalattackmitigator'
    CACHING                = 'caching'
    TE                     = 'te'
    FORECASTER             = 'forecaster'
    E2EORCHESTRATOR        = 'e2e-orchestrator'
    OPTICALCONTROLLER      = 'opticalcontroller'
    VNTMANAGER             = 'vnt-manager'
    BGPLS                  = 'bgpls-speaker'
    QKD_APP                = 'qkd_app'
    KPIMANAGER             = 'kpi-manager'
    KPIVALUEAPI            = 'kpi-value-api'
    KPIVALUEWRITER         = 'kpi-value-writer'
    TELEMETRY              = 'telemetry'
    TELEMETRYBACKEND       = 'telemetry-backend'
    ANALYTICS              = 'analytics'
    ANALYTICSBACKEND       = 'analytics-backend'
    QOSPROFILE             = 'qos-profile'
    OSMCLIENT              = 'osm-client'
    PLUGGABLES              = 'dscm-pluggable'

    # Used for test and debugging only
    DLT_GATEWAY    = 'dltgateway'
    LOAD_GENERATOR = 'load-generator'

# Default gRPC service ports
DEFAULT_SERVICE_GRPC_PORTS = {
    ServiceNameEnum.CONTEXT                .value :  1010,
    ServiceNameEnum.DEVICE                 .value :  2020,
    ServiceNameEnum.SERVICE                .value :  3030,
    ServiceNameEnum.SLICE                  .value :  4040,
    ServiceNameEnum.ZTP                    .value :  5050,
    ServiceNameEnum.ZTP_SERVER             .value :  5051,
    ServiceNameEnum.POLICY                 .value :  6060,
    ServiceNameEnum.MONITORING             .value :  7070,
    ServiceNameEnum.DLT                    .value :  8080,
    ServiceNameEnum.SIMAP_CONNECTOR        .value :  9090,
    ServiceNameEnum.L3_CAD                 .value : 10001,
    ServiceNameEnum.L3_AM                  .value : 10002,
    ServiceNameEnum.DBSCANSERVING          .value : 10008,
    ServiceNameEnum.OPTICALATTACKDETECTOR  .value : 10006,
    ServiceNameEnum.OPTICALATTACKMITIGATOR .value : 10007,
    ServiceNameEnum.OPTICALATTACKMANAGER   .value : 10005,
    ServiceNameEnum.INTERDOMAIN            .value : 10010,
    ServiceNameEnum.PATHCOMP               .value : 10020,
    ServiceNameEnum.TE                     .value : 10030,
    ServiceNameEnum.FORECASTER             .value : 10040,
    ServiceNameEnum.E2EORCHESTRATOR        .value : 10050,
    ServiceNameEnum.OPTICALCONTROLLER      .value : 10060,
    ServiceNameEnum.QKD_APP                .value : 10070,
    ServiceNameEnum.VNTMANAGER             .value : 10080,
    ServiceNameEnum.BGPLS                  .value : 20030,
    ServiceNameEnum.QOSPROFILE             .value : 20040,
    ServiceNameEnum.KPIMANAGER             .value : 30010,
    ServiceNameEnum.KPIVALUEAPI            .value : 30020,
    ServiceNameEnum.KPIVALUEWRITER         .value : 30030,
    ServiceNameEnum.TELEMETRY              .value : 30050,
    ServiceNameEnum.TELEMETRYBACKEND       .value : 30060,
    ServiceNameEnum.ANALYTICS              .value : 30080,
    ServiceNameEnum.ANALYTICSBACKEND       .value : 30090,
    ServiceNameEnum.AUTOMATION             .value : 30200,
    ServiceNameEnum.OSMCLIENT              .value : 30210,
    ServiceNameEnum.PLUGGABLES             .value : 30220,

    # Used for test and debugging only
    ServiceNameEnum.DLT_GATEWAY   .value : 50051,
    ServiceNameEnum.LOAD_GENERATOR.value : 50052,
}

# Default HTTP/REST-API service ports
DEFAULT_SERVICE_HTTP_PORTS = {
    ServiceNameEnum.NBI  .value      : 8080,
    ServiceNameEnum.WEBUI.value      : 8004,
    ServiceNameEnum.ZTP_SERVER.value : 8005,
}

# Default HTTP/REST-API service base URLs
DEFAULT_SERVICE_HTTP_BASEURLS = {
    ServiceNameEnum.NBI  .value : None,
    ServiceNameEnum.WEBUI.value : None,
}


def OpticalServiceType(value):
    if value == "multi_granular":
        return 1
    elif value == "flexi_grid":
        return 2
    elif value == "pmp":
        return 3
    else:
        return 1
