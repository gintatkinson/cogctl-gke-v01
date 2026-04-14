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

import grpc, json, logging
from typing import Any, Dict, Iterator, Set, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import (
    Connection, ConnectionEvent, ConnectionId, ConnectionIdList, ConnectionList,
    Context, ContextEvent, ContextId, ContextIdList, ContextList,
    Device, DeviceEvent, DeviceFilter, DeviceId, DeviceIdList, DeviceList,
    Empty, EventTypeEnum,
    Link, LinkEvent, LinkId, LinkIdList, LinkList,
    OpticalLink, OpticalLinkList,
    Service, ServiceEvent, ServiceFilter, ServiceId, ServiceIdList, ServiceList,
    Slice, SliceEvent, SliceFilter, SliceId, SliceIdList, SliceList,
    Topology, TopologyDetails, TopologyEvent, TopologyId, TopologyIdList, TopologyList
)
from common.proto.context_pb2_grpc import ContextServiceServicer
from common.proto.policy_pb2 import PolicyRule, PolicyRuleId, PolicyRuleIdList, PolicyRuleList
from common.tools.grpc.Tools import grpc_message_to_json, grpc_message_to_json_string
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.Link import json_link_id
from .InMemoryObjectDatabase import InMemoryObjectDatabase
from .MockMessageBroker import (
    TOPIC_CONNECTION, TOPIC_CONTEXT, TOPIC_DEVICE, TOPIC_LINK,
    TOPIC_SERVICE, TOPIC_SLICE, TOPIC_TOPOLOGY, TOPIC_POLICY,
    MockMessageBroker, notify_event
)

LOGGER = logging.getLogger(__name__)

class MockServicerImpl_Context(ContextServiceServicer):
    def __init__(self):
        LOGGER.debug('[__init__] Creating Servicer...')
        self.obj_db = InMemoryObjectDatabase()
        self.msg_broker = MockMessageBroker()
        LOGGER.debug('[__init__] Servicer Created')

    # ----- Common -----------------------------------------------------------------------------------------------------

    def _set(self, request, container_name, entry_uuid, entry_id_field_name, topic_name) -> Tuple[Any, Any]:
        exists = self.obj_db.has_entry(container_name, entry_uuid)
        entry = self.obj_db.set_entry(container_name, entry_uuid, request)
        event_type = EventTypeEnum.EVENTTYPE_UPDATE if exists else EventTypeEnum.EVENTTYPE_CREATE
        entry_id = getattr(entry, entry_id_field_name)
        dict_entry_id = grpc_message_to_json(entry_id)
        notify_event(self.msg_broker, topic_name, event_type, {entry_id_field_name: dict_entry_id})
        return entry_id, entry

    def _del(self, request, container_name, entry_uuid, entry_id_field_name, topic_name, context) -> Empty:
        self.obj_db.del_entry(container_name, entry_uuid, context)
        event_type = EventTypeEnum.EVENTTYPE_REMOVE
        dict_entry_id = grpc_message_to_json(request)
        notify_event(self.msg_broker, topic_name, event_type, {entry_id_field_name: dict_entry_id})
        return Empty()

    # ----- Context ----------------------------------------------------------------------------------------------------

    def ListContextIds(self, request : Empty, context : grpc.ServicerContext) -> ContextIdList:
        LOGGER.debug('[ListContextIds] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = ContextIdList(context_ids=[context.context_id for context in self.obj_db.get_entries('context')])
        LOGGER.debug('[ListContextIds] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def ListContexts(self, request : Empty, context : grpc.ServicerContext) -> ContextList:
        LOGGER.debug('[ListContexts] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = ContextList(contexts=self.obj_db.get_entries('context'))
        LOGGER.debug('[ListContexts] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetContext(self, request : ContextId, context : grpc.ServicerContext) -> Context:
        LOGGER.debug('[GetContext] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.get_entry('context', request.context_uuid.uuid, context)
        LOGGER.debug('[GetContext] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetContext(self, request : Context, context : grpc.ServicerContext) -> ContextId:
        LOGGER.debug('[SetContext] request={:s}'.format(grpc_message_to_json_string(request)))
        reply,_ = self._set(request, 'context', request.context_id.context_uuid.uuid, 'context_id', TOPIC_CONTEXT)
        LOGGER.debug('[SetContext] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def RemoveContext(self, request : ContextId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[RemoveContext] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self._del(request, 'context', request.context_uuid.uuid, 'context_id', TOPIC_CONTEXT, context)
        LOGGER.debug('[RemoveContext] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetContextEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[ContextEvent]:
        LOGGER.debug('[GetContextEvents] request={:s}'.format(grpc_message_to_json_string(request)))
        for message in self.msg_broker.consume({TOPIC_CONTEXT}): yield ContextEvent(**json.loads(message.content))


    # ----- Topology ---------------------------------------------------------------------------------------------------

    def ListTopologyIds(self, request : ContextId, context : grpc.ServicerContext) -> TopologyIdList:
        LOGGER.debug('[ListTopologyIds] request={:s}'.format(grpc_message_to_json_string(request)))
        topologies = self.obj_db.get_entries('topology[{:s}]'.format(str(request.context_uuid.uuid)))
        reply = TopologyIdList(topology_ids=[topology.topology_id for topology in topologies])
        LOGGER.debug('[ListTopologyIds] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def ListTopologies(self, request : ContextId, context : grpc.ServicerContext) -> TopologyList:
        LOGGER.debug('[ListTopologies] request={:s}'.format(grpc_message_to_json_string(request)))
        topologies = self.obj_db.get_entries('topology[{:s}]'.format(str(request.context_uuid.uuid)))
        reply = TopologyList(topologies=[topology for topology in topologies])
        LOGGER.debug('[ListTopologies] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetTopology(self, request : TopologyId, context : grpc.ServicerContext) -> Topology:
        LOGGER.debug('[GetTopology] request={:s}'.format(grpc_message_to_json_string(request)))
        container_name = 'topology[{:s}]'.format(str(request.context_id.context_uuid.uuid))
        reply = self.obj_db.get_entry(container_name, request.topology_uuid.uuid, context)
        LOGGER.debug('[GetTopology] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetTopologyDetails(self, request : TopologyId, context : grpc.ServicerContext) -> TopologyDetails:
        LOGGER.debug('[GetTopologyDetails] request={:s}'.format(grpc_message_to_json_string(request)))
        context_uuid = request.context_id.context_uuid.uuid
        container_name = 'topology[{:s}]'.format(str(context_uuid))
        topology_uuid = request.topology_uuid.uuid
        _reply = self.obj_db.get_entry(container_name, topology_uuid, context)
        reply = TopologyDetails()
        reply.topology_id.CopyFrom(_reply.topology_id) # pylint: disable=no-member
        reply.name = _reply.name
        if context_uuid == DEFAULT_CONTEXT_NAME and topology_uuid == DEFAULT_TOPOLOGY_NAME:
            for device in self.obj_db.get_entries('device'): reply.devices.append(device)   # pylint: disable=no-member
            for link   in self.obj_db.get_entries('link'  ): reply.links  .append(link  )   # pylint: disable=no-member
        else:
            # TODO: to be improved; Mock does not associate devices/links to topologies automatically
            for device_id in _reply.device_ids:
                device = self.obj_db.get_entry('device', device_id.device_uuid.uuid, context)
                reply.devices.append(device) # pylint: disable=no-member
            for link_id in _reply.link_ids:
                link = self.obj_db.get_entry('link', link_id.link_uuid.uuid, context)
                reply.links.append(link) # pylint: disable=no-member
        LOGGER.debug('[GetTopologyDetails] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetTopology(self, request : Topology, context : grpc.ServicerContext) -> TopologyId:
        LOGGER.debug('[SetTopology] request={:s}'.format(grpc_message_to_json_string(request)))
        context_uuid = str(request.topology_id.context_id.context_uuid.uuid)
        container_name = 'topology[{:s}]'.format(context_uuid)
        topology_uuid = request.topology_id.topology_uuid.uuid

        if self.obj_db.has_entry(container_name, topology_uuid):
            # merge device_ids and link_ids from database and request, and update request
            db_topology = self.obj_db.get_entry(container_name, topology_uuid, context)

            device_uuids = set()
            for device_id in request.device_ids: device_uuids.add(device_id.device_uuid.uuid)
            for device_id in db_topology.device_ids: device_uuids.add(device_id.device_uuid.uuid)

            link_uuids = set()
            for link_id in request.link_ids: link_uuids.add(link_id.link_uuid.uuid)
            for link_id in db_topology.link_ids: link_uuids.add(link_id.link_uuid.uuid)

            rw_request = Topology()
            rw_request.CopyFrom(request)

            # pylint: disable=no-member
            del rw_request.device_ids[:]
            for device_uuid in sorted(device_uuids):
                rw_request.device_ids.append(DeviceId(**json_device_id(device_uuid)))

            # pylint: disable=no-member
            del rw_request.link_ids[:]
            for link_uuid in sorted(link_uuids):
                rw_request.link_ids.append(LinkId(**json_link_id(link_uuid)))

            request = rw_request

        reply,_ = self._set(request, container_name, topology_uuid, 'topology_id', TOPIC_TOPOLOGY)

        context_ = self.obj_db.get_entry('context', context_uuid, context)
        for _topology_id in context_.topology_ids:
            if _topology_id.topology_uuid.uuid == topology_uuid: break
        else:
            # topology not found, add it
            topology_id = context_.topology_ids.add()
            topology_id.context_id.context_uuid.uuid = context_uuid
            topology_id.topology_uuid.uuid = topology_uuid

        LOGGER.debug('[SetTopology] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def RemoveTopology(self, request : TopologyId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[RemoveTopology] request={:s}'.format(grpc_message_to_json_string(request)))
        context_uuid = str(request.context_id.context_uuid.uuid)
        container_name = 'topology[{:s}]'.format(context_uuid)
        topology_uuid = request.topology_uuid.uuid
        reply = self._del(request, container_name, topology_uuid, 'topology_id', TOPIC_TOPOLOGY, context)

        context_ = self.obj_db.get_entry('context', context_uuid, context)
        for _topology_id in context_.topology_ids:
            if _topology_id.context_id.context_uuid.uuid != context_uuid: continue
            if _topology_id.topology_uuid.uuid != topology_uuid: continue
            context_.topology_ids.remove(_topology_id)
            break

        LOGGER.debug('[RemoveTopology] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetTopologyEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[TopologyEvent]:
        LOGGER.debug('[GetTopologyEvents] request={:s}'.format(grpc_message_to_json_string(request)))
        for message in self.msg_broker.consume({TOPIC_TOPOLOGY}): yield TopologyEvent(**json.loads(message.content))


    # ----- Device -----------------------------------------------------------------------------------------------------

    def ListDeviceIds(self, request : Empty, context : grpc.ServicerContext) -> DeviceIdList:
        LOGGER.debug('[ListDeviceIds] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = DeviceIdList(device_ids=[device.device_id for device in self.obj_db.get_entries('device')])
        LOGGER.debug('[ListDeviceIds] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def ListDevices(self, request : Empty, context : grpc.ServicerContext) -> DeviceList:
        LOGGER.debug('[ListDevices] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = DeviceList(devices=self.obj_db.get_entries('device'))
        LOGGER.debug('[ListDevices] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetDevice(self, request : DeviceId, context : grpc.ServicerContext) -> Device:
        LOGGER.debug('[GetDevice] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.get_entry('device', request.device_uuid.uuid, context)
        LOGGER.debug('[GetDevice] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetDevice(self, request : Context, context : grpc.ServicerContext) -> DeviceId:
        LOGGER.debug('[SetDevice] request={:s}'.format(grpc_message_to_json_string(request)))
        device_uuid = request.device_id.device_uuid.uuid
        reply, device = self._set(request, 'device', device_uuid, 'device_id', TOPIC_DEVICE)

        context_topology_uuids : Set[Tuple[str, str]] = set()
        context_topology_uuids.add((DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME))
        for endpoint in device.device_endpoints:
            endpoint_context_uuid = endpoint.endpoint_id.topology_id.context_id.context_uuid.uuid
            if len(endpoint_context_uuid) == 0: endpoint_context_uuid = DEFAULT_CONTEXT_NAME
            endpoint_topology_uuid = endpoint.endpoint_id.topology_id.topology_uuid.uuid
            if len(endpoint_topology_uuid) == 0: endpoint_topology_uuid = DEFAULT_TOPOLOGY_NAME
            context_topology_uuids.add((endpoint_context_uuid, endpoint_topology_uuid))

        for context_uuid,topology_uuid in context_topology_uuids:
            container_name = 'topology[{:s}]'.format(str(context_uuid))
            topology = self.obj_db.get_entry(container_name, topology_uuid, context)
            for _device_id in topology.device_ids:
                if _device_id.device_uuid.uuid == device_uuid: break
            else:
                # device not found, add it
                topology.device_ids.add().device_uuid.uuid = device_uuid

        LOGGER.debug('[SetDevice] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def RemoveDevice(self, request : DeviceId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[RemoveDevice] request={:s}'.format(grpc_message_to_json_string(request)))
        device_uuid = request.device_uuid.uuid
        device = self.obj_db.get_entry('device', device_uuid, context)
        reply = self._del(request, 'device', device_uuid, 'device_id', TOPIC_DEVICE, context)

        context_topology_uuids : Set[Tuple[str, str]] = set()
        context_topology_uuids.add((DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME))
        for endpoint in device.device_endpoints:
            endpoint_context_uuid = endpoint.endpoint_id.topology_id.context_id.context_uuid.uuid
            if len(endpoint_context_uuid) == 0: endpoint_context_uuid = DEFAULT_CONTEXT_NAME
            endpoint_topology_uuid = endpoint.endpoint_id.topology_id.topology_uuid.uuid
            if len(endpoint_topology_uuid) == 0: endpoint_topology_uuid = DEFAULT_TOPOLOGY_NAME
            context_topology_uuids.add((endpoint_context_uuid, endpoint_topology_uuid))

        for context_uuid,topology_uuid in context_topology_uuids:
            container_name = 'topology[{:s}]'.format(str(context_uuid))
            topology = self.obj_db.get_entry(container_name, topology_uuid, context)
            for device_id in topology.device_ids:
                if device_id.device_uuid.uuid == device_uuid:
                    topology.device_ids.remove(device_id)
                    break

        LOGGER.debug('[RemoveDevice] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetDeviceEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[DeviceEvent]:
        LOGGER.debug('[GetDeviceEvents] request={:s}'.format(grpc_message_to_json_string(request)))
        for message in self.msg_broker.consume({TOPIC_DEVICE}): yield DeviceEvent(**json.loads(message.content))

    def SelectDevice(self, request : DeviceFilter, context : grpc.ServicerContext) -> DeviceList:
        LOGGER.debug('[SelectDevice] request={:s}'.format(grpc_message_to_json_string(request)))
        container_entry_uuids : Dict[str, Set[str]] = {}
        container_name = 'device'
        for device_id in request.device_ids.device_ids:
            device_uuid = device_id.device_uuid.uuid
            container_entry_uuids.setdefault(container_name, set()).add(device_uuid)

        exclude_endpoints = not request.include_endpoints
        exclude_config_rules = not request.include_config_rules
        exclude_components  = not request.include_components

        devices = list()
        for container_name in sorted(container_entry_uuids.keys()):
             entry_uuids = container_entry_uuids[container_name]
        for device in self.obj_db.select_entries(container_name, entry_uuids):
            reply_device = Device()
            reply_device.CopyFrom(device)
            if exclude_endpoints:    del reply_device.device_endpoints [:] # pylint: disable=no-member
            if exclude_config_rules: del reply_device.device_config.config_rules[:] # pylint: disable=no-member
            if exclude_components:   del reply_device.components[:] # pylint: disable=no-member
            devices.append(reply_device)

        reply = DeviceList(devices=devices)
        LOGGER.debug('[SelectDevice] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply


    # ----- Link -------------------------------------------------------------------------------------------------------

    def ListLinkIds(self, request : Empty, context : grpc.ServicerContext) -> LinkIdList:
        LOGGER.debug('[ListLinkIds] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = LinkIdList(link_ids=[link.link_id for link in self.obj_db.get_entries('link')])
        LOGGER.debug('[ListLinkIds] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def ListLinks(self, request : Empty, context : grpc.ServicerContext) -> LinkList:
        LOGGER.debug('[ListLinks] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = LinkList(links=self.obj_db.get_entries('link'))
        LOGGER.debug('[ListLinks] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetLink(self, request : LinkId, context : grpc.ServicerContext) -> Link:
        LOGGER.debug('[GetLink] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.get_entry('link', request.link_uuid.uuid, context)
        LOGGER.debug('[GetLink] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetLink(self, request : Context, context : grpc.ServicerContext) -> LinkId:
        LOGGER.debug('[SetLink] request={:s}'.format(grpc_message_to_json_string(request)))
        link_uuid = request.link_id.link_uuid.uuid
        reply, link = self._set(request, 'link', link_uuid, 'link_id', TOPIC_LINK)

        context_topology_uuids : Set[Tuple[str, str]] = set()
        context_topology_uuids.add((DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME))
        for endpoint_id in link.link_endpoint_ids:
            endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
            if len(endpoint_context_uuid) == 0: endpoint_context_uuid = DEFAULT_CONTEXT_NAME
            endpoint_topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
            if len(endpoint_topology_uuid) == 0: endpoint_topology_uuid = DEFAULT_TOPOLOGY_NAME
            context_topology_uuids.add((endpoint_context_uuid, endpoint_topology_uuid))

        for context_uuid,topology_uuid in context_topology_uuids:
            container_name = 'topology[{:s}]'.format(str(context_uuid))
            topology = self.obj_db.get_entry(container_name, topology_uuid, context)
            for _link_id in topology.link_ids:
                if _link_id.link_uuid.uuid == link_uuid: break
            else:
                # link not found, add it
                topology.link_ids.add().link_uuid.uuid = link_uuid

        LOGGER.debug('[SetLink] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def RemoveLink(self, request : LinkId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[RemoveLink] request={:s}'.format(grpc_message_to_json_string(request)))
        link_uuid = request.link_uuid.uuid
        link = self.obj_db.get_entry('link', link_uuid, context)
        reply = self._del(request, 'link', link_uuid, 'link_id', TOPIC_LINK, context)

        context_topology_uuids : Set[Tuple[str, str]] = set()
        context_topology_uuids.add((DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME))
        for endpoint_id in link.link_endpoint_ids:
            endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
            if len(endpoint_context_uuid) == 0: endpoint_context_uuid = DEFAULT_CONTEXT_NAME
            endpoint_topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
            if len(endpoint_topology_uuid) == 0: endpoint_topology_uuid = DEFAULT_TOPOLOGY_NAME
            context_topology_uuids.add((endpoint_context_uuid, endpoint_topology_uuid))

        for context_uuid,topology_uuid in context_topology_uuids:
            container_name = 'topology[{:s}]'.format(str(context_uuid))
            topology = self.obj_db.get_entry(container_name, topology_uuid, context)
            for link_id in topology.link_ids:
                if link_id.link_uuid.uuid == link_uuid:
                    topology.link_ids.remove(link_id)
                    break

        LOGGER.debug('[RemoveLink] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetLinkEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[LinkEvent]:
        LOGGER.debug('[GetLinkEvents] request={:s}'.format(grpc_message_to_json_string(request)))
        for message in self.msg_broker.consume({TOPIC_LINK}): yield LinkEvent(**json.loads(message.content))


    # ----- Slice ------------------------------------------------------------------------------------------------------

    def ListSliceIds(self, request : ContextId, context : grpc.ServicerContext) -> SliceIdList:
        LOGGER.debug('[ListSliceIds] request={:s}'.format(grpc_message_to_json_string(request)))
        slices = self.obj_db.get_entries('slice[{:s}]'.format(str(request.context_uuid.uuid)))
        reply = SliceIdList(slice_ids=[slice.slice_id for slice in slices])
        LOGGER.debug('[ListSliceIds] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def ListSlices(self, request : ContextId, context : grpc.ServicerContext) -> SliceList:
        LOGGER.debug('[ListSlices] request={:s}'.format(grpc_message_to_json_string(request)))
        slices = self.obj_db.get_entries('slice[{:s}]'.format(str(request.context_uuid.uuid)))
        reply = SliceList(slices=[slice for slice in slices])
        LOGGER.debug('[ListSlices] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetSlice(self, request : SliceId, context : grpc.ServicerContext) -> Slice:
        LOGGER.debug('[GetSlice] request={:s}'.format(grpc_message_to_json_string(request)))
        container_name = 'slice[{:s}]'.format(str(request.context_id.context_uuid.uuid))
        reply = self.obj_db.get_entry(container_name, request.slice_uuid.uuid, context)
        LOGGER.debug('[GetSlice] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        LOGGER.debug('[SetSlice] request={:s}'.format(grpc_message_to_json_string(request)))
        context_uuid = str(request.slice_id.context_id.context_uuid.uuid)
        container_name = 'slice[{:s}]'.format(context_uuid)
        slice_uuid = request.slice_id.slice_uuid.uuid
        reply,_ = self._set(request, container_name, slice_uuid, 'slice_id', TOPIC_SLICE)

        context_ = self.obj_db.get_entry('context', context_uuid, context)
        for _slice_id in context_.slice_ids:
            if _slice_id.slice_uuid.uuid == slice_uuid: break
        else:
            # slice not found, add it
            slice_id = context_.slice_ids.add()
            slice_id.context_id.context_uuid.uuid = context_uuid
            slice_id.slice_uuid.uuid = slice_uuid

        LOGGER.debug('[SetSlice] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def RemoveSlice(self, request : SliceId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[RemoveSlice] request={:s}'.format(grpc_message_to_json_string(request)))
        context_uuid = str(request.context_id.context_uuid.uuid)
        container_name = 'slice[{:s}]'.format(context_uuid)
        slice_uuid = request.slice_uuid.uuid
        reply = self._del(request, container_name, slice_uuid, 'slice_id', TOPIC_SLICE, context)

        context_ = self.obj_db.get_entry('context', context_uuid, context)
        for _slice_id in context_.slice_ids:
            if _slice_id.context_id.context_uuid.uuid != context_uuid: continue
            if _slice_id.slice_uuid.uuid != slice_uuid: continue
            context_.slice_ids.remove(_slice_id)
            break

        LOGGER.debug('[RemoveSlice] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetSliceEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[SliceEvent]:
        LOGGER.debug('[GetSliceEvents] request={:s}'.format(grpc_message_to_json_string(request)))
        for message in self.msg_broker.consume({TOPIC_SLICE}): yield SliceEvent(**json.loads(message.content))

    def SelectSlice(self, request : SliceFilter, context : grpc.ServicerContext) -> SliceList:
        LOGGER.debug('[SelectSlice] request={:s}'.format(grpc_message_to_json_string(request)))
        container_entry_uuids : Dict[str, Set[str]] = {}
        for slice_id in request.slice_ids.slice_ids:
            container_name = 'slice[{:s}]'.format(str(slice_id.context_id.context_uuid.uuid))
            slice_uuid = slice_id.slice_uuid.uuid
            container_entry_uuids.setdefault(container_name, set()).add(slice_uuid)

        exclude_endpoint_ids = not request.include_endpoint_ids
        exclude_constraints  = not request.include_constraints
        exclude_service_ids  = not request.include_service_ids
        exclude_subslice_ids = not request.include_subslice_ids
        exclude_config_rules = not request.include_config_rules

        slices = list()
        for container_name in sorted(container_entry_uuids.keys()):
            entry_uuids = container_entry_uuids[container_name]
            for eslice in self.obj_db.select_entries(container_name, entry_uuids):
                reply_slice = Slice()
                reply_slice.CopyFrom(eslice)
                if exclude_endpoint_ids: del reply_slice.service_endpoint_ids[:] # pylint: disable=no-member
                if exclude_constraints : del reply_slice.service_constraints[:] # pylint: disable=no-member
                if exclude_service_ids : del reply_slice.slice_service_ids[:] # pylint: disable=no-member
                if exclude_subslice_ids : del reply_slice.slice_subslice_ids[:] # pylint: disable=no-member
                if exclude_config_rules: del reply_slice.slice_config .config_rules[:] # pylint: disable=no-member
                slices.append(reply_slice)

        reply = SliceList(slices=slices)
        LOGGER.debug('[SelectSlice] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply


    # ----- Service ----------------------------------------------------------------------------------------------------

    def ListServiceIds(self, request : ContextId, context : grpc.ServicerContext) -> ServiceIdList:
        LOGGER.debug('[ListServiceIds] request={:s}'.format(grpc_message_to_json_string(request)))
        services = self.obj_db.get_entries('service[{:s}]'.format(str(request.context_uuid.uuid)))
        reply = ServiceIdList(service_ids=[service.service_id for service in services])
        LOGGER.debug('[ListServiceIds] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def ListServices(self, request : ContextId, context : grpc.ServicerContext) -> ServiceList:
        LOGGER.debug('[ListServices] request={:s}'.format(grpc_message_to_json_string(request)))
        services = self.obj_db.get_entries('service[{:s}]'.format(str(request.context_uuid.uuid)))
        reply = ServiceList(services=[service for service in services])
        LOGGER.debug('[ListServices] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetService(self, request : ServiceId, context : grpc.ServicerContext) -> Service:
        LOGGER.debug('[GetService] request={:s}'.format(grpc_message_to_json_string(request)))
        container_name = 'service[{:s}]'.format(str(request.context_id.context_uuid.uuid))
        reply = self.obj_db.get_entry(container_name, request.service_uuid.uuid, context)
        LOGGER.debug('[GetService] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetService(self, request : Service, context : grpc.ServicerContext) -> ServiceId:
        LOGGER.debug('[SetService] request={:s}'.format(grpc_message_to_json_string(request)))
        context_uuid = str(request.service_id.context_id.context_uuid.uuid)
        container_name = 'service[{:s}]'.format(context_uuid)
        service_uuid = request.service_id.service_uuid.uuid
        reply,_ = self._set(request, container_name, service_uuid, 'service_id', TOPIC_SERVICE)

        context_ = self.obj_db.get_entry('context', context_uuid, context)
        for _service_id in context_.service_ids:
            if _service_id.service_uuid.uuid == service_uuid: break
        else:
            # service not found, add it
            service_id = context_.service_ids.add()
            service_id.context_id.context_uuid.uuid = context_uuid
            service_id.service_uuid.uuid = service_uuid

        LOGGER.debug('[SetService] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def RemoveService(self, request : ServiceId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[RemoveService] request={:s}'.format(grpc_message_to_json_string(request)))
        context_uuid = str(request.context_id.context_uuid.uuid)
        container_name = 'service[{:s}]'.format(context_uuid)
        service_uuid = request.service_uuid.uuid
        reply = self._del(request, container_name, service_uuid, 'service_id', TOPIC_SERVICE, context)

        context_ = self.obj_db.get_entry('context', context_uuid, context)
        for _service_id in context_.service_ids:
            if _service_id.context_id.context_uuid.uuid != context_uuid: continue
            if _service_id.service_uuid.uuid != service_uuid: continue
            context_.service_ids.remove(_service_id)
            break

        LOGGER.debug('[RemoveService] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetServiceEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[ServiceEvent]:
        LOGGER.debug('[GetServiceEvents] request={:s}'.format(grpc_message_to_json_string(request)))
        for message in self.msg_broker.consume({TOPIC_SERVICE}): yield ServiceEvent(**json.loads(message.content))

    def SelectService(self, request : ServiceFilter, context : grpc.ServicerContext) -> ServiceList:
        LOGGER.debug('[SelectService] request={:s}'.format(grpc_message_to_json_string(request)))
        container_entry_uuids : Dict[str, Set[str]] = {}
        for service_id in request.service_ids.service_ids:
            container_name = 'service[{:s}]'.format(str(service_id.context_id.context_uuid.uuid))
            service_uuid = service_id.service_uuid.uuid
            container_entry_uuids.setdefault(container_name, set()).add(service_uuid)

        exclude_endpoint_ids = not request.include_endpoint_ids
        exclude_constraints  = not request.include_constraints
        exclude_config_rules = not request.include_config_rules

        services = list()
        for container_name in sorted(container_entry_uuids.keys()):
            entry_uuids = container_entry_uuids[container_name]
            for service in self.obj_db.select_entries(container_name, entry_uuids):
                LOGGER.debug('service={:s}'.format(grpc_message_to_json_string(service)))
                reply_service = Service()
                reply_service.CopyFrom(service)
                if exclude_endpoint_ids: del reply_service.service_endpoint_ids[:] # pylint: disable=no-member
                if exclude_constraints : del reply_service.service_constraints[:] # pylint: disable=no-member
                if exclude_config_rules: del reply_service.service_config.config_rules[:] # pylint: disable=no-member
                services.append(reply_service)

        reply = ServiceList(services=services)
        LOGGER.debug('[SelectService] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply


    # ----- Connection -------------------------------------------------------------------------------------------------

    def ListConnectionIds(self, request : ServiceId, context : grpc.ServicerContext) -> ConnectionIdList:
        LOGGER.debug('[ListConnectionIds] request={:s}'.format(grpc_message_to_json_string(request)))
        container_name = 'service_connections[{:s}/{:s}]'.format(
            str(request.context_id.context_uuid.uuid), str(request.service_uuid.uuid))
        reply = ConnectionIdList(connection_ids=[c.connection_id for c in self.obj_db.get_entries(container_name)])
        LOGGER.debug('[ListConnectionIds] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def ListConnections(self, request : ServiceId, context : grpc.ServicerContext) -> ConnectionList:
        LOGGER.debug('[ListConnections] request={:s}'.format(grpc_message_to_json_string(request)))
        container_name = 'service_connections[{:s}/{:s}]'.format(
            str(request.context_id.context_uuid.uuid), str(request.service_uuid.uuid))
        reply = ConnectionList(connections=self.obj_db.get_entries(container_name))
        LOGGER.debug('[ListConnections] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetConnection(self, request : ConnectionId, context : grpc.ServicerContext) -> Connection:
        LOGGER.debug('[GetConnection] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.get_entry('connection', request.connection_uuid.uuid, context)
        LOGGER.debug('[GetConnection] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetConnection(self, request : Connection, context : grpc.ServicerContext) -> ConnectionId:
        LOGGER.debug('[SetConnection] request={:s}'.format(grpc_message_to_json_string(request)))
        container_name = 'service_connection[{:s}/{:s}]'.format(
            str(request.service_id.context_id.context_uuid.uuid), str(request.service_id.service_uuid.uuid))
        connection_uuid = request.connection_id.connection_uuid.uuid
        self.obj_db.set_entry(container_name, connection_uuid, request)
        reply,_ = self._set(request, 'connection', connection_uuid, 'connection_id', TOPIC_CONNECTION)
        LOGGER.debug('[SetConnection] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def RemoveConnection(self, request : ConnectionId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[RemoveConnection] request={:s}'.format(grpc_message_to_json_string(request)))
        connection = self.obj_db.get_entry('connection', request.connection_uuid.uuid, context)
        container_name = 'service_connection[{:s}/{:s}]'.format(
            str(connection.service_id.context_id.context_uuid.uuid), str(connection.service_id.service_uuid.uuid))
        connection_uuid = request.connection_uuid.uuid
        self.obj_db.del_entry(container_name, connection_uuid, context)
        reply = self._del(request, 'connection', connection_uuid, 'connection_id', TOPIC_CONNECTION, context)
        LOGGER.debug('[RemoveConnection] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetConnectionEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[ConnectionEvent]:
        LOGGER.debug('[GetConnectionEvents] request={:s}'.format(grpc_message_to_json_string(request)))
        for message in self.msg_broker.consume({TOPIC_CONNECTION}): yield ConnectionEvent(**json.loads(message.content))


    # ----- Policy Rule ------------------------------------------------------------------------------------------------

    def ListPolicyRuleIds(self, request : Empty, context : grpc.ServicerContext):   # pylint: disable=unused-argument
        LOGGER.debug('[ListPolicyRuleIds] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = PolicyRuleIdList(policyRuleIdList=[
            getattr(policy_rule, policy_rule.WhichOneof('policy_rule')).policyRuleBasic.policyRuleId
            for policy_rule in self.obj_db.get_entries('policy')
        ])
        LOGGER.debug('[ListPolicyRuleIds] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def ListPolicyRules(self, request : Empty, context : grpc.ServicerContext):     # pylint: disable=unused-argument
        LOGGER.debug('[ListPolicyRules] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = PolicyRuleList(policyRules=self.obj_db.get_entries('policy'))
        LOGGER.debug('[ListPolicyRules] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetPolicyRule(self, request : PolicyRuleId, context : grpc.ServicerContext):
        LOGGER.debug('[GetPolicyRule] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.get_entry('policy_rule', request.uuid.uuid, context)
        LOGGER.debug('[GetPolicyRule] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetPolicyRule(self, request : PolicyRule, context : grpc.ServicerContext):  # pylint: disable=unused-argument
        LOGGER.debug('[SetPolicyRule] request={:s}'.format(grpc_message_to_json_string(request)))
        policy_type = request.WhichOneof('policy_rule')
        policy_uuid = getattr(request, policy_type).policyRuleBasic.policyRuleId.uuid.uuid
        rule_id_field = '{:s}.policyRuleBasic.policyRuleId'.format(policy_type)
        reply, _ = self._set(request, 'policy', policy_uuid, rule_id_field, TOPIC_POLICY)
        LOGGER.debug('[SetPolicyRule] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def RemovePolicyRule(self, request : PolicyRuleId, context : grpc.ServicerContext):
        LOGGER.debug('[RemovePolicyRule] request={:s}'.format(grpc_message_to_json_string(request)))
        policy_type = request.WhichOneof('policy_rule')
        policy_uuid = getattr(request, policy_type).policyRuleBasic.policyRuleId.uuid.uuid
        rule_id_field = '{:s}.policyRuleBasic.policyRuleId'.format(policy_type)
        reply = self._del(request, 'policy', policy_uuid, rule_id_field, TOPIC_CONTEXT, context)
        LOGGER.debug('[RemovePolicyRule] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply


    # ----- Optical Link -----------------------------------------------------------------------------------------------

    def GetOpticalLinkList(self, request : Empty, context : grpc.ServicerContext) -> OpticalLinkList:
        LOGGER.debug('[GetOpticalLinkList] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = OpticalLinkList(optical_links=self.obj_db.get_entries('optical_link'))
        LOGGER.debug('[GetOpticalLinkList] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetOpticalLink(self, request : LinkId, context : grpc.ServicerContext) -> OpticalLink:
        LOGGER.debug('[GetOpticalLink] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.get_entry('optical_link', request.link_uuid.uuid, context)
        LOGGER.debug('[GetOpticalLink] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetOpticalLink(self, request : OpticalLink, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[SetOpticalLink] request={:s}'.format(grpc_message_to_json_string(request)))
        link_uuid = request.link_id.link_uuid.uuid
        reply, link = self._set(request, 'optical_link', link_uuid, 'link_id', TOPIC_LINK)

        context_topology_uuids : Set[Tuple[str, str]] = set()
        context_topology_uuids.add((DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME))
        for endpoint_id in link.link_endpoint_ids:
            endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
            if len(endpoint_context_uuid) == 0: endpoint_context_uuid = DEFAULT_CONTEXT_NAME
            endpoint_topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
            if len(endpoint_topology_uuid) == 0: endpoint_topology_uuid = DEFAULT_TOPOLOGY_NAME
            context_topology_uuids.add((endpoint_context_uuid, endpoint_topology_uuid))

        for context_uuid,topology_uuid in context_topology_uuids:
            container_name = 'topology[{:s}]'.format(str(context_uuid))
            topology = self.obj_db.get_entry(container_name, topology_uuid, context)
            for _optical_link_id in topology.optical_link_ids:
                if _optical_link_id.link_uuid.uuid == link_uuid: break
            else:
                # link not found, add it
                topology.optical_link_ids.add().link_uuid.uuid = link_uuid

        reply = Empty()
        LOGGER.debug('[SetOpticalLink] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def DeleteOpticalLink(self, request : LinkId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[DeleteOpticalLink] request={:s}'.format(grpc_message_to_json_string(request)))
        link_uuid = request.link_uuid.uuid
        optical_link = self.obj_db.get_entry('optical_link', link_uuid, context)
        reply = self._del(request, 'optical_link', link_uuid, 'link_id', TOPIC_LINK, context)

        context_topology_uuids : Set[Tuple[str, str]] = set()
        context_topology_uuids.add((DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME))
        for endpoint_id in optical_link.link_endpoint_ids:
            endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
            if len(endpoint_context_uuid) == 0: endpoint_context_uuid = DEFAULT_CONTEXT_NAME
            endpoint_topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
            if len(endpoint_topology_uuid) == 0: endpoint_topology_uuid = DEFAULT_TOPOLOGY_NAME
            context_topology_uuids.add((endpoint_context_uuid, endpoint_topology_uuid))

        for context_uuid,topology_uuid in context_topology_uuids:
            container_name = 'topology[{:s}]'.format(str(context_uuid))
            topology = self.obj_db.get_entry(container_name, topology_uuid, context)
            for optical_link_id in topology.optical_link_ids:
                if optical_link_id.link_uuid.uuid == link_uuid:
                    topology.optical_link_ids.remove(optical_link_id)
                    break

        LOGGER.debug('[DeleteOpticalLink] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply
