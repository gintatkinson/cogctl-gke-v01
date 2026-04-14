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


# This file overwrites default RestConf Server `app.py` file.

# Mock IETF ACTN SDN controller
# -----------------------------
# REST server implementing minimal support for:
# - IETF YANG Data Model for Transport Network Client Signals
#       Ref: https://www.ietf.org/archive/id/draft-ietf-ccamp-client-signal-yang-10.html
# - IETF YANG Data Model for Traffic Engineering Tunnels, Label Switched Paths and Interfaces
#       Ref: https://www.ietf.org/archive/id/draft-ietf-teas-yang-te-34.html

# NOTE: we need here OSUflex tunnels that are still not standardized; hardcoded.

import logging
from common.tools.rest_conf.server.restconf_server.RestConfServerApplication import RestConfServerApplication
from .Callbacks import CallbackEthTService, CallbackOsuTunnel
from .ResourceEthServices import EthService, EthServices
from .ResourceOsuTunnels import OsuTunnel, OsuTunnels
from .SimapUpdater import SimapUpdater


logging.basicConfig(
    level=logging.INFO,
    format='[Worker-%(process)d][%(asctime)s] %(levelname)s:%(name)s:%(message)s',
)
LOGGER = logging.getLogger(__name__)
logging.getLogger('RestConfClient').setLevel(logging.WARN)


LOGGER.info('Starting...')

simap_updater = SimapUpdater()

rcs_app = RestConfServerApplication()
rcs_app.register_host_meta()
rcs_app.register_restconf()

rcs_app.register_custom(
    OsuTunnels,
    '/restconf/v2/data/ietf-te:te/tunnels',
    add_prefix_to_urls=False,
    resource_class_args=(simap_updater,)
)
rcs_app.register_custom(
    OsuTunnel,
    '/restconf/v2/data/ietf-te:te/tunnels/tunnel=<string:osu_tunnel_name>',
    add_prefix_to_urls=False,
    resource_class_args=(simap_updater,)
)
rcs_app.register_custom(
    EthServices,
    '/restconf/v2/data/ietf-eth-tran-service:etht-svc',
    add_prefix_to_urls=False,
    resource_class_args=(simap_updater,)
)
rcs_app.register_custom(
    EthService,
    '/restconf/v2/data/ietf-eth-tran-service:etht-svc/etht-svc-instances=<string:etht_service_name>',
    add_prefix_to_urls=False,
    resource_class_args=(simap_updater,)
)

LOGGER.info('All connectors registered')

startup_data = rcs_app.get_startup_data()

networks = startup_data.get('ietf-network:networks', dict())
networks = networks.get('network', list())
if len(networks) == 1 and networks[0]['network-id'] == 'admin':
    simap_updater.upload_topology(networks[0])

    rcs_app.callback_dispatcher.register(CallbackOsuTunnel())
    rcs_app.callback_dispatcher.register(CallbackEthTService())
    LOGGER.info('All callbacks registered')

rcs_app.dump_configuration()
app = rcs_app.get_flask_app()

LOGGER.info('Initialization completed!')
