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
