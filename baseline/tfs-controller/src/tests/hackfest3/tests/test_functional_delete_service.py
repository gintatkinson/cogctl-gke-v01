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

import copy, logging, pytest
from common.Settings import get_setting
from common.tests.EventTools import EVENT_REMOVE, check_events
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.Service import json_service_id
from common.tools.object_factory.Link import json_link_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from common.proto.context_pb2 import ConfigActionEnum, ContextId, Device, DeviceId, Empty, LinkId, TopologyId, Service, ServiceId, DeviceOperationalStatusEnum
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from .Objects import CONTEXT_ID, CONTEXTS, DEVICES, LINKS, TOPOLOGIES, SERVICES

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


@pytest.fixture(scope='session')
def context_client():
    _client = ContextClient(get_setting('CONTEXTSERVICE_SERVICE_HOST'), get_setting('CONTEXTSERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()


@pytest.fixture(scope='session')
def device_client():
    _client = DeviceClient(get_setting('DEVICESERVICE_SERVICE_HOST'), get_setting('DEVICESERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def service_client():
    _client = ServiceClient(get_setting('SERVICESERVICE_SERVICE_HOST'), get_setting('SERVICESERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()

def test_rules_delete(
    context_client : ContextClient, device_client : DeviceClient, service_client : ServiceClient):  # pylint: disable=redefined-outer-name

    # ----- Create Services ---------------------------------------------------------------
    for service, endpoints in SERVICES:
        # Delete Service (table entries)
        service_uuid = service['service_id']['service_uuid']['uuid']
        print('Deleting Service {:s}'.format(service_uuid))
        service_p4 = copy.deepcopy(service)
        response = service_client.DeleteService(ServiceId(**json_service_id(service_uuid, CONTEXT_ID)))
