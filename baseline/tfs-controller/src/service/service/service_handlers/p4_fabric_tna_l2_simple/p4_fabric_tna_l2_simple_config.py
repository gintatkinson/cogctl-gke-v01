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
Common objects and methods for L2 forwarding based on the SD-Fabric dataplane model.
This dataplane covers both software based and hardware-based Stratum-enabled P4 switches,
such as the BMv2 software switch and Intel's Tofino/Tofino-2 switches.

SD-Fabric repo: https://github.com/stratum/fabric-tna
SD-Fabric docs: https://docs.sd-fabric.org/master/index.html
"""

import logging
from common.proto.context_pb2 import ConfigActionEnum

from service.service.service_handlers.p4_fabric_tna_commons.p4_fabric_tna_commons import *

LOGGER = logging.getLogger(__name__)

# L2 simple service handler settings
FORWARDING_LIST = "fwd_list"
HOST_MAC = "host_mac"

def rules_set_up_port_host(
        port : int,
        vlan_id : int,
        action : ConfigActionEnum, # type: ignore
        fwd_type=FORWARDING_TYPE_BRIDGING,
        eth_type=ETHER_TYPE_IPV4):
    # This is a host facing port
    port_type = PORT_TYPE_HOST

    return rules_set_up_port(
        port=port,
        port_type=port_type,
        fwd_type=fwd_type,
        vlan_id=vlan_id,
        action=action,
        eth_type=eth_type
    )

def rules_set_up_port_switch(
        port : int,
        vlan_id : int,
        action : ConfigActionEnum, # type: ignore
        fwd_type=FORWARDING_TYPE_BRIDGING,
        eth_type=ETHER_TYPE_IPV4):
    # This is a switch facing port
    port_type = PORT_TYPE_SWITCH

    return rules_set_up_port(
        port=port,
        port_type=port_type,
        fwd_type=fwd_type,
        vlan_id=vlan_id,
        action=action,
        eth_type=eth_type
    )
