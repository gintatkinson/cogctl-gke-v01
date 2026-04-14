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


from scapy.all import Packet, BitField
from collections import namedtuple

class IPPacket(Packet):
    name = "IPPacket"
    fields_desc = [
        BitField("ip_ver", 0, 4),
        BitField("ip_ihl", 0, 4),
        BitField("ip_dscp", 0, 6),
        BitField("ip_ecn", 0, 2),
        BitField("ip_len", 0, 16),
        BitField("ip_id", 0, 16),
        BitField("ip_flags", 0, 3),
        BitField("ip_frag", 0, 13),
        BitField("ip_ttl", 0, 8),
        BitField("ip_proto", 0, 8),
        BitField("ip_csum", 0, 16),
        BitField("ip_src", 0, 32),
        BitField("ip_dst", 0, 32)
    ]

class UDPPacket(Packet):
    name = "UDPPacket"
    fields_desc = [
        BitField("udp_port_src", 0, 16),
        BitField("udp_port_dst", 0, 16),
        BitField("udp_len", 0, 16),
        BitField("udp_csum", 0, 16)
    ]

"""
    Private source repo: https://github.com/SNVLab-WUT/int-collector/blob/main/collector/BPFCollector_v0_5.c
    fabric-tna repo: https://github.com/stratum/fabric-tna/blob/main/p4src/shared/header.p4

    Little Endian order
        BitField("nproto", 0, 4),
        BitField("ver", 0, 4),
        BitField("rsvd1", 0, 5),
        BitField("f", 0, 1),
        BitField("q", 0, 1),
        BitField("d", 0, 1),
        BitField("hw_id", 0, 6),
        BitField("rsvd2", 0, 10),

        BitField("queue_id", 0, 8),
        BitField("queue_occupancy", 0, 24),

    Big Endian order
        BitField("ver", 0, 4),
        BitField("nproto", 0, 4),
        BitField("d", 0, 1),
        BitField("q", 0, 1),
        BitField("f", 0, 1),
        BitField("rsvd1", 0, 5),
        BitField("rsvd2", 0, 10),
        BitField("hw_id", 0, 6),

        BitField("queue_occupancy", 0, 24),
        BitField("queue_id", 0, 8),
"""

class IntFixedReport(Packet):
    name = "IntFixedReport"
    fields_desc = [
        BitField("ver", 0, 4),
        BitField("nproto", 0, 4),
        BitField("d", 0, 1),
        BitField("q", 0, 1),
        BitField("f", 0, 1),
        BitField("rsvd1", 0, 5),
        BitField("rsvd2", 0, 10),
        BitField("hw_id", 0, 6),
        BitField("seq_num", 0, 32),
        BitField("ingress_timestamp", 0, 32),
        BitField("switch_id", 0, 32),
        BitField("ingress_port_id", 0, 16),
        BitField("egress_port_id", 0, 16)
    ]

class IntLocalReport(Packet):
    name = "IntLocalReport"
    fields_desc = [
        BitField("queue_occupancy", 0, 24),
        BitField("queue_id", 0, 8),
        BitField("egress_timestamp", 0, 32)
    ]

class IntDropReport(Packet):
    name = "IntDropReport"
    fields_desc = [
        BitField("queue_id", 0 , 8),
        BitField("drop_reason", 0, 8),
        BitField("_pad", 0, 16)
    ]

# Flow information structure
FlowInfo = namedtuple('FlowInfo', [
    'src_ip', 'dst_ip', 'src_port', 'dst_port', 'ip_proto',
    'flow_sink_time', 'num_int_hop', 'seq_num', 'switch_id',
    'ingress_timestamp', 'ingress_port_id', 'egress_port_id', 'queue_id',
    'queue_occupancy', 'egress_timestamp', 'is_drop', 'drop_reason',
    'hop_latency'
])
