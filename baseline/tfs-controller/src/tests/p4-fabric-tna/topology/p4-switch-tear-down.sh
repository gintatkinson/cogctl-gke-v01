#!bin/bash
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

# You must run this script as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

source "p4-switch-conf-common.sh"

kill_stratum() {
    pkill stratum
}

delete_virtual_interfaces() {
    ip netns exec ${SWITCH_NS} ip link delete ${SW_IFACE_INT}
}

delete_namespaces() {
    ip netns del ${SWITCH_NS}
}

bring_interfaces_up() {
    ifconfig ${SW_IFACE_DATA_EDGE} up
    ifconfig ${SW_IFACE_DATA_CORP} up
}

cleanup_iptables() {
    # gRPC entries
    entry_no=$(iptables --line-numbers -nvL | grep ${HOST_IFACE_INT} | cut -d " " -f 1 | head -1)
    iptables -D FORWARD ${entry_no}
    entry_no=$(iptables --line-numbers -nvL | grep ${HOST_IFACE_INT} | cut -d " " -f 1)
    iptables -D FORWARD ${entry_no}
    entry_no=$(iptables --line-numbers -nvL | grep ${SW_P4RT_GRPC_PORT} | cut -d " " -f 1)
    iptables -D FORWARD ${entry_no}

    entry_no=$(iptables -t nat --line-numbers -nvL | grep ${SW_P4RT_GRPC_PORT} | cut -d " " -f 1)
    iptables -t nat -D PREROUTING ${entry_no}

    entry_no=$(iptables -t nat --line-numbers -nvL | grep ${TOPO_INT_NET} | cut -d " " -f 1)
    iptables -t nat -D POSTROUTING ${entry_no}

    # Check new state
    echo "Forwarding tables"
    iptables --line-numbers -nvL
    echo -e ""
    echo "NAT tables"
    iptables -t nat --line-numbers -nvL
}

cleanup_tc() {
    sudo tc filter del dev ${HOST_IFACE_INT} parent ffff: \
        protocol all prio 2 u32 \
        match u32 0 0 flowid 1:1 \
        action mirred egress mirror dev ${HOST_IFACE_EXT}
    sudo tc qdisc del dev ${HOST_IFACE_INT} ingress

    # Check new state
    echo -e ""
    echo -e "Linux tc status"
    tc qdisc show
}

kill_stratum
delete_virtual_interfaces
delete_namespaces
# bring_interfaces_up
cleanup_iptables
cleanup_tc

exit 0
