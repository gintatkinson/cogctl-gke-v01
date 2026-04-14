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
from nbi.service.rest_server.nbi_plugins.dscm_oc import register_dscm_oc
from .Constants import LOCAL_HOST, NBI_SERVICE_PORT, NBI_SERVICE_PREFIX_URL


LOGGER = logging.getLogger(__name__)

class MockWebServer(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)

        self.nbi_app = NbiApplication(base_url=NBI_SERVICE_PREFIX_URL)
        register_dscm_oc(self.nbi_app)
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
