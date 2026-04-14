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


import logging, threading
from nbi.service.NbiApplication import NbiApplication
from nbi.service.camara_qod import register_camara_qod
from nbi.service.etsi_bwm import register_etsi_bwm_api
from nbi.service.health_probes import register_health_probes
from nbi.service.ietf_l2vpn import register_ietf_l2vpn
from nbi.service.ietf_l3vpn import register_ietf_l3vpn
from nbi.service.ietf_network import register_ietf_network
from nbi.service.restconf_root import register_restconf_root
from nbi.service.tfs_api import register_tfs_api
from nbi.service.well_known_meta import register_well_known
from .Constants import LOCAL_HOST, NBI_SERVICE_PORT, NBI_SERVICE_PREFIX_URL


LOGGER = logging.getLogger(__name__)

class MockWebServer(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)

        self.nbi_app = NbiApplication(base_url=NBI_SERVICE_PREFIX_URL)
        register_health_probes(self.nbi_app)
        register_well_known   (self.nbi_app)
        register_restconf_root(self.nbi_app)
        register_tfs_api      (self.nbi_app)
        register_etsi_bwm_api (self.nbi_app)
        #register_ietf_hardware(self.nbi_app)
        register_ietf_l2vpn   (self.nbi_app)
        register_ietf_l3vpn   (self.nbi_app)
        register_ietf_network (self.nbi_app)
        #register_ietf_nss     (self.nbi_app)
        #register_ietf_acl     (self.nbi_app)
        #register_qkd_app      (self.nbi_app)
        register_camara_qod   (self.nbi_app)
        self.nbi_app.dump_configuration()

    def run(self):
        try:
            self.nbi_app._sio.run(
                self.nbi_app.get_flask_app(),
                host=LOCAL_HOST, port=NBI_SERVICE_PORT,
                debug=True, use_reloader=False
            )
        except: # pylint: disable=bare-except
            LOGGER.exception('[MockWebServer::run] Unhandled Exception')
