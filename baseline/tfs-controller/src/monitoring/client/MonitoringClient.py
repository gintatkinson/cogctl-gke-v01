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
from common.proto.context_pb2 import Empty
from common.proto.monitoring_pb2 import Kpi, KpiDescriptor, KpiId, MonitorKpiRequest, \
    KpiDescriptorList, KpiQuery, KpiList, SubsDescriptor, SubscriptionID, SubsList, \
    SubsResponse, AlarmDescriptor, AlarmID, AlarmList, AlarmResponse, AlarmSubscription, RawKpiTable
from common.proto.monitoring_pb2_grpc import MonitoringServiceStub

LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')

class MonitoringClient:
    def __init__(self, host=None, port=None):
        if not host: host = get_service_host(ServiceNameEnum.MONITORING)
        if not port: port = get_service_port_grpc(ServiceNameEnum.MONITORING)
        self.endpoint = '{:s}:{:s}'.format(str(host), str(port))
        LOGGER.debug('Creating channel to {:s}...'.format(str(self.endpoint)))
        self.channel = None
        self.stub = None
        self.connect()
        LOGGER.debug('Channel created')

    def connect(self):
        self.channel = grpc.insecure_channel(self.endpoint)
        self.stub = MonitoringServiceStub(self.channel)

    def close(self):
        if self.channel is not None: self.channel.close()
        self.channel = None
        self.stub = None

    @RETRY_DECORATOR
    def SetKpi(self, request : KpiDescriptor) -> KpiId:
        LOGGER.debug('SetKpi: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetKpi(request)
        LOGGER.debug('SetKpi result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def DeleteKpi(self,request : KpiId) -> Empty:
        LOGGER.debug('DeleteKpi: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteKpi(request)
        LOGGER.info('DeleteKpi result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetKpiDescriptor(self, request : KpiId) -> KpiDescriptor:
        LOGGER.debug('GetKpiDescriptor: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetKpiDescriptor(request)
        LOGGER.debug('GetKpiDescriptor result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetKpiDescriptorList(self, request : Empty) -> KpiDescriptorList:
        LOGGER.debug('GetKpiDescriptorList: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetKpiDescriptorList(request)
        LOGGER.debug('GetKpiDescriptorList result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def IncludeKpi(self, request : Kpi) -> Empty:
        LOGGER.debug('IncludeKpi: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.IncludeKpi(request)
        LOGGER.debug('IncludeKpi result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def MonitorKpi(self, request : MonitorKpiRequest) -> Empty:
        LOGGER.debug('MonitorKpi: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.MonitorKpi(request)
        LOGGER.debug('MonitorKpi result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def QueryKpiData(self, request : KpiQuery) -> RawKpiTable:
        LOGGER.debug('QueryKpiData: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.QueryKpiData(request)
        LOGGER.debug('QueryKpiData result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetKpiSubscription(self, request : SubsDescriptor) -> Iterator[SubsResponse]:
        LOGGER.debug('SetKpiSubscription: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetKpiSubscription(request)
        LOGGER.debug('SetKpiSubscription result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetSubsDescriptor(self, request : SubscriptionID) -> SubsDescriptor:
        LOGGER.debug('GetSubsDescriptor: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetSubsDescriptor(request)
        LOGGER.debug('GetSubsDescriptor result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetSubscriptions(self, request : Empty) -> SubsList:
        LOGGER.debug('GetSubscriptions: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetSubscriptions(request)
        LOGGER.debug('GetSubscriptions result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def DeleteSubscription(self, request : SubscriptionID) -> Empty:
        LOGGER.debug('DeleteSubscription: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteSubscription(request)
        LOGGER.debug('DeleteSubscription result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def SetKpiAlarm(self, request : AlarmDescriptor) -> AlarmID:
        LOGGER.debug('SetKpiAlarm: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.SetKpiAlarm(request)
        LOGGER.debug('SetKpiAlarm result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetAlarms(self, request : Empty) -> AlarmList:
        LOGGER.debug('GetAlarms: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetAlarms(request)
        LOGGER.debug('GetAlarms result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    def GetAlarmDescriptor(self, request : AlarmID) -> AlarmDescriptor:
        LOGGER.debug('GetAlarmDescriptor: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetAlarmDescriptor(request)
        LOGGER.debug('GetAlarmDescriptor result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    def GetAlarmResponseStream(self, request : AlarmSubscription) -> AlarmResponse:
        LOGGER.debug('GetAlarmResponseStream: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetAlarmResponseStream(request)
        LOGGER.debug('GetAlarmResponseStream result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    def DeleteAlarm(self, request : AlarmID) -> Empty:
        LOGGER.debug('DeleteAlarm: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.DeleteAlarm(request)
        LOGGER.debug('DeleteAlarm result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetStreamKpi(self, request : KpiId) -> Iterator[Kpi]:
        LOGGER.debug('GetStreamKpi: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetStreamKpi(request)
        LOGGER.debug('GetStreamKpi result: {:s}'.format(grpc_message_to_json_string(response)))
        return response

    @RETRY_DECORATOR
    def GetInstantKpi(self, request : KpiId) -> Kpi:
        LOGGER.debug('GetInstantKpi: {:s}'.format(grpc_message_to_json_string(request)))
        response = self.stub.GetInstantKpi(request)
        LOGGER.debug('GetInstantKpi result: {:s}'.format(grpc_message_to_json_string(response)))
        return response


if __name__ == '__main__':
    import sys
    # get port
    _port = sys.argv[1] if len(sys.argv) > 1 else '7070'

    # make call to server
    client = MonitoringClient(port=_port)
