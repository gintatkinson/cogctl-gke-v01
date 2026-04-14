#!/bin/bash
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

# Switch lives in a namespace
SWITCH_NS="ns-switch"

# Physical interfaces
HOST_IFACE_EXT="ens3"     # Interface towards TFS (management)
SW_IFACE_DATA_EDGE="ens4" # Interface towards the edge subnet (data plane)
SW_IFACE_DATA_CORP="ens5" # Interface towards the corporate subnet (data plane)

# Virtual interfaces for INT
SW_IFACE_INT="veth-int-sw"
HOST_IFACE_INT="veth-int-host"

# IP subnet for INT
TOPO_INT_NET="10.0.0.0/24"
TOPO_INT_NET_IP="10.0.0.0"
TOPO_INT_NET_MASK="255.255.255.0"

# Transport port where the P4Runtime gRPC server is deployed on the switch
SW_P4RT_GRPC_PORT="50001"

# Transport port where the P4Runtime gNMI server is deployed on the switch
SW_P4RT_GNMI_PORT="50000"

# Transport port where Stratum listens to local calls
SW_P4RT_LOCAL_PORT="50101"
