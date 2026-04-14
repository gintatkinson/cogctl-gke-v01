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

import logging
from common.proto.context_pb2 import Device
from .bindings.networks.network.node import node
from .ComposeTermPoint import compose_term_point
from .NameMapping import NameMappings
from .NetworkTypeEnum import NetworkTypeEnum

LOGGER = logging.getLogger(__name__)

MAPPINGS_TE_NODE_NAME = {
    '10.0.10.1'  : 'OA',
    '10.0.20.1'  : 'P',
    '10.0.30.1'  : 'OE',
    '10.0.40.1'  : 'P',

    '128.32.10.1': 'ONT1',
    '128.32.20.1': 'ONT2',
    '128.32.33.5': 'OLT',
}

IGNORE_ENDPOINT_NAMES = {'mgmt', 'eth1'}

def compose_node(
    ietf_node_obj : node, device : Device, name_mappings : NameMappings, network_type : NetworkTypeEnum
) -> None:
    device_name = device.name

    name_mappings.store_device_name(device)

    ietf_node_obj.te_node_id = device_name

    ietf_node_obj.te._set_oper_status('up')
    ietf_node_obj.te.te_node_attributes.admin_status = 'up'
    ietf_node_obj.te.te_node_attributes.name = MAPPINGS_TE_NODE_NAME.get(device_name, device_name)

    for endpoint in device.device_endpoints:
        endpoint_name = endpoint.name
        if endpoint_name in IGNORE_ENDPOINT_NAMES: continue
        if network_type == NetworkTypeEnum.TE_OTN_TOPOLOGY and endpoint.endpoint_type != 'optical': continue

        ietf_tp_obj = ietf_node_obj.termination_point.add(endpoint_name)
        compose_term_point(ietf_tp_obj, device, endpoint, name_mappings, network_type)

    if network_type == NetworkTypeEnum.TE_OTN_TOPOLOGY:
        if device_name in {'10.0.30.1', '10.0.40.1'}:
            ntaw = ietf_node_obj.te.tunnel_termination_point.add('NTAw')
            ntaw.admin_status = 'up'
            ntaw.encoding = 'ietf-te-types:lsp-encoding-oduk'
            ntaw_llc = ntaw.local_link_connectivities.local_link_connectivity.add('500')
            ntaw_llc.is_allowed = True
            ntaw.name = '1-1-1-1-1'
            ntaw._set_oper_status('up')
            ntaw.protection_type = 'ietf-te-types:lsp-protection-unprotected'
            ntaw.switching_capability = 'ietf-te-types:switching-otn'

            ntax = ietf_node_obj.te.tunnel_termination_point.add('NTAx')
            ntax.admin_status = 'up'
            ntax.encoding = 'ietf-te-types:lsp-encoding-oduk'
            ntax_llc = ntax.local_link_connectivities.local_link_connectivity.add('501')
            ntax_llc.is_allowed = True
            ntax.name = '1-1-1-1-1'
            ntax._set_oper_status('up')
            ntax.protection_type = 'ietf-te-types:lsp-protection-unprotected'
            ntax.switching_capability = 'ietf-te-types:switching-otn'
        elif device_name in {'10.0.10.1', '10.0.20.1'}:
            ntax = ietf_node_obj.te.tunnel_termination_point.add('NTAx')
            ntax.admin_status = 'up'
            ntax.encoding = 'ietf-te-types:lsp-encoding-oduk'
            ntax_llc = ntax.local_link_connectivities.local_link_connectivity.add('501')
            ntax_llc.is_allowed = True
            ntax.name = '1-1-1-1-1'
            ntax._set_oper_status('up')
            ntax.protection_type = 'ietf-te-types:lsp-protection-unprotected'
            ntax.switching_capability = 'ietf-te-types:switching-otn'

            ntaw = ietf_node_obj.te.tunnel_termination_point.add('NTAw')
            ntaw.admin_status = 'up'
            ntaw.encoding = 'ietf-te-types:lsp-encoding-oduk'
            ntaw_llc = ntaw.local_link_connectivities.local_link_connectivity.add('500')
            ntaw_llc.is_allowed = True
            ntaw.name = '1-1-1-1-1'
            ntaw._set_oper_status('up')
            ntaw.protection_type = 'ietf-te-types:lsp-protection-unprotected'
            ntaw.switching_capability = 'ietf-te-types:switching-otn'
    elif network_type == NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY:
        if device_name in {'128.32.33.5'}:
            connectivity_matrices = ietf_node_obj.te.te_node_attributes.connectivity_matrices
            lr0 = connectivity_matrices.label_restrictions.label_restriction.add(0)
            lr0.label_start.te_label.vlanid = 21
            lr0.label_end.te_label.vlanid = 21
            lr1 = connectivity_matrices.label_restrictions.label_restriction.add(1)
            lr1.label_start.te_label.vlanid = 31
            lr1.label_end.te_label.vlanid = 31
