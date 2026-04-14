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

import copy, grpc, pytest #, time
from common.proto.context_pb2 import Context, ContextId, Device, DeviceId, Empty, Link, LinkId, Topology, TopologyId
#from common.proto.context_pb2 import ContextEvent, DeviceEvent, EventTypeEnum, LinkEvent, TopologyEvent
from context.client.ContextClient import ContextClient
#from context.client.EventsCollector import EventsCollector
from context.service.database.uuids.Link import link_get_uuid
#from .Constants import GET_EVENTS_TIMEOUT
from .Objects import (
    CONTEXT, CONTEXT_ID, DEVICE_R1, DEVICE_R1_ID, DEVICE_R2, DEVICE_R2_ID, LINK_R1_R2, LINK_R1_R2_ID, LINK_R1_R2_NAME,
    TOPOLOGY, TOPOLOGY_ID)

@pytest.mark.depends(on=['context/tests/test_device.py::test_device'])
def test_link(context_client : ContextClient) -> None:

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    #events_collector = EventsCollector(
    #    context_client, log_events_received=True,
    #    activate_context_collector = True, activate_topology_collector = True, activate_device_collector = True,
    #    activate_link_collector = True, activate_service_collector = False, activate_slice_collector = False,
    #    activate_connection_collector = False)
    #events_collector.start()
    #time.sleep(3)

    # ----- Prepare dependencies for the test and capture related events -----------------------------------------------
    response = context_client.SetContext(Context(**CONTEXT))
    context_uuid = response.context_uuid.uuid

    response = context_client.SetTopology(Topology(**TOPOLOGY))
    assert response.context_id.context_uuid.uuid == context_uuid
    topology_uuid = response.topology_uuid.uuid

    response = context_client.SetDevice(Device(**DEVICE_R1))
    device_r1_uuid = response.device_uuid.uuid

    response = context_client.SetDevice(Device(**DEVICE_R2))
    device_r2_uuid = response.device_uuid.uuid

    #events = events_collector.get_events(block=True, count=4, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(events[0], ContextEvent)
    #assert events[0].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[0].context_id.context_uuid.uuid == context_uuid
    #assert isinstance(events[1], TopologyEvent)
    #assert events[1].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[1].topology_id.context_id.context_uuid.uuid == context_uuid
    #assert events[1].topology_id.topology_uuid.uuid == topology_uuid
    #assert isinstance(events[2], DeviceEvent)
    #assert events[2].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[2].device_id.device_uuid.uuid == device_r1_uuid
    #assert isinstance(events[3], DeviceEvent)
    #assert events[3].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[3].device_id.device_uuid.uuid == device_r2_uuid

    # ----- Get when the object does not exist -------------------------------------------------------------------------
    link_id = LinkId(**LINK_R1_R2_ID)
    link_uuid = link_get_uuid(link_id, allow_random=False)
    with pytest.raises(grpc.RpcError) as e:
        context_client.GetLink(link_id)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    MSG = 'Link({:s}) not found; link_uuid generated was: {:s}'
    assert e.value.details() == MSG.format(LINK_R1_R2_NAME, link_uuid)

    # ----- List when the object does not exist ------------------------------------------------------------------------
    response = context_client.ListLinkIds(Empty())
    assert len(response.link_ids) == 0

    response = context_client.ListLinks(Empty())
    assert len(response.links) == 0

    # ----- Create the object ------------------------------------------------------------------------------------------
    response = context_client.SetLink(Link(**LINK_R1_R2))
    assert response.link_uuid.uuid == link_uuid

    # ----- Check create event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, LinkEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert event.link_id.link_uuid.uuid == link_uuid

    # ----- Get when the object exists ---------------------------------------------------------------------------------
    response = context_client.GetLink(LinkId(**LINK_R1_R2_ID))
    assert response.link_id.link_uuid.uuid == link_uuid
    assert response.name == LINK_R1_R2_NAME
    assert len(response.link_endpoint_ids) == 2
    assert response.HasField('attributes')
    # In proto3, HasField() does not work for scalar fields, using ListFields() instead.
    attribute_names = set([field.name for field,_ in response.attributes.ListFields()])
    assert 'total_capacity_gbps' in attribute_names
    assert abs(response.attributes.total_capacity_gbps - 100) < 1.e-12
    assert (
        ('used_capacity_gbps' not in attribute_names) or (
            ('used_capacity_gbps' in attribute_names) and (
                abs(response.attributes.used_capacity_gbps - response.attributes.total_capacity_gbps) < 1.e-12
            )
        )
    )

    # ----- List when the object exists --------------------------------------------------------------------------------
    response = context_client.ListLinkIds(Empty())
    assert len(response.link_ids) == 1
    assert response.link_ids[0].link_uuid.uuid == link_uuid

    response = context_client.ListLinks(Empty())
    assert len(response.links) == 1
    assert response.links[0].link_id.link_uuid.uuid == link_uuid
    assert response.links[0].name == LINK_R1_R2_NAME
    assert len(response.links[0].link_endpoint_ids) == 2

    # ----- Update the object ------------------------------------------------------------------------------------------
    new_link_name = 'new'
    LINK_UPDATED = copy.deepcopy(LINK_R1_R2)
    LINK_UPDATED['name'] = new_link_name
    LINK_UPDATED['attributes']['total_capacity_gbps'] = 200
    LINK_UPDATED['attributes']['used_capacity_gbps'] = 50
    response = context_client.SetLink(Link(**LINK_UPDATED))
    assert response.link_uuid.uuid == link_uuid

    # ----- Check update event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, LinkEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_UPDATE
    #assert event.link_id.link_uuid.uuid == link_uuid

    # ----- Get when the object is modified ----------------------------------------------------------------------------
    response = context_client.GetLink(LinkId(**LINK_R1_R2_ID))
    assert response.link_id.link_uuid.uuid == link_uuid
    assert response.name == new_link_name
    assert len(response.link_endpoint_ids) == 2
    assert response.HasField('attributes')
    # In proto3, HasField() does not work for scalar fields, using ListFields() instead.
    attribute_names = set([field.name for field,_ in response.attributes.ListFields()])
    assert 'total_capacity_gbps' in attribute_names
    assert abs(response.attributes.total_capacity_gbps - 200) < 1.e-12
    assert 'used_capacity_gbps' in attribute_names
    assert abs(response.attributes.used_capacity_gbps - 50) < 1.e-12

    # ----- List when the object is modified ---------------------------------------------------------------------------
    response = context_client.ListLinkIds(Empty())
    assert len(response.link_ids) == 1
    assert response.link_ids[0].link_uuid.uuid == link_uuid

    response = context_client.ListLinks(Empty())
    assert len(response.links) == 1
    assert response.links[0].link_id.link_uuid.uuid == link_uuid
    assert response.links[0].name == new_link_name
    assert len(response.links[0].link_endpoint_ids) == 2
    assert len(response.links[0].link_endpoint_ids) == 2
    assert response.links[0].HasField('attributes')
    # In proto3, HasField() does not work for scalar fields, using ListFields() instead.
    attribute_names = set([field.name for field,_ in response.links[0].attributes.ListFields()])
    assert 'total_capacity_gbps' in attribute_names
    assert abs(response.links[0].attributes.total_capacity_gbps - 200) < 1.e-12
    assert 'used_capacity_gbps' in attribute_names
    assert abs(response.links[0].attributes.used_capacity_gbps - 50) < 1.e-12

    # ----- Check relation was created ---------------------------------------------------------------------------------
    response = context_client.GetTopology(TopologyId(**TOPOLOGY_ID))
    assert response.topology_id.context_id.context_uuid.uuid == context_uuid
    assert response.topology_id.topology_uuid.uuid == topology_uuid
    assert len(response.device_ids) == 2
    assert response.device_ids[0].device_uuid.uuid in {device_r1_uuid, device_r2_uuid}
    assert response.device_ids[1].device_uuid.uuid in {device_r1_uuid, device_r2_uuid}
    assert len(response.link_ids) == 1
    assert response.link_ids[0].link_uuid.uuid == link_uuid

    # ----- Remove the object ------------------------------------------------------------------------------------------
    context_client.RemoveLink(LinkId(**LINK_R1_R2_ID))

    # ----- Check remove event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, LinkEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert event.link_id.link_uuid.uuid == link_uuid

    # ----- List after deleting the object -----------------------------------------------------------------------------
    response = context_client.ListLinkIds(Empty())
    assert len(response.link_ids) == 0

    response = context_client.ListLinks(Empty())
    assert len(response.links) == 0

    response = context_client.GetTopology(TopologyId(**TOPOLOGY_ID))
    assert response.topology_id.context_id.context_uuid.uuid == context_uuid
    assert response.topology_id.topology_uuid.uuid == topology_uuid
    assert len(response.device_ids) == 2
    assert response.device_ids[0].device_uuid.uuid in {device_r1_uuid, device_r2_uuid}
    assert response.device_ids[1].device_uuid.uuid in {device_r1_uuid, device_r2_uuid}
    assert len(response.link_ids) == 0

    # ----- Clean dependencies used in the test and capture related events ---------------------------------------------
    context_client.RemoveDevice(DeviceId(**DEVICE_R1_ID))
    context_client.RemoveDevice(DeviceId(**DEVICE_R2_ID))
    context_client.RemoveTopology(TopologyId(**TOPOLOGY_ID))
    context_client.RemoveContext(ContextId(**CONTEXT_ID))

    #events = events_collector.get_events(block=True, count=4, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(events[0], DeviceEvent)
    #assert events[0].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[0].device_id.device_uuid.uuid == device_r1_uuid
    #assert isinstance(events[1], DeviceEvent)
    #assert events[1].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[1].device_id.device_uuid.uuid == device_r2_uuid
    #assert isinstance(events[2], TopologyEvent)
    #assert events[2].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[2].topology_id.context_id.context_uuid.uuid == context_uuid
    #assert events[2].topology_id.topology_uuid.uuid == topology_uuid
    #assert isinstance(events[3], ContextEvent)
    #assert events[3].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[3].context_id.context_uuid.uuid == context_uuid

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()
