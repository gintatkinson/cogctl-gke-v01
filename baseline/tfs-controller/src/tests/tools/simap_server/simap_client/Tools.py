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

from .SimapClient import SimapClient

def create_simap_te(simap_client : SimapClient) -> None:
    te_topo = simap_client.network('te')
    te_topo.create()

    te_topo.node('ONT1').create(termination_point_ids=['200', '500'])
    te_topo.node('ONT2').create(termination_point_ids=['200', '500'])
    te_topo.node('OLT' ).create(termination_point_ids=['200', '201', '500', '501'])
    te_topo.link('L1').create('ONT1', '500', 'OLT', '200')
    te_topo.link('L2').create('ONT2', '500', 'OLT', '201')

    te_topo.node('PE1').create(termination_point_ids=['200', '500', '501'])
    te_topo.node('P1' ).create(termination_point_ids=['500', '501'])
    te_topo.node('P2' ).create(termination_point_ids=['500', '501'])
    te_topo.node('PE2').create(termination_point_ids=['200', '500', '501'])
    te_topo.link('L5' ).create('PE1', '500', 'P1',  '500')
    te_topo.link('L6' ).create('PE1', '501', 'P2',  '500')
    te_topo.link('L9' ).create('P1',  '501', 'PE2', '500')
    te_topo.link('L10').create('P2',  '501', 'PE2', '501')

    te_topo.node('OA'  ).create(termination_point_ids=['200', '500', '501'])
    te_topo.node('OTN1').create(termination_point_ids=['500', '501'])
    te_topo.node('OTN2').create(termination_point_ids=['500', '501'])
    te_topo.node('OE'  ).create(termination_point_ids=['200', '500', '501'])
    te_topo.link('L7'  ).create('OA',   '500', 'OTN1', '500')
    te_topo.link('L8'  ).create('OA',   '501', 'OTN2', '500')
    te_topo.link('L11' ).create('OTN1', '501', 'OE',   '500')
    te_topo.link('L12' ).create('OTN2', '501', 'OE',   '501')

    te_topo.link('L3').create('OLT', '500', 'PE1', '200')
    te_topo.link('L4').create('OLT', '501', 'OA',  '200')

    te_topo.node('POP1').create(termination_point_ids=['200', '201', '500'])
    te_topo.link('L13').create('PE2', '200', 'POP1', '500')

    te_topo.node('POP2').create(termination_point_ids=['200', '201', '500'])
    te_topo.link('L14').create('OE', '200', 'POP2', '500')


def create_simap_trans(simap_client : SimapClient) -> None:
    simap_trans = simap_client.network('simap-trans')
    simap_trans.create(supporting_network_ids=['te'])

    site_1 = simap_trans.node('site1')
    site_1.create(supporting_node_ids=[('te', 'PE1')])
    site_1.termination_point('200').create(supporting_termination_point_ids=[('te', 'PE1', '200')])
    site_1.termination_point('500').create(supporting_termination_point_ids=[('te', 'PE1', '500')])
    site_1.termination_point('501').create(supporting_termination_point_ids=[('te', 'PE1', '501')])

    site_2 = simap_trans.node('site2')
    site_2.create(supporting_node_ids=[('te', 'PE2')])
    site_2.termination_point('200').create(supporting_termination_point_ids=[('te', 'PE2', '200')])
    site_2.termination_point('500').create(supporting_termination_point_ids=[('te', 'PE2', '500')])
    site_2.termination_point('501').create(supporting_termination_point_ids=[('te', 'PE2', '501')])

    simap_trans.link('Trans-L1').create('site1', '500', 'site2', '500', supporting_link_ids=[('te', 'L5'), ('te', 'L9')])


def create_simap_aggnet(simap_client : SimapClient) -> None:
    simap_aggnet = simap_client.network('simap-aggnet')
    simap_aggnet.create(supporting_network_ids=['te', 'simap-trans'])

    sdp_1 = simap_aggnet.node('sdp1')
    sdp_1.create(supporting_node_ids=[('te', 'OLT')])
    sdp_1.termination_point('200').create(supporting_termination_point_ids=[('te', 'OLT', '200')])
    sdp_1.termination_point('201').create(supporting_termination_point_ids=[('te', 'OLT', '201')])
    sdp_1.termination_point('500').create(supporting_termination_point_ids=[('te', 'OLT', '500')])
    sdp_1.termination_point('501').create(supporting_termination_point_ids=[('te', 'OLT', '501')])

    sdp_2 = simap_aggnet.node('sdp2')
    sdp_2.create(supporting_node_ids=[('te', 'POP1')])
    sdp_2.termination_point('200').create(supporting_termination_point_ids=[('te', 'POP1', '200')])
    sdp_2.termination_point('201').create(supporting_termination_point_ids=[('te', 'POP1', '201')])
    sdp_2.termination_point('500').create(supporting_termination_point_ids=[('te', 'POP1', '500')])

    simap_aggnet.link('AggNet-L1').create('sdp1', '500', 'sdp2', '500', supporting_link_ids=[('te', 'L3'), ('simap-trans', 'Trans-L1'), ('te', 'L13')])


def create_simap_e2enet(simap_client : SimapClient) -> None:
    simap_e2e = simap_client.network('simap-e2e')
    simap_e2e.create(supporting_network_ids=['te', 'simap-trans'])

    sdp_1 = simap_e2e.node('sdp1')
    sdp_1.create(supporting_node_ids=[('te', 'ONT1')])
    sdp_1.termination_point('200').create(supporting_termination_point_ids=[('te', 'ONT1', '200')])
    sdp_1.termination_point('500').create(supporting_termination_point_ids=[('te', 'ONT1', '500')])

    sdp_2 = simap_e2e.node('sdp2')
    sdp_2.create(supporting_node_ids=[('te', 'POP1')])
    sdp_2.termination_point('200').create(supporting_termination_point_ids=[('te', 'POP1', '200')])
    sdp_2.termination_point('201').create(supporting_termination_point_ids=[('te', 'POP1', '201')])
    sdp_2.termination_point('500').create(supporting_termination_point_ids=[('te', 'POP1', '500')])

    simap_e2e.link('E2E-L1').create('sdp1', '500', 'sdp2', '500', supporting_link_ids=[('te', 'L1'), ('simap-aggnet', 'AggNet-L1')])
