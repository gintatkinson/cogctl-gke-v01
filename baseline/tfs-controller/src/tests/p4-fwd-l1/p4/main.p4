/*
 * Copyright 2019-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


#include <core.p4>
#include <v1model.p4>

typedef bit<9>   port_num_t;
typedef bit<48>  mac_addr_t;
typedef bit<16>  mcast_group_id_t;

//------------------------------------------------------------------------------
// HEADER DEFINITIONS
//------------------------------------------------------------------------------

header ethernet_t {
    mac_addr_t  dst_addr;
    mac_addr_t  src_addr;
    bit<16>     ether_type;
}

struct parsed_headers_t {
    ethernet_t  ethernet;
}

struct local_metadata_t {
    bool        is_multicast;
}


//------------------------------------------------------------------------------
// INGRESS PIPELINE
//------------------------------------------------------------------------------

parser ParserImpl (packet_in packet,
                   out parsed_headers_t hdr,
                   inout local_metadata_t local_metadata,
                   inout standard_metadata_t standard_metadata)
{
    state start {
      transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition accept;
    }
}


control VerifyChecksumImpl(inout parsed_headers_t hdr,
                           inout local_metadata_t meta)
{
    apply { /* EMPTY */ }
}


control IngressPipeImpl (inout parsed_headers_t    hdr,
                         inout local_metadata_t    local_metadata,
                         inout standard_metadata_t standard_metadata) {

    // Drop action shared by many tables.
    action drop() {
        mark_to_drop(standard_metadata);
    }

    action set_egress_port(port_num_t port) {
        standard_metadata.egress_spec = port;
    }

    action set_multicast_group(mcast_group_id_t gid) {
        // gid will be used by the Packet Replication Engine (PRE) in the
        // Traffic Manager--located right after the ingress pipeline, to
        // replicate a packet to multiple egress ports, specified by the control
        // plane by means of P4Runtime MulticastGroupEntry messages.
        standard_metadata.mcast_grp = gid;
        local_metadata.is_multicast = true;
    }

    // --- l2_exact_table ------------------

    table l2_exact_table {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            set_egress_port;
            set_multicast_group;
            @defaultonly drop;
        }
        const default_action = drop;
    }

    apply {
        l2_exact_table.apply();
    }
}

//------------------------------------------------------------------------------
// EGRESS PIPELINE
//------------------------------------------------------------------------------

control EgressPipeImpl (inout parsed_headers_t hdr,
                        inout local_metadata_t local_metadata,
                        inout standard_metadata_t standard_metadata) {
    apply { /* EMPTY */ }
}


control ComputeChecksumImpl(inout parsed_headers_t hdr,
                            inout local_metadata_t local_metadata)
{
    apply { /* EMPTY */ }
}


control DeparserImpl(packet_out packet, in parsed_headers_t hdr) {
    apply {
        packet.emit(hdr.ethernet);
    }
}


V1Switch(
    ParserImpl(),
    VerifyChecksumImpl(),
    IngressPipeImpl(),
    EgressPipeImpl(),
    ComputeChecksumImpl(),
    DeparserImpl()
) main;
