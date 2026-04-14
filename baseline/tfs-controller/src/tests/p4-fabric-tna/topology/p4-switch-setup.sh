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

# MAC addresses of the virtual INT interfaces
SW_INT_MAC="00:11:22:33:44:11"
HOST_INT_MAC="00:11:22:33:44:22"

# IP addresses of the virtual INT interfaces
SWITCH_INT_IP="10.0.0.1"
HOST_INT_IP="10.0.0.254"

SWITCH_INT_IP_NET=${SWITCH_INT_IP}"/24"
HOST_INT_IP_NET=${HOST_INT_IP}"/24"

# Subnets managed by the switch
DOMAIN_EDGE_IP="10.158.72.22/24" # Edge domain side IP address
DOMAIN_CORP_IP="172.16.10.4/24"  # Corporate domain side IP address

# INT subnet MTU
MTU_LEN=9000

kill_stratum() {
    pkill stratum
}

create_namespaces() {
    ip netns add ${SWITCH_NS}
}

create_virtual_interfaces() {
    ip link add ${HOST_IFACE_INT} type veth peer name ${SW_IFACE_INT}
}

assign_virtual_interfaces() {
    ip link set ${SW_IFACE_DATA_EDGE} netns ${SWITCH_NS}
    ip link set ${SW_IFACE_DATA_CORP} netns ${SWITCH_NS}
    ip link set ${SW_IFACE_INT} netns ${SWITCH_NS}
}

set_mac_addresses() {
    ip netns exec ${SWITCH_NS} ifconfig ${SW_IFACE_INT} hw ether ${SW_INT_MAC}
    ifconfig ${HOST_IFACE_INT} hw ether ${HOST_INT_MAC}
}

set_mtu() {
    ip netns exec ${SWITCH_NS} ip link set dev ${SW_IFACE_INT} mtu ${MTU_LEN}
    ip link set dev ${HOST_IFACE_INT} mtu ${MTU_LEN}
}

set_ip_addresses() {
    ip -n ${SWITCH_NS} addr add ${DOMAIN_EDGE_IP} dev ${SW_IFACE_DATA_EDGE}
    ip -n ${SWITCH_NS} addr add ${DOMAIN_CORP_IP} dev ${SW_IFACE_DATA_CORP}
    ip -n ${SWITCH_NS} addr add ${SWITCH_INT_IP_NET} dev ${SW_IFACE_INT}
    ifconfig ${HOST_IFACE_INT} ${HOST_INT_IP_NET}
}

bring_interfaces_up() {
    ip -n ${SWITCH_NS} link set ${SW_IFACE_DATA_EDGE} up
    ip -n ${SWITCH_NS} link set ${SW_IFACE_DATA_CORP} up
    ip -n ${SWITCH_NS} link set ${SW_IFACE_INT} up
    ifconfig ${HOST_IFACE_INT} up
}

disable_csum_offloading() {
    ip netns exec ${SWITCH_NS} ethtool -K ${SW_IFACE_DATA_EDGE} rx off tx off
    ip netns exec ${SWITCH_NS} ethtool -K ${SW_IFACE_DATA_CORP} rx off tx off
}

switch_default_gw() {
    ip netns exec ${SWITCH_NS} ip route add default via ${HOST_INT_IP}
}

enable_ip_fwd() {
    sysctl net.ipv4.ip_forward=1
    sysctl net.ipv4.conf.${HOST_IFACE_EXT}.forwarding=1
    sysctl net.ipv4.conf.${HOST_IFACE_INT}.forwarding=1
}

switch_access_to_internet() {
    iptables -P FORWARD DROP
    iptables -t nat -A POSTROUTING -s ${TOPO_INT_NET_IP}/${TOPO_INT_NET_MASK} -o ${HOST_IFACE_EXT} -j MASQUERADE
    iptables -A FORWARD -i ${HOST_IFACE_EXT} -o ${HOST_IFACE_INT} -j ACCEPT
    iptables -A FORWARD -o ${HOST_IFACE_EXT} -i ${HOST_IFACE_INT} -j ACCEPT
}

grpc_port_forwarding() {
    iptables -t nat -A PREROUTING -p tcp -i ${HOST_IFACE_EXT} --dport ${SW_P4RT_GRPC_PORT} -j DNAT --to-destination ${SWITCH_INT_IP}:${SW_P4RT_GRPC_PORT}
    iptables -A FORWARD -p tcp -d ${SWITCH_INT_IP} --dport ${SW_P4RT_GRPC_PORT} -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
}

int_packet_mirroring() {
    sudo tc qdisc add dev ${HOST_IFACE_INT} ingress
    sudo tc filter add dev ${HOST_IFACE_INT} parent ffff: \
        protocol all prio 2 u32 \
        match u32 0 0 flowid 1:1 \
        action mirred egress mirror dev ${HOST_IFACE_EXT}
}

kill_stratum
create_namespaces
create_virtual_interfaces
assign_virtual_interfaces
set_mac_addresses
set_mtu
set_ip_addresses
bring_interfaces_up
disable_csum_offloading
switch_default_gw
enable_ip_fwd
switch_access_to_internet
grpc_port_forwarding
int_packet_mirroring

exit 0
