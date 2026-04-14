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


import enum

class FamilyEnum(enum.Enum):
    IPV4   = 'ip'     # IPv4 address family.
    IPV6   = 'ip6'    # IPv6 address family.
    INET   = 'inet'   # Internet (IPv4/IPv6) address family.
    ARP    = 'arp'    # ARP address family, handling IPv4 ARP packets.
    BRIDGE = 'bridge' # Bridge address family, handling packets which traverse a bridge device.
    NETDEV = 'netdev' # Netdev address family, handling packets on ingress and egress.

def get_family_from_str(family : str) -> FamilyEnum:
    return FamilyEnum._value2member_map_[family]
