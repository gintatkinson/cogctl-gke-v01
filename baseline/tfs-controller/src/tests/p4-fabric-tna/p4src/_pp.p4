error {
    PacketRejectedByParser
}
#include <core.p4>
#define V1MODEL_VERSION 20180101
#include <v1model.p4>

typedef bit<9> PortId_t;
typedef bit<16> MulticastGroupId_t;
typedef bit<5> QueueId_t;
typedef bit<10> MirrorId_t;
typedef bit<16> ReplicationId_t;
enum bit<2> MeterColor_t {
    GREEN = 0,
    YELLOW = 1,
    RED = 2
}

typedef bit<1> BOOL;
typedef bit<8> FieldListIndex_t;
const PortId_t BMV2_DROP_PORT = 511;
const PortId_t FAKE_V1MODEL_RECIRC_PORT = 510;
const FieldListIndex_t PRESERVE_INT_MD = 241;
const FieldListIndex_t PRESERVE_INGRESS_PORT = 231;
const FieldListIndex_t NO_PRESERVATION = 0;
typedef bit<3> fwd_type_t;
typedef bit<32> next_id_t;
typedef bit<20> mpls_label_t;
typedef bit<48> mac_addr_t;
typedef bit<12> vlan_id_t;
typedef bit<32> ipv4_addr_t;
typedef bit<16> l4_port_t;
typedef bit<32> flow_hash_t;
typedef bit<4> slice_id_t;
typedef bit<2> tc_t;
typedef bit<(4 + 2)> slice_tc_t;
type bit<9> FabricPortId_t;
const bit<8> DEFAULT_APP_ID = 0;
const slice_id_t DEFAULT_SLICE_ID = 0;
const tc_t DEFAULT_TC = 0;
const QueueId_t QUEUE_ID_BEST_EFFORT = 0;
typedef bit<32> teid_t;
typedef bit<12> upf_ctr_idx_t;
typedef bit<8> tun_peer_id_t;
typedef bit<32> ue_session_id_t;
typedef bit<15> session_meter_idx_t;
typedef bit<15> app_meter_idx_t;
const session_meter_idx_t DEFAULT_SESSION_METER_IDX = 0;
const app_meter_idx_t DEFAULT_APP_METER_IDX = 0;
enum bit<2> EncapPresence {
    NONE = 0x0,
    GTPU_ONLY = 0x1,
    GTPU_WITH_PSC = 0x2,
    VXLAN = 0x3
}

const bit<16> GTPU_UDP_PORT = 2152;
const bit<3> GTP_V1 = 3w1;
const bit<8> GTPU_GPDU = 0xff;
const bit<1> GTP_PROTOCOL_TYPE_GTP = 1w1;
const bit<8> GTPU_NEXT_EXT_NONE = 0x0;
const bit<8> GTPU_NEXT_EXT_PSC = 0x85;
const bit<4> GTPU_EXT_PSC_TYPE_DL = 4w0;
const bit<4> GTPU_EXT_PSC_TYPE_UL = 4w1;
const bit<8> GTPU_EXT_PSC_LEN = 8w1;
enum bit<2> PortType_t {
    UNKNOWN = 0x0,
    EDGE = 0x1,
    INFRA = 0x2,
    INTERNAL = 0x3
}

const bit<16> ETHERTYPE_QINQ = 0x88a8;
const bit<16> ETHERTYPE_QINQ_NON_STD = 0x9100;
const bit<16> ETHERTYPE_VLAN = 0x8100;
const bit<16> ETHERTYPE_MPLS = 0x8847;
const bit<16> ETHERTYPE_MPLS_MULTICAST = 0x8848;
const bit<16> ETHERTYPE_IPV4 = 0x800;
const bit<16> ETHERTYPE_IPV6 = 0x86dd;
const bit<16> ETHERTYPE_ARP = 0x806;
const bit<16> ETHERTYPE_PPPOED = 0x8863;
const bit<16> ETHERTYPE_PPPOES = 0x8864;
const bit<16> ETHERTYPE_PACKET_OUT = 0xbf01;
const bit<16> ETHERTYPE_CPU_LOOPBACK_INGRESS = 0xbf02;
const bit<16> ETHERTYPE_CPU_LOOPBACK_EGRESS = 0xbf03;
const bit<16> ETHERTYPE_INT_WIP_IPV4 = 0xbf04;
const bit<16> ETHERTYPE_INT_WIP_MPLS = 0xbf05;
const bit<16> PPPOE_PROTOCOL_IP4 = 0x21;
const bit<16> PPPOE_PROTOCOL_IP6 = 0x57;
const bit<16> PPPOE_PROTOCOL_MPLS = 0x281;
const bit<8> PROTO_ICMP = 1;
const bit<8> PROTO_TCP = 6;
const bit<8> PROTO_UDP = 17;
const bit<8> PROTO_ICMPV6 = 58;
const bit<4> IPV4_MIN_IHL = 5;
const fwd_type_t FWD_BRIDGING = 0;
const fwd_type_t FWD_MPLS = 1;
const fwd_type_t FWD_IPV4_UNICAST = 2;
const fwd_type_t FWD_IPV4_MULTICAST = 3;
const fwd_type_t FWD_IPV6_UNICAST = 4;
const fwd_type_t FWD_IPV6_MULTICAST = 5;
const fwd_type_t FWD_UNKNOWN = 7;
const vlan_id_t DEFAULT_VLAN_ID = 12w4094;
const bit<8> DEFAULT_MPLS_TTL = 64;
const bit<8> DEFAULT_IPV4_TTL = 64;
const bit<16> VXLAN_UDP_PORT = 4789;
const bit<7> RECIRC_PORT_NUMBER = 7w68;
action nop() {
    NoAction();
}
enum bit<8> BridgedMdType_t {
    INVALID = 0,
    INGRESS_TO_EGRESS = 1,
    EGRESS_MIRROR = 2,
    INGRESS_MIRROR = 3,
    INT_INGRESS_DROP = 4,
    DEFLECTED = 5
}

enum bit<3> FabricMirrorType_t {
    INVALID = 0,
    INT_REPORT = 1,
    PACKET_IN = 2
}

const MirrorId_t PACKET_IN_MIRROR_SESSION_ID = 0x1ff;
enum bit<2> CpuLoopbackMode_t {
    DISABLED = 0,
    DIRECT = 1,
    INGRESS = 2
}

const bit<4> NPROTO_ETHERNET = 0;
const bit<4> NPROTO_TELEMETRY_DROP_HEADER = 1;
const bit<4> NPROTO_TELEMETRY_SWITCH_LOCAL_HEADER = 2;
const bit<16> REPORT_FIXED_HEADER_BYTES = 12;
const bit<16> DROP_REPORT_HEADER_BYTES = 12;
const bit<16> LOCAL_REPORT_HEADER_BYTES = 16;
const bit<8> INT_MIRROR_SESSION_BASE = 0x80;
const bit<10> V1MODEL_INT_MIRROR_SESSION = 0x1fa;
typedef bit<16> flow_report_filter_index_t;
typedef bit<16> drop_report_filter_index_t;
typedef bit<12> queue_report_filter_index_t;
typedef bit<16> queue_report_quota_t;
typedef bit<3> IntReportType_t;
const IntReportType_t INT_REPORT_TYPE_NO_REPORT = 0;
const IntReportType_t INT_REPORT_TYPE_DROP = 4;
const IntReportType_t INT_REPORT_TYPE_QUEUE = 2;
const IntReportType_t INT_REPORT_TYPE_FLOW = 1;
typedef bit<8> IntWipType_t;
const IntWipType_t INT_IS_NOT_WIP = 0;
const IntWipType_t INT_IS_WIP = 1;
const IntWipType_t INT_IS_WIP_WITH_MPLS = 2;
const bit<16> INT_WIP_ADJUST_IP_BYTES = 14 - 1 ^ 0xffff;
const bit<16> INT_WIP_ADJUST_UDP_BYTES = INT_WIP_ADJUST_IP_BYTES - 20;
const bit<16> INT_WIP_ADJUST_IP_MPLS_BYTES = INT_WIP_ADJUST_IP_BYTES - 4;
const bit<16> INT_WIP_ADJUST_UDP_MPLS_BYTES = INT_WIP_ADJUST_UDP_BYTES - 4;
enum bit<8> IntDropReason_t {
    DROP_REASON_UNKNOWN = 0,
    DROP_REASON_IP_TTL_ZERO = 26,
    DROP_REASON_ROUTING_V4_MISS = 29,
    DROP_REASON_ROUTING_V6_MISS = 29,
    DROP_REASON_PORT_VLAN_MAPPING_MISS = 55,
    DROP_REASON_TRAFFIC_MANAGER = 71,
    DROP_REASON_ACL_DENY = 80,
    DROP_REASON_BRIDGING_MISS = 89,
    DROP_REASON_NEXT_ID_MISS = 128,
    DROP_REASON_MPLS_MISS = 129,
    DROP_REASON_EGRESS_NEXT_MISS = 130,
    DROP_REASON_MPLS_TTL_ZERO = 131,
    DROP_REASON_UPF_DL_SESSION_MISS = 132,
    DROP_REASON_UPF_DL_SESSION_DROP = 133,
    DROP_REASON_UPF_UL_SESSION_MISS = 134,
    DROP_REASON_UPF_UL_SESSION_DROP = 135,
    DROP_REASON_UPF_DL_SESSION_DROP_BUFF = 136,
    DROP_REASON_UPF_DL_TERMINATION_MISS = 137,
    DROP_REASON_UPF_DL_TERMINATION_DROP = 138,
    DROP_REASON_UPF_UL_TERMINATION_MISS = 139,
    DROP_REASON_UPF_UL_TERMINATION_DROP = 140,
    DROP_REASON_UPF_UPLINK_RECIRC_DENY = 150,
    DROP_REASON_INGRESS_QOS_METER = 160,
    DROP_REASON_ROUTING_V4_DROP = 170,
    DROP_REASON_ROUTING_V6_DROP = 171
}

@controller_header("packet_in") header packet_in_header_t {
    FabricPortId_t ingress_port;
    bit<7>         _pad0;
}

@controller_header("packet_out") header packet_out_header_t {
    @padding 
    bit<7>            pad0;
    FabricPortId_t    egress_port;
    @padding 
    bit<3>            pad1;
    QueueId_t         queue_id;
    @padding 
    bit<5>            pad2;
    CpuLoopbackMode_t cpu_loopback_mode;
    bit<1>            do_forwarding;
    @padding 
    bit<16>           pad3;
    @padding 
    bit<48>           pad4;
    bit<16>           ether_type;
}

header ethernet_t {
    mac_addr_t dst_addr;
    mac_addr_t src_addr;
}

header eth_type_t {
    bit<16> value;
}

header vlan_tag_t {
    bit<16>   eth_type;
    bit<3>    pri;
    bit<1>    cfi;
    vlan_id_t vlan_id;
}

header mpls_t {
    mpls_label_t label;
    bit<3>       tc;
    bit<1>       bos;
    bit<8>       ttl;
}

header pppoe_t {
    bit<4>  version;
    bit<4>  type_id;
    bit<8>  code;
    bit<16> session_id;
    bit<16> length;
    bit<16> protocol;
}

header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<6>  dscp;
    bit<2>  ecn;
    bit<16> total_len;
    bit<16> identification;
    bit<3>  flags;
    bit<13> frag_offset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdr_checksum;
    bit<32> src_addr;
    bit<32> dst_addr;
}

header ipv6_t {
    bit<4>   version;
    bit<8>   traffic_class;
    bit<20>  flow_label;
    bit<16>  payload_len;
    bit<8>   next_hdr;
    bit<8>   hop_limit;
    bit<128> src_addr;
    bit<128> dst_addr;
}

header tcp_t {
    bit<16> sport;
    bit<16> dport;
}

header udp_t {
    bit<16> sport;
    bit<16> dport;
    bit<16> len;
    bit<16> checksum;
}

header icmp_t {
    bit<8> icmp_type;
    bit<8> icmp_code;
}

header vxlan_t {
    bit<8>  flags;
    bit<24> reserved;
    bit<24> vni;
    bit<8>  reserved_2;
}

header gtpu_t {
    bit<3>  version;
    bit<1>  pt;
    bit<1>  spare;
    bit<1>  ex_flag;
    bit<1>  seq_flag;
    bit<1>  npdu_flag;
    bit<8>  msgtype;
    bit<16> msglen;
    teid_t  teid;
}

header gtpu_options_t {
    bit<16> seq_num;
    bit<8>  n_pdu_num;
    bit<8>  next_ext;
}

header gtpu_ext_psc_t {
    bit<8> len;
    bit<4> type;
    bit<4> spare0;
    bit<1> ppp;
    bit<1> rqi;
    bit<6> qfi;
    bit<8> next_ext;
}

@flexible struct upf_bridged_metadata_t {
    tun_peer_id_t tun_peer_id;
    upf_ctr_idx_t upf_ctr_id;
    bit<6>        qfi;
    bool          needs_gtpu_encap;
    bool          skip_upf;
    bool          skip_egress_upf_ctr;
    teid_t        teid;
    bit<4>        _pad;
}

@pa_no_overlay("egress" , "hdr.report_fixed_header.rsvd") header report_fixed_header_t {
    bit<4>  ver;
    bit<4>  nproto;
    bit<3>  dqf;
    bit<15> rsvd;
    bit<6>  hw_id;
    bit<32> seq_no;
    bit<32> ig_tstamp;
}

@pa_container_size("egress" , "hdr.common_report_header.queue_id" , 8) @pa_container_size("egress" , "hdr.common_report_header.ig_port" , 16) @pa_container_size("egress" , "hdr.common_report_header.eg_port" , 16) @pa_no_overlay("egress" , "hdr.common_report_header.queue_id") @pa_no_overlay("egress" , "hdr.common_report_header.eg_port") header common_report_header_t {
    bit<32> switch_id;
    bit<7>  pad1;
    bit<9>  ig_port;
    bit<7>  pad2;
    bit<9>  eg_port;
    bit<3>  pad3;
    bit<5>  queue_id;
}

header drop_report_header_t {
    bit<8>  drop_reason;
    @padding 
    bit<16> pad;
}

header local_report_header_t {
    bit<5>  pad1;
    bit<19> queue_occupancy;
    bit<32> eg_tstamp;
}

@pa_no_overlay("egress" , "fabric_md.int_report_md.bmd_type") @pa_no_overlay("egress" , "fabric_md.int_report_md.mirror_type") @pa_no_overlay("egress" , "fabric_md.int_report_md.ig_port") @pa_no_overlay("egress" , "fabric_md.int_report_md.eg_port") @pa_no_overlay("egress" , "fabric_md.int_report_md.queue_id") @pa_no_overlay("egress" , "fabric_md.int_report_md.queue_occupancy") @pa_no_overlay("egress" , "fabric_md.int_report_md.ig_tstamp") @pa_no_overlay("egress" , "fabric_md.int_report_md.eg_tstamp") @pa_no_overlay("egress" , "fabric_md.int_report_md.drop_reason") @pa_no_overlay("egress" , "fabric_md.int_report_md.ip_eth_type") @pa_no_overlay("egress" , "fabric_md.int_report_md.report_type") @pa_no_overlay("egress" , "fabric_md.int_report_md.flow_hash") @pa_no_overlay("egress" , "fabric_md.int_report_md.encap_presence") header int_report_metadata_t {
    BridgedMdType_t    bmd_type;
    @padding 
    bit<5>             _pad0;
    FabricMirrorType_t mirror_type;
    @padding 
    bit<7>             _pad1;
    bit<9>             ig_port;
    @padding 
    bit<7>             _pad2;
    bit<9>             eg_port;
    @padding 
    bit<3>             _pad3;
    bit<5>             queue_id;
    @padding 
    bit<5>             _pad4;
    bit<19>            queue_occupancy;
    bit<32>            ig_tstamp;
    bit<32>            eg_tstamp;
    bit<8>             drop_reason;
    bit<16>            ip_eth_type;
    @padding 
    bit<6>             _pad5;
    EncapPresence      encap_presence;
    bit<3>             report_type;
    @padding 
    bit<5>             _pad6;
    flow_hash_t        flow_hash;
}

@flexible struct int_bridged_metadata_t {
    bit<3>          report_type;
    MirrorId_t      mirror_session_id;
    IntDropReason_t drop_reason;
    QueueId_t       queue_id;
    PortId_t        egress_port;
    IntWipType_t    wip_type;
}

struct int_metadata_t {
    bit<32> hop_latency;
    bit<48> timestamp;
    bool    vlan_stripped;
    bool    queue_report;
}

@flexible struct bridged_metadata_base_t {
    flow_hash_t   inner_hash;
    mpls_label_t  mpls_label;
    PortId_t      ig_port;
    bool          is_multicast;
    fwd_type_t    fwd_type;
    vlan_id_t     vlan_id;
    EncapPresence encap_presence;
    bit<8>        mpls_ttl;
    bit<48>       ig_tstamp;
    bit<16>       ip_eth_type;
    bit<10>       stats_flow_id;
    slice_tc_t    slice_tc;
}

header bridged_metadata_t {
    BridgedMdType_t         bmd_type;
    bridged_metadata_base_t base;
    int_bridged_metadata_t  int_bmd;
    bit<1>                  _pad0;
    bit<5>                  _pad2;
}

struct lookup_metadata_t {
    mac_addr_t eth_dst;
    mac_addr_t eth_src;
    bit<16>    eth_type;
    vlan_id_t  vlan_id;
    bool       is_ipv4;
    bit<32>    ipv4_src;
    bit<32>    ipv4_dst;
    bit<8>     ip_proto;
    l4_port_t  l4_sport;
    l4_port_t  l4_dport;
    bit<8>     icmp_type;
    bit<8>     icmp_code;
}

struct common_mirror_metadata_t {
    MirrorId_t      mirror_session_id;
    BridgedMdType_t bmd_type;
}

@pa_auto_init_metadata struct fabric_ingress_metadata_t {
    bridged_metadata_t       bridged;
    flow_hash_t              ecmp_hash;
    lookup_metadata_t        lkp;
    bit<32>                  routing_ipv4_dst;
    bool                     skip_forwarding;
    bool                     skip_next;
    next_id_t                next_id;
    bool                     egress_port_set;
    bool                     punt_to_cpu;
    bool                     ipv4_checksum_err;
    bool                     inner_ipv4_checksum_err;
    slice_id_t               slice_id;
    tc_t                     tc;
    bool                     tc_unknown;
    bool                     is_upf_hit;
    slice_id_t               upf_slice_id;
    tc_t                     upf_tc;
    MeterColor_t             upf_meter_color;
    PortType_t               ig_port_type;
    common_mirror_metadata_t mirror;
}

header common_egress_metadata_t {
    BridgedMdType_t    bmd_type;
    @padding 
    bit<5>             _pad;
    FabricMirrorType_t mirror_type;
}

header packet_in_mirror_metadata_t {
    BridgedMdType_t    bmd_type;
    @padding 
    bit<5>             _pad0;
    FabricMirrorType_t mirror_type;
    @padding 
    bit<7>             _pad1;
    PortId_t           ingress_port;
}

@pa_auto_init_metadata struct fabric_egress_metadata_t {
    bridged_metadata_t    bridged;
    PortId_t              cpu_port;
    int_report_metadata_t int_report_md;
    int_metadata_t        int_md;
    bit<16>               int_ipv4_len;
    bool                  is_int_recirc;
    bit<16>               pkt_length;
}

header fake_ethernet_t {
    @padding 
    bit<48> _pad0;
    @padding 
    bit<48> _pad1;
    bit<16> ether_type;
}

struct ingress_headers_t {
    packet_out_header_t packet_out;
    packet_in_header_t  packet_in;
    fake_ethernet_t     fake_ethernet;
    ethernet_t          ethernet;
    vlan_tag_t          vlan_tag;
    eth_type_t          eth_type;
    mpls_t              mpls;
    ipv4_t              ipv4;
    ipv6_t              ipv6;
    tcp_t               tcp;
    udp_t               udp;
    icmp_t              icmp;
    gtpu_t              gtpu;
    gtpu_options_t      gtpu_options;
    gtpu_ext_psc_t      gtpu_ext_psc;
    vxlan_t             vxlan;
    ethernet_t          inner_ethernet;
    eth_type_t          inner_eth_type;
    ipv4_t              inner_ipv4;
    tcp_t               inner_tcp;
    udp_t               inner_udp;
    icmp_t              inner_icmp;
}

struct egress_headers_t {
    packet_in_header_t     packet_in;
    fake_ethernet_t        fake_ethernet;
    ethernet_t             report_ethernet;
    eth_type_t             report_eth_type;
    mpls_t                 report_mpls;
    ipv4_t                 report_ipv4;
    udp_t                  report_udp;
    report_fixed_header_t  report_fixed_header;
    common_report_header_t common_report_header;
    local_report_header_t  local_report_header;
    drop_report_header_t   drop_report_header;
    ethernet_t             ethernet;
    vlan_tag_t             vlan_tag;
    eth_type_t             eth_type;
    mpls_t                 mpls;
    ipv4_t                 ipv4;
    ipv6_t                 ipv6;
    udp_t                  udp;
}

struct fabric_v1model_metadata_t {
    bool                      skip_egress;
    bool                      do_upf_uplink_recirc;
    bit<1>                    drop_ctl;
    IntReportType_t           int_mirror_type;
    fabric_ingress_metadata_t ingress;
    fabric_egress_metadata_t  egress;
    @field_list(PRESERVE_INT_MD) 
    IntReportType_t           recirc_preserved_report_type;
    @field_list(PRESERVE_INT_MD) 
    FabricPortId_t            recirc_preserved_egress_port;
    @field_list(PRESERVE_INT_MD) 
    IntDropReason_t           recirc_preserved_drop_reason;
    @field_list(PRESERVE_INGRESS_PORT) 
    FabricPortId_t            recirc_preserved_ingress_port;
}

struct v1model_header_t {
    ingress_headers_t ingress;
    egress_headers_t  egress;
}

parser FabricParser(packet_in packet, out v1model_header_t hdr, inout fabric_v1model_metadata_t fabric_md, inout standard_metadata_t standard_md) {
    state start {
        fabric_md.egress.pkt_length = (bit<16>)standard_md.packet_length;
        fabric_md.ingress.bridged.setValid();
        fabric_md.ingress.bridged.bmd_type = BridgedMdType_t.INGRESS_TO_EGRESS;
        fabric_md.ingress.bridged.base.ig_port = standard_md.ingress_port;
        fabric_md.recirc_preserved_ingress_port = (FabricPortId_t)standard_md.ingress_port;
        fabric_md.ingress.bridged.base.ig_tstamp = standard_md.ingress_global_timestamp;
        fabric_md.ingress.egress_port_set = false;
        fabric_md.ingress.punt_to_cpu = false;
        fabric_md.ingress.bridged.base.ip_eth_type = 0;
        fabric_md.ingress.bridged.int_bmd.drop_reason = IntDropReason_t.DROP_REASON_UNKNOWN;
        fabric_md.ingress.bridged.int_bmd.wip_type = INT_IS_NOT_WIP;
        fabric_md.ingress.bridged.base.encap_presence = EncapPresence.NONE;
        fabric_md.ingress.upf_meter_color = MeterColor_t.GREEN;
        transition check_ethernet;
    }
    state check_ethernet {
        fake_ethernet_t tmp = packet.lookahead<fake_ethernet_t>();
        transition select(tmp.ether_type) {
            ETHERTYPE_CPU_LOOPBACK_INGRESS: parse_fake_ethernet;
            ETHERTYPE_CPU_LOOPBACK_EGRESS: parse_fake_ethernet_and_accept;
            ETHERTYPE_PACKET_OUT: check_packet_out;
            ETHERTYPE_INT_WIP_IPV4: parse_int_wip_ipv4;
            ETHERTYPE_INT_WIP_MPLS: parse_int_wip_mpls;
            default: parse_ethernet;
        }
    }
    state check_packet_out {
        packet_out_header_t tmp = packet.lookahead<packet_out_header_t>();
        transition select(tmp.do_forwarding) {
            0: parse_packet_out_and_accept;
            default: strip_packet_out;
        }
    }
    state parse_int_wip_ipv4 {
        hdr.ingress.ethernet.setValid();
        hdr.ingress.eth_type.setValid();
        hdr.ingress.eth_type.value = ETHERTYPE_IPV4;
        fabric_md.ingress.bridged.int_bmd.wip_type = INT_IS_WIP;
        fabric_md.ingress.bridged.base.mpls_label = 0;
        fabric_md.ingress.bridged.base.mpls_ttl = DEFAULT_MPLS_TTL + 1;
        packet.advance(14 * 8);
        transition parse_ipv4;
    }
    state parse_int_wip_mpls {
        hdr.ingress.ethernet.setValid();
        hdr.ingress.eth_type.setValid();
        hdr.ingress.eth_type.value = ETHERTYPE_MPLS;
        fabric_md.ingress.bridged.int_bmd.wip_type = INT_IS_WIP_WITH_MPLS;
        packet.advance(14 * 8);
        transition parse_mpls;
    }
    state parse_packet_out_and_accept {
        packet.extract(hdr.ingress.packet_out);
        transition accept;
    }
    state strip_packet_out {
        packet.advance(14 * 8);
        transition parse_ethernet;
    }
    state parse_fake_ethernet {
        packet.extract(hdr.ingress.fake_ethernet);
        fake_ethernet_t tmp = packet.lookahead<fake_ethernet_t>();
        transition select(tmp.ether_type) {
            ETHERTYPE_INT_WIP_IPV4: parse_int_wip_ipv4;
            ETHERTYPE_INT_WIP_MPLS: parse_int_wip_mpls;
            default: parse_ethernet;
        }
    }
    state parse_fake_ethernet_and_accept {
        packet.extract(hdr.ingress.fake_ethernet);
        transition accept;
    }
    state parse_ethernet {
        packet.extract(hdr.ingress.ethernet);
        transition select(packet.lookahead<bit<16>>()) {
            ETHERTYPE_QINQ: parse_vlan_tag;
            ETHERTYPE_VLAN &&& 0xefff: parse_vlan_tag;
            default: parse_untagged;
        }
    }
    state parse_vlan_tag {
        packet.extract(hdr.ingress.vlan_tag);
        fabric_md.ingress.bridged.base.vlan_id = hdr.ingress.vlan_tag.vlan_id;
        transition select(packet.lookahead<bit<16>>()) {
            default: parse_eth_type;
        }
    }
    state parse_untagged {
        fabric_md.ingress.bridged.base.vlan_id = DEFAULT_VLAN_ID;
        transition parse_eth_type;
    }
    state parse_eth_type {
        packet.extract(hdr.ingress.eth_type);
        transition select(hdr.ingress.eth_type.value) {
            ETHERTYPE_MPLS: parse_mpls;
            ETHERTYPE_IPV4: parse_non_mpls;
            ETHERTYPE_IPV6: parse_non_mpls;
            default: accept;
        }
    }
    state parse_mpls {
        packet.extract(hdr.ingress.mpls);
        fabric_md.ingress.bridged.base.mpls_label = hdr.ingress.mpls.label;
        fabric_md.ingress.bridged.base.mpls_ttl = hdr.ingress.mpls.ttl;
        transition select(packet.lookahead<bit<4>>()) {
            4: parse_ipv4;
            6: parse_ipv6;
            default: reject_packet;
        }
    }
    state reject_packet {
        verify(false, error.PacketRejectedByParser);
        transition accept;
    }
    state parse_non_mpls {
        fabric_md.ingress.bridged.base.mpls_label = 0;
        fabric_md.ingress.bridged.base.mpls_ttl = DEFAULT_MPLS_TTL + 1;
        transition select(hdr.ingress.eth_type.value) {
            ETHERTYPE_IPV4: parse_ipv4;
            ETHERTYPE_IPV6: parse_ipv6;
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ingress.ipv4);
        fabric_md.ingress.routing_ipv4_dst = hdr.ingress.ipv4.dst_addr;
        fabric_md.ingress.bridged.base.ip_eth_type = ETHERTYPE_IPV4;
        transition select(hdr.ingress.ipv4.protocol) {
            PROTO_TCP: parse_tcp;
            PROTO_UDP: parse_udp;
            PROTO_ICMP: parse_icmp;
            default: accept;
        }
    }
    state parse_ipv6 {
        packet.extract(hdr.ingress.ipv6);
        fabric_md.ingress.bridged.base.ip_eth_type = ETHERTYPE_IPV6;
        transition select(hdr.ingress.ipv6.next_hdr) {
            PROTO_TCP: parse_tcp;
            PROTO_UDP: parse_udp;
            PROTO_ICMPV6: parse_icmp;
            default: accept;
        }
    }
    state parse_icmp {
        packet.extract(hdr.ingress.icmp);
        transition accept;
    }
    state parse_tcp {
        packet.extract(hdr.ingress.tcp);
        transition accept;
    }
    state parse_udp {
        packet.extract(hdr.ingress.udp);
        gtpu_t gtpu = packet.lookahead<gtpu_t>();
        transition select(hdr.ingress.udp.dport, gtpu.version, gtpu.msgtype) {
            (GTPU_UDP_PORT, GTP_V1, GTPU_GPDU): parse_gtpu;
            (VXLAN_UDP_PORT, default, default): parse_vxlan;
            default: accept;
        }
    }
    state parse_gtpu {
        packet.extract(hdr.ingress.gtpu);
        transition select(hdr.ingress.gtpu.ex_flag, hdr.ingress.gtpu.seq_flag, hdr.ingress.gtpu.npdu_flag) {
            (0, 0, 0): set_gtpu_only;
            default: parse_gtpu_options;
        }
    }
    state set_gtpu_only {
        fabric_md.ingress.bridged.base.encap_presence = EncapPresence.GTPU_ONLY;
        transition parse_inner_ipv4;
    }
    state parse_gtpu_options {
        packet.extract(hdr.ingress.gtpu_options);
        bit<8> gtpu_ext_len = packet.lookahead<bit<8>>();
        transition select(hdr.ingress.gtpu_options.next_ext, gtpu_ext_len) {
            (GTPU_NEXT_EXT_PSC, GTPU_EXT_PSC_LEN): parse_gtpu_ext_psc;
            default: accept;
        }
    }
    state parse_gtpu_ext_psc {
        packet.extract(hdr.ingress.gtpu_ext_psc);
        fabric_md.ingress.bridged.base.encap_presence = EncapPresence.GTPU_WITH_PSC;
        transition select(hdr.ingress.gtpu_ext_psc.next_ext) {
            GTPU_NEXT_EXT_NONE: parse_inner_ipv4;
            default: accept;
        }
    }
    state parse_vxlan {
        packet.extract(hdr.ingress.vxlan);
        fabric_md.ingress.bridged.base.encap_presence = EncapPresence.VXLAN;
        transition parse_inner_ethernet;
    }
    state parse_inner_ethernet {
        packet.extract(hdr.ingress.inner_ethernet);
        packet.extract(hdr.ingress.inner_eth_type);
        transition select(hdr.ingress.inner_eth_type.value) {
            ETHERTYPE_IPV4: parse_inner_ipv4;
            default: accept;
        }
    }
    state parse_inner_ipv4 {
        packet.extract(hdr.ingress.inner_ipv4);
        transition select(hdr.ingress.inner_ipv4.protocol) {
            PROTO_TCP: parse_inner_tcp;
            PROTO_UDP: parse_inner_udp;
            PROTO_ICMP: parse_inner_icmp;
            default: accept;
        }
    }
    state parse_inner_tcp {
        packet.extract(hdr.ingress.inner_tcp);
        transition accept;
    }
    state parse_inner_udp {
        packet.extract(hdr.ingress.inner_udp);
        transition accept;
    }
    state parse_inner_icmp {
        packet.extract(hdr.ingress.inner_icmp);
        transition accept;
    }
}

control FabricDeparser(packet_out packet, in v1model_header_t hdr) {
    apply {
        packet.emit(hdr.ingress.fake_ethernet);
        packet.emit(hdr.ingress.packet_in);
        packet.emit(hdr.egress.report_ethernet);
        packet.emit(hdr.egress.report_eth_type);
        packet.emit(hdr.egress.report_mpls);
        packet.emit(hdr.egress.report_ipv4);
        packet.emit(hdr.egress.report_udp);
        packet.emit(hdr.egress.report_fixed_header);
        packet.emit(hdr.egress.common_report_header);
        packet.emit(hdr.egress.local_report_header);
        packet.emit(hdr.egress.drop_report_header);
        packet.emit(hdr.ingress.ethernet);
        packet.emit(hdr.ingress.vlan_tag);
        packet.emit(hdr.ingress.eth_type);
        packet.emit(hdr.ingress.mpls);
        packet.emit(hdr.ingress.ipv4);
        packet.emit(hdr.ingress.ipv6);
        packet.emit(hdr.ingress.tcp);
        packet.emit(hdr.ingress.udp);
        packet.emit(hdr.ingress.icmp);
        packet.emit(hdr.ingress.gtpu);
        packet.emit(hdr.ingress.gtpu_options);
        packet.emit(hdr.ingress.gtpu_ext_psc);
        packet.emit(hdr.ingress.vxlan);
        packet.emit(hdr.ingress.inner_ethernet);
        packet.emit(hdr.ingress.inner_eth_type);
        packet.emit(hdr.ingress.inner_ipv4);
        packet.emit(hdr.ingress.inner_tcp);
        packet.emit(hdr.ingress.inner_udp);
        packet.emit(hdr.ingress.inner_icmp);
    }
}

control Acl(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md, inout standard_metadata_t standard_md, inout FabricPortId_t recirc_preserved_egress_port, inout bit<1> drop_ctl) {
    direct_counter(CounterType.packets_and_bytes) acl_counter;
    action set_next_id_acl(next_id_t next_id) {
        fabric_md.next_id = next_id;
        acl_counter.count();
        fabric_md.skip_next = false;
        drop_ctl = 0;
    }
    action copy_to_cpu() {
        clone_preserving_field_list(CloneType.I2E, (bit<32>)PACKET_IN_MIRROR_SESSION_ID, PRESERVE_INGRESS_PORT);
        acl_counter.count();
    }
    action punt_to_cpu() {
        copy_to_cpu();
        fabric_md.skip_next = true;
        fabric_md.punt_to_cpu = true;
        drop_ctl = 1;
    }
    action drop() {
        drop_ctl = 1;
        fabric_md.skip_next = true;
        fabric_md.bridged.int_bmd.drop_reason = IntDropReason_t.DROP_REASON_ACL_DENY;
        acl_counter.count();
    }
    action set_output_port(FabricPortId_t port_num) {
        standard_md.egress_spec = (PortId_t)port_num;
        recirc_preserved_egress_port = port_num;
        fabric_md.egress_port_set = true;
        fabric_md.skip_next = true;
        drop_ctl = 0;
        acl_counter.count();
    }
    action nop_acl() {
        acl_counter.count();
    }
    table acl {
        key = {
            fabric_md.bridged.base.ig_port: ternary @name("ig_port") ;
            fabric_md.lkp.eth_dst         : ternary @name("eth_dst") ;
            fabric_md.lkp.eth_src         : ternary @name("eth_src") ;
            fabric_md.lkp.vlan_id         : ternary @name("vlan_id") ;
            fabric_md.lkp.eth_type        : ternary @name("eth_type") ;
            fabric_md.lkp.ipv4_src        : ternary @name("ipv4_src") ;
            fabric_md.lkp.ipv4_dst        : ternary @name("ipv4_dst") ;
            fabric_md.lkp.ip_proto        : ternary @name("ip_proto") ;
            fabric_md.lkp.icmp_type       : ternary @name("icmp_type") ;
            fabric_md.lkp.icmp_code       : ternary @name("icmp_code") ;
            fabric_md.lkp.l4_sport        : ternary @name("l4_sport") ;
            fabric_md.lkp.l4_dport        : ternary @name("l4_dport") ;
            fabric_md.ig_port_type        : ternary @name("ig_port_type") ;
        }
        actions = {
            set_next_id_acl;
            punt_to_cpu;
            copy_to_cpu;
            drop;
            set_output_port;
            nop_acl;
        }
        const default_action = nop_acl();
        size = 1024;
        counters = acl_counter;
    }
    apply {
        acl.apply();
    }
}

control Next(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md, inout standard_metadata_t standard_md, inout FabricPortId_t recirc_preserved_egress_port) {
    @hidden action output(FabricPortId_t port_num) {
        standard_md.egress_spec = (PortId_t)port_num;
        recirc_preserved_egress_port = port_num;
        fabric_md.egress_port_set = true;
    }
    @hidden action rewrite_smac(mac_addr_t smac) {
        hdr.ethernet.src_addr = smac;
    }
    @hidden action rewrite_dmac(mac_addr_t dmac) {
        hdr.ethernet.dst_addr = dmac;
    }
    @hidden action routing(FabricPortId_t port_num, mac_addr_t smac, mac_addr_t dmac) {
        rewrite_smac(smac);
        rewrite_dmac(dmac);
        output(port_num);
    }
    direct_counter(CounterType.packets_and_bytes) simple_counter;
    action output_simple(FabricPortId_t port_num) {
        output(port_num);
        simple_counter.count();
    }
    action routing_simple(FabricPortId_t port_num, mac_addr_t smac, mac_addr_t dmac) {
        routing(port_num, smac, dmac);
        simple_counter.count();
    }
    table simple {
        key = {
            fabric_md.next_id: exact @name("next_id") ;
        }
        actions = {
            output_simple;
            routing_simple;
            @defaultonly nop;
        }
        const default_action = nop();
        counters = simple_counter;
        size = 1024;
    }
    @max_group_size(32w16) action_selector(HashAlgorithm.crc16, 32w16, 32w16) hashed_profile;
    direct_counter(CounterType.packets_and_bytes) hashed_counter;
    action output_hashed(FabricPortId_t port_num) {
        output(port_num);
        hashed_counter.count();
    }
    action routing_hashed(FabricPortId_t port_num, mac_addr_t smac, mac_addr_t dmac) {
        routing(port_num, smac, dmac);
        hashed_counter.count();
    }
    table hashed {
        key = {
            fabric_md.next_id  : exact @name("next_id") ;
            fabric_md.ecmp_hash: selector;
        }
        actions = {
            output_hashed;
            routing_hashed;
            @defaultonly nop;
        }
        implementation = hashed_profile;
        counters = hashed_counter;
        const default_action = nop();
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) multicast_counter;
    action set_mcast_group_id(MulticastGroupId_t group_id) {
        standard_md.mcast_grp = group_id;
        fabric_md.bridged.base.is_multicast = true;
        multicast_counter.count();
    }
    action reset_mcast_group_id() {
        standard_md.mcast_grp = 0;
        fabric_md.bridged.base.is_multicast = false;
    }
    table multicast {
        key = {
            fabric_md.next_id: exact @name("next_id") ;
        }
        actions = {
            set_mcast_group_id;
            @defaultonly reset_mcast_group_id;
        }
        counters = multicast_counter;
        const default_action = reset_mcast_group_id();
        size = 1024;
    }
    apply {
        simple.apply();
        hashed.apply();
        multicast.apply();
    }
}

control EgressNextControl(inout ingress_headers_t hdr, inout fabric_egress_metadata_t fabric_md, inout standard_metadata_t standard_md, inout IntDropReason_t recirc_preserved_drop_reason, inout bit<1> drop_ctl) {
    @hidden action pop_mpls_if_present() {
        hdr.mpls.setInvalid();
        hdr.eth_type.value = fabric_md.bridged.base.ip_eth_type;
    }
    @hidden action set_mpls() {
        hdr.mpls.setValid();
        hdr.mpls.label = fabric_md.bridged.base.mpls_label;
        hdr.mpls.tc = 3w0;
        hdr.mpls.bos = 1w1;
        hdr.mpls.ttl = fabric_md.bridged.base.mpls_ttl;
        hdr.eth_type.value = ETHERTYPE_MPLS;
    }
    @hidden action push_outer_vlan() {
        hdr.vlan_tag.setValid();
        hdr.vlan_tag.eth_type = ETHERTYPE_VLAN;
        hdr.vlan_tag.vlan_id = fabric_md.bridged.base.vlan_id;
    }
    direct_counter(CounterType.packets_and_bytes) egress_vlan_counter;
    action push_vlan() {
        push_outer_vlan();
        egress_vlan_counter.count();
    }
    action pop_vlan() {
        hdr.vlan_tag.setInvalid();
        egress_vlan_counter.count();
    }
    action drop() {
        drop_ctl = 1;
        egress_vlan_counter.count();
        recirc_preserved_drop_reason = IntDropReason_t.DROP_REASON_EGRESS_NEXT_MISS;
    }
    table egress_vlan {
        key = {
            fabric_md.bridged.base.vlan_id: exact @name("vlan_id") ;
            standard_md.egress_port       : exact @name("eg_port") ;
        }
        actions = {
            push_vlan;
            pop_vlan;
            @defaultonly drop;
        }
        const default_action = drop();
        counters = egress_vlan_counter;
        size = 1024;
    }
    apply {
        if (fabric_md.bridged.base.is_multicast && fabric_md.bridged.base.ig_port == standard_md.egress_port) {
            fabric_md.bridged.int_bmd.report_type = INT_REPORT_TYPE_NO_REPORT;
            drop_ctl = 1;
        }
        if (fabric_md.bridged.base.mpls_label == 0) {
            if (hdr.mpls.isValid()) {
                pop_mpls_if_present();
            }
        } else {
            set_mpls();
        }
        if (!fabric_md.is_int_recirc) {
            egress_vlan.apply();
        }
        bool regular_packet = true;
        regular_packet = !(fabric_md.bridged.bmd_type == BridgedMdType_t.INT_INGRESS_DROP || fabric_md.bridged.bmd_type == BridgedMdType_t.EGRESS_MIRROR);
        if (hdr.mpls.isValid()) {
            hdr.mpls.ttl = hdr.mpls.ttl - 1;
            if (hdr.mpls.ttl == 0) {
                drop_ctl = 1;
                recirc_preserved_drop_reason = IntDropReason_t.DROP_REASON_MPLS_TTL_ZERO;
            }
        } else {
            if (hdr.ipv4.isValid() && fabric_md.bridged.base.fwd_type != FWD_BRIDGING) {
                if (regular_packet) {
                    hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
                }
                if (hdr.ipv4.ttl == 0) {
                    drop_ctl = 1;
                    recirc_preserved_drop_reason = IntDropReason_t.DROP_REASON_IP_TTL_ZERO;
                }
            } else if (hdr.ipv6.isValid() && fabric_md.bridged.base.fwd_type != FWD_BRIDGING) {
                if (regular_packet) {
                    hdr.ipv6.hop_limit = hdr.ipv6.hop_limit - 1;
                }
                if (hdr.ipv6.hop_limit == 0) {
                    drop_ctl = 1;
                    recirc_preserved_drop_reason = IntDropReason_t.DROP_REASON_IP_TTL_ZERO;
                }
            }
        }
    }
}

const bit<10> UNSET_FLOW_ID = 0;
control StatsIngress(in lookup_metadata_t lkp, in PortId_t ig_port, out bit<10> stats_flow_id) {
    direct_counter(CounterType.packets_and_bytes) flow_counter;
    action count(bit<10> flow_id) {
        stats_flow_id = flow_id;
        flow_counter.count();
    }
    table flows {
        key = {
            lkp.ipv4_src: ternary @name("ipv4_src") ;
            lkp.ipv4_dst: ternary @name("ipv4_dst") ;
            lkp.ip_proto: ternary @name("ip_proto") ;
            lkp.l4_sport: ternary @name("l4_sport") ;
            lkp.l4_dport: ternary @name("l4_dport") ;
            ig_port     : exact @name("ig_port") ;
        }
        actions = {
            count;
        }
        const default_action = count(UNSET_FLOW_ID);
        const size = 1 << 10;
        counters = flow_counter;
    }
    apply {
        flows.apply();
    }
}

control StatsEgress(in bit<10> stats_flow_id, in PortId_t eg_port, in BridgedMdType_t bmd_type) {
    direct_counter(CounterType.packets_and_bytes) flow_counter;
    action count() {
        flow_counter.count();
    }
    table flows {
        key = {
            stats_flow_id: exact @name("stats_flow_id") ;
            eg_port      : exact @name("eg_port") ;
        }
        actions = {
            count;
        }
        const default_action = count;
        const size = 1 << 10;
        counters = flow_counter;
    }
    apply {
        if (bmd_type == BridgedMdType_t.INGRESS_TO_EGRESS) {
            flows.apply();
        }
    }
}

control Hasher(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md) {
    flow_hash_t max = 0xffffffff;
    flow_hash_t base = 0;
    apply {
        hash(fabric_md.bridged.base.inner_hash, HashAlgorithm.crc32, base, { fabric_md.lkp.ipv4_src, fabric_md.lkp.ipv4_dst, fabric_md.lkp.ip_proto, fabric_md.lkp.l4_sport, fabric_md.lkp.l4_dport }, max);
        if (hdr.gtpu.isValid()) {
            hash(fabric_md.ecmp_hash, HashAlgorithm.crc32, base, { hdr.ipv4.src_addr, hdr.ipv4.dst_addr, hdr.gtpu.teid }, max);
        } else if (fabric_md.lkp.is_ipv4) {
            fabric_md.ecmp_hash = fabric_md.bridged.base.inner_hash;
        } else {
            fabric_md.bridged.base.inner_hash = 0;
            hash(fabric_md.ecmp_hash, HashAlgorithm.crc32, base, { hdr.ethernet.dst_addr, hdr.ethernet.src_addr, hdr.eth_type.value }, max);
        }
    }
}

control IngressSliceTcClassifier(inout ingress_headers_t hdr, inout standard_metadata_t standard_md, inout fabric_ingress_metadata_t fabric_md) {
    direct_counter(CounterType.packets) classifier_stats;
    action set_slice_id_tc(slice_id_t slice_id, tc_t tc) {
        fabric_md.slice_id = slice_id;
        fabric_md.tc = tc;
        fabric_md.tc_unknown = false;
        classifier_stats.count();
    }
    action no_classification() {
        set_slice_id_tc(DEFAULT_SLICE_ID, DEFAULT_TC);
        fabric_md.tc_unknown = true;
    }
    action trust_dscp() {
        fabric_md.slice_id = hdr.ipv4.dscp[4 + 2 - 1:2];
        fabric_md.tc = hdr.ipv4.dscp[2 - 1:0];
        fabric_md.tc_unknown = false;
        classifier_stats.count();
    }
    table classifier {
        key = {
            fabric_md.bridged.base.ig_port: ternary @name("ig_port") ;
            fabric_md.lkp.ipv4_src        : ternary @name("ipv4_src") ;
            fabric_md.lkp.ipv4_dst        : ternary @name("ipv4_dst") ;
            fabric_md.lkp.ip_proto        : ternary @name("ip_proto") ;
            fabric_md.lkp.l4_sport        : ternary @name("l4_sport") ;
            fabric_md.lkp.l4_dport        : ternary @name("l4_dport") ;
        }
        actions = {
            set_slice_id_tc;
            trust_dscp;
            @defaultonly no_classification;
        }
        const default_action = no_classification();
        counters = classifier_stats;
        size = 512;
    }
    apply {
        classifier.apply();
    }
}

control IngressQos(inout fabric_ingress_metadata_t fabric_md, inout standard_metadata_t standard_md, inout bit<1> drop_ctl) {
    bit<2> packet_color = 2w0;
    @hidden action use_upf() {
        fabric_md.bridged.base.slice_tc = fabric_md.upf_slice_id ++ fabric_md.upf_tc;
    }
    @hidden action use_default() {
        fabric_md.bridged.base.slice_tc = fabric_md.slice_id ++ fabric_md.tc;
    }
    @hidden table set_slice_tc {
        key = {
            fabric_md.is_upf_hit: exact;
        }
        actions = {
            use_upf;
            use_default;
        }
        const size = 2;
        const entries = {
                        true : use_upf;
                        false : use_default;
        }
    }
    meter(1 << 4 + 2, MeterType.bytes) slice_tc_meter;
    direct_counter(CounterType.packets) queues_stats;
    action set_queue(QueueId_t qid) {
        queues_stats.count();
    }
    action meter_drop() {
        drop_ctl = 1;
        fabric_md.bridged.int_bmd.drop_reason = IntDropReason_t.DROP_REASON_INGRESS_QOS_METER;
        queues_stats.count();
    }
    table queues {
        key = {
            fabric_md.bridged.base.slice_tc: exact @name("slice_tc") ;
            packet_color                   : ternary @name("color") ;
        }
        actions = {
            set_queue;
            meter_drop;
        }
        const default_action = set_queue(QUEUE_ID_BEST_EFFORT);
        counters = queues_stats;
        size = 1 << 4 + 2 + 1;
    }
    action set_default_tc(tc_t tc) {
        fabric_md.bridged.base.slice_tc = fabric_md.bridged.base.slice_tc[4 + 2 - 1:2] ++ tc;
    }
    table default_tc {
        key = {
            fabric_md.bridged.base.slice_tc: ternary @name("slice_tc") ;
            fabric_md.tc_unknown           : exact @name("tc_unknown") ;
        }
        actions = {
            set_default_tc;
            @defaultonly nop;
        }
        const default_action = nop;
        size = 1 << 4;
    }
    apply {
        set_slice_tc.apply();
        default_tc.apply();
        if (fabric_md.upf_meter_color != MeterColor_t.RED) {
            slice_tc_meter.execute_meter((bit<32>)fabric_md.bridged.base.slice_tc, packet_color);
        } else {
            packet_color = MeterColor_t.RED;
        }
        queues.apply();
    }
}

control EgressDscpRewriter(inout fabric_egress_metadata_t fabric_md, inout standard_metadata_t standard_md, inout ingress_headers_t hdr) {
    bit<6> tmp_dscp = fabric_md.bridged.base.slice_tc;
    action rewrite() {
    }
    action clear() {
        tmp_dscp = 0;
    }
    table rewriter {
        key = {
            standard_md.egress_port: exact @name("eg_port") ;
        }
        actions = {
            rewrite;
            clear;
            @defaultonly nop;
        }
        const default_action = nop;
        size = 512;
    }
    apply {
        if (rewriter.apply().hit) {
            if (hdr.ipv4.isValid()) {
                hdr.ipv4.dscp = tmp_dscp;
            }
        }
    }
}

control FabricVerifyChecksum(inout v1model_header_t hdr, inout fabric_v1model_metadata_t meta) {
    apply {
        verify_checksum(hdr.ingress.ipv4.isValid(), { hdr.ingress.ipv4.version, hdr.ingress.ipv4.ihl, hdr.ingress.ipv4.dscp, hdr.ingress.ipv4.ecn, hdr.ingress.ipv4.total_len, hdr.ingress.ipv4.identification, hdr.ingress.ipv4.flags, hdr.ingress.ipv4.frag_offset, hdr.ingress.ipv4.ttl, hdr.ingress.ipv4.protocol, hdr.ingress.ipv4.src_addr, hdr.ingress.ipv4.dst_addr }, hdr.ingress.ipv4.hdr_checksum, HashAlgorithm.csum16);
        verify_checksum(hdr.ingress.inner_ipv4.isValid(), { hdr.ingress.inner_ipv4.version, hdr.ingress.inner_ipv4.ihl, hdr.ingress.inner_ipv4.dscp, hdr.ingress.inner_ipv4.ecn, hdr.ingress.inner_ipv4.total_len, hdr.ingress.inner_ipv4.identification, hdr.ingress.inner_ipv4.flags, hdr.ingress.inner_ipv4.frag_offset, hdr.ingress.inner_ipv4.ttl, hdr.ingress.inner_ipv4.protocol, hdr.ingress.inner_ipv4.src_addr, hdr.ingress.inner_ipv4.dst_addr }, hdr.ingress.inner_ipv4.hdr_checksum, HashAlgorithm.csum16);
    }
}

control FabricComputeChecksum(inout v1model_header_t hdr, inout fabric_v1model_metadata_t fabric_md) {
    apply {
        update_checksum(hdr.ingress.ipv4.isValid(), { hdr.ingress.ipv4.version, hdr.ingress.ipv4.ihl, hdr.ingress.ipv4.dscp, hdr.ingress.ipv4.ecn, hdr.ingress.ipv4.total_len, hdr.ingress.ipv4.identification, hdr.ingress.ipv4.flags, hdr.ingress.ipv4.frag_offset, hdr.ingress.ipv4.ttl, hdr.ingress.ipv4.protocol, hdr.ingress.ipv4.src_addr, hdr.ingress.ipv4.dst_addr }, hdr.ingress.ipv4.hdr_checksum, HashAlgorithm.csum16);
        update_checksum(hdr.ingress.inner_ipv4.isValid(), { hdr.ingress.inner_ipv4.version, hdr.ingress.inner_ipv4.ihl, hdr.ingress.inner_ipv4.dscp, hdr.ingress.inner_ipv4.ecn, hdr.ingress.inner_ipv4.total_len, hdr.ingress.inner_ipv4.identification, hdr.ingress.inner_ipv4.flags, hdr.ingress.inner_ipv4.frag_offset, hdr.ingress.inner_ipv4.ttl, hdr.ingress.inner_ipv4.protocol, hdr.ingress.inner_ipv4.src_addr, hdr.ingress.inner_ipv4.dst_addr }, hdr.ingress.inner_ipv4.hdr_checksum, HashAlgorithm.csum16);
        update_checksum(hdr.egress.report_ipv4.isValid(), { hdr.egress.report_ipv4.version, hdr.egress.report_ipv4.ihl, hdr.egress.report_ipv4.dscp, hdr.egress.report_ipv4.ecn, hdr.egress.report_ipv4.total_len, hdr.egress.report_ipv4.identification, hdr.egress.report_ipv4.flags, hdr.egress.report_ipv4.frag_offset, hdr.egress.report_ipv4.ttl, hdr.egress.report_ipv4.protocol, hdr.egress.report_ipv4.src_addr, hdr.egress.report_ipv4.dst_addr }, hdr.egress.report_ipv4.hdr_checksum, HashAlgorithm.csum16);
    }
}

control PacketIoIngress(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md, inout bool skip_egress, inout standard_metadata_t standard_md, inout FabricPortId_t recirc_preserved_egress_port) {
    @hidden action do_packet_out() {
        standard_md.egress_spec = (PortId_t)hdr.packet_out.egress_port;
        recirc_preserved_egress_port = hdr.packet_out.egress_port;
        fabric_md.egress_port_set = true;
        hdr.packet_out.setInvalid();
        skip_egress = true;
        fabric_md.bridged.setInvalid();
        exit;
    }
    apply {
        if (hdr.packet_out.isValid()) {
            do_packet_out();
        }
    }
}

control PacketIoEgress(inout ingress_headers_t hdr, inout fabric_egress_metadata_t fabric_md, inout standard_metadata_t standard_md, in FabricPortId_t preserved_ig_port) {
    action set_switch_info(FabricPortId_t cpu_port) {
        fabric_md.cpu_port = (PortId_t)cpu_port;
    }
    table switch_info {
        actions = {
            set_switch_info;
            @defaultonly nop;
        }
        default_action = nop;
        const size = 1;
    }
    apply {
        switch_info.apply();
        if (standard_md.egress_port == fabric_md.cpu_port) {
            hdr.packet_in.setValid();
            hdr.packet_in.ingress_port = preserved_ig_port;
            hdr.fake_ethernet.setInvalid();
            exit;
        }
        if (hdr.fake_ethernet.isValid() && hdr.fake_ethernet.ether_type == ETHERTYPE_CPU_LOOPBACK_EGRESS) {
            fabric_md.pkt_length = (bit<16>)standard_md.packet_length - 14;
        }
    }
}

control PreNext(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md) {
    direct_counter(CounterType.packets_and_bytes) next_mpls_counter;
    action set_mpls_label(mpls_label_t label) {
        fabric_md.bridged.base.mpls_label = label;
        next_mpls_counter.count();
    }
    table next_mpls {
        key = {
            fabric_md.next_id: exact @name("next_id") ;
        }
        actions = {
            set_mpls_label;
            @defaultonly nop;
        }
        const default_action = nop();
        counters = next_mpls_counter;
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) next_vlan_counter;
    action set_vlan(vlan_id_t vlan_id) {
        fabric_md.bridged.base.vlan_id = vlan_id;
        next_vlan_counter.count();
    }
    table next_vlan {
        key = {
            fabric_md.next_id: exact @name("next_id") ;
        }
        actions = {
            set_vlan;
            @defaultonly nop;
        }
        const default_action = nop();
        counters = next_vlan_counter;
        size = 1024;
    }
    apply {
        next_mpls.apply();
        next_vlan.apply();
    }
}

control Filtering(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md, inout standard_metadata_t standard_md) {
    direct_counter(CounterType.packets_and_bytes) ingress_port_vlan_counter;
    action deny() {
        fabric_md.skip_forwarding = true;
        fabric_md.skip_next = true;
        fabric_md.ig_port_type = PortType_t.UNKNOWN;
        fabric_md.bridged.int_bmd.drop_reason = IntDropReason_t.DROP_REASON_PORT_VLAN_MAPPING_MISS;
        ingress_port_vlan_counter.count();
    }
    action permit(PortType_t port_type) {
        fabric_md.ig_port_type = port_type;
        ingress_port_vlan_counter.count();
    }
    action permit_with_internal_vlan(vlan_id_t vlan_id, PortType_t port_type) {
        fabric_md.bridged.base.vlan_id = vlan_id;
        permit(port_type);
    }
    table ingress_port_vlan {
        key = {
            fabric_md.bridged.base.ig_port: exact @name("ig_port") ;
            hdr.vlan_tag.isValid()        : exact @name("vlan_is_valid") ;
            hdr.vlan_tag.vlan_id          : ternary @name("vlan_id") ;
        }
        actions = {
            deny();
            permit();
            permit_with_internal_vlan();
        }
        const default_action = deny();
        counters = ingress_port_vlan_counter;
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) fwd_classifier_counter;
    action set_forwarding_type(fwd_type_t fwd_type) {
        fabric_md.bridged.base.fwd_type = fwd_type;
        fwd_classifier_counter.count();
    }
    counter(8, CounterType.packets_and_bytes) fwd_type_counter;
    table fwd_classifier {
        key = {
            fabric_md.bridged.base.ig_port    : exact @name("ig_port") ;
            fabric_md.lkp.eth_dst             : ternary @name("eth_dst") ;
            fabric_md.lkp.eth_type            : ternary @name("eth_type") ;
            fabric_md.bridged.base.ip_eth_type: exact @name("ip_eth_type") ;
        }
        actions = {
            set_forwarding_type;
        }
        const default_action = set_forwarding_type(FWD_BRIDGING);
        counters = fwd_classifier_counter;
        size = 1024;
    }
    apply {
        ingress_port_vlan.apply();
        fwd_classifier.apply();
        fwd_type_counter.count((bit<32>)fabric_md.bridged.base.fwd_type);
    }
}

control Forwarding(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md, inout standard_metadata_t standard_md, inout bit<1> drop_ctl) {
    action set_int_drop_reason(bit<8> drop_reason) {
        fabric_md.bridged.int_bmd.drop_reason = (IntDropReason_t)drop_reason;
    }
    @hidden action set_next_id(next_id_t next_id) {
        fabric_md.next_id = next_id;
    }
    direct_counter(CounterType.packets_and_bytes) bridging_counter;
    action set_next_id_bridging(next_id_t next_id) {
        set_next_id(next_id);
        bridging_counter.count();
    }
    table bridging {
        key = {
            fabric_md.bridged.base.vlan_id: exact @name("vlan_id") ;
            hdr.ethernet.dst_addr         : ternary @name("eth_dst") ;
        }
        actions = {
            set_next_id_bridging;
            @defaultonly set_int_drop_reason;
        }
        const default_action = set_int_drop_reason(IntDropReason_t.DROP_REASON_BRIDGING_MISS);
        counters = bridging_counter;
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) mpls_counter;
    action pop_mpls_and_next(next_id_t next_id) {
        hdr.mpls.setInvalid();
        hdr.eth_type.value = fabric_md.bridged.base.ip_eth_type;
        fabric_md.bridged.base.mpls_label = 0;
        set_next_id(next_id);
        mpls_counter.count();
    }
    table mpls {
        key = {
            fabric_md.bridged.base.mpls_label: exact @name("mpls_label") ;
        }
        actions = {
            pop_mpls_and_next;
            @defaultonly set_int_drop_reason;
        }
        const default_action = set_int_drop_reason(IntDropReason_t.DROP_REASON_MPLS_MISS);
        counters = mpls_counter;
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) routing_v4_counter;
    action set_next_id_routing_v4(next_id_t next_id) {
        set_next_id(next_id);
        routing_v4_counter.count();
    }
    action nop_routing_v4() {
        routing_v4_counter.count();
    }
    action drop_routing_v4() {
        fabric_md.skip_next = true;
        routing_v4_counter.count();
        drop_ctl = 1;
    }
    table routing_v4 {
        key = {
            fabric_md.routing_ipv4_dst: lpm @name("ipv4_dst") ;
        }
        actions = {
            set_next_id_routing_v4;
            nop_routing_v4;
            drop_routing_v4;
            @defaultonly set_int_drop_reason;
        }
        default_action = set_int_drop_reason(IntDropReason_t.DROP_REASON_ROUTING_V4_MISS);
        counters = routing_v4_counter;
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) routing_v6_counter;
    action set_next_id_routing_v6(next_id_t next_id) {
        set_next_id(next_id);
        routing_v6_counter.count();
    }
    action drop_routing_v6() {
        fabric_md.skip_next = true;
        routing_v6_counter.count();
        drop_ctl = 1;
    }
    table routing_v6 {
        key = {
            hdr.ipv6.dst_addr: lpm @name("ipv6_dst") ;
        }
        actions = {
            set_next_id_routing_v6;
            drop_routing_v6;
            @defaultonly set_int_drop_reason;
        }
        default_action = set_int_drop_reason(IntDropReason_t.DROP_REASON_ROUTING_V6_MISS);
        counters = routing_v6_counter;
        size = 1024;
    }
    apply {
        if (hdr.ethernet.isValid() && fabric_md.bridged.base.fwd_type == FWD_BRIDGING) {
            bridging.apply();
        } else if (hdr.mpls.isValid() && fabric_md.bridged.base.fwd_type == FWD_MPLS) {
            mpls.apply();
        } else if (fabric_md.lkp.is_ipv4 && (fabric_md.bridged.base.fwd_type == FWD_IPV4_UNICAST || fabric_md.bridged.base.fwd_type == FWD_IPV4_MULTICAST)) {
            routing_v4.apply();
        } else if (hdr.ipv6.isValid() && fabric_md.bridged.base.fwd_type == FWD_IPV6_UNICAST) {
            routing_v6.apply();
        }
    }
}

control LookupMdInit(in ingress_headers_t hdr, out lookup_metadata_t lkp_md) {
    apply {
        lkp_md.eth_dst = hdr.ethernet.dst_addr;
        lkp_md.eth_src = hdr.ethernet.src_addr;
        lkp_md.eth_type = hdr.eth_type.value;
        lkp_md.vlan_id = 0;
        if (hdr.vlan_tag.isValid()) {
            lkp_md.vlan_id = hdr.vlan_tag.vlan_id;
        }
        lkp_md.is_ipv4 = false;
        lkp_md.ipv4_src = 0;
        lkp_md.ipv4_dst = 0;
        lkp_md.ip_proto = 0;
        lkp_md.l4_sport = 0;
        lkp_md.l4_dport = 0;
        lkp_md.icmp_type = 0;
        lkp_md.icmp_code = 0;
        if (hdr.inner_ipv4.isValid()) {
            lkp_md.is_ipv4 = true;
            lkp_md.ipv4_src = hdr.inner_ipv4.src_addr;
            lkp_md.ipv4_dst = hdr.inner_ipv4.dst_addr;
            lkp_md.ip_proto = hdr.inner_ipv4.protocol;
            if (hdr.inner_tcp.isValid()) {
                lkp_md.l4_sport = hdr.inner_tcp.sport;
                lkp_md.l4_dport = hdr.inner_tcp.dport;
            } else if (hdr.inner_udp.isValid()) {
                lkp_md.l4_sport = hdr.inner_udp.sport;
                lkp_md.l4_dport = hdr.inner_udp.dport;
            } else if (hdr.inner_icmp.isValid()) {
                lkp_md.icmp_type = hdr.inner_icmp.icmp_type;
                lkp_md.icmp_code = hdr.inner_icmp.icmp_code;
            }
        } else if (hdr.ipv4.isValid()) {
            lkp_md.is_ipv4 = true;
            lkp_md.ipv4_src = hdr.ipv4.src_addr;
            lkp_md.ipv4_dst = hdr.ipv4.dst_addr;
            lkp_md.ip_proto = hdr.ipv4.protocol;
            if (hdr.tcp.isValid()) {
                lkp_md.l4_sport = hdr.tcp.sport;
                lkp_md.l4_dport = hdr.tcp.dport;
            } else if (hdr.udp.isValid()) {
                lkp_md.l4_sport = hdr.udp.sport;
                lkp_md.l4_dport = hdr.udp.dport;
            } else if (hdr.icmp.isValid()) {
                lkp_md.icmp_type = hdr.icmp.icmp_type;
                lkp_md.icmp_code = hdr.icmp.icmp_code;
            }
        }
    }
}

control IntWatchlist(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md, inout standard_metadata_t standard_md, inout IntReportType_t recirc_preserved_report_type) {
    direct_counter(CounterType.packets_and_bytes) watchlist_counter;
    action mark_to_report() {
        fabric_md.bridged.int_bmd.report_type = INT_REPORT_TYPE_FLOW;
        recirc_preserved_report_type = INT_REPORT_TYPE_FLOW;
        watchlist_counter.count();
    }
    action no_report() {
        fabric_md.bridged.int_bmd.report_type = INT_REPORT_TYPE_NO_REPORT;
        recirc_preserved_report_type = INT_REPORT_TYPE_NO_REPORT;
    }
    action no_report_collector() {
        fabric_md.bridged.int_bmd.report_type = INT_REPORT_TYPE_NO_REPORT;
    }
    table watchlist {
        key = {
            fabric_md.lkp.is_ipv4 : exact @name("ipv4_valid") ;
            fabric_md.lkp.ipv4_src: ternary @name("ipv4_src") ;
            fabric_md.lkp.ipv4_dst: ternary @name("ipv4_dst") ;
            fabric_md.lkp.ip_proto: ternary @name("ip_proto") ;
            fabric_md.lkp.l4_sport: range @name("l4_sport") ;
            fabric_md.lkp.l4_dport: range @name("l4_dport") ;
        }
        actions = {
            mark_to_report;
            no_report_collector;
            @defaultonly no_report();
        }
        const default_action = no_report();
        const size = 64;
        counters = watchlist_counter;
    }
    apply {
        watchlist.apply();
    }
}

control IntIngress(inout ingress_headers_t hdr, inout fabric_ingress_metadata_t fabric_md, inout standard_metadata_t standard_md, inout bit<1> drop_ctl) {
    direct_counter(CounterType.packets_and_bytes) drop_report_counter;
    @hidden action report_drop() {
        fabric_md.bridged.bmd_type = BridgedMdType_t.INT_INGRESS_DROP;
        fabric_md.bridged.int_bmd.report_type = INT_REPORT_TYPE_DROP;
        fabric_md.bridged.base.vlan_id = DEFAULT_VLAN_ID;
        fabric_md.bridged.base.mpls_label = 0;
        drop_ctl = 0;
        standard_md.egress_spec = FAKE_V1MODEL_RECIRC_PORT;
        drop_report_counter.count();
    }
    @hidden table drop_report {
        key = {
            fabric_md.bridged.int_bmd.report_type: exact @name("int_report_type") ;
            drop_ctl                             : exact @name("drop_ctl") ;
            fabric_md.punt_to_cpu                : exact @name("punt_to_cpu") ;
            fabric_md.egress_port_set            : exact @name("egress_port_set") ;
            standard_md.mcast_grp                : ternary @name("mcast_group_id") ;
        }
        actions = {
            report_drop;
            @defaultonly nop;
        }
        const entries = {
                        (INT_REPORT_TYPE_FLOW, 1, false, false, default) : report_drop();
                        (INT_REPORT_TYPE_FLOW, 1, false, true, default) : report_drop();
                        (INT_REPORT_TYPE_FLOW, 0, false, false, 0) : report_drop();
        }
        const default_action = nop();
        counters = drop_report_counter;
    }
    apply {
        fabric_md.bridged.int_bmd.egress_port = standard_md.egress_spec;
        fabric_md.bridged.int_bmd.queue_id = 0;
        drop_report.apply();
    }
}

control IntEgress(inout v1model_header_t hdr_v1model, inout fabric_v1model_metadata_t fabric_v1model, inout standard_metadata_t standard_md) {
    const bit<48> DEFAULT_TIMESTAMP_MASK = 0xffffc0000000;
    const bit<32> DEFAULT_HOP_LATENCY_MASK = 0xffffff00;
    egress_headers_t hdr = hdr_v1model.egress;
    fabric_egress_metadata_t fabric_md = fabric_v1model.egress;
    direct_counter(CounterType.packets_and_bytes) report_counter;
    direct_counter(CounterType.packets_and_bytes) int_metadata_counter;
    QueueId_t egress_qid = 0;
    @hidden register<bit<32>>(1024) seq_number;
    @hidden action get_seq_number(in bit<32> seq_number_idx, out bit<32> result) {
        bit<32> reg = 0;
        seq_number.read(reg, seq_number_idx);
        reg = reg + 1;
        result = reg;
        seq_number.write(seq_number_idx, reg);
    }
    action check_quota() {
    }
    action reset_quota() {
    }
    table queue_latency_thresholds {
        key = {
            egress_qid                         : exact @name("egress_qid") ;
            fabric_md.int_md.hop_latency[31:16]: range @name("hop_latency_upper") ;
            fabric_md.int_md.hop_latency[15:0] : range @name("hop_latency_lower") ;
        }
        actions = {
            check_quota;
            reset_quota;
            @defaultonly nop;
        }
        default_action = nop();
        const size = 32 * 4;
    }
    action set_config(bit<32> hop_latency_mask, bit<48> timestamp_mask) {
        fabric_md.int_md.hop_latency = fabric_md.int_md.hop_latency & hop_latency_mask;
        fabric_md.int_md.timestamp = fabric_md.int_md.timestamp & timestamp_mask;
    }
    table config {
        actions = {
            @defaultonly set_config;
        }
        default_action = set_config(DEFAULT_HOP_LATENCY_MASK, DEFAULT_TIMESTAMP_MASK);
        const size = 1;
    }
    @hidden action _report_encap_common(ipv4_addr_t src_ip, ipv4_addr_t mon_ip, l4_port_t mon_port, bit<32> switch_id) {
        random(hdr.report_ipv4.identification, 0, 0xffff);
        hdr.report_ipv4.src_addr = src_ip;
        hdr.report_ipv4.dst_addr = mon_ip;
        hdr.report_udp.dport = mon_port;
        get_seq_number((bit<32>)hdr.report_fixed_header.hw_id, hdr.report_fixed_header.seq_no);
        hdr.report_fixed_header.dqf = fabric_md.int_report_md.report_type;
        hdr.common_report_header.switch_id = switch_id;
        hdr.common_report_header.pad1 = 0;
        hdr.common_report_header.pad2 = 0;
        hdr.common_report_header.pad3 = 0;
        hdr.eth_type.value = fabric_md.int_report_md.ip_eth_type;
        fabric_v1model.int_mirror_type = (bit<3>)FabricMirrorType_t.INVALID;
        report_counter.count();
    }
    action do_local_report_encap(ipv4_addr_t src_ip, ipv4_addr_t mon_ip, l4_port_t mon_port, bit<32> switch_id) {
        _report_encap_common(src_ip, mon_ip, mon_port, switch_id);
        hdr.report_eth_type.value = ETHERTYPE_INT_WIP_IPV4;
        hdr.report_fixed_header.nproto = NPROTO_TELEMETRY_SWITCH_LOCAL_HEADER;
        hdr.local_report_header.setValid();
    }
    action do_local_report_encap_mpls(ipv4_addr_t src_ip, ipv4_addr_t mon_ip, l4_port_t mon_port, mpls_label_t mon_label, bit<32> switch_id) {
        do_local_report_encap(src_ip, mon_ip, mon_port, switch_id);
        hdr.report_eth_type.value = ETHERTYPE_INT_WIP_MPLS;
        hdr.report_mpls.setValid();
        hdr.report_mpls.tc = 0;
        hdr.report_mpls.bos = 0;
        hdr.report_mpls.ttl = DEFAULT_MPLS_TTL;
        hdr.report_mpls.label = mon_label;
    }
    action do_drop_report_encap(ipv4_addr_t src_ip, ipv4_addr_t mon_ip, l4_port_t mon_port, bit<32> switch_id) {
        _report_encap_common(src_ip, mon_ip, mon_port, switch_id);
        hdr.report_eth_type.value = ETHERTYPE_INT_WIP_IPV4;
        hdr.report_fixed_header.nproto = NPROTO_TELEMETRY_DROP_HEADER;
        hdr.drop_report_header.setValid();
        hdr.local_report_header.setInvalid();
        hdr.drop_report_header.drop_reason = fabric_md.bridged.int_bmd.drop_reason;
    }
    action do_drop_report_encap_mpls(ipv4_addr_t src_ip, ipv4_addr_t mon_ip, l4_port_t mon_port, mpls_label_t mon_label, bit<32> switch_id) {
        do_drop_report_encap(src_ip, mon_ip, mon_port, switch_id);
        hdr.report_eth_type.value = ETHERTYPE_INT_WIP_MPLS;
        hdr.report_mpls.setValid();
        hdr.report_mpls.tc = 0;
        hdr.report_mpls.bos = 0;
        hdr.report_mpls.ttl = DEFAULT_MPLS_TTL;
        hdr.report_mpls.label = mon_label;
        hdr.report_mpls.label = mon_label;
    }
    table report {
        key = {
            fabric_md.int_report_md.bmd_type   : exact @name("bmd_type") ;
            fabric_md.int_report_md.mirror_type: exact @name("mirror_type") ;
            fabric_md.int_report_md.report_type: exact @name("int_report_type") ;
        }
        actions = {
            do_local_report_encap;
            do_local_report_encap_mpls;
            do_drop_report_encap;
            do_drop_report_encap_mpls;
            @defaultonly nop();
        }
        default_action = nop;
        const size = 6;
        counters = report_counter;
    }
    @hidden action init_int_metadata(bit<3> report_type) {
        fabric_md.bridged.int_bmd.mirror_session_id = V1MODEL_INT_MIRROR_SESSION;
        fabric_md.int_report_md.setValid();
        fabric_v1model.int_mirror_type = (bit<3>)FabricMirrorType_t.INT_REPORT;
        fabric_md.int_report_md.bmd_type = BridgedMdType_t.EGRESS_MIRROR;
        fabric_md.int_report_md.mirror_type = FabricMirrorType_t.INT_REPORT;
        fabric_md.int_report_md.report_type = fabric_md.bridged.int_bmd.report_type;
        fabric_md.int_report_md.ig_port = fabric_md.bridged.base.ig_port;
        fabric_md.int_report_md.eg_port = (PortId_t)standard_md.egress_port;
        fabric_md.int_report_md.queue_id = egress_qid;
        fabric_md.int_report_md.queue_occupancy = standard_md.deq_qdepth;
        fabric_md.int_report_md.ig_tstamp = fabric_md.bridged.base.ig_tstamp[31:0];
        fabric_md.int_report_md.eg_tstamp = standard_md.egress_global_timestamp[31:0];
        fabric_md.int_report_md.ip_eth_type = fabric_md.bridged.base.ip_eth_type;
        fabric_md.int_report_md.flow_hash = fabric_md.bridged.base.inner_hash;
        fabric_md.int_report_md.report_type = report_type;
        int_metadata_counter.count();
    }
    @hidden table int_metadata {
        key = {
            fabric_md.bridged.int_bmd.report_type: exact @name("int_report_type") ;
            fabric_v1model.drop_ctl              : exact @name("drop_ctl") ;
            fabric_md.int_md.queue_report        : exact @name("queue_report") ;
        }
        actions = {
            init_int_metadata;
            @defaultonly nop();
        }
        const default_action = nop();
        const entries = {
                        (INT_REPORT_TYPE_FLOW, 0, false) : init_int_metadata(INT_REPORT_TYPE_FLOW);
                        (INT_REPORT_TYPE_FLOW, 1, false) : init_int_metadata(INT_REPORT_TYPE_DROP);
        }
        counters = int_metadata_counter;
    }
    @hidden action adjust_ip_udp_len(bit<16> adjust_ip, bit<16> adjust_udp) {
        hdr_v1model.ingress.ipv4.total_len = fabric_md.pkt_length + adjust_ip;
        hdr_v1model.ingress.udp.len = fabric_md.pkt_length + adjust_udp;
    }
    @hidden table adjust_int_report_hdr_length {
        key = {
            fabric_md.bridged.int_bmd.wip_type: exact @name("is_int_wip") ;
        }
        actions = {
            @defaultonly nop();
            adjust_ip_udp_len;
        }
        const default_action = nop();
        const entries = {
                        INT_IS_WIP : adjust_ip_udp_len(INT_WIP_ADJUST_IP_BYTES, INT_WIP_ADJUST_UDP_BYTES);
                        INT_IS_WIP_WITH_MPLS : adjust_ip_udp_len(INT_WIP_ADJUST_IP_MPLS_BYTES, INT_WIP_ADJUST_UDP_MPLS_BYTES);
        }
    }
    apply {
        fabric_md.int_md.hop_latency = standard_md.egress_global_timestamp[31:0] - fabric_md.bridged.base.ig_tstamp[31:0];
        fabric_md.int_md.timestamp = standard_md.egress_global_timestamp;
        queue_latency_thresholds.apply();
        config.apply();
        hdr.report_fixed_header.hw_id = 4w0 ++ standard_md.egress_spec[8:7];
        if (fabric_md.int_report_md.isValid()) {
            report.apply();
        } else {
            if (int_metadata.apply().hit) {
                clone_preserving_field_list(CloneType.E2E, (bit<32>)fabric_md.bridged.int_bmd.mirror_session_id, PRESERVE_INT_MD);
            }
        }
        adjust_int_report_hdr_length.apply();
        fabric_v1model.egress = fabric_md;
        hdr_v1model.egress = hdr;
    }
}

control IntTnaEgressParserEmulator(inout v1model_header_t hdr_v1model, inout fabric_egress_metadata_t fabric_md, inout standard_metadata_t standard_md) {
    egress_headers_t hdr = hdr_v1model.egress;
    @hidden action set_common_int_headers() {
        hdr.report_ethernet.setValid();
        hdr.report_eth_type.setValid();
        hdr.report_ipv4.setValid();
        hdr.report_ipv4.version = 4w4;
        hdr.report_ipv4.ihl = 4w5;
        hdr.report_ipv4.dscp = 0;
        hdr.report_ipv4.ecn = 2w0;
        hdr.report_ipv4.flags = 0;
        hdr.report_ipv4.frag_offset = 0;
        hdr.report_ipv4.ttl = DEFAULT_IPV4_TTL;
        hdr.report_ipv4.protocol = PROTO_UDP;
        hdr.report_udp.setValid();
        hdr.report_udp.sport = 0;
        hdr.report_fixed_header.setValid();
        hdr.report_fixed_header.ver = 0;
        hdr.report_fixed_header.nproto = NPROTO_TELEMETRY_SWITCH_LOCAL_HEADER;
        hdr.report_fixed_header.rsvd = 0;
        hdr.common_report_header.setValid();
    }
    @hidden action set_common_int_drop_headers() {
        set_common_int_headers();
        fabric_md.int_report_md.setValid();
        fabric_md.int_report_md.ip_eth_type = ETHERTYPE_IPV4;
        fabric_md.int_report_md.report_type = INT_REPORT_TYPE_DROP;
        fabric_md.int_report_md.mirror_type = FabricMirrorType_t.INVALID;
        hdr.drop_report_header.setValid();
    }
    @hidden action parse_int_ingress_drop() {
        set_common_int_drop_headers();
        fabric_md.int_report_md.bmd_type = BridgedMdType_t.INT_INGRESS_DROP;
        fabric_md.int_report_md.encap_presence = fabric_md.bridged.base.encap_presence;
        fabric_md.int_report_md.flow_hash = fabric_md.bridged.base.inner_hash;
        hdr.drop_report_header.drop_reason = fabric_md.bridged.int_bmd.drop_reason;
        hdr.report_fixed_header.ig_tstamp = fabric_md.bridged.base.ig_tstamp[31:0];
        hdr.common_report_header.ig_port = fabric_md.bridged.base.ig_port;
        hdr.common_report_header.eg_port = 0;
        hdr.common_report_header.queue_id = 0;
    }
    @hidden action parse_int_report_mirror() {
        set_common_int_headers();
        fabric_md.bridged.bmd_type = fabric_md.int_report_md.bmd_type;
        fabric_md.bridged.base.vlan_id = DEFAULT_VLAN_ID;
        fabric_md.bridged.base.mpls_label = 0;
        hdr.report_fixed_header.ig_tstamp = fabric_md.int_report_md.ig_tstamp;
        hdr.common_report_header.ig_port = fabric_md.int_report_md.ig_port;
        hdr.common_report_header.eg_port = fabric_md.int_report_md.eg_port;
        hdr.common_report_header.queue_id = fabric_md.int_report_md.queue_id;
        hdr.local_report_header.setValid();
        hdr.local_report_header.queue_occupancy = fabric_md.int_report_md.queue_occupancy;
        hdr.local_report_header.eg_tstamp = fabric_md.int_report_md.eg_tstamp;
    }
    apply {
        fabric_md.is_int_recirc = true;
        hdr_v1model.ingress.vlan_tag.setInvalid();
        if (hdr_v1model.ingress.gtpu.isValid() || hdr_v1model.ingress.vxlan.isValid()) {
            hdr_v1model.ingress.ipv4.setInvalid();
            hdr_v1model.ingress.tcp.setInvalid();
            hdr_v1model.ingress.udp.setInvalid();
            hdr_v1model.ingress.icmp.setInvalid();
            hdr_v1model.ingress.vxlan.setInvalid();
            hdr_v1model.ingress.inner_ethernet.setInvalid();
            hdr_v1model.ingress.inner_eth_type.setInvalid();
            hdr_v1model.ingress.gtpu.setInvalid();
            hdr_v1model.ingress.gtpu_options.setInvalid();
            hdr_v1model.ingress.gtpu_ext_psc.setInvalid();
        }
        if ((bit<8>)fabric_md.bridged.int_bmd.report_type == BridgedMdType_t.INT_INGRESS_DROP) {
            parse_int_ingress_drop();
            recirculate_preserving_field_list(NO_PRESERVATION);
        } else {
            parse_int_report_mirror();
            recirculate_preserving_field_list(PRESERVE_INT_MD);
        }
        hdr_v1model.egress = hdr;
    }
}

control FabricIngress(inout v1model_header_t hdr, inout fabric_v1model_metadata_t fabric_md, inout standard_metadata_t standard_md) {
    LookupMdInit() lkp_md_init;
    StatsIngress() stats;
    PacketIoIngress() pkt_io;
    Filtering() filtering;
    Forwarding() forwarding;
    PreNext() pre_next;
    Acl() acl;
    Next() next;
    Hasher() hasher;
    IngressSliceTcClassifier() slice_tc_classifier;
    IngressQos() qos;
    IntWatchlist() int_watchlist;
    IntIngress() int_ingress;
    apply {
        mark_to_drop(standard_md);
        if (standard_md.parser_error == error.PacketRejectedByParser) {
            exit;
        }
        if (standard_md.instance_type == 4) {
            fabric_md.ingress.bridged.base.ig_port = FAKE_V1MODEL_RECIRC_PORT;
        }
        lkp_md_init.apply(hdr.ingress, fabric_md.ingress.lkp);
        pkt_io.apply(hdr.ingress, fabric_md.ingress, fabric_md.skip_egress, standard_md, fabric_md.recirc_preserved_egress_port);
        int_watchlist.apply(hdr.ingress, fabric_md.ingress, standard_md, fabric_md.recirc_preserved_report_type);
        stats.apply(fabric_md.ingress.lkp, fabric_md.ingress.bridged.base.ig_port, fabric_md.ingress.bridged.base.stats_flow_id);
        slice_tc_classifier.apply(hdr.ingress, standard_md, fabric_md.ingress);
        filtering.apply(hdr.ingress, fabric_md.ingress, standard_md);
        if (!fabric_md.ingress.skip_forwarding) {
            forwarding.apply(hdr.ingress, fabric_md.ingress, standard_md, fabric_md.drop_ctl);
        }
        hasher.apply(hdr.ingress, fabric_md.ingress);
        if (!fabric_md.ingress.skip_next) {
            pre_next.apply(hdr.ingress, fabric_md.ingress);
        }
        acl.apply(hdr.ingress, fabric_md.ingress, standard_md, fabric_md.recirc_preserved_egress_port, fabric_md.drop_ctl);
        if (!fabric_md.ingress.skip_next) {
            next.apply(hdr.ingress, fabric_md.ingress, standard_md, fabric_md.recirc_preserved_egress_port);
        }
        qos.apply(fabric_md.ingress, standard_md, fabric_md.drop_ctl);
        int_ingress.apply(hdr.ingress, fabric_md.ingress, standard_md, fabric_md.drop_ctl);
        fabric_md.egress.bridged = fabric_md.ingress.bridged;
        if (fabric_md.drop_ctl == 1) {
            mark_to_drop(standard_md);
        }
    }
}

control FabricEgress(inout v1model_header_t hdr, inout fabric_v1model_metadata_t fabric_md, inout standard_metadata_t standard_md) {
    StatsEgress() stats;
    PacketIoEgress() pkt_io_egress;
    EgressNextControl() egress_next;
    EgressDscpRewriter() dscp_rewriter;
    IntTnaEgressParserEmulator() parser_emulator;
    IntEgress() int_egress;
    apply {
        fabric_md.egress.cpu_port = 0;
        if (fabric_md.skip_egress) {
            exit;
        }
        if (standard_md.instance_type == 2) {
            fabric_md.egress.bridged.int_bmd.drop_reason = fabric_md.recirc_preserved_drop_reason;
            fabric_md.egress.bridged.int_bmd.report_type = fabric_md.recirc_preserved_report_type;
            parser_emulator.apply(hdr, fabric_md.egress, standard_md);
        }
        if ((bit<8>)fabric_md.egress.bridged.int_bmd.report_type == BridgedMdType_t.INT_INGRESS_DROP) {
            parser_emulator.apply(hdr, fabric_md.egress, standard_md);
        }
        pkt_io_egress.apply(hdr.ingress, fabric_md.egress, standard_md, fabric_md.recirc_preserved_ingress_port);
        stats.apply(fabric_md.egress.bridged.base.stats_flow_id, standard_md.egress_port, fabric_md.egress.bridged.bmd_type);
        egress_next.apply(hdr.ingress, fabric_md.egress, standard_md, fabric_md.recirc_preserved_drop_reason, fabric_md.drop_ctl);
        int_egress.apply(hdr, fabric_md, standard_md);
        dscp_rewriter.apply(fabric_md.egress, standard_md, hdr.ingress);
        if (fabric_md.do_upf_uplink_recirc) {
            recirculate_preserving_field_list(NO_PRESERVATION);
        }
        if (fabric_md.drop_ctl == 1) {
            mark_to_drop(standard_md);
        }
    }
}

V1Switch(FabricParser(), FabricVerifyChecksum(), FabricIngress(), FabricEgress(), FabricComputeChecksum(), FabricDeparser()) main;

