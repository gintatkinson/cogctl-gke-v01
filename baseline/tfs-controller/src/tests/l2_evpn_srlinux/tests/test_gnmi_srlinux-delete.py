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

import logging, os, time
os.environ['DEVICE_EMULATED_ONLY'] = 'YES'

# pylint: disable=wrong-import-position
from device.service.drivers.gnmi_nokia_srlinux.GnmiNokiaSrLinuxDriver import GnmiNokiaSrLinuxDriver
from .test_gnmi_nokia_srlinux import (
    interface, routing_policy, network_instance_default, vlan_interface,
    network_instance_vrf, tunnel_interface
)

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def test_gnmi_nokia_srlinux():
    driver_settings_leaf1 = {
        'protocol': 'gnmi',
        'username': 'admin',
        'password': 'NokiaSrl1!',
        'use_tls' : True,
    }
    dev1_driver = GnmiNokiaSrLinuxDriver('172.20.20.102', 57400, **driver_settings_leaf1)
    dev1_driver.Connect()
    resources_to_delete = [
        ####LEAF1#####
        interface('ethernet-1/49', True, 0, True, '192.168.11.1', '30'),
        routing_policy('all', 'accept'),
        network_instance_default(
            'default', 'ethernet-1/49.0', 'system0.0', True, 'ipv4-unicast', 101, 'all',
            'eBGP-underlay', 'all', 201, True, 'evpn', False, 'ipv4-unicast', 'all',
            'iBGP-overlay', 'all', 100, 100, 1, True, '10.0.0.2', 'iBGP-overlay', '10.0.0.1',
            '192.168.11.2', 'eBGP-underlay', '10.0.0.1'
        ),
        interface('system0', True, 0, True, '10.0.0.1', '32'),
        vlan_interface('ethernet-1/1', True, 0, 'bridged', True, 'untagged'),
        network_instance_vrf(
            'vrf-1', 'mac-vrf', True, 'ethernet-1/1.0', 'vxlan1.1', 1, True, 'vxlan1.1', 111,
            1, 'target:100:111', 'target:100:111'
        ),
        tunnel_interface('vxlan1', 1, 'bridged', 1),
    ]

    LOGGER.info('resources_to_delete = {:s}'.format(str(resources_to_delete)))
    results_deleteconfig_leaf1 = dev1_driver.DeleteConfig(resources_to_delete)
    LOGGER.info('results_delete = {:s}'.format(str(results_deleteconfig_leaf1)))
    time.sleep(1)
    dev1_driver.Disconnect()
