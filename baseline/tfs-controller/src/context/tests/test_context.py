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
from common.proto.context_pb2 import Context, ContextId, Empty
#from common.proto.context_pb2 import ContextEvent, EventTypeEnum
from context.client.ContextClient import ContextClient
#from context.client.EventsCollector import EventsCollector
from context.service.database.uuids.Context import context_get_uuid
#from .Constants import GET_EVENTS_TIMEOUT
from .Objects import CONTEXT, CONTEXT_ID, CONTEXT_NAME

def test_context(context_client : ContextClient) -> None:

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    #events_collector = EventsCollector(
    #    context_client, log_events_received=True,
    #    activate_context_collector = True, activate_topology_collector = False, activate_device_collector = False,
    #    activate_link_collector = False, activate_service_collector = False, activate_slice_collector = False,
    #    activate_connection_collector = False)
    #events_collector.start()
    #time.sleep(3) # wait for the events collector to start

    # ----- Get when the object does not exist -------------------------------------------------------------------------
    context_id = ContextId(**CONTEXT_ID)
    context_uuid = context_get_uuid(context_id, allow_random=False)
    with pytest.raises(grpc.RpcError) as e:
        context_client.GetContext(context_id)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    MSG = 'Context({:s}) not found; context_uuid generated was: {:s}'
    assert e.value.details() == MSG.format(CONTEXT_NAME, context_uuid)

    # ----- List when the object does not exist ------------------------------------------------------------------------
    response = context_client.ListContextIds(Empty())
    assert len(response.context_ids) == 0

    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == 0

    # ----- Create the object ------------------------------------------------------------------------------------------
    response = context_client.SetContext(Context(**CONTEXT))
    assert response.context_uuid.uuid == context_uuid

    # ----- Check create event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ContextEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert event.context_id.context_uuid.uuid == context_uuid

    # ----- Get when the object exists ---------------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.name == CONTEXT_NAME
    assert len(response.topology_ids) == 0
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    # ----- List when the object exists --------------------------------------------------------------------------------
    response = context_client.ListContextIds(Empty())
    assert len(response.context_ids) == 1
    assert response.context_ids[0].context_uuid.uuid == context_uuid

    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == 1
    assert response.contexts[0].context_id.context_uuid.uuid == context_uuid
    assert response.contexts[0].name == CONTEXT_NAME
    assert len(response.contexts[0].topology_ids) == 0
    assert len(response.contexts[0].service_ids) == 0
    assert len(response.contexts[0].slice_ids) == 0

    # ----- Update the object ------------------------------------------------------------------------------------------
    new_context_name = 'new'
    CONTEXT_WITH_NAME = copy.deepcopy(CONTEXT)
    CONTEXT_WITH_NAME['name'] = new_context_name
    response = context_client.SetContext(Context(**CONTEXT_WITH_NAME))
    assert response.context_uuid.uuid == context_uuid

    # ----- Check update event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ContextEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_UPDATE
    #assert event.context_id.context_uuid.uuid == context_uuid

    # ----- Get when the object is modified ----------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.name == new_context_name
    assert len(response.topology_ids) == 0
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    # ----- List when the object is modified ---------------------------------------------------------------------------
    response = context_client.ListContextIds(Empty())
    assert len(response.context_ids) == 1
    assert response.context_ids[0].context_uuid.uuid == context_uuid

    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == 1
    assert response.contexts[0].context_id.context_uuid.uuid == context_uuid
    assert response.contexts[0].name == new_context_name
    assert len(response.contexts[0].topology_ids) == 0
    assert len(response.contexts[0].service_ids) == 0
    assert len(response.contexts[0].slice_ids) == 0

    # ----- Remove the object ------------------------------------------------------------------------------------------
    context_client.RemoveContext(ContextId(**CONTEXT_ID))

    # ----- Check remove event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ContextEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert event.context_id.context_uuid.uuid == context_uuid

    # ----- List after deleting the object -----------------------------------------------------------------------------
    response = context_client.ListContextIds(Empty())
    assert len(response.context_ids) == 0

    response = context_client.ListContexts(Empty())
    assert len(response.contexts) == 0

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()
