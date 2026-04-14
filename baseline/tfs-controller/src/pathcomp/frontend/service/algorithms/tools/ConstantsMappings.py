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

from enum import IntEnum

class CapacityUnit(IntEnum):
    TB   = 0
    TBPS = 1
    GB   = 2
    GBPS = 3
    MB   = 4
    MBPS = 5
    KB   = 6
    KBPS = 7
    GHZ  = 8
    MHZ  = 9

CAPACITY_MULTIPLIER = {
    CapacityUnit.TB   : 1.e12,
    CapacityUnit.TBPS : 1.e12,
    CapacityUnit.GB   : 1.e9,
    CapacityUnit.GBPS : 1.e9,
    CapacityUnit.MB   : 1.e6,
    CapacityUnit.MBPS : 1.e6,
    CapacityUnit.KB   : 1.e3,
    CapacityUnit.KBPS : 1.e3,
    CapacityUnit.GHZ  : 1.e9,
    CapacityUnit.MHZ  : 1.e6,
}

class LinkPortDirection(IntEnum):
    BIDIRECTIONAL = 0
    INPUT         = 1
    OUTPUT        = 2
    UNKNOWN       = 3

class TerminationDirection(IntEnum):
    BIDIRECTIONAL = 0
    SINK          = 1
    SOURCE        = 2
    UNKNOWN       = 3

class TerminationState(IntEnum):
    CAN_NEVER_TERMINATE         = 0
    NOT_TERMINATED              = 1
    TERMINATED_SERVER_TO_CLIENT = 2
    TERMINATED_CLIENT_TO_SERVER = 3
    TERMINATED_BIDIRECTIONAL    = 4
    PERMENANTLY_TERMINATED      = 5
    TERMINATION_STATE_UNKNOWN   = 6

class LinkForwardingDirection(IntEnum):
    BIDIRECTIONAL  = 0
    UNIDIRECTIONAL = 1
    UNKNOWN        = 2
