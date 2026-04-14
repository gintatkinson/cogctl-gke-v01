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

//------------------------------------------------------------------------------
// HEADER DEFINITIONS
//------------------------------------------------------------------------------

#define MAX_INT_HEADERS 9

const bit<16> TYPE_IPV4 = 0x800;
const bit<5>  IPV4_OPTION_INT = 31;

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

typedef bit<13> switch_id_t;
typedef bit<13> queue_depth_t;
typedef bit<6>  output_port_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<6>    dscp;
    bit<2>    ecn;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header ipv4_option_t {
    bit<1> copyFlag;
    bit<2> optClass;
    bit<5> option;
    bit<8> optionLength;
}

header int_count_t {
    bit<16>   num_switches;
}

header int_header_t {
    switch_id_t switch_id;
    queue_depth_t queue_depth;
    output_port_t output_port;
}


struct parser_metadata_t {
    bit<16> num_headers_remaining;
}

struct local_metadata_t {
    parser_metadata_t  parser_metadata;
}

struct parsed_headers_t {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    ipv4_option_t ipv4_option;
    int_count_t   int_count;
    int_header_t[MAX_INT_HEADERS] int_headers;
}

error { IPHeaderWithoutOptions }

//------------------------------------------------------------------------------
// INGRESS PIPELINE
//------------------------------------------------------------------------------

parser ParserImpl(packet_in packet,
                out parsed_headers_t hdr,
                inout local_metadata_t local_metadata,
                inout standard_metadata_t standard_metadata) {

    state start {

        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType){
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        //Check if ihl is bigger than 5. Packets without ip options set ihl to 5.
        verify(hdr.ipv4.ihl >= 5, error.IPHeaderWithoutOptions);
        transition select(hdr.ipv4.ihl) {
            5             : accept;
            default       : parse_ipv4_option;
        }
    }

    state parse_ipv4_option {
        packet.extract(hdr.ipv4_option);
        transition select(hdr.ipv4_option.option){

            IPV4_OPTION_INT:  parse_int;
            default: accept;

        }
     }

    state parse_int {
        packet.extract(hdr.int_count);
        local_metadata.parser_metadata.num_headers_remaining = hdr.int_count.num_switches;
        transition select(local_metadata.parser_metadata.num_headers_remaining){
            0: accept;
            default: parse_int_headers;
        }
    }

    state parse_int_headers {
        packet.extract(hdr.int_headers.next);
        local_metadata.parser_metadata.num_headers_remaining = local_metadata.parser_metadata.num_headers_remaining -1 ;
        transition select(local_metadata.parser_metadata.num_headers_remaining){
            0: accept;
            default: parse_int_headers;
        }
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

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action set_egress_port(port_num_t port) {
        standard_metadata.egress_spec = port;
    }

    // --- l2_exact_table ------------------

    table l2_exact_table {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            set_egress_port;
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

    
    action add_int_header(switch_id_t swid){
        //increase int stack counter by one
        hdr.int_count.num_switches = hdr.int_count.num_switches + 1;
        hdr.int_headers.push_front(1);
        // This was not needed in older specs. Now by default pushed
        // invalid elements are
        hdr.int_headers[0].setValid();
        hdr.int_headers[0].switch_id = (bit<13>)swid;
        hdr.int_headers[0].queue_depth = (bit<13>)standard_metadata.deq_qdepth;
        hdr.int_headers[0].output_port = (bit<6>)standard_metadata.egress_port;

        //update ip header length
        hdr.ipv4.ihl = hdr.ipv4.ihl + 1;
        hdr.ipv4.totalLen = hdr.ipv4.totalLen + 4;
        hdr.ipv4_option.optionLength = hdr.ipv4_option.optionLength + 4;
    }

    table int_table {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            add_int_header;
            NoAction;
        }
        default_action = NoAction;
    }

    apply {
        if (hdr.int_count.isValid()){
            int_table.apply();
        }
    }
}


control ComputeChecksumImpl(inout parsed_headers_t hdr,
                            inout local_metadata_t local_metadata)
{
    apply {
        update_checksum(
	          hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	            hdr.ipv4.ihl,
              hdr.ipv4.dscp,
              hdr.ipv4.ecn,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);
    }
}

control DeparserImpl(packet_out packet, in parsed_headers_t hdr) {
    apply {

        //parsed headers have to be added again into the packet.
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.ipv4_option);
        packet.emit(hdr.int_count);
        packet.emit(hdr.int_headers);

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
