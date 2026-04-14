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
from common.Settings import get_setting
from common.tests.EventTools import EVENT_REMOVE, check_events
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.Link import json_link_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from common.proto.context_pb2 import ContextId, DeviceId, Empty, LinkId, TopologyId
from common.proto.monitoring_pb2 import KpiId, KpiDescriptorList, AlarmList, AlarmID
from device.client.DeviceClient import DeviceClient
from monitoring.client.MonitoringClient import MonitoringClient
from tests.Fixtures import context_client, device_client, monitoring_client
from .Objects import CONTEXT_ID, CONTEXTS, DEVICES, LINKS, TOPOLOGIES

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


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


def test_scenario_cleanup(
    context_client : ContextClient, device_client : DeviceClient, monitoring_client : MonitoringClient):  # pylint: disable=redefined-outer-name

    # ----- Start the EventsCollector ----------------------------------------------------------------------------------
    #events_collector = EventsCollector(context_client)
    #events_collector.start()

    #expected_events = []

    # ----- Delete Links and Validate Collected Events -----------------------------------------------------------------
    for link in LINKS:
        link_id = link['link_id']
        link_uuid = link_id['link_uuid']['uuid']
        LOGGER.info('Deleting Link {:s}'.format(link_uuid))
        context_client.RemoveLink(LinkId(**link_id))
        #expected_events.append(('LinkEvent', EVENT_REMOVE, json_link_id(link_uuid)))

    # ----- Delete Devices and Validate Collected Events ---------------------------------------------------------------
    for device, _ in DEVICES:
        device_id = device['device_id']
        device_uuid = device_id['device_uuid']['uuid']
        LOGGER.info('Deleting Device {:s}'.format(device_uuid))
        device_client.DeleteDevice(DeviceId(**device_id))
        #expected_events.append(('DeviceEvent', EVENT_REMOVE, json_device_id(device_uuid)))

    # ----- Delete Topologies and Validate Collected Events ------------------------------------------------------------
    for topology in TOPOLOGIES:
        topology_id = topology['topology_id']
        context_uuid = topology_id['context_id']['context_uuid']['uuid']
        topology_uuid = topology_id['topology_uuid']['uuid']
        LOGGER.info('Deleting Topology {:s}/{:s}'.format(context_uuid, topology_uuid))
        context_client.RemoveTopology(TopologyId(**topology_id))
        context_id = json_context_id(context_uuid)
        #expected_events.append(('TopologyEvent', EVENT_REMOVE, json_topology_id(topology_uuid, context_id=context_id)))

    # ----- Delete Contexts and Validate Collected Events --------------------------------------------------------------
    for context in CONTEXTS:
        context_id = context['context_id']
        context_uuid = context_id['context_uuid']['uuid']
        LOGGER.info('Deleting Context {:s}'.format(context_uuid))
        context_client.RemoveContext(ContextId(**context_id))
        #expected_events.append(('ContextEvent', EVENT_REMOVE, json_context_id(context_uuid)))

    # ----- Delete Alarms ----------------------------------------------------------------------------------------------
    response: AlarmList = monitoring_client.GetAlarms(Empty())
    for alarm in response.alarm_descriptor:
        alarm_id = AlarmID()
        alarm_id.alarm_id.uuid = alarm.alarm_id.alarm_id.uuid
        monitoring_client.DeleteAlarm(alarm_id)

    # ----- Delete Kpis ------------------------------------------------------------------------------------------------
    response: KpiDescriptorList = monitoring_client.GetKpiDescriptorList(Empty())
    for kpi_descriptor in response.kpi_descriptor_list:
        kpi_id = KpiId()
        kpi_id.kpi_id.uuid = kpi_descriptor.kpi_id.kpi_id.uuid
        monitoring_client.DeleteKpi(kpi_id)


    # ----- Validate Collected Events ----------------------------------------------------------------------------------
    #check_events(events_collector, expected_events)

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()


def test_scenario_empty_again(context_client : ContextClient, monitoring_client : MonitoringClient):  # pylint: disable=redefined-outer-name
    # ----- List entities - Ensure database is empty again -------------------------------------------------------------
    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == 0

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == 0

    response = context_client.ListLinks(Empty())
    assert len(response.links) == 0

    response = monitoring_client.GetAlarms(Empty())
    assert len(response.alarm_descriptor) == 0

    response = monitoring_client.GetKpiDescriptorList(Empty())
    assert len(response.kpi_descriptor_list) == 0
