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

import logging, os, sys, time
from pyangbind.lib.serialise import pybindIETFXMLEncoder, pybindIETFXMLDecoder
from lxml import etree
from netconf import nsmap_add, NSMAP, server, util
from device_definition import get_device_definition

logging.basicConfig(level=logging.DEBUG)

#nsmap_add("topology", "urn:topology")
#nsmap_add("connection", "urn:connection")

class MyServer(server.NetconfMethods):

    def __init__(self, username, password, port):
        host_key_value = os.path.join(os.path.abspath(os.path.dirname(__file__)), "server-key")
        auth = server.SSHUserPassController(username=username, password=password)
        auth.check_auth_none(username)
        self.server = server.NetconfSSHServer(server_ctl=auth, server_methods=self, host_key=host_key_value, port=port, debug=True)

        self.data = get_device_definition()

    def nc_append_capabilities(self, capabilities): 
        logging.debug("--GET capabilities--")
        util.subelm(capabilities, "capability").text = "urn:ietf:params:netconf:capability:xpath:1.0"
        #util.subelm(capabilities, "capability").text = NSMAP["topology"]
        #util.subelm(capabilities, "capability").text = NSMAP["connection"]

    def rpc_get(self, session, rpc, filter_or_none):
        #logging.debug("--GET--")
        #logging.debug(session)
        #logging.debug(etree.tostring(rpc))
        return util.filter_results(rpc, self.data, None)

    def rpc_get_config(self, session, rpc, source_elm, filter_or_none):
        #logging.debug("--GET CONFIG--")
        #logging.debug(session)
        #logging.debug(etree.tostring(rpc))
        return util.filter_results(rpc, self.data, None)

    def rpc_edit_config(self, session, rpc, target, default_operation, new_config):
        logging.debug("--EDIT CONFIG--")
        logging.debug(session)
        logging.debug(etree.tostring(rpc))
        logging.debug(etree.tostring(target))
        logging.debug(etree.tostring(default_operation))
        logging.debug(etree.tostring(new_config))

        #data_list = new_config.findall(".//xmlns:connection", namespaces={'xmlns': 'urn:connection'})
        #for connect in data_list:
        #    logging.debug("connect: " )
        #    logging.debug(etree.tostring(connect) )
        #    logging.debug("CURRENT CONNECTION")
        #    logging.debug(etree.tostring(self.data[1]) )
        #    self.data[1].append(connect)
        #    break  
        return util.filter_results(rpc, self.data, None)

    def close(self):
        self.server.close()

def main(*margs):
    port = sys.argv[1]
    s = MyServer("admin", "admin", int(port))
    
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
