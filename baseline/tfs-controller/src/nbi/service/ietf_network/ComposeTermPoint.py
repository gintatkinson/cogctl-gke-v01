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
from common.proto.context_pb2 import Device, EndPoint
from .bindings.networks.network.node.termination_point import termination_point
from .NameMapping import NameMappings
from .NetworkTypeEnum import NetworkTypeEnum

MAPPINGS_TE_NAME = {
    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.10.1', '200'): '1-1-1-1-1',
    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.10.1', '500'): '1-1-1-1-1',
    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.10.1', '501'): '1-1-1-1-1',

    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.20.1', '500'): '1-1-1-1-1',
    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.20.1', '501'): '1-1-1-1-1',

    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.30.1', '200'): '1-1-1-1-1',
    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.30.1', '500'): '1-1-1-1-1',
    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.30.1', '501'): '1-1-1-1-1',

    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.40.1', '500'): '1-1-1-1-1',
    (NetworkTypeEnum.TE_OTN_TOPOLOGY,      '10.0.40.1', '501'): '1-1-1-1-1',

    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.10.1', '200'): 'endpoint:111',
    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.10.1', '500'): 'endpoint:111',
    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.10.1', '501'): 'endpoint:111',

    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.20.1', '500'): 'endpoint:111',
    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.20.1', '501'): 'endpoint:111',

    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.30.1', '200'): 'endpoint:111',
    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.30.1', '500'): 'endpoint:111',
    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.30.1', '501'): 'endpoint:111',

    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.40.1', '500'): 'endpoint:111',
    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.40.1', '501'): 'endpoint:111',

    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '128.32.33.5', '500') : 'endpoint:111',
}

MAPPINGS_TE_TP_ID = {
    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.10.1', '200'): '128.32.33.254',
    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '10.0.30.1', '200'): '172.10.33.254',

    (NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY, '128.32.33.5', '500') : '128.32.33.2',
}

LOGGER = logging.getLogger(__name__)

def compose_term_point(
    ietf_tp_obj : termination_point, device : Device, endpoint : EndPoint, name_mappings : NameMappings,
    network_type : NetworkTypeEnum
) -> None:
    name_mappings.store_endpoint_name(device, endpoint)

    device_name   = device.name
    endpoint_name = endpoint.name

    ietf_tp_obj.te_tp_id = MAPPINGS_TE_TP_ID.get((network_type, device_name, endpoint_name), endpoint_name)

    if (network_type, device_name, endpoint_name) in MAPPINGS_TE_NAME:
        ietf_tp_obj.te._set_oper_status('up')
        ietf_tp_obj.te.admin_status = 'up'
        ietf_tp_obj.te.name = MAPPINGS_TE_NAME.get((network_type, device_name, endpoint_name), endpoint_name)

    if network_type == NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY:
        if (network_type, device_name, endpoint_name) in MAPPINGS_TE_NAME:
            ietf_if_sw_cap = ietf_tp_obj.te.interface_switching_capability.add(
                'ietf-te-types:switching-l2sc ietf-te-types:lsp-encoding-ethernet'
            )
            ietf_max_lsp_bw = ietf_if_sw_cap.max_lsp_bandwidth.add('7')
            ietf_max_lsp_bw.te_bandwidth.eth_bandwidth = 10_000_000 # Kbps

        #ietf_tp_obj.eth_svc.client_facing = True

        ietf_tp_obj.eth_svc.supported_classification.port_classification = True
        outer_tag = ietf_tp_obj.eth_svc.supported_classification.vlan_classification.outer_tag
        outer_tag.supported_tag_types.append('ietf-eth-tran-types:classify-c-vlan')
        outer_tag.supported_tag_types.append('ietf-eth-tran-types:classify-s-vlan')
        outer_tag.vlan_bundling = False
        outer_tag.vlan_range = '1-4094'

    elif network_type == NetworkTypeEnum.TE_OTN_TOPOLOGY:
        #ietf_tp_obj.te.client_svc.client_facing = False

        ietf_if_sw_cap = ietf_tp_obj.te.interface_switching_capability.add(
            'ietf-te-types:switching-otn ietf-te-types:lsp-encoding-oduk'
        )
        ietf_max_lsp_bw = ietf_if_sw_cap.max_lsp_bandwidth.add('7')
        ietf_max_lsp_bw.te_bandwidth.otn.odu_type = 'ietf-layer1-types:ODU4'
