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

import json, logging, os, pytest, time
from typing import Dict, Tuple
os.environ['DEVICE_EMULATED_ONLY'] = 'YES'

# pylint: disable=wrong-import-position
from device.service.drivers.gnmi_openconfig.GnmiOpenConfigDriver import GnmiOpenConfigDriver
#from device.service.driver_api._Driver import (
#    RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES, RESOURCE_ROUTING_POLICIES, RESOURCE_SERVICES
#)

logging.basicConfig(level=logging.DEBUG)
#logging.getLogger('ncclient.operations.rpc').setLevel(logging.INFO)
#logging.getLogger('ncclient.transport.parser').setLevel(logging.INFO)

LOGGER = logging.getLogger(__name__)


##### DRIVERS FIXTURE ##################################################################################################

DEVICES = {
    'SW1': {'address': '172.20.20.101', 'port': 6030, 'settings': {
        'username': 'admin', 'password': 'admin',
        'vendor': None, 'force_running': False, 'hostkey_verify': False, 'look_for_keys': False, 'allow_agent': False,
        'commit_per_rule': True, 'device_params': {'name': 'default'}, 'manager_params': {'timeout' : 120}
    }},
    'SW2': {'address': '10.1.1.87', 'port': 830, 'settings': {
        'username': 'ocnos', 'password': 'ocnos',
        'vendor': None, 'force_running': False, 'hostkey_verify': False, 'look_for_keys': False, 'allow_agent': False,
        'commit_per_rule': True, 'device_params': {'name': 'default'}, 'manager_params': {'timeout' : 120}
    }},
}

@pytest.fixture(scope='session')
def drivers() -> Dict[str, OpenConfigDriver]:
    _drivers : Dict[str, OpenConfigDriver] = dict()
    for device_name, driver_params in DEVICES.items():
        driver = OpenConfigDriver(driver_params['address'], driver_params['port'], **(driver_params['settings']))
        driver.Connect()
        _drivers[device_name] = driver
    yield _drivers
    time.sleep(1)
    for _,driver in _drivers.items():
        driver.Disconnect()


def network_instance(ni_name, ni_type, ni_router_id=None, ni_route_distinguisher=None) -> Tuple[str, Dict]:
    path = '/network_instance[{:s}]'.format(ni_name)
    data = {'name': ni_name, 'type': ni_type}
    if ni_router_id is not None: data['router_id'] = ni_router_id
    if ni_route_distinguisher is not None: data['route_distinguisher'] = ni_route_distinguisher
    return path, json.dumps(data)

def network_instance_add_protocol_bgp(ni_name, ni_type, ni_router_id, ni_bgp_as, neighbors=[]) -> Tuple[str, Dict]:
    path = '/network_instance[{:s}]/protocols[BGP]'.format(ni_name)
    data = {
        'name': ni_name, 'type': ni_type, 'router_id': ni_router_id, 'identifier': 'BGP',
        'protocol_name': ni_bgp_as, 'as': ni_bgp_as
    }
    if len(neighbors) > 0:
        data['neighbors'] = [
            {'ip_address': neighbor_ip_address, 'remote_as': neighbor_remote_as}
            for neighbor_ip_address, neighbor_remote_as in neighbors
        ]
    return path, json.dumps(data)

def network_instance_add_protocol_direct(ni_name, ni_type) -> Tuple[str, Dict]:
    path = '/network_instance[{:s}]/protocols[DIRECTLY_CONNECTED]'.format(ni_name)
    data = {
        'name': ni_name, 'type': ni_type, 'identifier': 'DIRECTLY_CONNECTED',
        'protocol_name': 'DIRECTLY_CONNECTED'
    }
    return path, json.dumps(data)

def network_instance_add_protocol_static(ni_name, ni_type) -> Tuple[str, Dict]:
    path = '/network_instance[{:s}]/protocols[STATIC]'.format(ni_name)
    data = {
        'name': ni_name, 'type': ni_type, 'identifier': 'STATIC',
        'protocol_name': 'STATIC'
    }
    return path, json.dumps(data)

#def network_instance_static_route(ni_name, prefix, next_hop, next_hop_index=0) -> Tuple[str, Dict]:
#    path = '/network_instance[{:s}]/static_route[{:s}]'.format(ni_name, prefix)
#    data = {'name': ni_name, 'prefix': prefix, 'next_hop': next_hop, 'next_hop_index': next_hop_index}
#    return path, json.dumps(data)

def network_instance_add_table_connection(
    ni_name, src_protocol, dst_protocol, address_family, default_import_policy, bgp_as=None
) -> Tuple[str, Dict]:
    path = '/network_instance[{:s}]/table_connections[{:s}][{:s}][{:s}]'.format(
        ni_name, src_protocol, dst_protocol, address_family
    )
    data = {
        'name': ni_name, 'src_protocol': src_protocol, 'dst_protocol': dst_protocol,
        'address_family': address_family, 'default_import_policy': default_import_policy,
    }
    if bgp_as is not None: data['as'] = bgp_as
    return path, json.dumps(data)

def interface(
    name, index, description=None, if_type=None, vlan_id=None, mtu=None, ipv4_address_prefix=None, enabled=None
) -> Tuple[str, Dict]:
    path = '/interface[{:s}]/subinterface[{:d}]'.format(name, index)
    data = {'name': name, 'index': index}
    if description is not None: data['description'] = description
    if if_type     is not None: data['type'       ] = if_type
    if vlan_id     is not None: data['vlan_id'    ] = vlan_id
    if mtu         is not None: data['mtu'        ] = mtu
    if enabled     is not None: data['enabled'    ] = enabled
    if ipv4_address_prefix is not None:
        ipv4_address, ipv4_prefix = ipv4_address_prefix
        data['address_ip'    ] = ipv4_address
        data['address_prefix'] = ipv4_prefix
    return path, json.dumps(data)

def network_instance_interface(ni_name, ni_type, if_name, if_index) -> Tuple[str, Dict]:
    path = '/network_instance[{:s}]/interface[{:s}.{:d}]'.format(ni_name, if_name, if_index)
    data = {'name': ni_name, 'type': ni_type, 'id': if_name, 'interface': if_name, 'subinterface': if_index}
    return path, json.dumps(data)

def test_configure(drivers : Dict[str, OpenConfigDriver]):
    #resources_to_get = []
    #resources_to_get = [RESOURCE_ENDPOINTS]
    #resources_to_get = [RESOURCE_INTERFACES]
    #resources_to_get = [RESOURCE_NETWORK_INSTANCES]
    #resources_to_get = [RESOURCE_ROUTING_POLICIES]
    #resources_to_get = [RESOURCE_SERVICES]
    #LOGGER.info('resources_to_get = {:s}'.format(str(resources_to_get)))
    #results_getconfig = driver.GetConfig(resources_to_get)
    #LOGGER.info('results_getconfig = {:s}'.format(str(results_getconfig)))

    csgw1_resources_to_set = [
        network_instance('ecoc24', 'L3VRF', '192.168.150.1', '65001:1'),
        network_instance_add_protocol_direct('ecoc24', 'L3VRF'),
        network_instance_add_protocol_static('ecoc24', 'L3VRF'),
        network_instance_add_protocol_bgp('ecoc24', 'L3VRF', '192.168.150.1', '65001', neighbors=[
            ('192.168.150.2', '65001')
        ]),
        network_instance_add_table_connection('ecoc24', 'DIRECTLY_CONNECTED', 'BGP', 'IPV4', 'ACCEPT_ROUTE', bgp_as='65001'),
        network_instance_add_table_connection('ecoc24', 'STATIC', 'BGP', 'IPV4', 'ACCEPT_ROUTE', bgp_as='65001'),
    
        interface('ce1', 0, if_type='ethernetCsmacd', mtu=1500),
        network_instance_interface('ecoc24', 'L3VRF', 'ce1', 0),
        interface('ce1', 0, if_type='ethernetCsmacd', mtu=1500, ipv4_address_prefix=('192.168.10.1', 24), enabled=True),
    
        interface('xe5', 0, if_type='ethernetCsmacd', mtu=1500),
        network_instance_interface('ecoc24', 'L3VRF', 'xe5', 0),
        interface('xe5', 0, if_type='ethernetCsmacd', mtu=1500, ipv4_address_prefix=('192.168.150.1', 24), enabled=True),
    ]
    LOGGER.info('CSGW1 resources_to_set = {:s}'.format(str(csgw1_resources_to_set)))
    results_setconfig = drivers['CSGW1'].SetConfig(csgw1_resources_to_set)
    LOGGER.info('CSGW1 results_setconfig = {:s}'.format(str(results_setconfig)))

    csgw2_resources_to_set = [
        network_instance('ecoc24', 'L3VRF', '192.168.150.2', '65001:1'),
        network_instance_add_protocol_direct('ecoc24', 'L3VRF'),
        network_instance_add_protocol_static('ecoc24', 'L3VRF'),
        network_instance_add_protocol_bgp('ecoc24', 'L3VRF', '192.168.150.2', '65001', neighbors=[
            ('192.168.150.1', '65001')
        ]),
        network_instance_add_table_connection('ecoc24', 'DIRECTLY_CONNECTED', 'BGP', 'IPV4', 'ACCEPT_ROUTE', bgp_as='65001'),
        network_instance_add_table_connection('ecoc24', 'STATIC', 'BGP', 'IPV4', 'ACCEPT_ROUTE', bgp_as='65001'),
    
        interface('ce1', 0, if_type='ethernetCsmacd', mtu=1500),
        network_instance_interface('ecoc24', 'L3VRF', 'ce1', 0),
        interface('ce1', 0, if_type='ethernetCsmacd', mtu=1500, ipv4_address_prefix=('192.168.20.1', 24), enabled=True),
    
        interface('xe5', 0, if_type='ethernetCsmacd', mtu=1500),
        network_instance_interface('ecoc24', 'L3VRF', 'xe5', 0),
        interface('xe5', 0, if_type='ethernetCsmacd', mtu=1500, ipv4_address_prefix=('192.168.150.2', 24), enabled=True),
    ]
    LOGGER.info('CSGW2 resources_to_set = {:s}'.format(str(csgw2_resources_to_set)))
    results_setconfig = drivers['CSGW2'].SetConfig(csgw2_resources_to_set)
    LOGGER.info('CSGW2 results_setconfig = {:s}'.format(str(results_setconfig)))

    csgw1_resources_to_delete = [
        network_instance_interface('ecoc24', 'L3VRF', 'ce1', 0),
        network_instance_interface('ecoc24', 'L3VRF', 'xe5', 0),
        #interface('ce1', 0),
        #interface('xe5', 0),
        network_instance('ecoc24', 'L3VRF'),
    ]
    LOGGER.info('CSGW1 resources_to_delete = {:s}'.format(str(csgw1_resources_to_delete)))
    results_deleteconfig = drivers['CSGW1'].DeleteConfig(csgw1_resources_to_delete)
    LOGGER.info('CSGW1 results_deleteconfig = {:s}'.format(str(results_deleteconfig)))

    csgw2_resources_to_delete = [
        network_instance_interface('ecoc24', 'L3VRF', 'ce1', 0),
        network_instance_interface('ecoc24', 'L3VRF', 'xe5', 0),
        #interface('ce1', 0),
        #interface('xe5', 0),
        network_instance('ecoc24', 'L3VRF'),
    ]
    LOGGER.info('CSGW2 resources_to_delete = {:s}'.format(str(csgw2_resources_to_delete)))
    results_deleteconfig = drivers['CSGW2'].DeleteConfig(csgw2_resources_to_delete)
    LOGGER.info('CSGW2 results_deleteconfig = {:s}'.format(str(results_deleteconfig)))






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

import os
os.environ['DEVICE_EMULATED_ONLY'] = 'YES'

# pylint: disable=wrong-import-position
import logging, pytest, time
from typing import Dict, List
from device.service.driver_api._Driver import (
    RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES,
    RESOURCE_ROUTING_POLICIES, RESOURCE_SERVICES
)
from device.service.drivers.gnmi_openconfig.GnmiOpenConfigDriver import GnmiOpenConfigDriver
from .storage.Storage import Storage
from .tools.manage_config import (
    check_config_endpoints, check_config_interfaces, check_config_network_instances, del_config, get_config, set_config
)
from .tools.check_updates import check_updates
from .tools.request_composers import (
    interface, network_instance, network_instance_interface, network_instance_static_route
)

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


##### DRIVER FIXTURE ###################################################################################################

DRIVER_SETTING_ADDRESS  = '172.20.20.101'
DRIVER_SETTING_PORT     = 6030
DRIVER_SETTING_USERNAME = 'admin'
DRIVER_SETTING_PASSWORD = 'admin'
DRIVER_SETTING_USE_TLS  = False

@pytest.fixture(scope='session')
def driver() -> GnmiOpenConfigDriver:
    _driver = GnmiOpenConfigDriver(
        DRIVER_SETTING_ADDRESS, DRIVER_SETTING_PORT,
        username=DRIVER_SETTING_USERNAME,
        password=DRIVER_SETTING_PASSWORD,
        use_tls=DRIVER_SETTING_USE_TLS,
    )
    _driver.Connect()
    yield _driver
    time.sleep(1)
    _driver.Disconnect()


##### STORAGE FIXTURE ##################################################################################################

@pytest.fixture(scope='session')
def storage() -> Dict:
    yield Storage()


##### NETWORK INSTANCE DETAILS #########################################################################################

NETWORK_INSTANCES = [
    {
        'name': 'test-l3-svc',
        'type': 'L3VRF',
        'interfaces': [
            {'name': 'Ethernet1',  'index': 0, 'ipv4_addr': '192.168.1.1',  'ipv4_prefix': 24, 'enabled': True},
            {'name': 'Ethernet10', 'index': 0, 'ipv4_addr': '192.168.10.1', 'ipv4_prefix': 24, 'enabled': True},
        ],
        'static_routes': [
            {'prefix': '172.0.0.0/24', 'next_hop': '172.16.0.2', 'metric': 1},
            {'prefix': '172.2.0.0/24', 'next_hop': '172.16.0.3', 'metric': 1},
        ]
    },
    #{
    #    'name': 'test-l2-svc',
    #    'type': 'L2VSI',
    #    'interfaces': [
    #        {'name': 'Ethernet2', 'index': 0, 'ipv4_addr': '192.168.1.1',  'ipv4_prefix': 24, 'enabled': True},
    #        {'name': 'Ethernet4', 'index': 0, 'ipv4_addr': '192.168.10.1', 'ipv4_prefix': 24, 'enabled': True},
    #    ],
    #    'static_routes': [
    #        {'prefix': '172.0.0.0/24', 'next_hop': '172.16.0.2', 'metric': 1},
    #        {'prefix': '172.2.0.0/24', 'next_hop': '172.16.0.3', 'metric': 1},
    #    ]
    #}
]


##### TEST METHODS #####################################################################################################

def test_get_endpoints(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    results_getconfig = get_config(driver, [RESOURCE_ENDPOINTS])
    storage.endpoints.populate(results_getconfig)
    check_config_endpoints(driver, storage)


def test_get_interfaces(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    results_getconfig = get_config(driver, [RESOURCE_INTERFACES])
    storage.interfaces.populate(results_getconfig)
    check_config_interfaces(driver, storage)


def test_get_network_instances(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    results_getconfig = get_config(driver, [RESOURCE_NETWORK_INSTANCES])
    storage.network_instances.populate(results_getconfig)
    check_config_network_instances(driver, storage)


def test_set_network_instances(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    check_config_interfaces(driver, storage)
    check_config_network_instances(driver, storage)

    resources_to_set = list()
    ni_names = list()
    for ni in NETWORK_INSTANCES:
        ni_name = ni['name']
        ni_type = ni['type']
        resources_to_set.append(network_instance(ni_name, ni_type))
        ni_names.append(ni_name)
        storage.network_instances.network_instances.add(ni_name, {'type': ni_type})
        storage.network_instances.protocols.add(ni_name, 'DIRECTLY_CONNECTED')
        storage.network_instances.tables.add(ni_name, 'DIRECTLY_CONNECTED', 'IPV4')
        storage.network_instances.tables.add(ni_name, 'DIRECTLY_CONNECTED', 'IPV6')

    results_setconfig = set_config(driver, resources_to_set)
    check_updates(results_setconfig, '/network_instance[{:s}]', ni_names)

    check_config_interfaces(driver, storage, max_retries=10, retry_delay=2.0)
    check_config_network_instances(driver, storage, max_retries=10, retry_delay=2.0)


def test_add_interfaces_to_network_instance(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    check_config_interfaces(driver, storage)
    check_config_network_instances(driver, storage)

    resources_to_set = list()
    ni_if_names = list()
    for ni in NETWORK_INSTANCES:
        ni_name = ni['name']
        for ni_if in ni.get('interfaces', list()):
            if_name     = ni_if['name' ]
            subif_index = ni_if['index']
            resources_to_set.append(network_instance_interface(ni_name, if_name, subif_index))
            ni_if_names.append((ni_name, '{:s}.{:d}'.format(if_name, subif_index)))
            storage.network_instances.interfaces.add(ni_name, if_name, subif_index)

    results_setconfig = set_config(driver, resources_to_set)
    check_updates(results_setconfig, '/network_instance[{:s}]/interface[{:s}]', ni_if_names)

    check_config_interfaces(driver, storage, max_retries=10, retry_delay=2.0)
    check_config_network_instances(driver, storage, max_retries=10, retry_delay=2.0)


def test_set_interfaces(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    check_config_interfaces(driver, storage)
    check_config_network_instances(driver, storage)

    resources_to_set = list()
    if_names = list()
    for ni in NETWORK_INSTANCES:
        for ni_if in ni.get('interfaces', list()):
            if_name      = ni_if['name'       ]
            subif_index  = ni_if['index'      ]
            ipv4_address = ni_if['ipv4_addr'  ]
            ipv4_prefix  = ni_if['ipv4_prefix']
            enabled      = ni_if['enabled'    ]
            resources_to_set.append(interface(
                if_name, subif_index, ipv4_address, ipv4_prefix, enabled
            ))
            if_names.append(if_name)
            storage.interfaces.ipv4_addresses.add(if_name, subif_index, ipv4_address, {
                'origin' : 'STATIC', 'prefix': ipv4_prefix
            })
            default_vlan = storage.network_instances.vlans.get('default', 1)
            default_vlan_members : List[str] = default_vlan.setdefault('members', list())
            if if_name in default_vlan_members: default_vlan_members.remove(if_name)

    results_setconfig = set_config(driver, resources_to_set)
    check_updates(results_setconfig, '/interface[{:s}]', if_names)

    check_config_interfaces(driver, storage, max_retries=10, retry_delay=2.0)
    check_config_network_instances(driver, storage, max_retries=10, retry_delay=2.0)


def test_set_network_instance_static_routes(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    check_config_interfaces(driver, storage)
    check_config_network_instances(driver, storage)

    resources_to_set = list()
    ni_sr_prefixes = list()
    for ni in NETWORK_INSTANCES:
        ni_name = ni['name']
        for ni_sr in ni.get('static_routes', list()):
            ni_sr_prefix   = ni_sr['prefix'  ]
            ni_sr_next_hop = ni_sr['next_hop']
            ni_sr_metric   = ni_sr['metric'  ]
            ni_sr_next_hop_index = 'AUTO_{:d}_{:s}'.format(ni_sr_metric, '-'.join(ni_sr_next_hop.split('.')))
            resources_to_set.append(network_instance_static_route(
                ni_name, ni_sr_prefix, ni_sr_next_hop_index, ni_sr_next_hop, metric=ni_sr_metric
            ))
            ni_sr_prefixes.append((ni_name, ni_sr_prefix))
            storage.network_instances.protocols.add(ni_name, 'STATIC')
            storage.network_instances.protocol_static.add(ni_name, 'STATIC', ni_sr_prefix, {
                'prefix': ni_sr_prefix, 'next_hops': {
                    ni_sr_next_hop_index: {'next_hop': ni_sr_next_hop, 'metric': ni_sr_metric}
                }
            })
            storage.network_instances.tables.add(ni_name, 'STATIC', 'IPV4')
            storage.network_instances.tables.add(ni_name, 'STATIC', 'IPV6')

    results_setconfig = set_config(driver, resources_to_set)
    check_updates(results_setconfig, '/network_instance[{:s}]/static_route[{:s}]', ni_sr_prefixes)

    check_config_interfaces(driver, storage, max_retries=10, retry_delay=2.0)
    check_config_network_instances(driver, storage, max_retries=10, retry_delay=2.0)


def test_del_network_instance_static_routes(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    check_config_interfaces(driver, storage)
    check_config_network_instances(driver, storage)

    resources_to_delete = list()
    ni_sr_prefixes = list()
    for ni in NETWORK_INSTANCES:
        ni_name = ni['name']
        for ni_sr in ni.get('static_routes', list()):
            ni_sr_prefix   = ni_sr['prefix'  ]
            ni_sr_next_hop = ni_sr['next_hop']
            ni_sr_metric   = ni_sr['metric'  ]
            ni_sr_next_hop_index = 'AUTO_{:d}_{:s}'.format(ni_sr_metric, '-'.join(ni_sr_next_hop.split('.')))
            resources_to_delete.append(network_instance_static_route(
                ni_name, ni_sr_prefix, ni_sr_next_hop_index, ni_sr_next_hop, metric=ni_sr_metric
            ))
            ni_sr_prefixes.append((ni_name, ni_sr_prefix))

            storage.network_instances.protocols.remove(ni_name, 'STATIC')
            storage.network_instances.protocol_static.remove(ni_name, 'STATIC', ni_sr_prefix)
            storage.network_instances.tables.remove(ni_name, 'STATIC', 'IPV4')
            storage.network_instances.tables.remove(ni_name, 'STATIC', 'IPV6')

    results_deleteconfig = del_config(driver, resources_to_delete)
    check_updates(results_deleteconfig, '/network_instance[{:s}]/static_route[{:s}]', ni_sr_prefixes)

    check_config_interfaces(driver, storage, max_retries=10, retry_delay=2.0)
    #check_config_network_instances(driver, storage, max_retries=10, retry_delay=2.0)


def test_del_interfaces(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    check_config_interfaces(driver, storage)
    #check_config_network_instances(driver, storage)

    resources_to_delete = list()
    if_names = list()
    for ni in NETWORK_INSTANCES:
        for ni_if in ni.get('interfaces', list()):
            if_name      = ni_if['name'       ]
            subif_index  = ni_if['index'      ]
            ipv4_address = ni_if['ipv4_addr'  ]
            ipv4_prefix  = ni_if['ipv4_prefix']
            enabled      = ni_if['enabled'    ]
            resources_to_delete.append(interface(if_name, subif_index, ipv4_address, ipv4_prefix, enabled))
            if_names.append(if_name)
            storage.interfaces.ipv4_addresses.remove(if_name, subif_index, ipv4_address)
            default_vlan = storage.network_instances.vlans.get('default', 1)
            default_vlan_members : List[str] = default_vlan.setdefault('members', list())
            if if_name not in default_vlan_members: default_vlan_members.append(if_name)

    results_deleteconfig = del_config(driver, resources_to_delete)
    check_updates(results_deleteconfig, '/interface[{:s}]', if_names)

    check_config_interfaces(driver, storage, max_retries=10, retry_delay=2.0)
    #check_config_network_instances(driver, storage, max_retries=10, retry_delay=2.0)


def test_del_interfaces_from_network_instance(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    check_config_interfaces(driver, storage)
    #check_config_network_instances(driver, storage)

    resources_to_delete = list()
    ni_if_names = list()
    for ni in NETWORK_INSTANCES:
        ni_name = ni['name']
        for ni_if in ni.get('interfaces', list()):
            if_name     = ni_if['name' ]
            subif_index = ni_if['index']
            resources_to_delete.append(network_instance_interface(ni_name, if_name, subif_index))
            ni_if_names.append((ni_name, '{:s}.{:d}'.format(if_name, subif_index)))
            storage.network_instances.interfaces.remove(ni_name, if_name, subif_index)

    results_deleteconfig = del_config(driver, resources_to_delete)
    check_updates(results_deleteconfig, '/network_instance[{:s}]/interface[{:s}]', ni_if_names)
    
    check_config_interfaces(driver, storage, max_retries=10, retry_delay=2.0)
    #check_config_network_instances(driver, storage, max_retries=10, retry_delay=2.0)


def test_del_network_instances(
    driver : GnmiOpenConfigDriver,  # pylint: disable=redefined-outer-name
    storage : Storage,              # pylint: disable=redefined-outer-name
) -> None:
    check_config_interfaces(driver, storage)
    #check_config_network_instances(driver, storage)

    resources_to_delete = list()
    ni_names = list()
    for ni in NETWORK_INSTANCES:
        ni_name = ni['name']
        ni_type = ni['type']
        resources_to_delete.append(network_instance(ni_name, ni_type))
        ni_names.append(ni_name)
        storage.network_instances.network_instances.remove(ni_name)
        storage.network_instances.protocols.remove(ni_name, 'DIRECTLY_CONNECTED')
        storage.network_instances.tables.remove(ni_name, 'DIRECTLY_CONNECTED', 'IPV4')
        storage.network_instances.tables.remove(ni_name, 'DIRECTLY_CONNECTED', 'IPV6')

    results_deleteconfig = del_config(driver, resources_to_delete)
    check_updates(results_deleteconfig, '/network_instance[{:s}]', ni_names)

    check_config_interfaces(driver, storage, max_retries=10, retry_delay=2.0)
    check_config_network_instances(driver, storage, max_retries=10, retry_delay=2.0)
