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
    Connection, ConnectionId, Context, ContextId, Device, DeviceId, EndPointId, Service, ServiceId, Topology,
    TopologyId)
#from common.proto.context_pb2 import (
#    ConnectionEvent, ContextEvent, DeviceEvent, EventTypeEnum, ServiceEvent, TopologyEvent)
from context.client.ContextClient import ContextClient
#from context.client.EventsCollector import EventsCollector
from context.service.database.uuids.Connection import connection_get_uuid
from context.service.database.uuids.EndPoint import endpoint_get_uuid
#from .Constants import GET_EVENTS_TIMEOUT
from .Objects import (
    CONNECTION_R1_R3, CONNECTION_R1_R3_ID, CONNECTION_R1_R3_NAME, CONTEXT, CONTEXT_ID, DEVICE_R1, DEVICE_R1_ID,
    DEVICE_R2, DEVICE_R2_ID, DEVICE_R3, DEVICE_R3_ID, SERVICE_R1_R2, SERVICE_R1_R2_ID, SERVICE_R1_R3, SERVICE_R1_R3_ID,
    SERVICE_R2_R3, SERVICE_R2_R3_ID, TOPOLOGY, TOPOLOGY_ID)

@pytest.mark.depends(on=['context/tests/test_service.py::test_service', 'context/tests/test_slice.py::test_slice'])
def test_connection(context_client : ContextClient) -> None:

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    #events_collector = EventsCollector(
    #    context_client, log_events_received=True,
    #    activate_context_collector = True, activate_topology_collector = True, activate_device_collector = True,
    #    activate_link_collector = True, activate_service_collector = True, activate_slice_collector = True,
    #    activate_connection_collector = True)
    #events_collector.start()
    #time.sleep(3)

    # ----- Prepare dependencies for the test and capture related events -----------------------------------------------
    response = context_client.SetContext(Context(**CONTEXT))
    context_uuid = response.context_uuid.uuid

    response = context_client.SetTopology(Topology(**TOPOLOGY))
    assert response.context_id.context_uuid.uuid == context_uuid
    #topology_uuid = response.topology_uuid.uuid

    response = context_client.SetDevice(Device(**DEVICE_R1))
    #device_r1_uuid = response.device_uuid.uuid

    response = context_client.SetDevice(Device(**DEVICE_R2))
    #device_r2_uuid = response.device_uuid.uuid

    response = context_client.SetDevice(Device(**DEVICE_R3))
    #device_r3_uuid = response.device_uuid.uuid

    response = context_client.SetService(Service(**SERVICE_R1_R2))
    assert response.context_id.context_uuid.uuid == context_uuid
    #service_r1_r2_uuid = response.service_uuid.uuid

    response = context_client.SetService(Service(**SERVICE_R2_R3))
    assert response.context_id.context_uuid.uuid == context_uuid
    #service_r2_r3_uuid = response.service_uuid.uuid

    response = context_client.SetService(Service(**SERVICE_R1_R3))
    assert response.context_id.context_uuid.uuid == context_uuid
    service_r1_r3_uuid = response.service_uuid.uuid

    #events = events_collector.get_events(block=True, count=8, timeout=GET_EVENTS_TIMEOUT)
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
    #assert isinstance(events[5], ServiceEvent)
    #assert events[5].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[5].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[5].service_id.service_uuid.uuid == service_r1_r2_uuid
    #assert isinstance(events[6], ServiceEvent)
    #assert events[6].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[6].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[6].service_id.service_uuid.uuid == service_r2_r3_uuid
    #assert isinstance(events[7], ServiceEvent)
    #assert events[7].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[7].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[7].service_id.service_uuid.uuid == service_r1_r3_uuid

    # ----- Get when the object does not exist -------------------------------------------------------------------------
    connection_id = ConnectionId(**CONNECTION_R1_R3_ID)
    connection_uuid = connection_get_uuid(connection_id, allow_random=False)
    with pytest.raises(grpc.RpcError) as e:
        context_client.GetConnection(connection_id)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    MSG = 'Connection({:s}) not found; connection_uuid generated was: {:s}'
    assert e.value.details() == MSG.format(CONNECTION_R1_R3_NAME, connection_uuid)

    # ----- List when the object does not exist ------------------------------------------------------------------------
    response = context_client.ListConnectionIds(ServiceId(**SERVICE_R1_R3_ID))
    assert len(response.connection_ids) == 0

    response = context_client.ListConnections(ServiceId(**SERVICE_R1_R3_ID))
    assert len(response.connections) == 0

    # ----- Create the object ------------------------------------------------------------------------------------------
    with pytest.raises(grpc.RpcError) as e:
        WRONG_CONNECTION = copy.deepcopy(CONNECTION_R1_R3)
        WRONG_CONNECTION['path_hops_endpoint_ids'][0]\
            ['topology_id']['context_id']['context_uuid']['uuid'] = 'wrong-context-uuid'
        context_client.SetConnection(Connection(**WRONG_CONNECTION))
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    wrong_endpoint_id = EndPointId(**WRONG_CONNECTION['path_hops_endpoint_ids'][0])
    _,_,wrong_endpoint_uuid = endpoint_get_uuid(wrong_endpoint_id, allow_random=False)
    msg = 'endpoint({:s}) not found; while inserting in table "connection_endpoint"'.format(wrong_endpoint_uuid)
    assert e.value.details() == msg
    # TODO: should we check that all endpoints belong to same topology?
    # TODO: should we check that endpoints form links over the topology?

    response = context_client.SetConnection(Connection(**CONNECTION_R1_R3))
    connection_r1_r3_uuid = response.connection_uuid.uuid

    # ----- Check create event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ConnectionEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert event.connection_id.connection_uuid.uuid == connection_r1_r3_uuid

    # ----- Get when the object exists ---------------------------------------------------------------------------------
    response = context_client.GetConnection(ConnectionId(**CONNECTION_R1_R3_ID))
    assert response.connection_id.connection_uuid.uuid == connection_r1_r3_uuid
    assert response.service_id.context_id.context_uuid.uuid == context_uuid
    assert response.service_id.service_uuid.uuid == service_r1_r3_uuid
    assert len(response.path_hops_endpoint_ids) == 6
    assert len(response.sub_service_ids) == 2

    # ----- List when the object exists --------------------------------------------------------------------------------
    response = context_client.ListConnectionIds(ServiceId(**SERVICE_R1_R3_ID))
    assert len(response.connection_ids) == 1
    assert response.connection_ids[0].connection_uuid.uuid == connection_r1_r3_uuid

    response = context_client.ListConnections(ServiceId(**SERVICE_R1_R3_ID))
    assert len(response.connections) == 1
    assert response.connections[0].connection_id.connection_uuid.uuid == connection_r1_r3_uuid
    assert len(response.connections[0].path_hops_endpoint_ids) == 6
    assert len(response.connections[0].sub_service_ids) == 2

    # ----- Update the object ------------------------------------------------------------------------------------------
    # TODO: change something... path? subservices?
    response = context_client.SetConnection(Connection(**CONNECTION_R1_R3))
    assert response.connection_uuid.uuid == connection_r1_r3_uuid

    # ----- Check update event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ConnectionEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_UPDATE
    #assert event.connection_id.connection_uuid.uuid == connection_r1_r3_uuid

    # ----- Get when the object is modified ----------------------------------------------------------------------------
    response = context_client.GetConnection(ConnectionId(**CONNECTION_R1_R3_ID))
    assert response.connection_id.connection_uuid.uuid == connection_r1_r3_uuid
    assert response.service_id.context_id.context_uuid.uuid == context_uuid
    assert response.service_id.service_uuid.uuid == service_r1_r3_uuid
    assert len(response.path_hops_endpoint_ids) == 6
    assert len(response.sub_service_ids) == 2

    # ----- List when the object is modified ---------------------------------------------------------------------------
    response = context_client.ListConnectionIds(ServiceId(**SERVICE_R1_R3_ID))
    assert len(response.connection_ids) == 1
    assert response.connection_ids[0].connection_uuid.uuid == connection_r1_r3_uuid

    response = context_client.ListConnections(ServiceId(**SERVICE_R1_R3_ID))
    assert len(response.connections) == 1
    assert response.connections[0].connection_id.connection_uuid.uuid == connection_r1_r3_uuid
    assert len(response.connections[0].path_hops_endpoint_ids) == 6
    assert len(response.connections[0].sub_service_ids) == 2

    # ----- Remove the object ------------------------------------------------------------------------------------------
    context_client.RemoveConnection(ConnectionId(**CONNECTION_R1_R3_ID))

    # ----- Check remove event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ConnectionEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert event.connection_id.connection_uuid.uuid == connection_r1_r3_uuid

    # ----- List after deleting the object -----------------------------------------------------------------------------
    response = context_client.ListConnectionIds(ServiceId(**SERVICE_R1_R3_ID))
    assert len(response.connection_ids) == 0

    response = context_client.ListConnections(ServiceId(**SERVICE_R1_R3_ID))
    assert len(response.connections) == 0

    # ----- Clean dependencies used in the test and capture related events ---------------------------------------------
    context_client.RemoveService(ServiceId(**SERVICE_R1_R3_ID))
    context_client.RemoveService(ServiceId(**SERVICE_R2_R3_ID))
    context_client.RemoveService(ServiceId(**SERVICE_R1_R2_ID))
    context_client.RemoveDevice(DeviceId(**DEVICE_R1_ID))
    context_client.RemoveDevice(DeviceId(**DEVICE_R2_ID))
    context_client.RemoveDevice(DeviceId(**DEVICE_R3_ID))
    context_client.RemoveTopology(TopologyId(**TOPOLOGY_ID))
    context_client.RemoveContext(ContextId(**CONTEXT_ID))

    #events = events_collector.get_events(block=True, count=8, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(events[0], ServiceEvent)
    #assert events[0].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[0].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[0].service_id.service_uuid.uuid == service_r1_r3_uuid
    #assert isinstance(events[1], ServiceEvent)
    #assert events[1].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[1].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[1].service_id.service_uuid.uuid == service_r2_r3_uuid
    #assert isinstance(events[2], ServiceEvent)
    #assert events[2].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[2].service_id.context_id.context_uuid.uuid == context_uuid
    #assert events[2].service_id.service_uuid.uuid == service_r1_r2_uuid
    #assert isinstance(events[3], DeviceEvent)
    #assert events[3].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[3].device_id.device_uuid.uuid == device_r1_uuid
    #assert isinstance(events[4], DeviceEvent)
    #assert events[4].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[4].device_id.device_uuid.uuid == device_r2_uuid
    #assert isinstance(events[5], DeviceEvent)
    #assert events[5].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[5].device_id.device_uuid.uuid == device_r3_uuid
    #assert isinstance(events[6], TopologyEvent)
    #assert events[6].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[6].topology_id.context_id.context_uuid.uuid == context_uuid
    #assert events[6].topology_id.topology_uuid.uuid == topology_uuid
    #assert isinstance(events[7], ContextEvent)
    #assert events[7].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[7].context_id.context_uuid.uuid == context_uuid

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()
