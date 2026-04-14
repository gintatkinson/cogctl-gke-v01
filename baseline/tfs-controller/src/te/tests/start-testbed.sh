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

set -e

ROOTDIR="$( cd $( dirname $0 ); pwd )"
RUNDIR="$( pwd )"
NETGENDIR="${RUNDIR}/netgen"

if [[ ! -f "${NETGENDIR}/exe/netgen" ]]; then
    echo "Failed to find Netgen binary at ${NETGENDIR}/exe/netgen"
    exit 1
fi

PCE_IP=$( kubectl --namespace tfs get $(kubectl --namespace tfs get pods --selector=app=teservice -o name) --template '{{.status.podIP}}' )
echo "Teraflow PCE IP address: $PCE_IP"
NAMESPACES=$( ip netns list | cut -d' ' -f1 )
PCE_NETNS=""
for n in $NAMESPACES; do
    if sudo ip -n $n addr list | grep $PCE_IP > /dev/null; then
        echo "Teraflow TE service namespace: $n"
        PCE_NETNS=$n
        break
    fi    
done
if [[ -z $PCE_NETNS ]]; then
    echo "Teraflow network namespace for TE service not found"
    exit1
fi

IFS=. read PCE_IP1 PCE_IP2 PCE_IP3 PCE_IP4 <<< "$PCE_IP"

export PCE_IP
export PCE_NETNS
export RT1_PCE_INT_IF_IP="$PCE_IP1.$PCE_IP2.$PCE_IP3.10"
export RT1_PCE_EXT_IF_IP="$PCE_IP1.$PCE_IP2.$PCE_IP3.11"
export RT6_PCE_INT_IF_IP="$PCE_IP1.$PCE_IP2.$PCE_IP3.12"
export RT6_PCE_EXT_IF_IP="$PCE_IP1.$PCE_IP2.$PCE_IP3.13"

cp "${ROOTDIR}/netgen-config.yml" "${RUNDIR}/config.yml"
cat "${ROOTDIR}/netgen-topology.yml.template" | envsubst > "${RUNDIR}/topology.yml"

sudo -i bash -c "\
    cd ${RUNDIR}/netgen;\
    sysctl -w net.ipv4.conf.all.rp_filter=0;\
    PATH=/usr/lib/frr:\$PATH ./exe/netgen ../topology.yml -c ../config.yml"
