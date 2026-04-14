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


# Enable eventlet for async networking
# NOTE: monkey_patch needs to be executed before importing any other module.
import eventlet
eventlet.monkey_patch()

#pylint: disable=wrong-import-position
import logging
from common.tools.kafka.Variables import KafkaTopic
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    get_env_var_name, get_http_bind_address, get_log_level,
    get_service_baseurl_http, get_service_port_http,
    wait_for_environment_variables
)
from .NbiApplication import NbiApplication
from .camara_qod import register_camara_qod
from .dscm_oc import register_dscm_oc
from .e2e_services import register_etsi_api
from .etsi_bwm import register_etsi_bwm_api
from .health_probes import register_health_probes
from .ietf_acl import register_ietf_acl
from .ietf_hardware import register_ietf_hardware
from .ietf_l2vpn import register_ietf_l2vpn
from .ietf_l3vpn import register_ietf_l3vpn
from .ietf_network import register_ietf_network
from .ietf_network_slice import register_ietf_nss
from .osm_nbi import register_osm_api
from .qkd_app import register_qkd_app
from .restconf_root import register_restconf_root
from .sse_telemetry import register_telemetry_subscription
from .tfs_api import register_tfs_api
#from .topology_updates import register_topology_updates
from .vntm_recommend import register_vntm_recommend
from .well_known_meta import register_well_known

LOG_LEVEL = get_log_level()
logging.basicConfig(
    level=LOG_LEVEL,
    format="[Worker-%(process)d][%(asctime)s] %(levelname)s:%(name)s:%(message)s",
)
logging.getLogger('kafka.client').setLevel(logging.WARNING)
logging.getLogger('kafka.cluster').setLevel(logging.WARNING)
logging.getLogger('kafka.conn').setLevel(logging.WARNING)
logging.getLogger('kafka.consumer.fetcher').setLevel(logging.WARNING)
logging.getLogger('kafka.consumer.group').setLevel(logging.WARNING)
logging.getLogger('kafka.consumer.subscription_state').setLevel(logging.WARNING)
logging.getLogger('kafka.metrics.metrics').setLevel(logging.WARNING)
logging.getLogger('kafka.producer.kafka').setLevel(logging.WARNING)
logging.getLogger('kafka.producer.record_accumulator').setLevel(logging.WARNING)
logging.getLogger('kafka.producer.sender').setLevel(logging.WARNING)
logging.getLogger('kafka.protocol.parser').setLevel(logging.WARNING)
logging.getLogger('socketio.server').setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Starting...')

wait_for_environment_variables([
    get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     ),
    get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
    get_env_var_name(ServiceNameEnum.DEVICE,  ENVVAR_SUFIX_SERVICE_HOST     ),
    get_env_var_name(ServiceNameEnum.DEVICE,  ENVVAR_SUFIX_SERVICE_PORT_GRPC),
    get_env_var_name(ServiceNameEnum.SERVICE, ENVVAR_SUFIX_SERVICE_HOST     ),
    get_env_var_name(ServiceNameEnum.SERVICE, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
])

BASE_URL = get_service_baseurl_http(ServiceNameEnum.NBI) or ''

LOGGER.info('Creating missing Kafka topics...')
KafkaTopic.create_all_topics()
LOGGER.info('Created required Kafka topics')

nbi_app = NbiApplication(base_url=BASE_URL)
register_camara_qod      (nbi_app)
register_dscm_oc         (nbi_app)
register_etsi_api        (nbi_app)
register_etsi_bwm_api    (nbi_app)
register_health_probes   (nbi_app)
register_ietf_acl        (nbi_app)
register_ietf_hardware   (nbi_app)
register_ietf_l2vpn      (nbi_app)
register_ietf_l3vpn      (nbi_app)
register_ietf_network    (nbi_app)
register_ietf_nss        (nbi_app)
register_osm_api         (nbi_app)
register_qkd_app         (nbi_app)
register_restconf_root   (nbi_app)
register_telemetry_subscription(nbi_app)
register_tfs_api         (nbi_app)
#register_topology_updates(nbi_app) # does not work; check if eventlet-grpc side effects
register_vntm_recommend  (nbi_app)
register_well_known      (nbi_app)
LOGGER.info('All connectors registered')

nbi_app.dump_configuration()
app = nbi_app.get_flask_app()

LOGGER.info('Initialization completed!')

if __name__ == '__main__':
    # Only used to run it locally during development stage;
    # otherwise, app is directly launched by gunicorn.
    BIND_ADDRESS = get_http_bind_address()
    BIND_PORT    = get_service_port_http(ServiceNameEnum.NBI)
    nbi_app._sio.run(
        app, host=BIND_ADDRESS, port=BIND_PORT,
        debug=True, use_reloader=False
    )
