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

import logging, os
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, Empty, ServiceStatusEnum, ServiceTypeEnum
from common.proto.qkd_app_pb2 import QKDAppStatusEnum, QKDAppTypesEnum
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from qkd_app.client.QKDAppClient import QKDAppClient
from service.client.ServiceClient import ServiceClient
from .Fixtures import (     # pylint: disable=unused-import
    context_client, device_client, service_client, qkd_app_client
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))


def compose_path(file_name : str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', file_name)


def test_check_qkd_apps_before(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    qkd_app_client : QKDAppClient,  # pylint: disable=redefined-outer-name
):
    # Check there are no services
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 0

    response = qkd_app_client.ListApps(ADMIN_CONTEXT_ID)
    LOGGER.warning('QKDApps[{:d}] = {:s}'.format(
        len(response.apps), grpc_message_to_json_string(response)
    ))
    assert len(response.apps) == 0

def test_create_direct_link_qkd1_qkd2(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    device_client  : DeviceClient,  # pylint: disable=redefined-outer-name
    service_client : ServiceClient, # pylint: disable=redefined-outer-name
):
    descriptor_file = compose_path('tfs-02-direct-link-qkd1-qkd2.json')

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(
        descriptors_file=descriptor_file, context_client=context_client,
        device_client=device_client, service_client=service_client
    )
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)

    # Verify the scenario has 1 service and 0 slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 1
    assert len(response.slice_ids) == 0

    # Check there are no slices
    response = context_client.ListSlices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Slices[{:d}] = {:s}'.format(
        len(response.slices), grpc_message_to_json_string(response)
    ))
    assert len(response.slices) == 0

    # Check there is 1 service
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 1

    for service in response.services:
        service_id = service.service_id
        assert service.service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE
        assert service.service_type == ServiceTypeEnum.SERVICETYPE_QKD

        response = context_client.ListConnections(service_id)
        LOGGER.warning('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
            grpc_message_to_json_string(service_id), len(response.connections),
            grpc_message_to_json_string(response)
        ))
        assert len(response.connections) == 1

def test_create_direct_link_qkd2_qkd3(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    device_client  : DeviceClient,  # pylint: disable=redefined-outer-name
    service_client : ServiceClient, # pylint: disable=redefined-outer-name
):
    descriptor_file = compose_path('tfs-03-direct-link-qkd2-qkd3.json')

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(
        descriptors_file=descriptor_file, context_client=context_client,
        device_client=device_client, service_client=service_client
    )
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)

    # Verify the scenario has 1 service and 0 slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 2
    assert len(response.slice_ids) == 0

    # Check there are no slices
    response = context_client.ListSlices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Slices[{:d}] = {:s}'.format(
        len(response.slices), grpc_message_to_json_string(response)
    ))
    assert len(response.slices) == 0

    # Check there is 1 service
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 2

    for service in response.services:
        service_id = service.service_id
        assert service.service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE
        assert service.service_type == ServiceTypeEnum.SERVICETYPE_QKD

        response = context_client.ListConnections(service_id)
        LOGGER.warning('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
            grpc_message_to_json_string(service_id), len(response.connections),
            grpc_message_to_json_string(response)
        ))
        assert len(response.connections) == 1

def test_create_virtual_link_qkd1_qkd3(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    device_client  : DeviceClient,  # pylint: disable=redefined-outer-name
    service_client : ServiceClient, # pylint: disable=redefined-outer-name
):
    descriptor_file = compose_path('tfs-04-virtual-link-qkd1-qkd3.json')

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(
        descriptors_file=descriptor_file, context_client=context_client,
        device_client=device_client, service_client=service_client
    )
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)

    # Verify the scenario has 1 service and 0 slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 3
    assert len(response.slice_ids) == 0

    # Check there are no slices
    response = context_client.ListSlices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Slices[{:d}] = {:s}'.format(
        len(response.slices), grpc_message_to_json_string(response)
    ))
    assert len(response.slices) == 0

    # Check there is 1 service
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 3

    for service in response.services:
        service_id = service.service_id
        assert service.service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE
        assert service.service_type == ServiceTypeEnum.SERVICETYPE_QKD

        response = context_client.ListConnections(service_id)
        LOGGER.warning('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
            grpc_message_to_json_string(service_id), len(response.connections),
            grpc_message_to_json_string(response)
        ))
        assert len(response.connections) == 1

def test_check_qkd_apps_after(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    qkd_app_client : QKDAppClient,  # pylint: disable=redefined-outer-name
):
    response = context_client.ListDevices(Empty())
    LOGGER.warning('Devices[{:d}] = {:s}'.format(
        len(response.devices), grpc_message_to_json_string(response)
    ))
    device_uuid_to_name = {
        device.name : device.device_id.device_uuid.uuid
        for device in response.devices
    }

    device_qkd1_uuid = device_uuid_to_name.get('QKD1')
    assert device_qkd1_uuid is not None

    device_qkd3_uuid = device_uuid_to_name.get('QKD3')
    assert device_qkd3_uuid is not None

    pending_device_pairs = {
        (device_qkd1_uuid, device_qkd3_uuid),
        (device_qkd3_uuid, device_qkd1_uuid),
    }

    response = qkd_app_client.ListApps(ADMIN_CONTEXT_ID)
    LOGGER.warning('QKDApps[{:d}] = {:s}'.format(
        len(response.apps), grpc_message_to_json_string(response)
    ))
    assert len(response.apps) == 2

    for app in response.apps:
        assert app.app_status == QKDAppStatusEnum.QKDAPPSTATUS_ON
        assert app.app_type == QKDAppTypesEnum.QKDAPPTYPES_INTERNAL
        local_device_id = app.local_device_id.device_uuid.uuid
        remote_device_id = app.remote_device_id.device_uuid.uuid
        device_pair = (local_device_id, remote_device_id)
        assert device_pair in pending_device_pairs
        pending_device_pairs.remove(device_pair)

    assert len(pending_device_pairs) == 0
