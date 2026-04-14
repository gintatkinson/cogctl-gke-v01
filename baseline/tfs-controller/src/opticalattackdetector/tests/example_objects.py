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

from copy import deepcopy

from common.Constants import DEFAULT_CONTEXT_UUID, DEFAULT_TOPOLOGY_UUID
from common.proto.context_pb2 import (ConfigActionEnum, DeviceDriverEnum,
                                      DeviceOperationalStatusEnum,
                                      ServiceStatusEnum, ServiceTypeEnum)

# Some example objects to be used by the tests

# Helper methods
def config_rule(action, resource_value):
    return {"action": action, "resource_value": resource_value}


def endpoint_id(topology_id, device_id, endpoint_uuid):
    return {
        "topology_id": deepcopy(topology_id),
        "device_id": deepcopy(device_id),
        "endpoint_uuid": {"uuid": endpoint_uuid},
    }


def endpoint(topology_id, device_id, endpoint_uuid, endpoint_type):
    return {
        "endpoint_id": endpoint_id(topology_id, device_id, endpoint_uuid),
        "endpoint_type": endpoint_type,
    }


# use "deepcopy" to prevent propagating forced changes during tests
CONTEXT_ID = {"context_uuid": {"uuid": DEFAULT_CONTEXT_UUID}}
CONTEXT = {
    "context_id": deepcopy(CONTEXT_ID),
    "topology_ids": [],
    "service_ids": [],
}

CONTEXT_ID_2 = {"context_uuid": {"uuid": "test"}}
CONTEXT_2 = {
    "context_id": deepcopy(CONTEXT_ID_2),
    "topology_ids": [],
    "service_ids": [],
}

TOPOLOGY_ID = {
    "context_id": deepcopy(CONTEXT_ID),
    "topology_uuid": {"uuid": DEFAULT_TOPOLOGY_UUID},
}
TOPOLOGY = {
    "topology_id": deepcopy(TOPOLOGY_ID),
    "device_ids": [],
    "link_ids": [],
}

DEVICE1_UUID = "DEV1"
DEVICE1_ID = {"device_uuid": {"uuid": DEVICE1_UUID}}
DEVICE1 = {
    "device_id": deepcopy(DEVICE1_ID),
    "device_type": "packet-router",
    "device_config": {
        "config_rules": [
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "value1"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "value2"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "value3"),
        ]
    },
    "device_operational_status": DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED,
    "device_drivers": [
        DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG,
        DeviceDriverEnum.DEVICEDRIVER_P4,
    ],
    "device_endpoints": [
        endpoint(TOPOLOGY_ID, DEVICE1_ID, "EP2", "port-packet-100G"),
        endpoint(TOPOLOGY_ID, DEVICE1_ID, "EP3", "port-packet-100G"),
        endpoint(TOPOLOGY_ID, DEVICE1_ID, "EP100", "port-packet-10G"),
    ],
}

DEVICE2_UUID = "DEV2"
DEVICE2_ID = {"device_uuid": {"uuid": DEVICE2_UUID}}
DEVICE2 = {
    "device_id": deepcopy(DEVICE2_ID),
    "device_type": "packet-router",
    "device_config": {
        "config_rules": [
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "dev/rsrc1/value", "value4"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "dev/rsrc2/value", "value5"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "dev/rsrc3/value", "value6"),
        ]
    },
    "device_operational_status": DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED,
    "device_drivers": [
        DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG,
        DeviceDriverEnum.DEVICEDRIVER_P4,
    ],
    "device_endpoints": [
        endpoint(TOPOLOGY_ID, DEVICE2_ID, "EP1", "port-packet-100G"),
        endpoint(TOPOLOGY_ID, DEVICE2_ID, "EP3", "port-packet-100G"),
        endpoint(TOPOLOGY_ID, DEVICE2_ID, "EP100", "port-packet-10G"),
    ],
}

DEVICE3_UUID = "DEV3"
DEVICE3_ID = {"device_uuid": {"uuid": DEVICE3_UUID}}
DEVICE3 = {
    "device_id": deepcopy(DEVICE3_ID),
    "device_type": "packet-router",
    "device_config": {
        "config_rules": [
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "dev/rsrc1/value", "value4"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "dev/rsrc2/value", "value5"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "dev/rsrc3/value", "value6"),
        ]
    },
    "device_operational_status": DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED,
    "device_drivers": [
        DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG,
        DeviceDriverEnum.DEVICEDRIVER_P4,
    ],
    "device_endpoints": [
        endpoint(TOPOLOGY_ID, DEVICE3_ID, "EP1", "port-packet-100G"),
        endpoint(TOPOLOGY_ID, DEVICE3_ID, "EP2", "port-packet-100G"),
        endpoint(TOPOLOGY_ID, DEVICE3_ID, "EP100", "port-packet-10G"),
    ],
}

LINK_DEV1_DEV2_UUID = "DEV1/EP2 ==> DEV2/EP1"
LINK_DEV1_DEV2_ID = {"link_uuid": {"uuid": LINK_DEV1_DEV2_UUID}}
LINK_DEV1_DEV2 = {
    "link_id": deepcopy(LINK_DEV1_DEV2_ID),
    "link_endpoint_ids": [
        endpoint_id(TOPOLOGY_ID, DEVICE1_ID, "EP2"),
        endpoint_id(TOPOLOGY_ID, DEVICE2_ID, "EP1"),
    ],
}

LINK_DEV2_DEV3_UUID = "DEV2/EP3 ==> DEV3/EP2"
LINK_DEV2_DEV3_ID = {"link_uuid": {"uuid": LINK_DEV2_DEV3_UUID}}
LINK_DEV2_DEV3 = {
    "link_id": deepcopy(LINK_DEV2_DEV3_ID),
    "link_endpoint_ids": [
        endpoint_id(TOPOLOGY_ID, DEVICE2_ID, "EP3"),
        endpoint_id(TOPOLOGY_ID, DEVICE3_ID, "EP2"),
    ],
}

LINK_DEV1_DEV3_UUID = "DEV1/EP3 ==> DEV3/EP1"
LINK_DEV1_DEV3_ID = {"link_uuid": {"uuid": LINK_DEV1_DEV3_UUID}}
LINK_DEV1_DEV3 = {
    "link_id": deepcopy(LINK_DEV1_DEV3_ID),
    "link_endpoint_ids": [
        endpoint_id(TOPOLOGY_ID, DEVICE1_ID, "EP3"),
        endpoint_id(TOPOLOGY_ID, DEVICE3_ID, "EP1"),
    ],
}

SERVICE_DEV1_DEV2_UUID = "SVC:DEV1/EP100-DEV2/EP100"
SERVICE_DEV1_DEV2_ID = {
    "context_id": deepcopy(CONTEXT_ID),
    "service_uuid": {"uuid": SERVICE_DEV1_DEV2_UUID},
}
SERVICE_DEV1_DEV2 = {
    "service_id": deepcopy(SERVICE_DEV1_DEV2_ID),
    "service_type": ServiceTypeEnum.SERVICETYPE_L3NM,
    "service_endpoint_ids": [
        endpoint_id(TOPOLOGY_ID, DEVICE1_ID, "EP100"),
        endpoint_id(TOPOLOGY_ID, DEVICE2_ID, "EP100"),
    ],
    # 'service_constraints': [
    #     {'constraint_type': 'latency_ms', 'constraint_value': '15.2'},
    #     {'constraint_type': 'jitter_us', 'constraint_value': '1.2'},
    # ],
    "service_status": {"service_status": ServiceStatusEnum.SERVICESTATUS_ACTIVE},
    "service_config": {
        "config_rules": [
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc1/value", "value7"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc2/value", "value8"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc3/value", "value9"),
        ]
    },
}

SERVICE_DEV1_DEV3_UUID = "SVC:DEV1/EP100-DEV3/EP100"
SERVICE_DEV1_DEV3_ID = {
    "context_id": deepcopy(CONTEXT_ID),
    "service_uuid": {"uuid": SERVICE_DEV1_DEV3_UUID},
}
SERVICE_DEV1_DEV3 = {
    "service_id": deepcopy(SERVICE_DEV1_DEV3_ID),
    "service_type": ServiceTypeEnum.SERVICETYPE_L3NM,
    "service_endpoint_ids": [
        endpoint_id(TOPOLOGY_ID, DEVICE1_ID, "EP100"),
        endpoint_id(TOPOLOGY_ID, DEVICE3_ID, "EP100"),
    ],
    # 'service_constraints': [
    #     {'constraint_type': 'latency_ms', 'constraint_value': '5.8'},
    #     {'constraint_type': 'jitter_us', 'constraint_value': '0.1'},
    # ],
    "service_status": {"service_status": ServiceStatusEnum.SERVICESTATUS_ACTIVE},
    "service_config": {
        "config_rules": [
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc1/value", "value7"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc2/value", "value8"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc3/value", "value9"),
        ]
    },
}

SERVICE_DEV2_DEV3_UUID = "SVC:DEV2/EP100-DEV3/EP100"
SERVICE_DEV2_DEV3_ID = {
    "context_id": deepcopy(CONTEXT_ID),
    "service_uuid": {"uuid": SERVICE_DEV2_DEV3_UUID},
}
SERVICE_DEV2_DEV3 = {
    "service_id": deepcopy(SERVICE_DEV2_DEV3_ID),
    "service_type": ServiceTypeEnum.SERVICETYPE_L3NM,
    "service_endpoint_ids": [
        endpoint_id(TOPOLOGY_ID, DEVICE2_ID, "EP100"),
        endpoint_id(TOPOLOGY_ID, DEVICE3_ID, "EP100"),
    ],
    # 'service_constraints': [
    #     {'constraint_type': 'latency_ms', 'constraint_value': '23.1'},
    #     {'constraint_type': 'jitter_us', 'constraint_value': '3.4'},
    # ],
    "service_status": {"service_status": ServiceStatusEnum.SERVICESTATUS_ACTIVE},
    "service_config": {
        "config_rules": [
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc1/value", "value7"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc2/value", "value8"),
            config_rule(ConfigActionEnum.CONFIGACTION_SET, "svc/rsrc3/value", "value9"),
        ]
    },
}
