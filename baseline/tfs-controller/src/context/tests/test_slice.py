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

import copy, grpc, pytest, time
from common.proto.context_pb2 import (
    Context, ContextId, Device, DeviceId, Link, LinkId, Service, ServiceId, Slice, SliceId, SliceStatusEnum, Topology,
    TopologyId)
#from common.proto.context_pb2 import (
#    ContextEvent, DeviceEvent, EventTypeEnum, LinkEvent, ServiceEvent, SliceEvent, TopologyEvent)
from context.client.ContextClient import ContextClient
#from context.client.EventsCollector import EventsCollector
from context.service.database.uuids.Slice import slice_get_uuid
#from .Constants import GET_EVENTS_TIMEOUT
from .Objects import (
    CONTEXT, CONTEXT_ID, CONTEXT_NAME, DEVICE_R1, DEVICE_R1_ID, DEVICE_R2, DEVICE_R2_ID, DEVICE_R3, DEVICE_R3_ID,
    LINK_R1_R2, LINK_R1_R2_ID, LINK_R1_R3, LINK_R1_R3_ID, LINK_R2_R3, LINK_R2_R3_ID, SERVICE_R1_R2, SERVICE_R1_R2_ID,
    SERVICE_R2_R3, SERVICE_R2_R3_ID, SLICE_R1_R3, SLICE_R1_R3_ID, SLICE_R1_R3_NAME, TOPOLOGY, TOPOLOGY_ID)

@pytest.mark.depends(on=['context/tests/test_service.py::test_service'])
def test_slice(context_client : ContextClient) -> None:

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    #events_collector = EventsCollector(
    #    context_client, log_events_received=True,
    #    activate_context_collector = True, activate_topology_collector = True, activate_device_collector = True,
    #    activate_link_collector = True, activate_service_collector = True, activate_slice_collector = True,
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

    response = context_client.SetDevice(Device(**DEVICE_R3))
    device_r3_uuid = response.device_uuid.uuid
    
    response = context_client.SetLink(Link(**LINK_R1_R2))
    link_r1_r2_uuid = response.link_uuid.uuid
    
    response = context_client.SetLink(Link(**LINK_R1_R3))
    link_r1_r3_uuid = response.link_uuid.uuid
    
    response = context_client.SetLink(Link(**LINK_R2_R3))
    link_r2_r3_uuid = response.link_uuid.uuid
    
    response = context_client.SetService(Service(**SERVICE_R1_R2))
    assert response.context_id.context_uuid.uuid == context_uuid
    service_r1_r2_uuid = response.service_uuid.uuid

    response = context_client.SetService(Service(**SERVICE_R2_R3))
    assert response.context_id.context_uuid.uuid == context_uuid
    service_r2_r3_uuid = response.service_uuid.uuid

    #events = events_collector.get_events(block=True, count=10, timeout=GET_EVENTS_TIMEOUT)
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
    #assert isinstance(events[4], DeviceEvent)
    #assert events[4].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[4].device_id.device_uuid.uuid == device_r3_uuid
    #assert isinstance(events[5], LinkEvent)
    #assert events[5].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[5].link_id.link_uuid.uuid == link_r1_r2_uuid
    #assert isinstance(events[6], LinkEvent)
    #assert events[6].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[6].link_id.link_uuid.uuid == link_r1_r3_uuid
    #assert isinstance(events[7], LinkEvent)
    #assert events[7].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[7].link_id.link_uuid.uuid == link_r2_r3_uuid
    #assert isinstance(events[8], ServiceEvent)
    #assert events[8].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[8].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[8].service_id.service_uuid.uuid == service_r1_r2_uuid
    #assert isinstance(events[9], ServiceEvent)
    #assert events[9].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[9].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[9].service_id.service_uuid.uuid == service_r2_r3_uuid

    # ----- Get when the object does not exist -------------------------------------------------------------------------
    slice_id = SliceId(**SLICE_R1_R3_ID)
    context_uuid,slice_uuid = slice_get_uuid(slice_id, allow_random=False)
    with pytest.raises(grpc.RpcError) as e:
        context_client.GetSlice(slice_id)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    MSG = 'Slice({:s}/{:s}) not found; context_uuid generated was: {:s}; slice_uuid generated was: {:s}'
    assert e.value.details() == MSG.format(CONTEXT_NAME, SLICE_R1_R3_NAME, context_uuid, slice_uuid)

    # ----- List when the object does not exist ------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 1
    assert len(response.service_ids) == 2
    assert len(response.slice_ids) == 0

    response = context_client.ListSliceIds(ContextId(**CONTEXT_ID))
    assert len(response.slice_ids) == 0

    response = context_client.ListSlices(ContextId(**CONTEXT_ID))
    assert len(response.slices) == 0

    # ----- Create the object ------------------------------------------------------------------------------------------
    with pytest.raises(grpc.RpcError) as e:
        WRONG_UUID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
        WRONG_SLICE = copy.deepcopy(SLICE_R1_R3)
        WRONG_SLICE['slice_endpoint_ids'][0]['topology_id']['context_id']['context_uuid']['uuid'] = WRONG_UUID
        context_client.SetSlice(Slice(**WRONG_SLICE))
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    MSG = 'request.slice_endpoint_ids[0].topology_id.context_id.context_uuid.uuid({}) is invalid; '\
          'should be == request.slice_id.context_id.context_uuid.uuid({})'
    raw_context_uuid = slice_id.context_id.context_uuid.uuid # pylint: disable=no-member
    assert e.value.details() == MSG.format(WRONG_UUID, raw_context_uuid)

    response = context_client.SetSlice(Slice(**SLICE_R1_R3))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.slice_uuid.uuid == slice_uuid

    # ----- Check create event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, SliceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert event.slice_id.context_id.context_uuid.uuid == context_uuid
    #assert event.slice_id.slice_uuid.uuid == slice_uuid

    # ----- Get when the object exists ---------------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.name == CONTEXT_NAME
    assert len(response.topology_ids) == 1
    assert len(response.service_ids) == 2
    assert len(response.slice_ids) == 1
    assert response.slice_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.slice_ids[0].slice_uuid.uuid == slice_uuid

    response = context_client.GetSlice(SliceId(**SLICE_R1_R3_ID))
    assert response.slice_id.context_id.context_uuid.uuid == context_uuid
    assert response.slice_id.slice_uuid.uuid == slice_uuid
    assert response.name == SLICE_R1_R3_NAME
    assert len(response.slice_endpoint_ids) == 2
    assert len(response.slice_constraints) == 2
    assert response.slice_status.slice_status == SliceStatusEnum.SLICESTATUS_PLANNED
    assert len(response.slice_config.config_rules) == 3

    # ----- List when the object exists --------------------------------------------------------------------------------
    response = context_client.ListSliceIds(ContextId(**CONTEXT_ID))
    assert len(response.slice_ids) == 1
    assert response.slice_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.slice_ids[0].slice_uuid.uuid == slice_uuid

    response = context_client.ListSlices(ContextId(**CONTEXT_ID))
    assert len(response.slices) == 1
    assert response.slices[0].slice_id.context_id.context_uuid.uuid == context_uuid
    assert response.slices[0].slice_id.slice_uuid.uuid == slice_uuid
    assert response.slices[0].name == SLICE_R1_R3_NAME
    assert len(response.slices[0].slice_endpoint_ids) == 2
    assert len(response.slices[0].slice_constraints) == 2
    assert response.slices[0].slice_status.slice_status == SliceStatusEnum.SLICESTATUS_PLANNED
    assert len(response.slices[0].slice_config.config_rules) == 3

    # ----- Update the object ------------------------------------------------------------------------------------------
    new_slice_name = 'new'
    SLICE_UPDATED = copy.deepcopy(SLICE_R1_R3)
    SLICE_UPDATED['name'] = new_slice_name
    SLICE_UPDATED['slice_status']['slice_status'] = SliceStatusEnum.SLICESTATUS_ACTIVE
    response = context_client.SetSlice(Slice(**SLICE_UPDATED))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.slice_uuid.uuid == slice_uuid

    # ----- Check update event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, SliceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_UPDATE
    #assert event.slice_id.context_id.context_uuid.uuid == context_uuid
    #assert event.slice_id.slice_uuid.uuid == slice_uuid

    # ----- Get when the object is modified ----------------------------------------------------------------------------
    response = context_client.GetSlice(SliceId(**SLICE_R1_R3_ID))
    assert response.slice_id.context_id.context_uuid.uuid == context_uuid
    assert response.slice_id.slice_uuid.uuid == slice_uuid
    assert response.name == new_slice_name
    assert len(response.slice_endpoint_ids) == 2
    assert len(response.slice_constraints) == 2
    assert response.slice_status.slice_status == SliceStatusEnum.SLICESTATUS_ACTIVE
    assert len(response.slice_config.config_rules) == 3

    # ----- List when the object is modified ---------------------------------------------------------------------------
    response = context_client.ListSliceIds(ContextId(**CONTEXT_ID))
    assert len(response.slice_ids) == 1
    assert response.slice_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.slice_ids[0].slice_uuid.uuid == slice_uuid

    response = context_client.ListSlices(ContextId(**CONTEXT_ID))
    assert len(response.slices) == 1
    assert response.slices[0].slice_id.context_id.context_uuid.uuid == context_uuid
    assert response.slices[0].slice_id.slice_uuid.uuid == slice_uuid
    assert response.slices[0].name == new_slice_name
    assert len(response.slices[0].slice_endpoint_ids) == 2
    assert len(response.slices[0].slice_constraints) == 2
    assert response.slices[0].slice_status.slice_status == SliceStatusEnum.SLICESTATUS_ACTIVE
    assert len(response.slices[0].slice_config.config_rules) == 3

    # ----- Remove the object ------------------------------------------------------------------------------------------
    context_client.RemoveSlice(SliceId(**SLICE_R1_R3_ID))

    # ----- Check remove event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, SliceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert event.slice_id.context_id.context_uuid.uuid == context_uuid
    #assert event.slice_id.slice_uuid.uuid == slice_uuid

    # ----- List after deleting the object -----------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 1
    assert len(response.service_ids) == 2
    assert len(response.slice_ids) == 0

    response = context_client.ListSliceIds(ContextId(**CONTEXT_ID))
    assert len(response.slice_ids) == 0

    response = context_client.ListSlices(ContextId(**CONTEXT_ID))
    assert len(response.slices) == 0

    # ----- Clean dependencies used in the test and capture related events ---------------------------------------------
    context_client.RemoveService(ServiceId(**SERVICE_R1_R2_ID))
    context_client.RemoveService(ServiceId(**SERVICE_R2_R3_ID))
    context_client.RemoveLink(LinkId(**LINK_R1_R2_ID))
    context_client.RemoveLink(LinkId(**LINK_R1_R3_ID))
    context_client.RemoveLink(LinkId(**LINK_R2_R3_ID))
    context_client.RemoveDevice(DeviceId(**DEVICE_R1_ID))
    context_client.RemoveDevice(DeviceId(**DEVICE_R2_ID))
    context_client.RemoveDevice(DeviceId(**DEVICE_R3_ID))
    context_client.RemoveTopology(TopologyId(**TOPOLOGY_ID))
    context_client.RemoveContext(ContextId(**CONTEXT_ID))

    #events = events_collector.get_events(block=True, count=10)
    #assert isinstance(events[0], ServiceEvent)
    #assert events[0].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[0].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[0].service_id.service_uuid.uuid == service_r1_r2_uuid
    #assert isinstance(events[1], ServiceEvent)
    #assert events[1].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[1].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[1].service_id.service_uuid.uuid == service_r2_r3_uuid
    #assert isinstance(events[2], LinkEvent)
    #assert events[2].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[2].link_id.link_uuid.uuid == link_r1_r2_uuid
    #assert isinstance(events[3], LinkEvent)
    #assert events[3].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[3].link_id.link_uuid.uuid == link_r1_r3_uuid
    #assert isinstance(events[4], LinkEvent)
    #assert events[4].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[4].link_id.link_uuid.uuid == link_r2_r3_uuid
    #assert isinstance(events[5], DeviceEvent)
    #assert events[5].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[5].device_id.device_uuid.uuid == device_r1_uuid
    #assert isinstance(events[6], DeviceEvent)
    #assert events[6].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[6].device_id.device_uuid.uuid == device_r2_uuid
    #assert isinstance(events[7], DeviceEvent)
    #assert events[7].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[7].device_id.device_uuid.uuid == device_r3_uuid
    #assert isinstance(events[8], TopologyEvent)
    #assert events[8].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[8].topology_id.context_id.context_uuid.uuid == context_uuid
    #assert events[8].topology_id.topology_uuid.uuid == topology_uuid
    #assert isinstance(events[9], ContextEvent)
    #assert events[9].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[9].context_id.context_uuid.uuid == context_uuid

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()
