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

import logging, pytest
from common.DeviceTypes import DeviceTypeEnum
from common.Settings import get_setting
from common.tests.EventTools import EVENT_REMOVE, EVENT_UPDATE, check_events
from common.tools.object_factory.Connection import json_connection_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.Service import json_service_id
from common.tools.grpc.Tools import grpc_message_to_json_string
from nbi.tests.mock_osm.MockOSM import MockOSM
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from common.proto.context_pb2 import ContextId, Empty, ServiceTypeEnum
from tests.Fixtures import context_client
from .Fixtures import osm_wim
from .Objects import (
    CONTEXT_ID, CONTEXTS, DEVICE_O1_UUID, DEVICE_R1_UUID, DEVICE_R3_UUID, DEVICES, LINKS, TOPOLOGIES, WIM_MAPPING,
    WIM_PASSWORD, WIM_USERNAME)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DEVTYPE_EMU_PR  = DeviceTypeEnum.EMULATED_PACKET_ROUTER.value
DEVTYPE_EMU_OLS = DeviceTypeEnum.EMULATED_OPEN_LINE_SYSTEM.value


def test_scenario_is_correct(context_client : ContextClient):  # pylint: disable=redefined-outer-name
    # ----- List entities - Ensure service is created ------------------------------------------------------------------
    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == len(CONTEXTS)

    response = context_client.ListTopologies(ContextId(**CONTEXT_ID))
    assert len(response.topologies) == len(TOPOLOGIES)

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == len(DEVICES)

    response = context_client.ListLinks(Empty())
    assert len(response.links) == len(LINKS)

    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    LOGGER.info('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
    assert len(response.services) == 2 # L3NM + TAPI
    for service in response.services:
        service_id = service.service_id
        response = context_client.ListConnections(service_id)
        LOGGER.info('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
            grpc_message_to_json_string(service_id), len(response.connections), grpc_message_to_json_string(response)))
        assert len(response.connections) == 1 # one connection per service


def test_service_removal(context_client : ContextClient, osm_wim : MockOSM): # pylint: disable=redefined-outer-name
    # ----- Start the EventsCollector ----------------------------------------------------------------------------------
    #events_collector = EventsCollector(context_client, log_events_received=True)
    #events_collector.start()

    # ----- Delete Service ---------------------------------------------------------------------------------------------
    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    LOGGER.info('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
    assert len(response.services) == 2 # L3NM + TAPI
    service_uuids = set()
    for service in response.services:
        if service.service_type != ServiceTypeEnum.SERVICETYPE_L3NM: continue
        service_uuid = service.service_id.service_uuid.uuid
        service_uuids.add(service_uuid)
        osm_wim.conn_info[service_uuid] = {}

    assert len(service_uuids) == 1  # assume a single L3NM service has been created
    service_uuid = set(service_uuids).pop()

    osm_wim.delete_connectivity_service(service_uuid)

    # ----- Validate collected events ----------------------------------------------------------------------------------
    #packet_connection_uuid = '{:s}:{:s}'.format(service_uuid, DEVTYPE_EMU_PR)
    #optical_connection_uuid = '{:s}:optical:{:s}'.format(service_uuid, DEVTYPE_EMU_OLS)
    #optical_service_uuid = '{:s}:optical'.format(service_uuid)

    #expected_events = [
    #    ('ConnectionEvent', EVENT_REMOVE, json_connection_id(packet_connection_uuid)),
    #    ('DeviceEvent',     EVENT_UPDATE, json_device_id(DEVICE_R1_UUID)),
    #    ('DeviceEvent',     EVENT_UPDATE, json_device_id(DEVICE_R3_UUID)),
    #    ('ServiceEvent',    EVENT_REMOVE, json_service_id(service_uuid, context_id=CONTEXT_ID)),
    #    ('ConnectionEvent', EVENT_REMOVE, json_connection_id(optical_connection_uuid)),
    #    ('DeviceEvent',     EVENT_UPDATE, json_device_id(DEVICE_O1_UUID)),
    #    ('ServiceEvent',    EVENT_REMOVE, json_service_id(optical_service_uuid, context_id=CONTEXT_ID)),
    #]
    #check_events(events_collector, expected_events)

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()


def test_services_removed(context_client : ContextClient):  # pylint: disable=redefined-outer-name
    # ----- List entities - Ensure service is removed ------------------------------------------------------------------
    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == len(CONTEXTS)

    response = context_client.ListTopologies(ContextId(**CONTEXT_ID))
    assert len(response.topologies) == len(TOPOLOGIES)

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == len(DEVICES)

    response = context_client.ListLinks(Empty())
    assert len(response.links) == len(LINKS)

    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    assert len(response.services) == 0
