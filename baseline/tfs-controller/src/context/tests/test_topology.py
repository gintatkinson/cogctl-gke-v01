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
from common.proto.context_pb2 import (
    Context, ContextEvent, ContextId, EventTypeEnum, Topology, TopologyEvent, TopologyId)
from context.client.ContextClient import ContextClient
#from context.client.EventsCollector import EventsCollector
from context.service.database.uuids.Topology import topology_get_uuid
from .Constants import GET_EVENTS_TIMEOUT
from .Objects import CONTEXT, CONTEXT_ID, CONTEXT_NAME, TOPOLOGY, TOPOLOGY_ID, TOPOLOGY_NAME

@pytest.mark.depends(on=['context/tests/test_context.py::test_context'])
def test_topology(context_client : ContextClient) -> None:

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    #events_collector = EventsCollector(
    #    context_client, log_events_received=True,
    #    activate_context_collector = True, activate_topology_collector = True, activate_device_collector = False,
    #    activate_link_collector = False, activate_service_collector = False, activate_slice_collector = False,
    #    activate_connection_collector = False)
    #events_collector.start()
    #time.sleep(3) # wait for the events collector to start

    # ----- Prepare dependencies for the test and capture related events -----------------------------------------------
    response = context_client.SetContext(Context(**CONTEXT))
    context_uuid = response.context_uuid.uuid

    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ContextEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert event.context_id.context_uuid.uuid == context_uuid

    # ----- Get when the object does not exist -------------------------------------------------------------------------
    topology_id = TopologyId(**TOPOLOGY_ID)
    context_uuid,topology_uuid = topology_get_uuid(topology_id, allow_random=False)
    with pytest.raises(grpc.RpcError) as e:
        context_client.GetTopology(topology_id)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    MSG = 'Topology({:s}/{:s}) not found; context_uuid generated was: {:s}; topology_uuid generated was: {:s}'
    assert e.value.details() == MSG.format(CONTEXT_NAME, TOPOLOGY_NAME, context_uuid, topology_uuid)

    # ----- List when the object does not exist ------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 0
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    response = context_client.ListTopologyIds(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 0

    response = context_client.ListTopologies(ContextId(**CONTEXT_ID))
    assert len(response.topologies) == 0

    # ----- Create the object ------------------------------------------------------------------------------------------
    response = context_client.SetTopology(Topology(**TOPOLOGY))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.topology_uuid.uuid == topology_uuid

    # ----- Check create event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, TopologyEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert event.topology_id.context_id.context_uuid.uuid == context_uuid
    #assert event.topology_id.topology_uuid.uuid == topology_uuid

    # ----- Get when the object exists ---------------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.name == CONTEXT_NAME
    assert len(response.topology_ids) == 1
    assert response.topology_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.topology_ids[0].topology_uuid.uuid == topology_uuid
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    response = context_client.GetTopology(TopologyId(**TOPOLOGY_ID))
    assert response.topology_id.context_id.context_uuid.uuid == context_uuid
    assert response.topology_id.topology_uuid.uuid == topology_uuid
    assert response.name == TOPOLOGY_NAME
    assert len(response.device_ids) == 0
    assert len(response.link_ids) == 0

    # ----- List when the object exists --------------------------------------------------------------------------------
    response = context_client.ListTopologyIds(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 1
    assert response.topology_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.topology_ids[0].topology_uuid.uuid == topology_uuid

    response = context_client.ListTopologies(ContextId(**CONTEXT_ID))
    assert len(response.topologies) == 1
    assert response.topologies[0].topology_id.context_id.context_uuid.uuid == context_uuid
    assert response.topologies[0].topology_id.topology_uuid.uuid == topology_uuid
    assert response.topologies[0].name == TOPOLOGY_NAME
    assert len(response.topologies[0].device_ids) == 0
    assert len(response.topologies[0].link_ids) == 0

    # ----- Update the object ------------------------------------------------------------------------------------------
    new_topology_name = 'new'
    TOPOLOGY_UPDATED = copy.deepcopy(TOPOLOGY)
    TOPOLOGY_UPDATED['name'] = new_topology_name
    response = context_client.SetTopology(Topology(**TOPOLOGY_UPDATED))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.topology_uuid.uuid == topology_uuid

    # ----- Check update event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, TopologyEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_UPDATE
    #assert event.topology_id.context_id.context_uuid.uuid == context_uuid
    #assert event.topology_id.topology_uuid.uuid == topology_uuid

    # ----- Get when the object is modified ----------------------------------------------------------------------------
    response = context_client.GetTopology(TopologyId(**TOPOLOGY_ID))
    assert response.topology_id.context_id.context_uuid.uuid == context_uuid
    assert response.topology_id.topology_uuid.uuid == topology_uuid
    assert response.name == new_topology_name
    assert len(response.device_ids) == 0
    assert len(response.link_ids) == 0

    # ----- List when the object is modified ---------------------------------------------------------------------------
    response = context_client.ListTopologyIds(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 1
    assert response.topology_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.topology_ids[0].topology_uuid.uuid == topology_uuid

    response = context_client.ListTopologies(ContextId(**CONTEXT_ID))
    assert len(response.topologies) == 1
    assert response.topologies[0].topology_id.context_id.context_uuid.uuid == context_uuid
    assert response.topologies[0].topology_id.topology_uuid.uuid == topology_uuid
    assert response.topologies[0].name == new_topology_name
    assert len(response.topologies[0].device_ids) == 0
    assert len(response.topologies[0].link_ids) == 0

    # ----- Remove the object ------------------------------------------------------------------------------------------
    context_client.RemoveTopology(TopologyId(**TOPOLOGY_ID))

    # ----- Check remove event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, TopologyEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert event.topology_id.context_id.context_uuid.uuid == context_uuid
    #assert event.topology_id.topology_uuid.uuid == topology_uuid

    # ----- List after deleting the object -----------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 0
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    response = context_client.ListTopologyIds(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 0

    response = context_client.ListTopologies(ContextId(**CONTEXT_ID))
    assert len(response.topologies) == 0

    # ----- Clean dependencies used in the test and capture related events ---------------------------------------------
    context_client.RemoveContext(ContextId(**CONTEXT_ID))

    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ContextEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert event.context_id.context_uuid.uuid == context_uuid

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()
