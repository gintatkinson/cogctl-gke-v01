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

from typing import Dict

from .NetworkTypeEnum import NetworkTypeEnum

def manual_fixes(json_response : Dict) -> None:
    # TODO: workaround to set network types manually. Currently does not work; refine bindings.
    # Seems limitation of pyangbind using multiple augmentations and nested empty containers.
    for json_network in json_response['ietf-network:networks']['network']:
        net_te_topo_id = json_network.get('ietf-te-topology:te-topology-identifier', {}).get('topology-id')
        if net_te_topo_id is None: continue
        net_te_topo_type = json_network['network-types']['ietf-te-topology:te-topology']
        if net_te_topo_id == '1':
            network_type = NetworkTypeEnum.TE_OTN_TOPOLOGY
            net_te_topo_type['ietf-otn-topology:otn-topology'] = {}
        elif net_te_topo_id == '2':
            network_type = NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY
            net_te_topo_type['ietf-eth-te-topology:eth-tran-topology'] = {}
        else:
            network_type = None

        for json_node in json_network.get('node', []):
            for json_tp in json_node.get('ietf-network-topology:termination-point', []):
                json_tp_te = json_tp.get('ietf-te-topology:te', {})

                if network_type == NetworkTypeEnum.TE_OTN_TOPOLOGY:
                    json_tp_te_cs = json_tp_te.setdefault('ietf-otn-topology:client-svc', {})
                    json_tp_te_cs['client-facing'] = False
                elif network_type == NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY:
                    if 'ietf-eth-te-topology:eth-svc' in json_tp:
                        client_facing = json_tp['tp-id'] in {'200', '201'}
                        json_tp['ietf-eth-te-topology:eth-svc']['client-facing'] = client_facing

                # Fix value type of bandwidth
                for json_if_sw_cap in json_tp_te.get('interface-switching-capability', []):
                    for json_max_lsp_bandwidth in json_if_sw_cap.get('max-lsp-bandwidth', []):
                        json_te_bw = json_max_lsp_bandwidth.get('te-bandwidth', {})
                        if network_type == NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY:
                            if 'ietf-eth-te-topology:eth-bandwidth' in json_te_bw:
                                eth_bw = json_te_bw['ietf-eth-te-topology:eth-bandwidth']
                                if isinstance(eth_bw, str):
                                    json_te_bw['ietf-eth-te-topology:eth-bandwidth'] = int(eth_bw)

        for json_link in json_network.get('ietf-network-topology:link', []):
            json_link_te_attributes = json_link.get('ietf-te-topology:te', {}).get('te-link-attributes', {})

            # Fix value type of bandwidth
            json_te_bw = json_link_te_attributes.get('max-link-bandwidth', {}).get('te-bandwidth', {})
            if network_type == NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY:
                if 'ietf-eth-te-topology:eth-bandwidth' in json_te_bw:
                    eth_bw = json_te_bw['ietf-eth-te-topology:eth-bandwidth']
                    if isinstance(eth_bw, str):
                        json_te_bw['ietf-eth-te-topology:eth-bandwidth'] = int(eth_bw)

                for json_unresv_bandwidth in json_link_te_attributes.get('unreserved-bandwidth', []):
                    json_te_bw = json_unresv_bandwidth.get('te-bandwidth', {})
                    if 'ietf-eth-te-topology:eth-bandwidth' in json_te_bw:
                        eth_bw = json_te_bw['ietf-eth-te-topology:eth-bandwidth']
                        if isinstance(eth_bw, str):
                            json_te_bw['ietf-eth-te-topology:eth-bandwidth'] = int(eth_bw)
