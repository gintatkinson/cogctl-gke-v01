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
from .SimapClient import SimapClient


LOGGER = logging.getLogger(__name__)


def set_simap_e2e_net(simap_client : SimapClient) -> None:
    simap = simap_client.network('e2e')
    simap.update(supporting_network_ids=['admin', 'agg'])

    node_a = simap.node('sdp1')
    node_a.update(supporting_node_ids=[('admin', 'ONT1')])
    node_a.termination_point('200').update(supporting_termination_point_ids=[('admin', 'ONT1', '200')])
    node_a.termination_point('500').update(supporting_termination_point_ids=[('admin', 'ONT1', '500')])

    node_b = simap.node('sdp2')
    node_b.update(supporting_node_ids=[('admin', 'POP2')])
    node_b.termination_point('200').update(supporting_termination_point_ids=[('admin', 'POP2', '200')])
    node_b.termination_point('201').update(supporting_termination_point_ids=[('admin', 'POP2', '201')])
    node_b.termination_point('500').update(supporting_termination_point_ids=[('admin', 'POP2', '500')])

    link = simap.link('E2E-L1')
    link.update(
        'sdp1', '500', 'sdp2', '500',
        supporting_link_ids=[
            ('admin', 'L1'), ('admin', 'L3'), ('agg', 'AggNet-L1')
        ]
    )


def delete_simap_e2e_net(simap_client : SimapClient) -> None:
    simap = simap_client.network('e2e')
    simap.update(supporting_network_ids=['admin', 'agg'])

    link = simap.link('E2E-L1')
    link.delete()


def set_simap_agg_net(simap_client : SimapClient) -> None:
    simap = simap_client.network('agg')
    simap.update(supporting_network_ids=['admin', 'trans-pkt'])

    node_a = simap.node('sdp1')
    node_a.update(supporting_node_ids=[('admin', 'OLT')])
    node_a.termination_point('200').update(supporting_termination_point_ids=[('admin', 'OLT', '200')])
    node_a.termination_point('201').update(supporting_termination_point_ids=[('admin', 'OLT', '201')])
    node_a.termination_point('500').update(supporting_termination_point_ids=[('admin', 'OLT', '500')])
    node_a.termination_point('501').update(supporting_termination_point_ids=[('admin', 'OLT', '501')])

    node_b = simap.node('sdp2')
    node_b.update(supporting_node_ids=[('admin', 'POP2')])
    node_b.termination_point('200').update(supporting_termination_point_ids=[('admin', 'POP2', '200')])
    node_b.termination_point('201').update(supporting_termination_point_ids=[('admin', 'POP2', '201')])
    node_b.termination_point('500').update(supporting_termination_point_ids=[('admin', 'POP2', '500')])

    link = simap.link('AggNet-L1')
    link.update(
        'sdp1', '500', 'sdp2', '500',
        supporting_link_ids=[
            ('trans-pkt', 'Trans-L1'), ('admin', 'L13')
        ]
    )


def delete_simap_agg_net(simap_client : SimapClient) -> None:
    simap = simap_client.network('agg')
    simap.update(supporting_network_ids=['admin', 'trans-pkt'])

    link = simap.link('AggNet-L1')
    link.delete()


def set_simap_trans_pkt(simap_client : SimapClient) -> None:
    simap = simap_client.network('trans-pkt')
    simap.update(supporting_network_ids=['admin'])

    node_a = simap.node('site1')
    node_a.update(supporting_node_ids=[('admin', 'P-PE1')])
    node_a.termination_point('200').update(supporting_termination_point_ids=[('admin', 'P-PE1', '200')])
    node_a.termination_point('500').update(supporting_termination_point_ids=[('admin', 'P-PE1', '500')])
    node_a.termination_point('501').update(supporting_termination_point_ids=[('admin', 'P-PE1', '501')])

    node_b = simap.node('site2')
    node_b.update(supporting_node_ids=[('admin', 'P-PE2')])
    node_b.termination_point('200').update(supporting_termination_point_ids=[('admin', 'P-PE2', '200')])
    node_b.termination_point('500').update(supporting_termination_point_ids=[('admin', 'P-PE2', '500')])
    node_b.termination_point('501').update(supporting_termination_point_ids=[('admin', 'P-PE2', '501')])

    link = simap.link('Trans-L1')
    link.update(
        'site1', '500', 'site2', '500',
        supporting_link_ids=[
            ('admin', 'L5'), ('admin', 'L9')
        ]
    )


def delete_simap_trans_pkt(simap_client : SimapClient) -> None:
    simap = simap_client.network('trans-pkt')
    simap.update(supporting_network_ids=['admin'])

    link = simap.link('Trans-L1')
    link.delete()


def set_mock_simap(simap_client : SimapClient, domain_name : str) -> None:
    if domain_name == 'trans-pkt':
        set_simap_trans_pkt(simap_client)
    elif domain_name == 'agg':
        set_simap_agg_net(simap_client)
    elif domain_name == 'e2e':
        set_simap_e2e_net(simap_client)
    else:
        MSG = 'Unsupported Topology({:s}) to set SIMAP'
        LOGGER.warning(MSG.format(str(domain_name)))


def delete_mock_simap(simap_client : SimapClient, domain_name : str) -> None:
    if domain_name == 'trans-pkt':
        delete_simap_trans_pkt(simap_client)
    elif domain_name == 'agg':
        delete_simap_agg_net(simap_client)
    elif domain_name == 'e2e':
        delete_simap_e2e_net(simap_client)
    else:
        MSG = 'Unsupported Topology({:s}) to delete SIMAP'
        LOGGER.warning(MSG.format(str(domain_name)))
