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

import grpc, logging
from typing import Iterator
from common.Constants import ServiceNameEnum
from common.Settings import get_service_host, get_service_port_grpc
from common.tools.client.RetryDecorator import retry, delay_exponential
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.proto.context_pb2 import (
    AnyEvent, Connection, ConnectionEvent, ConnectionId, ConnectionIdList, ConnectionList,
    Context, ContextEvent, ContextId, ContextIdList, ContextList,
    Device, DeviceEvent, DeviceFilter, DeviceId, DeviceIdList, DeviceList,
    Empty, EndPointIdList, EndPointNameList,
    Link, LinkEvent, LinkId, LinkIdList, LinkList,
    OpticalConfig, OpticalConfigId, OpticalConfigList , OpticalLink, OpticalLinkList,
    Service, ServiceConfigRule, ServiceEvent, ServiceFilter, ServiceId, ServiceIdList, ServiceList,
    Slice, SliceEvent, SliceFilter, SliceId, SliceIdList, SliceList,
    Topology, TopologyDetails, TopologyEvent, TopologyId, TopologyIdList, TopologyList,
    OpticalBand, OpticalBandId, OpticalBandList
)
from common.proto.context_pb2_grpc import ContextServiceStub
from common.proto.context_policy_pb2_grpc import ContextPolicyServiceStub
from common.proto.policy_pb2 import PolicyRuleIdList, PolicyRuleId, PolicyRuleList, PolicyRule

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class ContextClient:
    def __init__(self, host=None, port=None):
        if not host: host = get_service_host(ServiceNameEnum.CONTEXT)
        if not port: port = get_service_port_grpc(ServiceNameEnum.CONTEXT)
        self.endpoint = '{:s}:{:s}'.format(str(host), str(port))
        LOGGER.debug('Creating channel to {:s}...'.format(str(self.endpoint)))
        self.channel = None
        self.stub = None
        self.policy_stub = None
        self.connect()
        LOGGER.debug('Channel created')

    def connect(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = ContextServiceStub(self.channel)
        self.policy_stub = ContextPolicyServiceStub(self.channel)

    def close(self):
        if self.channel is not None: self.channel.close()
        self.channel = None
        self.stub = None
        self.policy_stub = None

    @RETRY_DECORATOR
    def GetAllEvents(self, request: Empty) -> Iterator[AnyEvent]:
        LOGGER.debug('GetAllEvents request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetAllEvents(request)
        LOGGER.debug('GetAllEvents result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListContextIds(self, request: Empty) -> ContextIdList:
        LOGGER.debug('ListContextIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListContextIds(request)
        LOGGER.debug('ListContextIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListContexts(self, request: Empty) -> ContextList:
        LOGGER.debug('ListContexts request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListContexts(request)
        LOGGER.debug('ListContexts result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetContext(self, request: ContextId) -> Context:
        LOGGER.debug('GetContext request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetContext(request)
        LOGGER.debug('GetContext result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetContext(self, request: Context) -> ContextId:
        LOGGER.debug('SetContext request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetContext(request)
        LOGGER.debug('SetContext result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RemoveContext(self, request: ContextId) -> Empty:
        LOGGER.debug('RemoveContext request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.RemoveContext(request)
        LOGGER.debug('RemoveContext result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetContextEvents(self, request: Empty) -> Iterator[ContextEvent]:
        LOGGER.debug('GetContextEvents request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetContextEvents(request)
        LOGGER.debug('GetContextEvents result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListTopologyIds(self, request: ContextId) -> TopologyIdList:
        LOGGER.debug('ListTopologyIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListTopologyIds(request)
        LOGGER.debug('ListTopologyIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListTopologies(self, request: ContextId) -> TopologyList:
        LOGGER.debug('ListTopologies request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListTopologies(request)
        LOGGER.debug('ListTopologies result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetTopology(self, request: TopologyId) -> Topology:
        LOGGER.debug('GetTopology request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetTopology(request)
        LOGGER.debug('GetTopology result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetTopology(self, request: Topology) -> TopologyId:
        LOGGER.debug('SetTopology request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetTopology(request)
        LOGGER.debug('SetTopology result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RemoveTopology(self, request: TopologyId) -> Empty:
        LOGGER.debug('RemoveTopology request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.RemoveTopology(request)
        LOGGER.debug('RemoveTopology result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetTopologyEvents(self, request: Empty) -> Iterator[TopologyEvent]:
        LOGGER.debug('GetTopologyEvents request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetTopologyEvents(request)
        LOGGER.debug('GetTopologyEvents result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetTopologyDetails(self, request: TopologyId) -> TopologyDetails:
        LOGGER.debug('GetTopologyDetails request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetTopologyDetails(request)
        LOGGER.debug('GetTopologyDetails result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListDeviceIds(self, request: Empty) -> DeviceIdList:
        LOGGER.debug('ListDeviceIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListDeviceIds(request)
        LOGGER.debug('ListDeviceIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListDevices(self, request: Empty) -> DeviceList:
        LOGGER.debug('ListDevices request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListDevices(request)
        LOGGER.debug('ListDevices result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetDevice(self, request: DeviceId) -> Device:
        LOGGER.debug('GetDevice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetDevice(request)
        LOGGER.debug('GetDevice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetDevice(self, request: Device) -> DeviceId:
        LOGGER.debug('SetDevice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetDevice(request)
        LOGGER.debug('SetDevice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RemoveDevice(self, request: DeviceId) -> Empty:
        LOGGER.debug('RemoveDevice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.RemoveDevice(request)
        LOGGER.debug('RemoveDevice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SelectDevice(self, request: DeviceFilter) -> DeviceList:
        LOGGER.debug('SelectDevice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SelectDevice(request)
        LOGGER.debug('SelectDevice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetDeviceEvents(self, request: Empty) -> Iterator[DeviceEvent]:
        LOGGER.debug('GetDeviceEvents request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetDeviceEvents(request)
        LOGGER.debug('GetDeviceEvents result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListEndPointNames(self, request: EndPointIdList) -> EndPointNameList:
        LOGGER.debug('ListEndPointNames request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListEndPointNames(request)
        LOGGER.debug('ListEndPointNames result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListLinkIds(self, request: Empty) -> LinkIdList:
        LOGGER.debug('ListLinkIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListLinkIds(request)
        LOGGER.debug('ListLinkIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListLinks(self, request: Empty) -> LinkList:
        LOGGER.debug('ListLinks request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListLinks(request)
        LOGGER.debug('ListLinks result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetLink(self, request: LinkId) -> Link:
        LOGGER.debug('GetLink request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetLink(request)
        LOGGER.debug('GetLink result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetLink(self, request: Link) -> LinkId:
        LOGGER.debug('SetLink request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetLink(request)
        LOGGER.debug('SetLink result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RemoveLink(self, request: LinkId) -> Empty:
        LOGGER.debug('RemoveLink request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.RemoveLink(request)
        LOGGER.debug('RemoveLink result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetLinkEvents(self, request: Empty) -> Iterator[LinkEvent]:
        LOGGER.debug('GetLinkEvents request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetLinkEvents(request)
        LOGGER.debug('GetLinkEvents result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListServiceIds(self, request: ContextId) -> ServiceIdList:
        LOGGER.debug('ListServiceIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListServiceIds(request)
        LOGGER.debug('ListServiceIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListServices(self, request: ContextId) -> ServiceList:
        LOGGER.debug('ListServices request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListServices(request)
        LOGGER.debug('ListServices result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetService(self, request: ServiceId) -> Service:
        LOGGER.debug('GetService request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetService(request)
        LOGGER.debug('GetService result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetService(self, request: Service) -> ServiceId:
        LOGGER.debug('SetService request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetService(request)
        LOGGER.debug('SetService result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def UnsetService(self, request: Service) -> ServiceId:
        LOGGER.debug('UnsetService request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.UnsetService(request)
        LOGGER.debug('UnsetService result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RemoveService(self, request: ServiceId) -> Empty:
        LOGGER.debug('RemoveService request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.RemoveService(request)
        LOGGER.debug('RemoveService result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SelectService(self, request: ServiceFilter) -> ServiceList:
        LOGGER.debug('SelectService request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SelectService(request)
        LOGGER.debug('SelectService result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetServiceEvents(self, request: Empty) -> Iterator[ServiceEvent]:
        LOGGER.debug('GetServiceEvents request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetServiceEvents(request)
        LOGGER.debug('GetServiceEvents result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListSliceIds(self, request: ContextId) -> SliceIdList:
        LOGGER.debug('ListSliceIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListSliceIds(request)
        LOGGER.debug('ListSliceIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListSlices(self, request: ContextId) -> SliceList:
        LOGGER.debug('ListSlices request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListSlices(request)
        LOGGER.debug('ListSlices result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetSlice(self, request: SliceId) -> Slice:
        LOGGER.debug('GetSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetSlice(request)
        LOGGER.debug('GetSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetSlice(self, request: Slice) -> SliceId:
        LOGGER.debug('SetSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetSlice(request)
        LOGGER.debug('SetSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def UnsetSlice(self, request: Slice) -> SliceId:
        LOGGER.debug('UnsetSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.UnsetSlice(request)
        LOGGER.debug('UnsetSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RemoveSlice(self, request: SliceId) -> Empty:
        LOGGER.debug('RemoveSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.RemoveSlice(request)
        LOGGER.debug('RemoveSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SelectSlice(self, request: SliceFilter) -> SliceList:
        LOGGER.debug('SelectSlice request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SelectSlice(request)
        LOGGER.debug('SelectSlice result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetSliceEvents(self, request: Empty) -> Iterator[SliceEvent]:
        LOGGER.debug('GetSliceEvents request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetSliceEvents(request)
        LOGGER.debug('GetSliceEvents result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListConnectionIds(self, request: ServiceId) -> ConnectionIdList:
        LOGGER.debug('ListConnectionIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListConnectionIds(request)
        LOGGER.debug('ListConnectionIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListConnections(self, request: ServiceId) -> ConnectionList:
        LOGGER.debug('ListConnections request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.ListConnections(request)
        LOGGER.debug('ListConnections result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetConnection(self, request: ConnectionId) -> Connection:
        LOGGER.debug('GetConnection request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetConnection(request)
        LOGGER.debug('GetConnection result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetConnection(self, request: Connection) -> ConnectionId:
        LOGGER.debug('SetConnection request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetConnection(request)
        LOGGER.debug('SetConnection result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RemoveConnection(self, request: ConnectionId) -> Empty:
        LOGGER.debug('RemoveConnection request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.RemoveConnection(request)
        LOGGER.debug('RemoveConnection result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetConnectionEvents(self, request: Empty) -> Iterator[ConnectionEvent]:
        LOGGER.debug('GetConnectionEvents request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetConnectionEvents(request)
        LOGGER.debug('GetConnectionEvents result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListPolicyRuleIds(self, request: Empty) -> PolicyRuleIdList:
        LOGGER.debug('ListPolicyRuleIds request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.policy_stub.ListPolicyRuleIds(request)
        LOGGER.debug('ListPolicyRuleIds result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def ListPolicyRules(self, request: Empty) -> PolicyRuleList:
        LOGGER.debug('ListPolicyRules request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.policy_stub.ListPolicyRules(request)
        LOGGER.debug('ListPolicyRules result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetPolicyRule(self, request: PolicyRuleId) -> PolicyRule:
        LOGGER.info('GetPolicyRule request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.policy_stub.GetPolicyRule(request)
        LOGGER.info('GetPolicyRule result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetPolicyRule(self, request: PolicyRule) -> PolicyRuleId:
        LOGGER.debug('SetPolicyRule request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.policy_stub.SetPolicyRule(request)
        LOGGER.debug('SetPolicyRule result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def RemovePolicyRule(self, request: PolicyRuleId) -> Empty:
        LOGGER.debug('RemovePolicyRule request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.policy_stub.RemovePolicyRule(request)
        LOGGER.debug('RemovePolicyRule result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    #//////////////// Experimental //////////////////

    @RETRY_DECORATOR
    def SetOpticalConfig(self, request : OpticalConfig) -> OpticalConfigId:
        LOGGER.debug('SetOpticalConfig request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetOpticalConfig(request)
        LOGGER.debug('SetOpticalConfig result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    @RETRY_DECORATOR
    def UpdateOpticalConfig(self, request : OpticalConfig) -> OpticalConfigId:
        LOGGER.debug('SetOpticalConfig request: {:s}'.format(grpc_message_to_json_string(request)))
        response_future = self.stub.UpdateOpticalConfig.future(request)
        response = response_future.result()
        LOGGER.debug('SetOpticalConfig result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetOpticalConfig(self, request : Empty) -> OpticalConfigList:
        LOGGER.debug('GetOpticalConfig request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetOpticalConfig(request)
        LOGGER.debug('GetOpticalConfig result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SelectOpticalConfig(self,request : OpticalConfigId) -> OpticalConfigList:
        LOGGER.debug('SelectOpticalConfig request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SelectOpticalConfig(request)
        LOGGER.debug('SelectOpticalConfig result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    @RETRY_DECORATOR
    def DeleteOpticalConfig(self,request : OpticalConfigId) -> Empty:
        LOGGER.debug('DeleteOpticalConfig request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteOpticalConfig(request)
        LOGGER.debug('DeleteOpticalConfig result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    @RETRY_DECORATOR
    def DeleteOpticalChannel(self,request : OpticalConfig) -> Empty:
        LOGGER.debug('DeleteOpticalChannel request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteOpticalChannel(request)
        LOGGER.debug('DeleteOpticalChannel result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    
    @RETRY_DECORATOR
    def GetOpticalBand(self, request : Empty) -> OpticalBandList:
        LOGGER.debug('GetOpticalBand request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetOpticalBand(request)
        LOGGER.debug('GetOpticalBand result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    @RETRY_DECORATOR
    def SelectOpticalBand(self, request : OpticalBandId) -> OpticalBand:
        LOGGER.debug('SelectOpticalBand request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SelectOpticalBand(request)
        LOGGER.debug('SelectOpticalBand result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetOpticalBand(self,request : OpticalBand) -> Empty:
        LOGGER.debug('SetOpticalBand request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetOpticalBand(request)
        LOGGER.debug('SetOpticalBand result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    #--------------------------- Optical Link ------------------------
    def GetOpticalLinkList(self, request: Empty) -> OpticalLinkList:
        LOGGER.debug('ListOpticalLinks request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetOpticalLinkList(request)
        LOGGER.debug('ListOpticalLinks result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetOpticalLink(self, request: LinkId) -> OpticalLink:
        LOGGER.debug('GetOpticalLink request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetOpticalLink(request)
        LOGGER.debug('GetOpticalLink result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetOpticalLink(self, request: OpticalLink) -> LinkId:
        LOGGER.debug('SetOpticalLink request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetOpticalLink(request)
        LOGGER.debug('SetOpticalLink result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def DeleteOpticalLink(self, request: LinkId) -> Empty:
        LOGGER.debug('RemoveOpticalLink request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteOpticalLink(request)
        LOGGER.debug('RemoveOpticalLink result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
    
    
    # --------------------------------- Service ConfigRule Deletion ------------------
    
    @RETRY_DECORATOR
    def DeleteServiceConfigRule(self, request: ServiceConfigRule) -> Empty:
        LOGGER.debug('ServiceConfigRule Delete request: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteServiceConfigRule(request)
        LOGGER.debug('ServiceConfigRule Delete result: {:s}'.format(grpc_message_to_json_string(response)))
        return response
