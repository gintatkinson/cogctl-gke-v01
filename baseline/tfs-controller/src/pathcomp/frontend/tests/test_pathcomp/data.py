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


import json
from typing import Dict, Tuple
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import ConfigActionEnum, Device

path_hops = [
    {'device': 'DC1',      'ingress_ep': 'int',                  'egress_ep': 'eth1'                 },
    {'device': 'PE1',      'ingress_ep': '1/1',                  'egress_ep': '1/2'                  },
    {'device': 'MW1-2',    'ingress_ep': '172.18.0.1:1',         'egress_ep': '172.18.0.2:1'         },
    {'device': 'HUB1',     'ingress_ep': '1/1',                  'egress_ep': 'XR-T1'                },
    {'device': 'splitter', 'ingress_ep': 'common',               'egress_ep': 'leaf1'                },
    {'device': 'OLS',      'ingress_ep': 'node_1_port_13-input', 'egress_ep': 'node_4_port_13-output'},
    {'device': 'LEAF2',    'ingress_ep': 'XR-T1',                'egress_ep': '1/1'                  },
    {'device': 'PE4',      'ingress_ep': '1/1',                  'egress_ep': '1/2'                  },
    {'device': 'DC2',      'ingress_ep': 'eth2',                 'egress_ep': 'int'                  }
]

device_data = {
    'TFS'     : {'controller_uuid': None,  'device_type': DeviceTypeEnum.TERAFLOWSDN_CONTROLLER   },
    'IPM'     : {'controller_uuid': None,  'device_type': DeviceTypeEnum.XR_CONSTELLATION         },
    'OLS'     : {'controller_uuid': None,  'device_type': DeviceTypeEnum.OPEN_LINE_SYSTEM         },
    'MW1-2'   : {'controller_uuid': None,  'device_type': DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM   },
    'MW3-4'   : {'controller_uuid': None,  'device_type': DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM   },

    'DC1'     : {'controller_uuid': None,  'device_type': DeviceTypeEnum.EMULATED_DATACENTER      },
    'DC2'     : {'controller_uuid': None,  'device_type': DeviceTypeEnum.EMULATED_DATACENTER      },

    'PE1'     : {'controller_uuid': 'TFS', 'device_type': DeviceTypeEnum.PACKET_ROUTER            },
    'PE2'     : {'controller_uuid': 'TFS', 'device_type': DeviceTypeEnum.PACKET_ROUTER            },
    'PE3'     : {'controller_uuid': 'TFS', 'device_type': DeviceTypeEnum.PACKET_ROUTER            },
    'PE4'     : {'controller_uuid': 'TFS', 'device_type': DeviceTypeEnum.PACKET_ROUTER            },

    'HUB1'    : {'controller_uuid': 'IPM', 'device_type': DeviceTypeEnum.PACKET_ROUTER            },
    'LEAF1'   : {'controller_uuid': 'IPM', 'device_type': DeviceTypeEnum.PACKET_ROUTER            },
    'LEAF2'   : {'controller_uuid': 'IPM', 'device_type': DeviceTypeEnum.PACKET_ROUTER            },

    'splitter': {'controller_uuid': None,  'device_type': DeviceTypeEnum.EMULATED_OPTICAL_SPLITTER},
}

def process_device(device_uuid, json_device) -> Tuple[Dict, Device]:
    grpc_device = Device()
    grpc_device.device_id.device_uuid.uuid = device_uuid            # pylint: disable=no-member
    grpc_device.device_type = json_device['device_type'].value
    controller_uuid = json_device.get('controller_uuid')
    if controller_uuid is not None:
        config_rule = grpc_device.device_config.config_rules.add()  # pylint: disable=no-member
        config_rule.action = ConfigActionEnum.CONFIGACTION_SET
        config_rule.custom.resource_key = '_controller'
        config_rule.custom.resource_value = json.dumps({'uuid': controller_uuid})
    return json_device, grpc_device

device_dict = {
    device_uuid:process_device(device_uuid, json_device)
    for device_uuid,json_device in device_data.items()
}
