#!/usr/bin/python
# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import json, requests, networkx as nx
from requests.auth import HTTPBasicAuth

IP = '127.0.0.1'
PORT = 8080
TOPO_UUID = 'ols-topo'
TOPO_URL = 'http://{:s}:{:d}/restconf/data/tapi-common:context/'\
    'tapi-topology:topology-context/topology={:s}/'

def retrieve_topology(ip, port, topo_uuid, user='', passwd=''):
    print ("Reading network-topology")
    topo_url = TOPO_URL.format(ip, port, topo_uuid)
    response = requests.get(topo_url, auth=HTTPBasicAuth(user, passwd))
    topology = response.json()
    print ("Retrieved Topology: " + json.dumps(topology, indent=4))
    return topology

def to_png_matplotlib(nwk_graph, topo_uuid):
    import matplotlib.pyplot as plt
    nx.draw(nwk_graph, pos=nx.spring_layout(nwk_graph, scale=500))
    plt.show(block=False)
    plt.savefig('{:s}.png'.format(topo_uuid), format='PNG')
    plt.close()

def to_png_pydot(nwk_graph, topo_uuid):
    from networkx.drawing.nx_pydot import write_dot, to_pydot
    write_dot(nwk_graph, '{:s}.dot'.format(topo_uuid))
    dot_graph = to_pydot(nwk_graph)
    with open('{:s}.png'.format(topo_uuid), 'wb') as f:
        f.write(dot_graph.create(format='png'))

def draw_topology(topology):
    nwk_graph = nx.DiGraph()

    for node in topology['node']:
        if node['owned-node-edge-point']:
            nwk_graph.add_node(node['uuid'])

    for link in topology['link']:
        node1 = link['node-edge-point'][0]['node-uuid']
        node2 = link['node-edge-point'][1]['node-uuid']
        nwk_graph.add_edge(node1, node2)

    #to_png_matplotlib(nwk_graph, topology['uuid'])
    to_png_pydot(nwk_graph, topology['uuid'])

if __name__ == "__main__":
    draw_topology(retrieve_topology(IP, PORT, TOPO_UUID))
