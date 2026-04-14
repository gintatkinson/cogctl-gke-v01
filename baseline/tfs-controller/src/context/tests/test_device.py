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
    Context, ContextId, Device, DeviceDriverEnum, DeviceId, DeviceOperationalStatusEnum, Empty, Topology, TopologyId)
#from common.proto.context_pb2 import ContextEvent, DeviceEvent, EventTypeEnum, TopologyEvent
from context.client.ContextClient import ContextClient
#from context.client.EventsCollector import EventsCollector
from context.service.database.uuids.Device import device_get_uuid
#from .Constants import GET_EVENTS_TIMEOUT
from .Objects import CONTEXT, CONTEXT_ID, DEVICE_R1, DEVICE_R1_ID, DEVICE_R1_NAME, TOPOLOGY, TOPOLOGY_ID

@pytest.mark.depends(on=['context/tests/test_topology.py::test_topology'])
def test_device(context_client : ContextClient) -> None:

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    #events_collector = EventsCollector(
    #    context_client, log_events_received=True,
    #    activate_context_collector = True, activate_topology_collector = True, activate_device_collector = True,
    #    activate_link_collector = False, activate_service_collector = False, activate_slice_collector = False,
    #    activate_connection_collector = False)
    #events_collector.start()
    #time.sleep(3)

    # ----- Prepare dependencies for the test and capture related events -----------------------------------------------
    response = context_client.SetContext(Context(**CONTEXT))
    context_uuid = response.context_uuid.uuid

    response = context_client.SetTopology(Topology(**TOPOLOGY))
    assert response.context_id.context_uuid.uuid == context_uuid
    topology_uuid = response.topology_uuid.uuid

    #events = events_collector.get_events(block=True, count=2, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(events[0], ContextEvent)
    #assert events[0].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[0].context_id.context_uuid.uuid == context_uuid
    #assert isinstance(events[1], TopologyEvent)
    #assert events[1].event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert events[1].topology_id.context_id.context_uuid.uuid == context_uuid
    #assert events[1].topology_id.topology_uuid.uuid == topology_uuid

    # ----- Get when the object does not exist -------------------------------------------------------------------------
    device_id = DeviceId(**DEVICE_R1_ID)
    device_uuid = device_get_uuid(device_id, allow_random=False)
    with pytest.raises(grpc.RpcError) as e:
        context_client.GetDevice(device_id)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    MSG = 'Device({:s}) not found; device_uuid generated was: {:s}'
    assert e.value.details() == MSG.format(DEVICE_R1_NAME, device_uuid)

    # ----- List when the object does not exist ------------------------------------------------------------------------
    response = context_client.ListDeviceIds(Empty())
    assert len(response.device_ids) == 0

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == 0

    # ----- Create the object ------------------------------------------------------------------------------------------
    with pytest.raises(grpc.RpcError) as e:
        WRONG_DEVICE = copy.deepcopy(DEVICE_R1)
        WRONG_DEVICE_UUID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
        WRONG_DEVICE['device_endpoints'][0]['endpoint_id']['device_id']['device_uuid']['uuid'] = WRONG_DEVICE_UUID
        context_client.SetDevice(Device(**WRONG_DEVICE))
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    MSG = 'request.device_endpoints[0].device_id.device_uuid.uuid({}) is invalid; '\
          'should be == request.device_id.device_uuid.uuid({})'
    assert e.value.details() == MSG.format(WRONG_DEVICE_UUID, device_id.device_uuid.uuid) # pylint: disable=no-member

    response = context_client.SetDevice(Device(**DEVICE_R1))
    assert response.device_uuid.uuid == device_uuid

    # ----- Check create event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, DeviceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    #assert event.device_id.device_uuid.uuid == device_uuid

    # ----- Get when the object exists ---------------------------------------------------------------------------------
    response = context_client.GetDevice(DeviceId(**DEVICE_R1_ID))
    assert response.device_id.device_uuid.uuid == device_uuid
    assert response.name == DEVICE_R1_NAME
    assert response.device_type == 'packet-router'
    assert len(response.device_config.config_rules) == 3
    assert response.device_operational_status == DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED
    assert len(response.device_drivers) == 1
    assert DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG in response.device_drivers
    assert len(response.device_endpoints) == 4

    # ----- List when the object exists --------------------------------------------------------------------------------
    response = context_client.ListDeviceIds(Empty())
    assert len(response.device_ids) == 1
    assert response.device_ids[0].device_uuid.uuid == device_uuid

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == 1
    assert response.devices[0].device_id.device_uuid.uuid == device_uuid
    assert response.devices[0].name == DEVICE_R1_NAME
    assert response.devices[0].device_type == 'packet-router'
    assert len(response.devices[0].device_config.config_rules) == 3
    assert response.devices[0].device_operational_status == DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED
    assert len(response.devices[0].device_drivers) == 1
    assert DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG in response.devices[0].device_drivers
    assert len(response.devices[0].device_endpoints) == 4

    # ----- Update the object ------------------------------------------------------------------------------------------
    new_device_name = 'new'
    new_device_driver = DeviceDriverEnum.DEVICEDRIVER_UNDEFINED
    DEVICE_UPDATED = copy.deepcopy(DEVICE_R1)
    DEVICE_UPDATED['name'] = new_device_name
    DEVICE_UPDATED['device_operational_status'] = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED
    DEVICE_UPDATED['device_drivers'].append(new_device_driver)
    response = context_client.SetDevice(Device(**DEVICE_UPDATED))
    assert response.device_uuid.uuid == device_uuid

    # ----- Check update event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, DeviceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_UPDATE
    #assert event.device_id.device_uuid.uuid == device_uuid

    # ----- Get when the object is modified ----------------------------------------------------------------------------
    response = context_client.GetDevice(DeviceId(**DEVICE_R1_ID))
    assert response.device_id.device_uuid.uuid == device_uuid
    assert response.name == new_device_name
    assert response.device_type == 'packet-router'
    assert len(response.device_config.config_rules) == 3
    assert response.device_operational_status == DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED
    assert len(response.device_drivers) == 2
    assert DeviceDriverEnum.DEVICEDRIVER_UNDEFINED in response.device_drivers
    assert DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG in response.device_drivers
    assert len(response.device_endpoints) == 4

    # ----- List when the object is modified ---------------------------------------------------------------------------
    response = context_client.ListDeviceIds(Empty())
    assert len(response.device_ids) == 1
    assert response.device_ids[0].device_uuid.uuid == device_uuid

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == 1
    assert response.devices[0].device_id.device_uuid.uuid == device_uuid
    assert response.devices[0].name == new_device_name
    assert response.devices[0].device_type == 'packet-router'
    assert len(response.devices[0].device_config.config_rules) == 3
    assert response.devices[0].device_operational_status == DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED
    assert len(response.devices[0].device_drivers) == 2
    assert DeviceDriverEnum.DEVICEDRIVER_UNDEFINED in response.devices[0].device_drivers
    assert DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG in response.devices[0].device_drivers
    assert len(response.devices[0].device_endpoints) == 4

    # ----- Check relation was created ---------------------------------------------------------------------------------
    response = context_client.GetTopology(TopologyId(**TOPOLOGY_ID))
    assert response.topology_id.context_id.context_uuid.uuid == context_uuid
    assert response.topology_id.topology_uuid.uuid == topology_uuid
    assert len(response.device_ids) == 1
    assert response.device_ids[0].device_uuid.uuid == device_uuid
    assert len(response.link_ids) == 0

    # ----- Remove the object ------------------------------------------------------------------------------------------
    context_client.RemoveDevice(DeviceId(**DEVICE_R1_ID))

    # ----- Check remove event -----------------------------------------------------------------------------------------
    #event = events_collector.get_event(block=True, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(event, DeviceEvent)
    #assert event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert event.device_id.device_uuid.uuid == device_uuid

    # ----- List after deleting the object -----------------------------------------------------------------------------
    response = context_client.ListDeviceIds(Empty())
    assert len(response.device_ids) == 0

    response = context_client.ListDevices(Empty())
    assert len(response.devices) == 0

    response = context_client.GetTopology(TopologyId(**TOPOLOGY_ID))
    assert response.topology_id.context_id.context_uuid.uuid == context_uuid
    assert response.topology_id.topology_uuid.uuid == topology_uuid
    assert len(response.device_ids) == 0
    assert len(response.link_ids) == 0

    # ----- Clean dependencies used in the test and capture related events ---------------------------------------------
    context_client.RemoveTopology(TopologyId(**TOPOLOGY_ID))
    context_client.RemoveContext(ContextId(**CONTEXT_ID))

    #events = events_collector.get_events(block=True, count=2, timeout=GET_EVENTS_TIMEOUT)
    #assert isinstance(events[0], TopologyEvent)
    #assert events[0].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[0].topology_id.context_id.context_uuid.uuid == context_uuid
    #assert events[0].topology_id.topology_uuid.uuid == topology_uuid
    #assert isinstance(events[1], ContextEvent)
    #assert events[1].event.event_type == EventTypeEnum.EVENTTYPE_REMOVE
    #assert events[1].context_id.context_uuid.uuid == context_uuid

    # ----- Stop the EventsCollector -----------------------------------------------------------------------------------
    #events_collector.stop()
