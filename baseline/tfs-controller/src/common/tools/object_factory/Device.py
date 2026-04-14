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

import copy
from typing import Dict, List, Optional, Tuple
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import DeviceDriverEnum, DeviceOperationalStatusEnum
from common.tools.object_factory.ConfigRule import json_config_rule_set

DEVICE_DISABLED = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED

DEVICE_EMUDC_TYPE   = DeviceTypeEnum.EMULATED_DATACENTER.value
DEVICE_EMUOLS_TYPE  = DeviceTypeEnum.EMULATED_OPEN_LINE_SYSTEM.value
DEVICE_EMUPR_TYPE   = DeviceTypeEnum.EMULATED_PACKET_ROUTER.value
DEVICE_EMU_DRIVERS  = [DeviceDriverEnum.DEVICEDRIVER_UNDEFINED]
DEVICE_EMU_ADDRESS  = '127.0.0.1'
DEVICE_EMU_PORT     = '0'

DEVICE_PR_TYPE      = DeviceTypeEnum.PACKET_ROUTER.value
DEVICE_PR_DRIVERS   = [DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG]

DEVICE_TAPI_TYPE    = DeviceTypeEnum.OPEN_LINE_SYSTEM.value
DEVICE_TAPI_DRIVERS = [DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API]

DEVICE_XR_CONSTELLATION_TYPE    = DeviceTypeEnum.XR_CONSTELLATION.value
DEVICE_XR_CONSTELLATION_DRIVERS = [DeviceDriverEnum.DEVICEDRIVER_XR]

# check which enum type and value assign to microwave device
DEVICE_MICROWAVE_TYPE    = DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM.value
DEVICE_MICROWAVE_DRIVERS = [DeviceDriverEnum.DEVICEDRIVER_IETF_NETWORK_TOPOLOGY]

DEVICE_P4_TYPE      = DeviceTypeEnum.P4_SWITCH.value
DEVICE_P4_DRIVERS   = [DeviceDriverEnum.DEVICEDRIVER_P4]

DEVICE_TFS_TYPE    = DeviceTypeEnum.TERAFLOWSDN_CONTROLLER.value
DEVICE_TFS_DRIVERS = [DeviceDriverEnum.DEVICEDRIVER_IETF_L2VPN]

DEVICE_IETF_ACTN_TYPE    = DeviceTypeEnum.OPEN_LINE_SYSTEM.value
DEVICE_IETF_ACTN_DRIVERS = [DeviceDriverEnum.DEVICEDRIVER_IETF_ACTN]

DEVICE_SMARTNIC_TYPE = DeviceTypeEnum.SMARTNIC.value
DEVICE_SMARTNIC_DRIVERS = [DeviceDriverEnum.DEVICEDRIVER_SMARTNIC]

def json_device_id(device_uuid : str):
    return {'device_uuid': {'uuid': device_uuid}}

def json_device(
        device_uuid : str, device_type : str, status : DeviceOperationalStatusEnum, name : Optional[str] = None,
        endpoints : List[Dict] = [], config_rules : List[Dict] = [], drivers : List[Dict] = []
    ):
    result = {
        'device_id'                : json_device_id(device_uuid),
        'device_type'              : device_type,
        'device_config'            : {'config_rules': copy.deepcopy(config_rules)},
        'device_operational_status': status,
        'device_drivers'           : copy.deepcopy(drivers),
        'device_endpoints'         : copy.deepcopy(endpoints),
    }
    if name is not None: result['name'] = name
    return result

def json_device_emulated_packet_router_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_EMU_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_EMUPR_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_emulated_tapi_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_EMU_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_EMUOLS_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_emulated_datacenter_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_EMU_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_EMUDC_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_packetrouter_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_PR_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_PR_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_tapi_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_TAPI_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_TAPI_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_xr_constellation_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_XR_CONSTELLATION_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_XR_CONSTELLATION_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints,
        config_rules=config_rules, drivers=drivers)

def json_device_microwave_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_MICROWAVE_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_MICROWAVE_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_p4_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_P4_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_P4_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_tfs_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_TFS_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_TFS_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_ietf_actn_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_IETF_ACTN_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_IETF_ACTN_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_smartnic_disabled(
        device_uuid : str, name : Optional[str] = None, endpoints : List[Dict] = [], config_rules : List[Dict] = [],
        drivers : List[Dict] = DEVICE_SMARTNIC_DRIVERS
    ):
    return json_device(
        device_uuid, DEVICE_SMARTNIC_TYPE, DEVICE_DISABLED, name=name, endpoints=endpoints, config_rules=config_rules,
        drivers=drivers)

def json_device_connect_rules(address : str, port : int, settings : Dict = {}) -> List[Dict]:
    return [
        json_config_rule_set('_connect/address',  address),
        json_config_rule_set('_connect/port',     port),
        json_config_rule_set('_connect/settings', settings),
    ]

def json_device_emulated_connect_rules(
    endpoint_descriptors : List[Dict], address : str = DEVICE_EMU_ADDRESS, port : int = DEVICE_EMU_PORT
) -> List[Dict]:
    settings = {'endpoints': endpoint_descriptors}
    return json_device_connect_rules(address, port, settings=settings)
