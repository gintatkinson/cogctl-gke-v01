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

from enum import Enum

class RequestType(Enum):
    SERVICE_L2NM = 'svc-l2nm'
    SERVICE_L3NM = 'svc-l3nm'
    SERVICE_TAPI = 'svc-tapi'
    SERVICE_MW   = 'svc-mw'
    SLICE_L2NM   = 'slc-l2nm'
    SLICE_L3NM   = 'slc-l3nm'

ENDPOINT_COMPATIBILITY = {
    'PHOTONIC_MEDIA:FLEX:G_6_25GHZ:INPUT': 'PHOTONIC_MEDIA:FLEX:G_6_25GHZ:OUTPUT',
    'PHOTONIC_MEDIA:DWDM:G_50GHZ:INPUT'  : 'PHOTONIC_MEDIA:DWDM:G_50GHZ:OUTPUT',
}

DEFAULT_AVAILABILITY_RANGES   = [[0.0, 99.9999]]
DEFAULT_CAPACITY_GBPS_RANGES  = [[0.1, 100.00]]
DEFAULT_E2E_LATENCY_MS_RANGES = [[5.0, 100.00]]

DEFAULT_MAX_WORKERS = 10
