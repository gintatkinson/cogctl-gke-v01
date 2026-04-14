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

import logging
from common.proto.context_pb2 import ServiceId, DeviceId, LinkId, ServiceStatusEnum, ServiceTypeEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.Service import json_service_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from tests.Fixtures import context_client, device_client, service_client # pylint: disable=unused-import
from tests.tools.test_tools_p4 import ADMIN_CONTEXT_ID

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def test_clean_services(
    context_client : ContextClient,  # pylint: disable=redefined-outer-name
    service_client : ServiceClient  # pylint: disable=redefined-outer-name
) -> None:
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
    
    for service in response.services:
        service_id = service.service_id
        assert service_id

        service_uuid = service_id.service_uuid.uuid
        context_uuid = service_id.context_id.context_uuid.uuid
        assert service.service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE
        assert service.service_type == ServiceTypeEnum.SERVICETYPE_INT

        # Delete service
        service_client.DeleteService(ServiceId(**json_service_id(service_uuid, json_context_id(context_uuid))))

def test_clean_links(
    context_client : ContextClient,  # pylint: disable=redefined-outer-name
) -> None:
    response = context_client.ListLinks(ADMIN_CONTEXT_ID)
    
    for link in response.links:
        link_id = link.link_id

        # Delete link
        context_client.RemoveLink(LinkId(**link_id))

def test_clean_devices(
    context_client : ContextClient,  # pylint: disable=redefined-outer-name
    device_client : DeviceClient   # pylint: disable=redefined-outer-name
) -> None:
    response = context_client.ListDevices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Devices[{:d}] = {:s}'.format(len(response.devices), grpc_message_to_json_string(response)))
    
    for device in response.devices:
        device_uuid = device.device_id.device_uuid.uuid
        device_json = json_device_id(device_uuid)

        # Delete device
        device_client.DeleteDevice(DeviceId(**device_json))

def test_clean_context(
    context_client : ContextClient  # pylint: disable=redefined-outer-name
) -> None:
    # Verify the scenario has no services/slices
    response = context_client.ListTopologies(ADMIN_CONTEXT_ID)

    for topology in response.topologies:
        topology_id = topology.topology_id
        response = context_client.RemoveTopology(topology_id)

    response = context_client.RemoveContext(ADMIN_CONTEXT_ID)
