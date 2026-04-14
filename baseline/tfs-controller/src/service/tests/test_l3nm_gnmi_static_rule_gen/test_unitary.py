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

# Run with:
# $ PYTHONPATH=./src python -m service.tests.test_l3nm_gnmi_static_rule_gen.test_unitary

import logging
from typing import List, Optional, Tuple
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import Device, DeviceOperationalStatusEnum, Service
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.tools.object_factory.Device import json_device, json_device_id
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_id
from common.tools.object_factory.Service import json_service_l3nm_planned
from .MockServiceHandler import MockServiceHandler
from .MockTaskExecutor import CacheableObjectType, MockTaskExecutor

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

SERVICE_DC1_DC2 = Service(**json_service_l3nm_planned(
    'svc-dc1-dc2-uuid',
    endpoint_ids=[
        json_endpoint_id(json_device_id('DC1'), 'int'),
        json_endpoint_id(json_device_id('DC2'), 'int'),
    ],
    config_rules=[
        json_config_rule_set('/device[DC1]/endpoint[eth0]/settings', {
            'ipv4_address': '192.168.10.10', 'ipv4_prefix_len': 24, 'sub_interface_index': 0
        }),
        json_config_rule_set('/device[R1]/endpoint[1/2]/settings', {
            'ipv4_address': '10.0.1.1', 'ipv4_prefix_len': 24, 'sub_interface_index': 0
        }),
        #json_config_rule_set('/device[R2]/endpoint[1/2]/settings', {
        #    'ipv4_address': '10.0.2.1', 'ipv4_prefix_len': 24, 'sub_interface_index': 0
        #}),
        json_config_rule_set('/device[DC2]/endpoint[eth0]/settings', {
            'ipv4_address': '192.168.20.10', 'ipv4_prefix_len': 24, 'sub_interface_index': 0
        }),
    ]
))

SERVICE_DC1_DC3 = Service(**json_service_l3nm_planned(
    'svc-dc1-dc3-uuid',
    endpoint_ids=[
        json_endpoint_id(json_device_id('DC1'), 'int'),
        json_endpoint_id(json_device_id('DC3'), 'int'),
    ],
    config_rules=[
        json_config_rule_set('/device[DC1]/endpoint[eth0]/settings', {
            'ipv4_address': '192.168.10.10', 'ipv4_prefix_len': 24, 'sub_interface_index': 0
        }),
        #json_config_rule_set('/device[R1]/endpoint[1/2]/settings', {
        #    'ipv4_address': '10.0.1.1', 'ipv4_prefix_len': 24, 'sub_interface_index': 0
        #}),
        json_config_rule_set('/device[R4]/endpoint[1/1]/settings', {
            'ipv4_address': '10.0.4.1', 'ipv4_prefix_len': 24, 'sub_interface_index': 0
        }),
        json_config_rule_set('/device[DC3]/endpoint[eth0]/settings', {
            'ipv4_address': '192.168.30.10', 'ipv4_prefix_len': 24, 'sub_interface_index': 0
        }),
    ]
))

CONNECTION_ENDPOINTS_DC1_DC2 : List[Tuple[str, str, Optional[str]]] = [
    ('DC1', 'int',  None), ('DC1', 'eth0', None),
    ('R1',  '1/1',  None), ('R1',  '1/2',  None),
    ('R2',  '1/1',  None), ('R2',  '1/2',  None),
    ('R3',  '1/1',  None), ('R3',  '1/2',  None),
    ('DC2', 'eth0', None), ('DC2', 'int',  None),
]

CONNECTION_ENDPOINTS_DC1_DC3 : List[Tuple[str, str, Optional[str]]] = [
    ('DC1', 'int',  None), ('DC1', 'eth0', None),
    ('R1',  '1/1',  None), ('R1',  '1/2',  None),
    ('R2',  '1/1',  None), ('R2',  '1/3',  None),
    ('R4',  '1/1',  None), ('R4',  '1/2',  None),
    ('DC3', 'eth0', None), ('DC3', 'int',  None),
]

def test_l3nm_gnmi_static_rule_gen() -> None:
    dev_op_st_enabled = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED

    mock_task_executor = MockTaskExecutor()
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'DC1', Device(**json_device(
        'uuid-DC1', DeviceTypeEnum.EMULATED_DATACENTER.value, dev_op_st_enabled, name='DC1', endpoints=[
            json_endpoint(json_device_id('uuid-DC1'), 'uuid-int',  'packet', name='int' ),
            json_endpoint(json_device_id('uuid-DC1'), 'uuid-eth0', 'packet', name='eth0'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'DC2', Device(**json_device(
        'uuid-DC2', DeviceTypeEnum.EMULATED_DATACENTER.value, dev_op_st_enabled, name='DC2', endpoints=[
            json_endpoint(json_device_id('uuid-DC2'), 'uuid-int',  'packet', name='int' ),
            json_endpoint(json_device_id('uuid-DC2'), 'uuid-eth0', 'packet', name='eth0'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'DC3', Device(**json_device(
        'uuid-DC3', DeviceTypeEnum.EMULATED_DATACENTER.value, dev_op_st_enabled, name='DC3', endpoints=[
            json_endpoint(json_device_id('uuid-DC3'), 'uuid-int',  'packet', name='int' ),
            json_endpoint(json_device_id('uuid-DC3'), 'uuid-eth0', 'packet', name='eth0'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'R1', Device(**json_device(
        'uuid-R1', DeviceTypeEnum.EMULATED_PACKET_ROUTER.value, dev_op_st_enabled, name='R1', endpoints=[
            json_endpoint(json_device_id('uuid-R1'), 'uuid-1/1', 'packet', name='1/1'),
            json_endpoint(json_device_id('uuid-R1'), 'uuid-1/2', 'packet', name='1/2'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'R2', Device(**json_device(
        'uuid-R2', DeviceTypeEnum.EMULATED_PACKET_ROUTER.value, dev_op_st_enabled, name='R2', endpoints=[
            json_endpoint(json_device_id('uuid-R2'), 'uuid-1/1', 'packet', name='1/1'),
            json_endpoint(json_device_id('uuid-R2'), 'uuid-1/2', 'packet', name='1/2'),
            json_endpoint(json_device_id('uuid-R2'), 'uuid-1/3', 'packet', name='1/3'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'R3', Device(**json_device(
        'uuid-R3', DeviceTypeEnum.EMULATED_PACKET_ROUTER.value, dev_op_st_enabled, name='R3', endpoints=[
            json_endpoint(json_device_id('uuid-R3'), 'uuid-1/1', 'packet', name='1/1'),
            json_endpoint(json_device_id('uuid-R3'), 'uuid-1/2', 'packet', name='1/2'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'R4', Device(**json_device(
        'uuid-R4', DeviceTypeEnum.EMULATED_PACKET_ROUTER.value, dev_op_st_enabled, name='R4', endpoints=[
            json_endpoint(json_device_id('uuid-R4'), 'uuid-1/1', 'packet', name='1/1'),
            json_endpoint(json_device_id('uuid-R4'), 'uuid-1/2', 'packet', name='1/2'),
        ]
    )))

    mock_service_handler = MockServiceHandler(SERVICE_DC1_DC2, mock_task_executor)
    mock_service_handler.SetEndpoint(CONNECTION_ENDPOINTS_DC1_DC2)

    mock_service_handler = MockServiceHandler(SERVICE_DC1_DC3, mock_task_executor)
    mock_service_handler.SetEndpoint(CONNECTION_ENDPOINTS_DC1_DC3)

if __name__ == '__main__':
    test_l3nm_gnmi_static_rule_gen()
