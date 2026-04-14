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
# $ PYTHONPATH=./src python -m service.tests.test_l3nm_gnmi_static_rule_gen.test_unitary_sns4sns

import logging
from typing import List, Optional, Tuple
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import Connection, Device, DeviceOperationalStatusEnum, Service
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.tools.object_factory.Connection import json_connection
from common.tools.object_factory.Device import json_device, json_device_id
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_id
from common.tools.object_factory.Service import json_service_l3nm_planned
from .MockServiceHandler import MockServiceHandler
from .MockTaskExecutor import CacheableObjectType, MockTaskExecutor

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

SERVICE = Service(**json_service_l3nm_planned(
    'svc-core-edge-uuid',
    endpoint_ids=[
        json_endpoint_id(json_device_id('core-net'), 'eth1'),
        json_endpoint_id(json_device_id('edge-net'), 'eth1'),
    ],
    config_rules=[
        json_config_rule_set('/settings', {'address_families': ['IPV4'], 'mtu': 1500}),
        json_config_rule_set('/static_routing', {}),

        json_config_rule_set('/device[core-net]/endpoint[eth1]/settings', {
            'address_ip': '10.10.10.0', 'neighbor_address': '10.10.10.229', 'address_prefix': 24, 'index': 0
        }),
        json_config_rule_set('/device[edge-net]/endpoint[eth1]/settings', {
            'address_ip': '10.158.72.0', 'neighbor_address': '10.158.72.229', 'address_prefix': 24, 'index': 0
        }),
    ]
))

CONNECTION_ENDPOINTS : List[Tuple[str, str, Optional[str]]] = [
    #('core-net', 'int',   None),
    ('core-net', 'eth1',  None), ('r1',       'eth10', None),
    ('r1',       'eth2',  None), ('r2',       'eth1',  None),
    ('r2',       'eth10', None), ('edge-net', 'eth1',  None),
    #('edge-net', 'int',   None),
]

def test_l3nm_gnmi_static_rule_gen() -> None:
    dev_op_st_enabled = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED

    mock_task_executor = MockTaskExecutor()
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'core-net', Device(**json_device(
        'core-net', DeviceTypeEnum.EMULATED_DATACENTER.value, dev_op_st_enabled, name='core-net',
        endpoints=[
            json_endpoint(json_device_id('core-net'), 'int',  'packet', name='int' ),
            json_endpoint(json_device_id('core-net'), 'eth1', 'packet', name='eth1'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'edge-net', Device(**json_device(
        'edge-net', DeviceTypeEnum.EMULATED_DATACENTER.value, dev_op_st_enabled, name='edge-net',
        endpoints=[
            json_endpoint(json_device_id('edge-net'), 'int',  'packet', name='int' ),
            json_endpoint(json_device_id('edge-net'), 'eth1', 'packet', name='eth1'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'r1', Device(**json_device(
        'r1', DeviceTypeEnum.EMULATED_PACKET_ROUTER.value, dev_op_st_enabled, name='r1',
        endpoints=[
            json_endpoint(json_device_id('r1'), 'eth2',  'packet', name='eth2' ),
            json_endpoint(json_device_id('r1'), 'eth10', 'packet', name='eth10'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.DEVICE, 'r2', Device(**json_device(
        'r2', DeviceTypeEnum.EMULATED_PACKET_ROUTER.value, dev_op_st_enabled, name='r2',
        endpoints=[
            json_endpoint(json_device_id('r1'), 'eth1',  'packet', name='eth1' ),
            json_endpoint(json_device_id('r1'), 'eth10', 'packet', name='eth10'),
        ]
    )))
    mock_task_executor._store_grpc_object(CacheableObjectType.CONNECTION, 'conn', Connection(**json_connection(
        'conn', path_hops_endpoint_ids=[
            json_endpoint_id(json_device_id(device_uuid), endpoint_uuid=endpoint_uuid)
            for device_uuid, endpoint_uuid, _ in CONNECTION_ENDPOINTS
        ]
    )))

    mock_service_handler = MockServiceHandler(SERVICE, mock_task_executor)
    mock_service_handler.SetEndpoint(CONNECTION_ENDPOINTS, connection_uuid='conn')
    mock_service_handler.DeleteEndpoint(CONNECTION_ENDPOINTS, connection_uuid='conn')

if __name__ == '__main__':
    test_l3nm_gnmi_static_rule_gen()
