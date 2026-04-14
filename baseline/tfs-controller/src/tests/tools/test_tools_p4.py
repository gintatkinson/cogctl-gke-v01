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
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, DeviceOperationalStatusEnum,\
    DeviceDriverEnum, ServiceTypeEnum, ServiceStatusEnum
from common.tools.object_factory.Context import json_context_id

# Context info
CONTEXT_NAME_P4 = DEFAULT_CONTEXT_NAME
ADMIN_CONTEXT_ID = ContextId(**json_context_id(CONTEXT_NAME_P4))

# Device and rule cardinality variables
DEV_NB = 4
P4_DEV_NB = 1
CONNECTION_RULES = 3
ENDPOINT_RULES = 3
INT_RULES = 19
L2_RULES = 10
L3_RULES = 4
ACL_RULES = 1

DATAPLANE_RULES_NB_INT_B1 = 5
DATAPLANE_RULES_NB_INT_B2 = 6
DATAPLANE_RULES_NB_INT_B3 = 8
DATAPLANE_RULES_NB_RT_WEST = 7
DATAPLANE_RULES_NB_RT_EAST = 7
DATAPLANE_RULES_NB_ACL = 1
DATAPLANE_RULES_NB_TOT = \
    DATAPLANE_RULES_NB_INT_B1 +\
    DATAPLANE_RULES_NB_INT_B2 +\
    DATAPLANE_RULES_NB_INT_B3 +\
    DATAPLANE_RULES_NB_RT_WEST +\
    DATAPLANE_RULES_NB_RT_EAST +\
    DATAPLANE_RULES_NB_ACL

# Service-related variables
SVC_NB = 1
NO_SERVICES = 0
NO_SLICES = 0

TEST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    )) + '/p4-fabric-tna/descriptors')
assert os.path.exists(TEST_PATH), "Invalid path to P4 SD-Fabric tests"

# Topology descriptor
DESC_TOPO = os.path.join(TEST_PATH, 'topology.json')
assert os.path.exists(DESC_TOPO), "Invalid path to the SD-Fabric topology descriptor"

# SBI descriptors
# The switch cannot digest all rules at once, hence we insert in batches
DESC_FILE_RULES_INSERT_INT_B1 = os.path.join(TEST_PATH, 'sbi-rules-insert-int-b1.json')
assert os.path.exists(DESC_FILE_RULES_INSERT_INT_B1),\
    "Invalid path to the SD-Fabric INT SBI descriptor (batch #1)"

DESC_FILE_RULES_INSERT_INT_B2 = os.path.join(TEST_PATH, 'sbi-rules-insert-int-b2.json')
assert os.path.exists(DESC_FILE_RULES_INSERT_INT_B2),\
    "Invalid path to the SD-Fabric INT SBI descriptor (batch #2)"

DESC_FILE_RULES_INSERT_INT_B3 = os.path.join(TEST_PATH, 'sbi-rules-insert-int-b3.json')
assert os.path.exists(DESC_FILE_RULES_INSERT_INT_B3),\
    "Invalid path to the SD-Fabric INT SBI descriptor (batch #3)"

DESC_FILE_RULES_INSERT_ROUTING_WEST = os.path.join(TEST_PATH, 'sbi-rules-insert-routing-west.json')
assert os.path.exists(DESC_FILE_RULES_INSERT_ROUTING_WEST),\
    "Invalid path to the SD-Fabric routing SBI descriptor (domain1-side)"

DESC_FILE_RULES_INSERT_ROUTING_EAST = os.path.join(TEST_PATH, 'sbi-rules-insert-routing-east.json')
assert os.path.exists(DESC_FILE_RULES_INSERT_ROUTING_EAST),\
    "Invalid path to the SD-Fabric routing SBI descriptor (domain2-side)"

DESC_FILE_RULES_INSERT_ACL = os.path.join(TEST_PATH, 'sbi-rules-insert-acl.json')
assert os.path.exists(DESC_FILE_RULES_INSERT_ACL),\
    "Invalid path to the SD-Fabric ACL SBI descriptor"

DESC_FILE_RULES_DELETE_ALL = os.path.join(TEST_PATH, 'sbi-rules-remove.json')
assert os.path.exists(DESC_FILE_RULES_DELETE_ALL),\
    "Invalid path to the SD-Fabric rule removal SBI descriptor"

# Service descriptors
DESC_FILE_SERVICE_P4_INT = os.path.join(TEST_PATH, 'service-p4-int.json')
assert os.path.exists(DESC_FILE_SERVICE_P4_INT),\
    "Invalid path to the SD-Fabric INT service descriptor"

DESC_FILE_SERVICE_P4_L2_SIMPLE = os.path.join(TEST_PATH, 'service-p4-l2-simple.json')
assert os.path.exists(DESC_FILE_SERVICE_P4_L2_SIMPLE),\
    "Invalid path to the SD-Fabric L2 simple service descriptor"

DESC_FILE_SERVICE_P4_L3 = os.path.join(TEST_PATH, 'service-p4-l3.json')
assert os.path.exists(DESC_FILE_SERVICE_P4_L3),\
    "Invalid path to the SD-Fabric L3 service descriptor"

DESC_FILE_SERVICE_P4_ACL = os.path.join(TEST_PATH, 'service-p4-acl.json')
assert os.path.exists(DESC_FILE_SERVICE_P4_ACL),\
    "Invalid path to the SD-Fabric ACL service descriptor"

def identify_number_of_p4_devices(devices) -> int:
    p4_dev_no = 0

    # Iterate all devices
    for device in devices:
        # Skip non-P4 devices
        if not DeviceDriverEnum.DEVICEDRIVER_P4 in device.device_drivers: continue

        p4_dev_no += 1
    
    return p4_dev_no

def get_number_of_rules(devices) -> int:
    total_rules_no = 0

    # Iterate all devices
    for device in devices:
        # Skip non-P4 devices
        if not DeviceDriverEnum.DEVICEDRIVER_P4 in device.device_drivers: continue

        # We want the device to be active
        assert device.device_operational_status == \
            DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED

        # Get the configuration rules of this device
        config_rules = device.device_config.config_rules

        # Expected rule cardinality
        total_rules_no += len(config_rules)
    
    return total_rules_no

def verify_number_of_rules(devices, desired_rules_nb : int) -> None:
    # Iterate all devices
    for device in devices:
        # Skip non-P4 devices
        if not DeviceDriverEnum.DEVICEDRIVER_P4 in device.device_drivers: continue

        # We want the device to be active
        assert device.device_operational_status == \
            DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED

        # Get the configuration rules of this device
        config_rules = device.device_config.config_rules

        # Expected rule cardinality
        assert len(config_rules) == desired_rules_nb

def verify_active_service_type(services, target_service_type : ServiceTypeEnum) -> bool: # type: ignore
    # Iterate all services
    for service in services:
        # Ignore services of other types
        if service.service_type != target_service_type:
            continue

        service_id = service.service_id
        assert service_id
        assert service.service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE
        assert service.service_config
        return True
    
    return False
