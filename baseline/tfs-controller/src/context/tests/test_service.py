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
    Context, ContextId, Device, DeviceId, Service, ServiceId, ServiceStatusEnum, ServiceTypeEnum, Topology, TopologyId)
#from common.proto.context_pb2 import (
#    ContextEvent, DeviceEvent, EventTypeEnum, ServiceEvent, TopologyEvent)
from context.client.ContextClient import ContextClient
#from context.client.EventsCollector import EventsCollector
from context.service.database.uuids.Service import service_get_uuid
#from .Constants import GET_EVENTS_TIMEOUT
from .Objects import (
    CONTEXT, CONTEXT_ID, CONTEXT_NAME, DEVICE_R1, DEVICE_R1_ID, SERVICE_R1_R2_NAME, DEVICE_R2, DEVICE_R2_ID,
    SERVICE_R1_R2, SERVICE_R1_R2_ID, TOPOLOGY, TOPOLOGY_ID)

@pytest.mark.depends(on=['context/tests/test_link.py::test_link'])
def test_service(context_client : ContextClient) -> None:

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    #events_collector = EventsCollector(
    #    context_client, log_events_received=True,
    #    activate_context_collector = True, activate_topology_collector = True, activate_device_collector = True,
    #    activate_link_collector = True, activate_service_collector = True, activate_slice_collector = False,
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
    service_id = ServiceId(**SERVICE_R1_R2_ID)
    context_uuid,service_uuid = service_get_uuid(service_id, allow_random=False)
    with pytest.raises(grpc.RpcError) as e:
        context_client.GetService(service_id)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    MSG = 'Service({:s}/{:s}) not found; context_uuid generated was: {:s}; service_uuid generated was: {:s}'
    assert e.value.details() == MSG.format(CONTEXT_NAME, SERVICE_R1_R2_NAME, context_uuid, service_uuid)

    # ----- List when the object does not exist ------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 1
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    response = context_client.ListServiceIds(ContextId(**CONTEXT_ID))
    assert len(response.service_ids) == 0

    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    assert len(response.services) == 0

    # ----- Create the object ------------------------------------------------------------------------------------------
    with pytest.raises(grpc.RpcError) as e:
        WRONG_UUID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
        WRONG_SERVICE = copy.deepcopy(SERVICE_R1_R2)
        WRONG_SERVICE['service_endpoint_ids'][0]['topology_id']['context_id']['context_uuid']['uuid'] = WRONG_UUID
        context_client.SetService(Service(**WRONG_SERVICE))
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    MSG = 'request.service_endpoint_ids[0].topology_id.context_id.context_uuid.uuid({}) is invalid; '\
          'should be == request.service_id.context_id.context_uuid.uuid({})'
    raw_context_uuid = service_id.context_id.context_uuid.uuid # pylint: disable=no-member
    assert e.value.details() == MSG.format(WRONG_UUID, raw_context_uuid)

    response = context_client.SetService(Service(**SERVICE_R1_R2))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.service_uuid.uuid == service_uuid

    # ----- Check create event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ServiceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert event.service_id.context_id.context_uuid.uuid == context_uuid
    #assert event.service_id.service_uuid.uuid == service_uuid

    # ----- Get when the object exists ---------------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.name == CONTEXT_NAME
    assert len(response.topology_ids) == 1
    assert len(response.service_ids) == 1
    assert response.service_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.service_ids[0].service_uuid.uuid == service_uuid
    assert len(response.slice_ids) == 0

    response = context_client.GetService(ServiceId(**SERVICE_R1_R2_ID))
    assert response.service_id.context_id.context_uuid.uuid == context_uuid
    assert response.service_id.service_uuid.uuid == service_uuid
    assert response.name == SERVICE_R1_R2_NAME
    assert response.service_type == ServiceTypeEnum.SERVICETYPE_L3NM
    assert len(response.service_endpoint_ids) == 2
    assert len(response.service_constraints) == 2
    assert response.service_status.service_status == ServiceStatusEnum.SERVICESTATUS_PLANNED
    assert len(response.service_config.config_rules) == 3

    # ----- List when the object exists --------------------------------------------------------------------------------
    response = context_client.ListServiceIds(ContextId(**CONTEXT_ID))
    assert len(response.service_ids) == 1
    assert response.service_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.service_ids[0].service_uuid.uuid == service_uuid

    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    assert len(response.services) == 1
    assert response.services[0].service_id.context_id.context_uuid.uuid == context_uuid
    assert response.services[0].service_id.service_uuid.uuid == service_uuid
    assert response.services[0].name == SERVICE_R1_R2_NAME
    assert response.services[0].service_type == ServiceTypeEnum.SERVICETYPE_L3NM
    assert len(response.services[0].service_endpoint_ids) == 2
    assert len(response.services[0].service_constraints) == 2
    assert response.services[0].service_status.service_status == ServiceStatusEnum.SERVICESTATUS_PLANNED
    assert len(response.services[0].service_config.config_rules) == 3

    # ----- Update the object ------------------------------------------------------------------------------------------
    new_service_name = 'new'
    SERVICE_UPDATED = copy.deepcopy(SERVICE_R1_R2)
    SERVICE_UPDATED['name'] = new_service_name
    SERVICE_UPDATED['service_status']['service_status'] = ServiceStatusEnum.SERVICESTATUS_ACTIVE
    response = context_client.SetService(Service(**SERVICE_UPDATED))
    assert response.context_id.context_uuid.uuid == context_uuid
    assert response.service_uuid.uuid == service_uuid

    # ----- Check update event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ServiceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_UPDATE
    #assert event.service_id.context_id.context_uuid.uuid == context_uuid
    #assert event.service_id.service_uuid.uuid == service_uuid

    # ----- Get when the object is modified ----------------------------------------------------------------------------
    response = context_client.GetService(ServiceId(**SERVICE_R1_R2_ID))
    assert response.service_id.context_id.context_uuid.uuid == context_uuid
    assert response.service_id.service_uuid.uuid == service_uuid
    assert response.name == new_service_name
    assert response.service_type == ServiceTypeEnum.SERVICETYPE_L3NM
    assert len(response.service_endpoint_ids) == 2
    assert len(response.service_constraints) == 2
    assert response.service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE
    assert len(response.service_config.config_rules) == 3

    # ----- List when the object is modified ---------------------------------------------------------------------------
    response = context_client.ListServiceIds(ContextId(**CONTEXT_ID))
    assert len(response.service_ids) == 1
    assert response.service_ids[0].context_id.context_uuid.uuid == context_uuid
    assert response.service_ids[0].service_uuid.uuid == service_uuid

    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    assert len(response.services) == 1
    assert response.services[0].service_id.context_id.context_uuid.uuid == context_uuid
    assert response.services[0].service_id.service_uuid.uuid == service_uuid
    assert response.services[0].name == new_service_name
    assert response.services[0].service_type == ServiceTypeEnum.SERVICETYPE_L3NM
    assert len(response.services[0].service_endpoint_ids) == 2
    assert len(response.services[0].service_constraints) == 2
    assert response.services[0].service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE
    assert len(response.services[0].service_config.config_rules) == 3

    # ----- Remove the object ------------------------------------------------------------------------------------------
    context_client.RemoveService(ServiceId(**SERVICE_R1_R2_ID))

    # ----- Check remove event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, ServiceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert event.service_id.context_id.context_uuid.uuid == context_uuid
    #assert event.service_id.service_uuid.uuid == service_uuid

    # ----- List after deleting the object -----------------------------------------------------------------------------
    response = context_client.GetContext(ContextId(**CONTEXT_ID))
    assert len(response.topology_ids) == 1
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    response = context_client.ListServiceIds(ContextId(**CONTEXT_ID))
    assert len(response.service_ids) == 0

    response = context_client.ListServices(ContextId(**CONTEXT_ID))
    assert len(response.services) == 0

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
