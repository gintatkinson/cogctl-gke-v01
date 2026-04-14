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

import sys
import time
import logging
import os

import binding_topology
from pyangbind.lib.serialise import pybindIETFXMLEncoder, pybindIETFXMLDecoder

from netconf import nsmap_add, NSMAP
from netconf import server, util
from lxml import etree

logging.basicConfig(level=logging.DEBUG)


nsmap_add("topology", "urn:topology")

class MyServer(object):

    def __init__(self, username, password, port):
        host_key_value = os.path.join(os.path.abspath(os.path.dirname(__file__)), "server-key")
        auth = server.SSHUserPassController(username=username, password=password)
        self.server = server.NetconfSSHServer(server_ctl=auth, server_methods=self, port=port, host_key=host_key_value, debug=False)
        self.load_file()

    def load_file(self):    
        # create configuration
        xml_root = open('topology.xml', 'r').read()
        print(xml_root)
        topo = pybindIETFXMLDecoder.decode(xml_root, binding_topology, "topology")
        xml = pybindIETFXMLEncoder.serialise(topo)
        tree = etree.XML(xml)
        data = util.elm("nc:data")
        data.append(tree)
        self.node_topology = data

    def nc_append_capabilities(self, capabilities): 
        util.subelm(capabilities, "capability").text = "urn:ietf:params:netconf:capability:xpath:1.0"
        util.subelm(capabilities, "capability").text = NSMAP["topology"]

    def rpc_get_config(self, session, rpc, source_elm, filter_or_none):
        logging.debug("--GET CONFIG--")
        logging.debug(session)
        logging.debug(etree.tostring(rpc))

        return util.filter_results(rpc, self.node_topology, None)


    def close(self):
        self.server.close()




def main(*margs):
    s = MyServer("admin","admin", 8300)
    
    if sys.stdout.isatty():
        logging.debug("^C to quit server")

    try:
        while True:
            time.sleep(1)
    
    except Exception:
        logging.debug("quitting server")

    s.close()

if __name__ == "__main__":
    main()
