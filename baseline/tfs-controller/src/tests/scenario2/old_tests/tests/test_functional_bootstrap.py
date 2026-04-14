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
from common.proto.monitoring_pb2 import KpiDescriptorList
from common.tests.EventTools import EVENT_CREATE, EVENT_UPDATE, check_events
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.Link import json_link_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from monitoring.client.MonitoringClient import MonitoringClient
from context.client.EventsCollector import EventsCollector
from common.proto.context_pb2 import Context, ContextId, Device, Empty, Link, Topology
from common.proto.monitoring_pb2 import AlarmDescriptor, AlarmList
from device.client.DeviceClient import DeviceClient
from .Objects import CONTEXT_ID, CONTEXTS, DEVICES, LINKS, TOPOLOGIES
from tests.Fixtures import context_client, device_client, monitoring_client
from .Fixtures import alarm_descriptor

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def test_scenario_empty(context_client : ContextClient):  # pylint: disable=redefined-outer-name
    # ----- List entities - Ensure database is empty -------------------------------------------------------------------
    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == 0

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == 0

    response = context_client.ListLinks(Empty())
    assert len(response.links) == 0


def test_prepare_scenario(context_client : ContextClient):  # pylint: disable=redefined-outer-name

    # ----- Start the EventsCollector ----------------------------------------------------------------------------------
    #events_collector = EventsCollector(context_client)
    #events_collector.start()

    #expected_events = []

    # ----- Create Contexts and Topologies -----------------------------------------------------------------------------
    for context in CONTEXTS:
        context_uuid = context['context_id']['context_uuid']['uuid']
        LOGGER.info('Adding Context {:s}'.format(context_uuid))
        response = context_client.SetContext(Context(**context))
        assert response.context_uuid.uuid == context_uuid
        #expected_events.append(('ContextEvent', EVENT_CREATE, json_context_id(context_uuid)))

    for topology in TOPOLOGIES:
        context_uuid = topology['topology_id']['context_id']['context_uuid']['uuid']
        topology_uuid = topology['topology_id']['topology_uuid']['uuid']
        LOGGER.info('Adding Topology {:s}/{:s}'.format(context_uuid, topology_uuid))
        response = context_client.SetTopology(Topology(**topology))
        assert response.context_id.context_uuid.uuid == context_uuid
        assert response.topology_uuid.uuid == topology_uuid
        context_id = json_context_id(context_uuid)
        #expected_events.append(('TopologyEvent', EVENT_CREATE, json_topology_id(topology_uuid, context_id=context_id)))

    # ----- Validate Collected Events ----------------------------------------------------------------------------------
    #check_events(events_collector, expected_events)

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()


def test_scenario_ready(context_client : ContextClient):  # pylint: disable=redefined-outer-name
    # ----- List entities - Ensure scenario is ready -------------------------------------------------------------------
    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == len(CONTEXTS)

    response = context_client.ListTopologies(ContextId(**CONTEXT_ID))
    assert len(response.topologies) == len(TOPOLOGIES)

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == 0

    response = context_client.ListLinks(Empty())
    assert len(response.links) == 0

    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    assert len(response.services) == 0


def test_devices_bootstraping(
    context_client : ContextClient, device_client : DeviceClient):  # pylint: disable=redefined-outer-name

    # ----- Start the EventsCollector ----------------------------------------------------------------------------------
    #events_collector = EventsCollector(context_client, log_events_received=True)
    #events_collector.start()

    #expected_events = []

    # ----- Create Devices and Validate Collected Events ---------------------------------------------------------------
    for device, connect_rules in DEVICES:
        device_uuid = device['device_id']['device_uuid']['uuid']
        LOGGER.info('Adding Device {:s}'.format(device_uuid))

        device_with_connect_rules = copy.deepcopy(device)
        device_with_connect_rules['device_config']['config_rules'].extend(connect_rules)
        response = device_client.AddDevice(Device(**device_with_connect_rules))
        assert response.device_uuid.uuid == device_uuid

        #expected_events.extend([
        #    # Device creation, update for ztp to start the device
        #    ('DeviceEvent', EVENT_CREATE, json_device_id(device_uuid)),
        #    #('DeviceEvent', EVENT_UPDATE, json_device_id(device_uuid)),
        #])

        #response = context_client.GetDevice(response)
        #for endpoint in response.device_endpoints:
        #    for _ in endpoint.kpi_sample_types:
        #        # Monitoring configures monitoring for endpoint
        #        expected_events.append(('DeviceEvent', EVENT_UPDATE, json_device_id(device_uuid)))

    # ----- Validate Collected Events ----------------------------------------------------------------------------------
    #check_events(events_collector, expected_events)

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()


def test_devices_bootstrapped(context_client : ContextClient):  # pylint: disable=redefined-outer-name
    # ----- List entities - Ensure bevices are created -----------------------------------------------------------------
    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == len(CONTEXTS)

    response = context_client.ListTopologies(ContextId(**CONTEXT_ID))
    assert len(response.topologies) == len(TOPOLOGIES)

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == len(DEVICES)

    response = context_client.ListLinks(Empty())
    assert len(response.links) == 0

    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    assert len(response.services) == 0


def test_links_creation(context_client : ContextClient):  # pylint: disable=redefined-outer-name

    # ----- Start the EventsCollector ----------------------------------------------------------------------------------
    #events_collector = EventsCollector(context_client)
    #events_collector.start()

    #expected_events = []

    # ----- Create Links and Validate Collected Events -----------------------------------------------------------------
    for link in LINKS:
        link_uuid = link['link_id']['link_uuid']['uuid']
        LOGGER.info('Adding Link {:s}'.format(link_uuid))
        response = context_client.SetLink(Link(**link))
        assert response.link_uuid.uuid == link_uuid
        #expected_events.append(('LinkEvent', EVENT_CREATE, json_link_id(link_uuid)))

    # ----- Validate Collected Events ----------------------------------------------------------------------------------
    #check_events(events_collector, expected_events)

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()


def test_links_created(context_client : ContextClient):  # pylint: disable=redefined-outer-name
    # ----- List entities - Ensure links are created -------------------------------------------------------------------
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


def test_scenario_kpis_created(monitoring_client: MonitoringClient):
    """
    This test validates that KPIs related to the service/device/endpoint were created
    during the service creation process.
    """
    response: KpiDescriptorList = monitoring_client.GetKpiDescriptorList(Empty())
    LOGGER.info("Number of KPIs created: {}".format(len(response.kpi_descriptor_list)))
    # TODO: replace the magic number `16` below for a formula that adapts to the number
    # of links and devices
    assert len(response.kpi_descriptor_list) == 16


def test_scenario_alarms_created(monitoring_client: MonitoringClient, alarm_descriptor : AlarmDescriptor):
    # ----- Create one alarm per Kpi created ----------------------------------------------------------------------------
    response: KpiDescriptorList = monitoring_client.GetKpiDescriptorList(Empty())

    for kpi_descriptor in response.kpi_descriptor_list:
        new_alarm_descriptor                    = alarm_descriptor
        new_alarm_descriptor.kpi_id.kpi_id.uuid = kpi_descriptor.kpi_id.kpi_id.uuid
        monitoring_client.SetKpiAlarm(new_alarm_descriptor)

    response: AlarmList = monitoring_client.GetAlarms(Empty())
    assert len(response.alarm_descriptor) == 16
