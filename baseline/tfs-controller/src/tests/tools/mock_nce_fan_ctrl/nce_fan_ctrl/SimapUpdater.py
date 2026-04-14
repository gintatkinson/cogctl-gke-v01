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


import logging, os
from typing import Dict
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from .SimapClient import SimapClient


SIMAP_ADDRESS = os.environ.get('SIMAP_ADDRESS')
SIMAP_PORT    = os.environ.get('SIMAP_PORT'   )


class SimapUpdater:
    def __init__(self):
        self._simap_client = None

        if SIMAP_ADDRESS is None: return
        if SIMAP_PORT    is None: return

        self._restconf_client = RestConfClient(
            SIMAP_ADDRESS, port=SIMAP_PORT,
            logger=logging.getLogger('RestConfClient')
        )
        self._simap_client = SimapClient(self._restconf_client)


    def upload_topology(self, network_data : Dict) -> None:
        if self._simap_client is None: return

        network_id = network_data['network-id']
        te_topo = self._simap_client.network(network_id)
        te_topo.update()

        nodes = network_data.get('node', list())
        for node in nodes:
            node_id = node['node-id']
            tp_ids = [
                tp['tp-id']
                for tp in node['ietf-network-topology:termination-point']
            ]
            te_topo.node(node_id).update(termination_point_ids=tp_ids)

        links = network_data.get('ietf-network-topology:link', list())
        for link in links:
            link_id   = link['link-id']
            link_src  = link['source']
            link_dst  = link['destination']
            link_src_node_id = link_src['source-node']
            link_src_tp_id   = link_src['source-tp']
            link_dst_node_id = link_dst['dest-node']
            link_dst_tp_id   = link_dst['dest-tp']

            te_topo.link(link_id).update(
                link_src_node_id, link_src_tp_id, link_dst_node_id, link_dst_tp_id
            )
