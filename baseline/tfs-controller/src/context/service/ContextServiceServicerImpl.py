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

import grpc, logging, sqlalchemy
from typing import Iterator
from common.message_broker.MessageBroker import MessageBroker
from common.proto.context_pb2 import (
    AnyEvent, Connection, ConnectionEvent, ConnectionId, ConnectionIdList, ConnectionList,
    Context, ContextEvent, ContextId, ContextIdList, ContextList,
    Device, DeviceEvent, DeviceFilter, DeviceId, DeviceIdList, DeviceList,
    Empty, EndPointIdList, EndPointNameList,
    Link, LinkEvent, LinkId, LinkIdList, LinkList,
    Service, ServiceConfigRule, ServiceEvent, ServiceFilter, ServiceId, ServiceIdList, ServiceList,
    Slice, SliceEvent, SliceFilter, SliceId, SliceIdList, SliceList,
    Topology, TopologyDetails, TopologyEvent, TopologyId, TopologyIdList, TopologyList,
    OpticalConfigList, OpticalConfigId, OpticalConfig, OpticalLink, OpticalLinkList,
    OpticalBand, OpticalBandId, OpticalBandList
)
from common.proto.policy_pb2 import PolicyRuleIdList, PolicyRuleId, PolicyRuleList, PolicyRule
from common.proto.context_pb2_grpc import ContextServiceServicer
from common.proto.context_policy_pb2_grpc import ContextPolicyServiceServicer
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from .database.ConfigRule import delete_config_rule
from .database.Connection import (
    connection_delete, connection_get, connection_list_ids, connection_list_objs, connection_set
)
from .database.Context import (
    context_delete, context_get, context_list_ids, context_list_objs, context_set
)
from .database.Device import (
    device_delete, device_get, device_list_ids, device_list_objs, device_select, device_set
)
from .database.EndPoint import endpoint_list_names
from .database.Events import EventTopicEnum, consume_all_events, consume_events
from .database.Link import (
    link_delete, link_get, link_list_ids, link_list_objs, link_set
)
from .database.PolicyRule import (
    policyrule_delete, policyrule_get, policyrule_list_ids, policyrule_list_objs,
    policyrule_set
)
from .database.Service import (
    service_delete, service_get, service_list_ids, service_list_objs, service_select,
    service_set, service_unset
)
from .database.Slice import (
    slice_delete, slice_get, slice_list_ids, slice_list_objs, slice_select,
    slice_set, slice_unset
)
from .database.Topology import (
    topology_delete, topology_get, topology_get_details, topology_list_ids,
    topology_list_objs, topology_set
)
from .database.OpticalBand import (
    get_optical_band, set_optical_band, select_optical_band
)
from .database.OpticalConfig import (
    set_opticalconfig, select_opticalconfig, get_opticalconfig, delete_opticalconfig,
    update_opticalconfig, delete_opticalchannel
)
from .database.OpticalLink import (
    optical_link_delete, optical_link_get, optical_link_list_objs, optical_link_set
)


LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Context', 'RPC')

class ContextServiceServicerImpl(ContextServiceServicer, ContextPolicyServiceServicer):
    def __init__(self, db_engine : sqlalchemy.engine.Engine, messagebroker : MessageBroker) -> None:
        LOGGER.debug('Creating Servicer...')
        self.db_engine = db_engine
        self.messagebroker = messagebroker
        LOGGER.debug('Servicer Created')

    def _get_metrics(self) -> MetricsPool: return METRICS_POOL


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetAllEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[AnyEvent]:
        for message in consume_all_events(self.messagebroker): yield message


    # ----- Context ----------------------------------------------------------------------------------------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListContextIds(self, request : Empty, context : grpc.ServicerContext) -> ContextIdList:
        return context_list_ids(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListContexts(self, request : Empty, context : grpc.ServicerContext) -> ContextList:
        return context_list_objs(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetContext(self, request : ContextId, context : grpc.ServicerContext) -> Context:
        return context_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetContext(self, request : Context, context : grpc.ServicerContext) -> ContextId:
        return context_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveContext(self, request : ContextId, context : grpc.ServicerContext) -> Empty:
        return context_delete(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetContextEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[ContextEvent]:
        for message in consume_events(self.messagebroker, {EventTopicEnum.CONTEXT}): yield message


    # ----- Topology ---------------------------------------------------------------------------------------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListTopologyIds(self, request : ContextId, context : grpc.ServicerContext) -> TopologyIdList:
        return topology_list_ids(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListTopologies(self, request : ContextId, context : grpc.ServicerContext) -> TopologyList:
        return topology_list_objs(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetTopology(self, request : TopologyId, context : grpc.ServicerContext) -> Topology:
        return topology_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetTopologyDetails(self, request : TopologyId, context : grpc.ServicerContext) -> TopologyDetails:
        return topology_get_details(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetTopology(self, request : Topology, context : grpc.ServicerContext) -> TopologyId:
        return topology_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveTopology(self, request : TopologyId, context : grpc.ServicerContext) -> Empty:
        return topology_delete(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetTopologyEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[TopologyEvent]:
        for message in consume_events(self.messagebroker, {EventTopicEnum.TOPOLOGY}): yield message


    # ----- Device -----------------------------------------------------------------------------------------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListDeviceIds(self, request : Empty, context : grpc.ServicerContext) -> DeviceIdList:
        return device_list_ids(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListDevices(self, request : Empty, context : grpc.ServicerContext) -> DeviceList:
        return device_list_objs(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetDevice(self, request : DeviceId, context : grpc.ServicerContext) -> Device:
        return device_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetDevice(self, request : Device, context : grpc.ServicerContext) -> DeviceId:
        return device_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveDevice(self, request : DeviceId, context : grpc.ServicerContext) -> Empty:
        return device_delete(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SelectDevice(self, request : DeviceFilter, context : grpc.ServicerContext) -> DeviceList:
        return device_select(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetDeviceEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[DeviceEvent]:
        for message in consume_events(self.messagebroker, {EventTopicEnum.DEVICE}): yield message

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListEndPointNames(self, request : EndPointIdList, context : grpc.ServicerContext) -> EndPointNameList:
        return endpoint_list_names(self.db_engine, request)


    # ----- Link -------------------------------------------------------------------------------------------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListLinkIds(self, request : Empty, context : grpc.ServicerContext) -> LinkIdList:
        return link_list_ids(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListLinks(self, request : Empty, context : grpc.ServicerContext) -> LinkList:
        return link_list_objs(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetLink(self, request : LinkId, context : grpc.ServicerContext) -> Link:
        return link_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetLink(self, request : Link, context : grpc.ServicerContext) -> LinkId:
        return link_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveLink(self, request : LinkId, context : grpc.ServicerContext) -> Empty:
        return link_delete(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetLinkEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[LinkEvent]:
        for message in consume_events(self.messagebroker, {EventTopicEnum.LINK}): yield message


    # ----- Service ----------------------------------------------------------------------------------------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListServiceIds(self, request : ContextId, context : grpc.ServicerContext) -> ServiceIdList:
        return service_list_ids(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListServices(self, request : ContextId, context : grpc.ServicerContext) -> ServiceList:
        return service_list_objs(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetService(self, request : ServiceId, context : grpc.ServicerContext) -> Service:
        return service_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetService(self, request : Service, context : grpc.ServicerContext) -> ServiceId:
        return service_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def UnsetService(self, request : Service, context : grpc.ServicerContext) -> ServiceId:
        return service_unset(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveService(self, request : ServiceId, context : grpc.ServicerContext) -> Empty:
        return service_delete(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SelectService(self, request : ServiceFilter, context : grpc.ServicerContext) -> ServiceList:
        return service_select(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetServiceEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[ServiceEvent]:
        for message in consume_events(self.messagebroker, {EventTopicEnum.SERVICE}): yield message


    # ----- Slice ----------------------------------------------------------------------------------------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListSliceIds(self, request : ContextId, context : grpc.ServicerContext) -> SliceIdList:
        return slice_list_ids(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListSlices(self, request : ContextId, context : grpc.ServicerContext) -> SliceList:
        return slice_list_objs(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetSlice(self, request : SliceId, context : grpc.ServicerContext) -> Slice:
        return slice_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        return slice_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def UnsetSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        return slice_unset(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveSlice(self, request : SliceId, context : grpc.ServicerContext) -> Empty:
        return slice_delete(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SelectSlice(self, request : SliceFilter, context : grpc.ServicerContext) -> SliceList:
        return slice_select(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetSliceEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[SliceEvent]:
        for message in consume_events(self.messagebroker, {EventTopicEnum.SLICE}): yield message


    # ----- Connection -------------------------------------------------------------------------------------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListConnectionIds(self, request : ServiceId, context : grpc.ServicerContext) -> ConnectionIdList:
        return connection_list_ids(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListConnections(self, request : ContextId, context : grpc.ServicerContext) -> ConnectionList:
        return connection_list_objs(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetConnection(self, request : ConnectionId, context : grpc.ServicerContext) -> Connection:
        return connection_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetConnection(self, request : Connection, context : grpc.ServicerContext) -> ConnectionId:
        return connection_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveConnection(self, request : ConnectionId, context : grpc.ServicerContext) -> Empty:
        return connection_delete(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetConnectionEvents(self, request : Empty, context : grpc.ServicerContext) -> Iterator[ConnectionEvent]:
        for message in consume_events(self.messagebroker, {EventTopicEnum.CONNECTION}): yield message


    # ----- Policy Rule ------------------------------------------------------------------------------------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListPolicyRuleIds(self, request : Empty, context: grpc.ServicerContext) -> PolicyRuleIdList:
        return policyrule_list_ids(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListPolicyRules(self, request : Empty, context: grpc.ServicerContext) -> PolicyRuleList:
        return policyrule_list_objs(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetPolicyRule(self, request : PolicyRuleId, context: grpc.ServicerContext) -> PolicyRule:
        return policyrule_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetPolicyRule(self, request : PolicyRule, context: grpc.ServicerContext) -> PolicyRuleId:
        return policyrule_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemovePolicyRule(self, request : PolicyRuleId, context: grpc.ServicerContext) -> Empty:
        return policyrule_delete(self.db_engine, self.messagebroker, request)

    # ---------------------------- Experimental -------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetOpticalConfig(self, request : Empty, context : grpc.ServicerContext) -> OpticalConfigList:
        result = get_opticalconfig(self.db_engine)
        return OpticalConfigList(opticalconfigs=result)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetOpticalConfig(self, request : OpticalConfig, context : grpc.ServicerContext) -> OpticalConfigId:
        result = set_opticalconfig(self.db_engine, request)
        return OpticalConfigId(**result)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def UpdateOpticalConfig(self, request : OpticalConfig, context : grpc.ServicerContext) -> OpticalConfigId:
        result = update_opticalconfig(self.db_engine, request)
        return OpticalConfigId(**result)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SelectOpticalConfig(self, request : OpticalConfigId, context : grpc.ServicerContext) -> OpticalConfig:
        result = select_opticalconfig(self.db_engine, request)
        optical_config_id = OpticalConfigId()
        device_id = DeviceId()
        optical_config_id.CopyFrom(result.opticalconfig_id)
        device_id.CopyFrom(result.device_id)
        return OpticalConfig(config=result.config, opticalconfig_id=optical_config_id , device_id=device_id)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteOpticalConfig(self, request : OpticalConfigId, context : grpc.ServicerContext) -> Empty:
        delete_opticalconfig(self.db_engine, self.messagebroker, request)
        return Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteOpticalChannel(self, request : OpticalConfig, context : grpc.ServicerContext) -> Empty:
        delete_opticalchannel(self.db_engine, self.messagebroker, request)
        return Empty()
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetOpticalBand(self, request : Empty, context : grpc.ServicerContext) -> OpticalBandList:
        result = get_optical_band(self.db_engine)
        return OpticalBandList(opticalbands=result)
    
    safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SelectOpticalBand(self, request : OpticalBandId, context : grpc.ServicerContext) -> OpticalBand:
        result = select_optical_band(self.db_engine,request )
        return result

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetOpticalBand(self, request : OpticalBand, context : grpc.ServicerContext) -> Empty:
        result = set_optical_band(self.db_engine, request)
        return Empty()


    #--------------------- Experimental Optical Link -------------------

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetOpticalLinkList(self, request : Empty, context : grpc.ServicerContext) -> OpticalLinkList:
        return optical_link_list_objs(self.db_engine)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetOpticalLink(self, request : LinkId, context : grpc.ServicerContext) -> OpticalLink:
        return optical_link_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetOpticalLink(self, request : Link, context : grpc.ServicerContext) -> LinkId:
        return optical_link_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteOpticalLink(self, request : LinkId, context : grpc.ServicerContext) -> Empty:
        return optical_link_delete(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteServiceConfigRule(self, request : ServiceConfigRule, context : grpc.ServicerContext) -> Empty:
        return delete_config_rule(self.db_engine,  request)
