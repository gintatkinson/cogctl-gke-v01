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

import copy, deepdiff, json, logging, operator, os, pytest, time
from flask import Flask, jsonify, make_response
from flask_restful import Resource
from common.proto.context_pb2 import ConfigActionEnum, Device, DeviceId
from common.tools.descriptor.Tools import format_custom_config_rules
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Device import (
    json_device_connect_rules, json_device_id, json_device_ietf_actn_disabled
)
from common.tools.rest_api.server.GenericRestServer import GenericRestServer
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from device.service.DeviceService import DeviceService
from device.service.driver_api._Driver import _Driver
from tests.tools.mock_ietf_actn_sdn_ctrl.ResourceEthServices import EthService, EthServices
from tests.tools.mock_ietf_actn_sdn_ctrl.ResourceOsuTunnels import OsuTunnel, OsuTunnels

os.environ['DEVICE_EMULATED_ONLY'] = 'TRUE'
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    mock_service, device_service, context_client, device_client, monitoring_client, test_prepare_environment
)

DEVICE_UUID         = 'DEVICE-IETF-ACTN'
DEVICE_ADDRESS      = '127.0.0.1'
DEVICE_PORT         = 8080
DEVICE_USERNAME     = 'admin'
DEVICE_PASSWORD     = 'admin'
DEVICE_SCHEME       = 'http'
DEVICE_TIMEOUT      = 120
DEVICE_VERIFY_CERTS = False

DEVICE_ID = json_device_id(DEVICE_UUID)
DEVICE    = json_device_ietf_actn_disabled(DEVICE_UUID)

DEVICE_CONNECT_RULES = json_device_connect_rules(DEVICE_ADDRESS, DEVICE_PORT, {
    'scheme'      : DEVICE_SCHEME,
    'username'    : DEVICE_USERNAME,
    'password'    : DEVICE_PASSWORD,
    'timeout'     : DEVICE_TIMEOUT,
    'verify_certs': DEVICE_VERIFY_CERTS,
})

DATA_FILE_CONFIG_RULES           = 'device/tests/data/ietf_actn/config_rules.json'
DATA_FILE_DECONFIG_RULES         = 'device/tests/data/ietf_actn/deconfig_rules.json'
DATA_FILE_EXPECTED_OSU_TUNNELS   = 'device/tests/data/ietf_actn/expected_osu_tunnels.json'
DATA_FILE_EXPECTED_ETHT_SERVICES = 'device/tests/data/ietf_actn/expected_etht_services.json'

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture(scope='session')
def ietf_actn_sdn_ctrl(
    device_service : DeviceService,     # pylint: disable=redefined-outer-name
) -> Flask:
    _rest_server = GenericRestServer(DEVICE_PORT, bind_address=DEVICE_ADDRESS)
    _rest_server.app.config['DEBUG'      ] = True
    _rest_server.app.config['ENV'        ] = 'development'
    _rest_server.app.config['SERVER_NAME'] = '{:s}:{:d}'.format(DEVICE_ADDRESS, DEVICE_PORT)
    _rest_server.app.config['TESTING'    ] = True

    class HostMeta(Resource):
        def get(self):
            host_meta = {'links': [{'rel': 'restconf', 'href': '/restconf'}]}
            return make_response(jsonify(host_meta), 200)

    class Root(Resource):
        def get(self):
            return make_response(jsonify({}), 200)

    class Network(Resource):
        def get(self, network_id : str):
            network_topology = {'ietf-network:network': []}
            return make_response(jsonify(network_topology), 200)

    RESTCONF_V1 = '/restconf/data'
    RESTCONF_V2 = '/restconf/v2/data'

    add_rsrc = _rest_server.add_resource
    add_rsrc(HostMeta, '/.well-known/host-meta', endpoint='well-known.host-meta')
    add_rsrc(Root,     RESTCONF_V1 + '/', endpoint='restconf.v1.root')
    add_rsrc(Root,     RESTCONF_V2 + '/', endpoint='restconf.v2.root')

    RESTCONF_NETWORK = RESTCONF_V1 + '/ietf-network:networks/network=<string:network_id>'
    add_rsrc(Network,  RESTCONF_NETWORK)

    RESTCONF_TE_TUNNELS = RESTCONF_V2 + '/ietf-te:te/tunnels'
    add_rsrc(OsuTunnels,  RESTCONF_TE_TUNNELS)
    add_rsrc(OsuTunnel,   RESTCONF_TE_TUNNELS + '/tunnel=<string:osu_tunnel_name>')

    RESTCONF_ETHT_SERVICES = RESTCONF_V2 + '/ietf-eth-tran-service:etht-svc'
    add_rsrc(EthServices, RESTCONF_ETHT_SERVICES)
    add_rsrc(EthService,  RESTCONF_ETHT_SERVICES + '/etht-svc-instances=<string:etht_service_name>')

    _rest_server.start()
    time.sleep(1) # bring time for the server to start
    yield _rest_server
    _rest_server.shutdown()
    _rest_server.join()


def test_device_ietf_actn_add(
    device_client : DeviceClient,           # pylint: disable=redefined-outer-name
    device_service : DeviceService,         # pylint: disable=redefined-outer-name
    ietf_actn_sdn_ctrl : GenericRestServer, # pylint: disable=redefined-outer-name
) -> None:
    DEVICE_WITH_CONNECT_RULES = copy.deepcopy(DEVICE)
    DEVICE_WITH_CONNECT_RULES['device_config']['config_rules'].extend(DEVICE_CONNECT_RULES)
    device_client.AddDevice(Device(**DEVICE_WITH_CONNECT_RULES))
    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver: _Driver = driver_instance_cache.get(DEVICE_UUID)
    assert driver is not None


def test_device_ietf_actn_get(
    context_client : ContextClient,         # pylint: disable=redefined-outer-name
    device_client : DeviceClient,           # pylint: disable=redefined-outer-name
    ietf_actn_sdn_ctrl : GenericRestServer, # pylint: disable=redefined-outer-name
) -> None:

    initial_config = device_client.GetInitialConfig(DeviceId(**DEVICE_ID))
    LOGGER.info('initial_config = {:s}'.format(grpc_message_to_json_string(initial_config)))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_ID))
    LOGGER.info('device_data = {:s}'.format(grpc_message_to_json_string(device_data)))


def test_device_ietf_actn_configure(
    device_client : DeviceClient,           # pylint: disable=redefined-outer-name
    device_service : DeviceService,         # pylint: disable=redefined-outer-name
    ietf_actn_sdn_ctrl : GenericRestServer, # pylint: disable=redefined-outer-name
) -> None:
    ietf_actn_client = ietf_actn_sdn_ctrl.app.test_client()

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_UUID)
    assert driver is not None

    retrieved_osu_tunnels = ietf_actn_client.get('/restconf/v2/data/ietf-te:te/tunnels')
    retrieved_osu_tunnels = retrieved_osu_tunnels.json
    LOGGER.info('osu_tunnels = {:s}'.format(str(retrieved_osu_tunnels)))
    expected_osu_tunnels = {'ietf-te:tunnel': []}
    osu_tunnels_diff = deepdiff.DeepDiff(expected_osu_tunnels, retrieved_osu_tunnels)
    if len(osu_tunnels_diff) > 0:
        LOGGER.error('PRE OSU TUNNELS - Differences:\n{:s}'.format(str(osu_tunnels_diff.pretty())))
    assert len(osu_tunnels_diff) == 0

    retrieved_etht_services = ietf_actn_client.get('/restconf/v2/data/ietf-eth-tran-service:etht-svc')
    retrieved_etht_services = retrieved_etht_services.json
    LOGGER.info('etht_services = {:s}'.format(str(retrieved_etht_services)))
    expected_etht_services = {'ietf-eth-tran-service:etht-svc': {'etht-svc-instances': []}}
    etht_services_diff = deepdiff.DeepDiff(expected_etht_services, retrieved_etht_services)
    if len(etht_services_diff) > 0:
        LOGGER.error('PRE ETHT SERVICES - Differences:\n{:s}'.format(str(etht_services_diff.pretty())))
    assert len(etht_services_diff) == 0

    retrieved_driver_config_rules = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    LOGGER.info('driver_config = {:s}'.format(str(retrieved_driver_config_rules)))
    assert isinstance(retrieved_driver_config_rules, list)
    retrieved_driver_config_rules = [
        (resource_key, resource_value)
        for resource_key, resource_value in retrieved_driver_config_rules
        if resource_key != '/endpoints/endpoint[mgmt]'
    ]
    if len(retrieved_driver_config_rules) > 0:
        LOGGER.error('PRE DRIVER CONFIG RULES - Differences:\n{:s}'.format(str(retrieved_driver_config_rules)))
    assert len(retrieved_driver_config_rules) == 0

    DEVICE_WITH_CONFIG_RULES = copy.deepcopy(DEVICE)
    with open(DATA_FILE_CONFIG_RULES, 'r', encoding='UTF-8') as f:
        config_rules = format_custom_config_rules(json.load(f))
        DEVICE_WITH_CONFIG_RULES['device_config']['config_rules'].extend(config_rules)
    device_client.ConfigureDevice(Device(**DEVICE_WITH_CONFIG_RULES))

    retrieved_osu_tunnels = ietf_actn_client.get('/restconf/v2/data/ietf-te:te/tunnels')
    retrieved_osu_tunnels = retrieved_osu_tunnels.json
    LOGGER.info('osu_tunnels = {:s}'.format(str(retrieved_osu_tunnels)))
    with open(DATA_FILE_EXPECTED_OSU_TUNNELS, 'r', encoding='UTF-8') as f:
        expected_osu_tunnels = json.load(f)
    osu_tunnels_diff = deepdiff.DeepDiff(expected_osu_tunnels, retrieved_osu_tunnels)
    if len(osu_tunnels_diff) > 0:
        LOGGER.error('POST OSU TUNNELS - Differences:\n{:s}'.format(str(osu_tunnels_diff.pretty())))
    assert len(osu_tunnels_diff) == 0

    retrieved_etht_services = ietf_actn_client.get('/restconf/v2/data/ietf-eth-tran-service:etht-svc')
    retrieved_etht_services = retrieved_etht_services.json
    LOGGER.info('etht_services = {:s}'.format(str(retrieved_etht_services)))
    with open(DATA_FILE_EXPECTED_ETHT_SERVICES, 'r', encoding='UTF-8') as f:
        expected_etht_services = json.load(f)
    etht_services_diff = deepdiff.DeepDiff(expected_etht_services, retrieved_etht_services)
    if len(etht_services_diff) > 0:
        LOGGER.error('POST ETHT SERVICES - Differences:\n{:s}'.format(str(etht_services_diff.pretty())))
    assert len(etht_services_diff) == 0

    retrieved_driver_config_rules = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    LOGGER.info('driver_config = {:s}'.format(str(retrieved_driver_config_rules)))
    retrieved_driver_config_rules = [
        {'action': 1, 'custom': {'resource_key': resource_key, 'resource_value': resource_value}}
        for resource_key, resource_value in retrieved_driver_config_rules
        if resource_key != '/endpoints/endpoint[mgmt]'
    ]
    with open(DATA_FILE_CONFIG_RULES, 'r', encoding='UTF-8') as f:
        expected_driver_config_rules = sorted(json.load(f), key=lambda cr: cr['custom']['resource_key'])
    driver_config_rules_diff = deepdiff.DeepDiff(expected_driver_config_rules, retrieved_driver_config_rules)
    if len(driver_config_rules_diff) > 0:
        LOGGER.error('POST DRIVER CONFIG RULES - Differences:\n{:s}'.format(str(driver_config_rules_diff.pretty())))
    assert len(driver_config_rules_diff) == 0


def test_device_ietf_actn_deconfigure(
    device_client : DeviceClient,           # pylint: disable=redefined-outer-name
    device_service : DeviceService,         # pylint: disable=redefined-outer-name
    ietf_actn_sdn_ctrl : GenericRestServer, # pylint: disable=redefined-outer-name
) -> None:
    ietf_actn_client = ietf_actn_sdn_ctrl.app.test_client()

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_UUID)
    assert driver is not None

    retrieved_osu_tunnels = ietf_actn_client.get('/restconf/v2/data/ietf-te:te/tunnels')
    retrieved_osu_tunnels = retrieved_osu_tunnels.json
    LOGGER.info('osu_tunnels = {:s}'.format(str(retrieved_osu_tunnels)))
    with open(DATA_FILE_EXPECTED_OSU_TUNNELS, 'r', encoding='UTF-8') as f:
        expected_osu_tunnels = json.load(f)
    osu_tunnels_diff = deepdiff.DeepDiff(expected_osu_tunnels, retrieved_osu_tunnels)
    if len(osu_tunnels_diff) > 0:
        LOGGER.error('PRE OSU TUNNELS - Differences:\n{:s}'.format(str(osu_tunnels_diff.pretty())))
    assert len(osu_tunnels_diff) == 0

    retrieved_etht_services = ietf_actn_client.get('/restconf/v2/data/ietf-eth-tran-service:etht-svc')
    retrieved_etht_services = retrieved_etht_services.json
    LOGGER.info('etht_services = {:s}'.format(str(retrieved_etht_services)))
    with open(DATA_FILE_EXPECTED_ETHT_SERVICES, 'r', encoding='UTF-8') as f:
        expected_etht_services = json.load(f)
    etht_services_diff = deepdiff.DeepDiff(expected_etht_services, retrieved_etht_services)
    if len(etht_services_diff) > 0:
        LOGGER.error('PRE ETHT SERVICES - Differences:\n{:s}'.format(str(etht_services_diff.pretty())))
    assert len(etht_services_diff) == 0

    retrieved_driver_config_rules = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    LOGGER.info('driver_config = {:s}'.format(str(retrieved_driver_config_rules)))
    retrieved_driver_config_rules = [
        {'action': 1, 'custom': {'resource_key': resource_key, 'resource_value': resource_value}}
        for resource_key, resource_value in retrieved_driver_config_rules
        if resource_key != '/endpoints/endpoint[mgmt]'
    ]
    with open(DATA_FILE_CONFIG_RULES, 'r', encoding='UTF-8') as f:
        expected_driver_config_rules = sorted(json.load(f), key=lambda cr: cr['custom']['resource_key'])
    driver_config_rules_diff = deepdiff.DeepDiff(expected_driver_config_rules, retrieved_driver_config_rules)
    if len(driver_config_rules_diff) > 0:
        LOGGER.error('PRE DRIVER CONFIG RULES - Differences:\n{:s}'.format(str(driver_config_rules_diff.pretty())))
    assert len(driver_config_rules_diff) == 0

    DEVICE_WITH_DECONFIG_RULES = copy.deepcopy(DEVICE)
    with open(DATA_FILE_DECONFIG_RULES, 'r', encoding='UTF-8') as f:
        deconfig_rules = format_custom_config_rules(json.load(f))
        DEVICE_WITH_DECONFIG_RULES['device_config']['config_rules'].extend(deconfig_rules)
    device_client.ConfigureDevice(Device(**DEVICE_WITH_DECONFIG_RULES))

    retrieved_osu_tunnels = ietf_actn_client.get('/restconf/v2/data/ietf-te:te/tunnels')
    retrieved_osu_tunnels = retrieved_osu_tunnels.json
    LOGGER.info('osu_tunnels = {:s}'.format(str(retrieved_osu_tunnels)))
    expected_osu_tunnels = {'ietf-te:tunnel': []}
    osu_tunnels_diff = deepdiff.DeepDiff(expected_osu_tunnels, retrieved_osu_tunnels)
    if len(osu_tunnels_diff) > 0:
        LOGGER.error('POST OSU TUNNELS - Differences:\n{:s}'.format(str(osu_tunnels_diff.pretty())))
    assert len(osu_tunnels_diff) == 0

    retrieved_etht_services = ietf_actn_client.get('/restconf/v2/data/ietf-eth-tran-service:etht-svc')
    retrieved_etht_services = retrieved_etht_services.json
    LOGGER.info('etht_services = {:s}'.format(str(retrieved_etht_services)))
    expected_etht_services = {'ietf-eth-tran-service:etht-svc': {'etht-svc-instances': []}}
    etht_services_diff = deepdiff.DeepDiff(expected_etht_services, retrieved_etht_services)
    if len(etht_services_diff) > 0:
        LOGGER.error('POST ETHT SERVICES - Differences:\n{:s}'.format(str(etht_services_diff.pretty())))
    assert len(etht_services_diff) == 0

    retrieved_driver_config_rules = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    LOGGER.info('retrieved_driver_config_rules = {:s}'.format(str(retrieved_driver_config_rules)))
    assert isinstance(retrieved_driver_config_rules, list)
    retrieved_driver_config_rules = [
        (resource_key, resource_value)
        for resource_key, resource_value in retrieved_driver_config_rules
        if resource_key != '/endpoints/endpoint[mgmt]'
    ]
    if len(retrieved_driver_config_rules) > 0:
        LOGGER.error('POST DRIVER CONFIG RULES - Differences:\n{:s}'.format(str(retrieved_driver_config_rules)))
    assert len(retrieved_driver_config_rules) == 0


def test_device_ietf_actn_delete(
    device_client : DeviceClient,           # pylint: disable=redefined-outer-name
    device_service : DeviceService,         # pylint: disable=redefined-outer-name
    ietf_actn_sdn_ctrl : GenericRestServer, # pylint: disable=redefined-outer-name
) -> None:
    device_client.DeleteDevice(DeviceId(**DEVICE_ID))
    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_UUID, {})
    assert driver is None
