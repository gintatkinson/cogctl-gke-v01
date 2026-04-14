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

from common.proto.context_pb2 import Link
from .bindings.networks.network.link import link
from .NameMapping import NameMappings
from .NetworkTypeEnum import NetworkTypeEnum

def compose_link(
    ietf_link_obj : link, link_specs : Link, name_mappings : NameMappings, network_type : NetworkTypeEnum
) -> None:
    src_endpoint_id = link_specs.link_endpoint_ids[0]
    ietf_link_obj.source.source_node = name_mappings.get_device_name(src_endpoint_id.device_id)
    ietf_link_obj.source.source_tp   = name_mappings.get_endpoint_name(src_endpoint_id)

    dst_endpoint_id = link_specs.link_endpoint_ids[-1]
    ietf_link_obj.destination.dest_node = name_mappings.get_device_name(dst_endpoint_id.device_id)
    ietf_link_obj.destination.dest_tp   = name_mappings.get_endpoint_name(dst_endpoint_id)

    ietf_link_obj.te._set_oper_status('up')

    te_link_attrs = ietf_link_obj.te.te_link_attributes
    te_link_attrs.access_type = 'point-to-point'
    te_link_attrs.admin_status = 'up'
    te_link_attrs.name = link_specs.name

    if network_type == NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY:
        link_total_cap_kbps = link_specs.attributes.total_capacity_gbps * 1e6
        link_used_cap_kbps  = link_specs.attributes.used_capacity_gbps * 1e6
        link_avail_cap_kbps = link_total_cap_kbps - link_used_cap_kbps

        te_link_attrs.max_link_bandwidth.te_bandwidth.eth_bandwidth = link_total_cap_kbps
        unresv_bw = te_link_attrs.unreserved_bandwidth.add(7)
        unresv_bw.te_bandwidth.eth_bandwidth = link_avail_cap_kbps
    elif network_type == NetworkTypeEnum.TE_OTN_TOPOLOGY:
        te_link_attrs.te_delay_metric = 1
        oduitem = te_link_attrs.max_link_bandwidth.te_bandwidth.otn.odulist.add('ietf-layer1-types:ODU0')
        oduitem.ts_number = 80

        unresv_bw = te_link_attrs.unreserved_bandwidth.add(7)
        oduitem = unresv_bw.te_bandwidth.otn.odulist.add('ietf-layer1-types:ODU0')
        oduitem.ts_number = 80
