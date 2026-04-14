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


cd openconfig

pyang -f tree -o ../openconfig-components.tree \
    platform/openconfig-platform-common.yang \
    platform/openconfig-platform-types.yang \
    platform/openconfig-platform.yang \
    system/openconfig-alarm-types.yang \
    types/openconfig-types.yang \
    types/openconfig-yang-types.yang

pyang -f tree -o ../openconfig-interfaces.tree \
    interfaces/openconfig-if-aggregate.yang \
    interfaces/openconfig-if-ethernet.yang \
    interfaces/openconfig-if-ip.yang \
    interfaces/openconfig-interfaces.yang \
    openconfig-extensions.yang \
    openconfig-transport/openconfig-transport-types.yang \
    platform/openconfig-platform-types.yang \
    types/openconfig-inet-types.yang \
    types/openconfig-types.yang \
    types/openconfig-yang-types.yang \
    vlan/openconfig-vlan-types.yang \
    vlan/openconfig-vlan.yang

pyang -f tree -o ../openconfig-acl.tree \
    acl/openconfig-acl.yang \
    acl/openconfig-icmpv4-types.yang \
    acl/openconfig-icmpv6-types.yang \
    acl/openconfig-packet-match-types.yang \
    acl/openconfig-packet-match.yang \
    defined-sets/openconfig-defined-sets.yang \
    interfaces/openconfig-interfaces.yang \
    mpls/openconfig-mpls-types.yang \
    openconfig-transport/openconfig-transport-types.yang \
    platform/openconfig-platform-types.yang \
    types/openconfig-inet-types.yang \
    types/openconfig-types.yang \
    types/openconfig-yang-types.yang
