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
#
import csv, logging, os, time
os.environ['DEVICE_EMULATED_ONLY'] = 'YES'

 #pylint: disable=wrong-import-position
from device.service.drivers.gnmi_nokia_srlinux.GnmiNokiaSrLinuxDriver import GnmiNokiaSrLinuxDriver
from device.service.driver_api._Driver import (
    RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES, RESOURCE_TUNNEL_INTERFACE,
    RESOURCE_ROUTING_POLICY, #RESOURCE_ENDPOINTS,
)
#from test_gnmi_nokia_srlinux import (
#    interface, routing_policy, network_instance_default, vlan_interface,
#    network_instance_vrf, tunnel_interface
#)

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
#
#def test_gnmi_nokia_srlinux():
#    driver_settings_leaf1 = {
#        'protocol': 'gnmi',
#        'username': 'admin',
#        'password': 'NokiaSrl1!',
#        'use_tls': True,
#    }
#    dev1_driver = GnmiNokiaSrLinuxDriver('172.20.20.102', 57400, **driver_settings_leaf1)
#    dev1_driver.Connect()
#    resources_to_get_leaf1 = [
#       RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES, RESOURCE_TUNNEL_INTERFACE,
#       RESOURCE_ROUTING_POLICY
#    ]
#    #resources_to_get_leaf1 = [RESOURCE_NETWORK_INSTANCES]
#    LOGGER.info('resources_to_get = {:s}'.format(str(resources_to_get_leaf1)))
#    results_getconfig_leaf1 = dev1_driver.GetConfig(resources_to_get_leaf1)
#    LOGGER.info('results_getconfig = {:s}'.format(str(results_getconfig_leaf1)))
#    time.sleep(1)
#    dev1_driver.Disconnect()

#time computing:

# Assuming GnmiNokiaSrLinuxDriver and other required functions are imported correctly
# Replace LOGGER with logging to maintain consistency
#
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
#def test_gnmi_nokia_srlinux():
#    driver_settings_leaf1 = {
#        'protocol': 'gnmi',
#        'username': 'admin',
#        'password': 'NokiaSrl1!',
#        'use_tls': True,
#    }
#    driver_settings_leaf2 = {
#        'protocol': 'gnmi',
#        'username': 'admin',
#        'password': 'NokiaSrl1!',
#        'use_tls': True,
#    }
#    driver_settings_spine = {
#        'protocol': 'gnmi',
#        'username': 'admin',
#        'password': 'NokiaSrl1!',
#        'use_tls': True,
#    }
#
#    dev1_driver = GnmiNokiaSrLinuxDriver('172.20.20.102', 57400, **driver_settings_leaf1)
#    dev2_driver = GnmiNokiaSrLinuxDriver('172.20.20.103', 57400, **driver_settings_leaf2)
#    spine_driver = GnmiNokiaSrLinuxDriver('172.20.20.101', 57400, **driver_settings_spine)
#
#    dev1_driver.Connect()
#    dev2_driver.Connect()
#    spine_driver.Connect()
#
#    # Resources to get for all devices
#    resources_to_get = [
#       RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES, RESOURCE_TUNNEL_INTERFACE,
#       RESOURCE_ROUTING_POLICY
#    ]
#
#    # Initialize lists to store elapsed times for each device
#    elapsed_times_leaf1 = []
#    elapsed_times_leaf2 = []
#    elapsed_times_spine = []
#
#    for i in range(10):  # Run the test 10 times
#        t0_iteration = time.time()
#
#        # Measure time for GetConfig on Leaf 1
#        t0_leaf1 = time.time()
#        results_getconfig_leaf1 = dev1_driver.GetConfig(resources_to_get)
#        logging.info('Results of GetConfig on Leaf 1 in iteration %d: %s', i, results_getconfig_leaf1)
#        time.sleep(1)
#        t1_leaf1 = time.time()
#        elapsed_time_leaf1 = t1_leaf1 - t0_leaf1
#        elapsed_times_leaf1.append(elapsed_time_leaf1)
#        logging.info("Elapsed time for GetConfig on Leaf 1 in iteration %d: %.2f seconds", i, elapsed_time_leaf1)
#
#        # Measure time for GetConfig on Leaf 2
#        t0_leaf2 = time.time()
#        results_getconfig_leaf2 = dev2_driver.GetConfig(resources_to_get)
#        logging.info('Results of GetConfig on Leaf 2 in iteration %d: %s', i, results_getconfig_leaf2)
#        time.sleep(1)
#        t1_leaf2 = time.time()
#        elapsed_time_leaf2 = t1_leaf2 - t0_leaf2
#        elapsed_times_leaf2.append(elapsed_time_leaf2)
#        logging.info("Elapsed time for GetConfig on Leaf 2 in iteration %d: %.2f seconds", i, elapsed_time_leaf2)
#
#        # Measure time for GetConfig on Spine
#        t0_spine = time.time()
#        results_getconfig_spine = spine_driver.GetConfig(resources_to_get)
#        logging.info('Results of GetConfig on Spine in iteration %d: %s', i, results_getconfig_spine)
#        time.sleep(1)
#        t1_spine = time.time()
#        elapsed_time_spine = t1_spine - t0_spine
#        elapsed_times_spine.append(elapsed_time_spine)
#        logging.info("Elapsed time for GetConfig on Spine in iteration %d: %.2f seconds", i, elapsed_time_spine)
#
#        # Measure the end time for the iteration
#        t1_iteration = time.time()
#        elapsed_time_iteration = t1_iteration - t0_iteration
#        logging.info("Total elapsed time for iteration %d: %.2f seconds", i, elapsed_time_iteration)
#
#    # Log the elapsed times for each device after all iterations
#    logging.info("Elapsed times for Leaf 1: %s", elapsed_times_leaf1)
#    logging.info("Elapsed times for Leaf 2: %s", elapsed_times_leaf2)
#    logging.info("Elapsed times for Spine: %s", elapsed_times_spine)
#
#    # Disconnect from devices
#    dev1_driver.Disconnect()
#    dev2_driver.Disconnect()
#    spine_driver.Disconnect()
#
#    return elapsed_times_leaf1, elapsed_times_leaf2, elapsed_times_spine



# Assuming GnmiNokiaSrLinuxDriver and other required functions are imported correctly
# Replace LOGGER with logging to maintain consistency

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_gnmi_nokia_srlinux():
    driver_settings_leaf1 = {
        'protocol': 'gnmi',
        'username': 'admin',
        'password': 'NokiaSrl1!',
        'use_tls': True,
    }
    driver_settings_leaf2 = {
        'protocol': 'gnmi',
        'username': 'admin',
        'password': 'NokiaSrl1!',
        'use_tls': True,
    }
    driver_settings_spine = {
        'protocol': 'gnmi',
        'username': 'admin',
        'password': 'NokiaSrl1!',
        'use_tls': True,
    }

    dev1_driver = GnmiNokiaSrLinuxDriver('172.20.20.102', 57400, **driver_settings_leaf1)
    dev2_driver = GnmiNokiaSrLinuxDriver('172.20.20.103', 57400, **driver_settings_leaf2)
    spine_driver = GnmiNokiaSrLinuxDriver('172.20.20.101', 57400, **driver_settings_spine)

    dev1_driver.Connect()
    dev2_driver.Connect()
    spine_driver.Connect()

    # Resources to get for all devices
    resources = [
        RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES, RESOURCE_TUNNEL_INTERFACE,
        RESOURCE_ROUTING_POLICY
    ]

    # Initialize dictionaries to store timing information for each resource and device
    timing_info_leaf1 = {resource: [] for resource in resources}
    timing_info_leaf2 = {resource: [] for resource in resources}
    timing_info_spine = {resource: [] for resource in resources}

    for resource in resources:
        logging.info("Checking resource: %s", resource)

        for i in range(1000):  # Run the test 10 times
            t0_iteration = time.time()

            # Measure time for GetConfig on Leaf 1
            t0_leaf1 = time.time()
            results_getconfig_leaf1 = dev1_driver.GetConfig([resource])
            t1_leaf1 = time.time()
            elapsed_time_leaf1 = t1_leaf1 - t0_leaf1
            timing_info_leaf1[resource].append(elapsed_time_leaf1)

            # Measure time for GetConfig on Leaf 2
            t0_leaf2 = time.time()
            results_getconfig_leaf2 = dev2_driver.GetConfig([resource])
            t1_leaf2 = time.time()
            elapsed_time_leaf2 = t1_leaf2 - t0_leaf2
            timing_info_leaf2[resource].append(elapsed_time_leaf2)

            # Measure time for GetConfig on Spine
            t0_spine = time.time()
            results_getconfig_spine = spine_driver.GetConfig([resource])
            t1_spine = time.time()
            elapsed_time_spine = t1_spine - t0_spine
            timing_info_spine[resource].append(elapsed_time_spine)

            # Measure the end time for the iteration
            t1_iteration = time.time()
            elapsed_time_iteration = t1_iteration - t0_iteration
            logging.info(
                "Total elapsed time for resource %s in iteration %d: %.2f seconds",
                resource, i, elapsed_time_iteration
            )

    # Log the timing information for each resource and device at the end
    for resource in resources:
        logging.info("Timing information for resource %s on Leaf 1: %s", resource, timing_info_leaf1[resource])
        logging.info("Timing information for resource %s on Leaf 2: %s", resource, timing_info_leaf2[resource])
        logging.info("Timing information for resource %s on Spine: %s", resource, timing_info_spine[resource])

    # Assume timing_info_leaf1, timing_info_leaf2, and timing_info_spine are dictionaries containing your timing data
    with open('timing_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Resource', 'Leaf1_Times', 'Leaf2_Times', 'Spine_Times']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for resource in resources:
            writer.writerow({
                'Resource': resource,
                'Leaf1_Times': timing_info_leaf1[resource],
                'Leaf2_Times': timing_info_leaf2[resource],
                'Spine_Times': timing_info_spine[resource]
            })

    # Disconnect from devices
    dev1_driver.Disconnect()
    dev2_driver.Disconnect()
    spine_driver.Disconnect()
