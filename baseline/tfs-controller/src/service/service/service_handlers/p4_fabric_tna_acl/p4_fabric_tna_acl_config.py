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
Common objects and methods for In-band Network Telemetry (INT) dataplane
based on the SD-Fabric dataplane model.
This dataplane covers both software based and hardware-based Stratum-enabled P4 switches,
such as the BMv2 software switch and Intel's Tofino/Tofino-2 switches.

SD-Fabric repo: https://github.com/stratum/fabric-tna
SD-Fabric docs: https://docs.sd-fabric.org/master/index.html
"""

import logging

from service.service.service_handlers.p4_fabric_tna_commons.p4_fabric_tna_commons import *

LOGGER = logging.getLogger(__name__)

# ACL service handler settings
ACL = "acl"
ACTION = "action"
ACTION_DROP = "drop"
ACTION_ALLOW = "allow"
ACTION_LIST = [ACTION_ALLOW, ACTION_DROP]

def is_valid_acl_action(action : str) -> bool:
    return action in ACTION_LIST
