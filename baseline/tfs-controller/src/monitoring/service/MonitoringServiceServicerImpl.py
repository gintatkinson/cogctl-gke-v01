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

import logging, os, grpc
from queue import Queue
from typing import Iterator
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import Empty
from common.proto.device_pb2 import MonitoringSettings
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.monitoring_pb2_grpc import MonitoringServiceServicer
from common.proto.monitoring_pb2 import AlarmResponse, AlarmDescriptor, AlarmList, SubsList, KpiId, \
    KpiDescriptor, KpiList, KpiQuery, SubsDescriptor, SubscriptionID, AlarmID, KpiDescriptorList, \
    MonitorKpiRequest, Kpi, AlarmSubscription, SubsResponse, RawKpiTable, RawKpi, RawKpiList
from common.tools.timestamp.Converters import timestamp_string_to_float, timestamp_utcnow_to_float
from device.client.DeviceClient import DeviceClient
from monitoring.service import ManagementDBTools, MetricsDBTools
from monitoring.service.AlarmManager import AlarmManager
from monitoring.service.NameMapping import NameMapping
from monitoring.service.SubscriptionManager import SubscriptionManager

LOGGER = logging.getLogger(__name__)

METRICSDB_HOSTNAME = os.environ.get("METRICSDB_HOSTNAME")
METRICSDB_ILP_PORT = os.environ.get("METRICSDB_ILP_PORT")
METRICSDB_REST_PORT = os.environ.get("METRICSDB_REST_PORT")
METRICSDB_TABLE_MONITORING_KPIS = os.environ.get("METRICSDB_TABLE_MONITORING_KPIS")

METRICS_POOL = MetricsPool('Monitoring', 'RPC')

class MonitoringServiceServicerImpl(MonitoringServiceServicer):
    def __init__(self, name_mapping : NameMapping):
        LOGGER.info('Init monitoringService')

        # Init sqlite monitoring db
        self.management_db = ManagementDBTools.ManagementDB('monitoring.db')
        self.deviceClient = DeviceClient()
        self.metrics_db = MetricsDBTools.MetricsDB(
            METRICSDB_HOSTNAME, name_mapping, METRICSDB_ILP_PORT, METRICSDB_REST_PORT, METRICSDB_TABLE_MONITORING_KPIS)
        self.subs_manager = SubscriptionManager(self.metrics_db)
        self.alarm_manager = AlarmManager(self.metrics_db)
        LOGGER.info('MetricsDB initialized')

    # SetKpi (SetKpiRequest) returns (KpiId) {}
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetKpi(
            self, request: KpiDescriptor, grpc_context: grpc.ServicerContext
    ) -> KpiId:
        response = KpiId()
        kpi_description = request.kpi_description
        kpi_sample_type = request.kpi_sample_type
        kpi_device_id = request.device_id.device_uuid.uuid
        kpi_endpoint_id = request.endpoint_id.endpoint_uuid.uuid
        kpi_service_id = request.service_id.service_uuid.uuid
        kpi_slice_id = request.slice_id.slice_uuid.uuid
        kpi_connection_id = request.connection_id.connection_uuid.uuid
        kpi_link_id = request.link_id.link_uuid.uuid
        if request.kpi_id.kpi_id.uuid != "":
            response.kpi_id.uuid = request.kpi_id.kpi_id.uuid
            # Here the code to modify an existing kpi
        else:
            data = self.management_db.insert_KPI(
                kpi_description, kpi_sample_type, kpi_device_id, kpi_endpoint_id, kpi_service_id, kpi_slice_id,
                kpi_connection_id, kpi_link_id)
            response.kpi_id.uuid = str(data)
        return response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteKpi(self, request: KpiId, grpc_context: grpc.ServicerContext) -> Empty:
        kpi_id = int(request.kpi_id.uuid)
        kpi = self.management_db.get_KPI(kpi_id)
        if kpi:
            self.management_db.delete_KPI(kpi_id)
        else:
            LOGGER.info('DeleteKpi error: KpiID({:s}): not found in database'.format(str(kpi_id)))
        return Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetKpiDescriptor(self, request: KpiId, grpc_context: grpc.ServicerContext) -> KpiDescriptor:
        kpi_id = request.kpi_id.uuid
        kpi_db = self.management_db.get_KPI(int(kpi_id))
        kpiDescriptor = KpiDescriptor()
        if kpi_db is None:
            LOGGER.info('GetKpiDescriptor error: KpiID({:s}): not found in database'.format(str(kpi_id)))
        else:
            kpiDescriptor.kpi_description                       = kpi_db[1]
            kpiDescriptor.kpi_sample_type                       = kpi_db[2]
            kpiDescriptor.device_id.device_uuid.uuid            = str(kpi_db[3])
            kpiDescriptor.endpoint_id.endpoint_uuid.uuid        = str(kpi_db[4])
            kpiDescriptor.service_id.service_uuid.uuid          = str(kpi_db[5])
            kpiDescriptor.slice_id.slice_uuid.uuid              = str(kpi_db[6])
            kpiDescriptor.connection_id.connection_uuid.uuid    = str(kpi_db[7])
            kpiDescriptor.link_id.link_uuid.uuid                = str(kpi_db[8])
        return kpiDescriptor

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetKpiDescriptorList(self, request: Empty, grpc_context: grpc.ServicerContext) -> KpiDescriptorList:
        kpi_descriptor_list = KpiDescriptorList()
        data = self.management_db.get_KPIS()
        LOGGER.debug(f"data: {data}")
        for item in data:
            kpi_descriptor = KpiDescriptor()
            kpi_descriptor.kpi_id.kpi_id.uuid                   = str(item[0])
            kpi_descriptor.kpi_description                      = item[1]
            kpi_descriptor.kpi_sample_type                      = item[2]
            kpi_descriptor.device_id.device_uuid.uuid           = str(item[3])
            kpi_descriptor.endpoint_id.endpoint_uuid.uuid       = str(item[4])
            kpi_descriptor.service_id.service_uuid.uuid         = str(item[5])
            kpi_descriptor.slice_id.slice_uuid.uuid             = str(item[6])
            kpi_descriptor.connection_id.connection_uuid.uuid   = str(item[7])
            kpi_descriptor.link_id.link_uuid.uuid               = str(item[8])
            kpi_descriptor_list.kpi_descriptor_list.append(kpi_descriptor)
        return kpi_descriptor_list

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def IncludeKpi(self, request: Kpi, grpc_context: grpc.ServicerContext) -> Empty:
        kpi_id = request.kpi_id.kpi_id.uuid
        kpiDescriptor = self.GetKpiDescriptor(request.kpi_id, grpc_context)

        if kpiDescriptor is None:
            LOGGER.info('IncludeKpi error: KpiID({:s}): not found in database'.format(str(kpi_id)))
        else:
            kpiSampleType = KpiSampleType.Name(kpiDescriptor.kpi_sample_type).upper().replace('KPISAMPLETYPE_', '')
            kpiId = kpi_id
            deviceId = kpiDescriptor.device_id.device_uuid.uuid
            endpointId = kpiDescriptor.endpoint_id.endpoint_uuid.uuid
            serviceId = kpiDescriptor.service_id.service_uuid.uuid
            sliceId   = kpiDescriptor.slice_id.slice_uuid.uuid
            connectionId = kpiDescriptor.connection_id.connection_uuid.uuid
            linkId = kpiDescriptor.link_id.link_uuid.uuid
            time_stamp = request.timestamp.timestamp
            kpi_value = getattr(request.kpi_value, request.kpi_value.WhichOneof('value'))

            # Build the structure to be included as point in the MetricsDB
            self.metrics_db.write_KPI(time_stamp, kpiId, kpiSampleType, deviceId, endpointId, serviceId, sliceId, connectionId, linkId, kpi_value)
        return Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def MonitorKpi(self, request: MonitorKpiRequest, grpc_context: grpc.ServicerContext) -> Empty:
        kpi_id = int(request.kpi_id.kpi_id.uuid)
        kpi = self.management_db.get_KPI(kpi_id)
        response = Empty()
        if kpi:
            # Sets the request to send to the device service
            monitor_device_request = MonitoringSettings()
            kpiDescriptor = self.GetKpiDescriptor(request.kpi_id, grpc_context)
            monitor_device_request.kpi_descriptor.CopyFrom(kpiDescriptor)
            monitor_device_request.kpi_id.kpi_id.uuid = request.kpi_id.kpi_id.uuid
            monitor_device_request.sampling_duration_s = request.monitoring_window_s
            monitor_device_request.sampling_interval_s = request.sampling_rate_s
            if not self.management_db.check_monitoring_flag(kpi_id):
                device_client = DeviceClient()
                device_client.MonitorDeviceKpi(monitor_device_request)
                self.management_db.set_monitoring_flag(kpi_id,True)
                self.management_db.check_monitoring_flag(kpi_id)
            else:
                LOGGER.warning('MonitorKpi warning: KpiID({:s}) is currently being monitored'.format(str(kpi_id)))
        else:
            LOGGER.info('MonitorKpi error: KpiID({:s}): not found in database'.format(str(kpi_id)))
        return response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def QueryKpiData(self, request: KpiQuery, grpc_context: grpc.ServicerContext) -> RawKpiTable:
        raw_kpi_table = RawKpiTable()
        kpi_id_list             = request.kpi_ids
        monitoring_window_s     = request.monitoring_window_s
        last_n_samples          = request.last_n_samples
        start_timestamp         = request.start_timestamp.timestamp
        end_timestamp           = request.end_timestamp.timestamp

        # Check if all the Kpi_ids exist
        for item in kpi_id_list:
            kpi_id = item.kpi_id.uuid
            kpiDescriptor = self.GetKpiDescriptor(item, grpc_context)
            if kpiDescriptor is None:
                LOGGER.info('QueryKpiData error: KpiID({:s}): not found in database'.format(str(kpi_id)))
                break
            else:
                # Execute query per Kpi_id and introduce their kpi_list in the table
                kpi_list = self.metrics_db.get_raw_kpi_list(kpi_id,monitoring_window_s,last_n_samples,start_timestamp,end_timestamp)
                raw_kpi_list = RawKpiList()
                raw_kpi_list.kpi_id.kpi_id.uuid = kpi_id

                LOGGER.debug(str(kpi_list))

                if kpi_list is None:
                    LOGGER.info('QueryKpiData error: KpiID({:s}): points not found in metrics database'.format(str(kpi_id)))
                else:
                    for item in kpi_list:
                        raw_kpi = RawKpi()
                        raw_kpi.timestamp.timestamp = timestamp_string_to_float(item[0])
                        raw_kpi.kpi_value.floatVal  = item[1]
                        raw_kpi_list.raw_kpis.append(raw_kpi)

                raw_kpi_table.raw_kpi_lists.append(raw_kpi_list)
        return raw_kpi_table

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetKpiSubscription(self, request: SubsDescriptor, grpc_context: grpc.ServicerContext) -> SubsResponse:
        subs_queue = Queue()

        kpi_id = request.kpi_id.kpi_id.uuid
        sampling_duration_s = request.sampling_duration_s
        sampling_interval_s = request.sampling_interval_s
        start_timestamp = request.start_timestamp.timestamp
        end_timestamp = request.end_timestamp.timestamp

        subscriber = "localhost"  # Investigate how to get info from the requester

        subs_id = self.management_db.insert_subscription(kpi_id, subscriber, sampling_duration_s,
                                                            sampling_interval_s, start_timestamp, end_timestamp)
        self.subs_manager.create_subscription(subs_queue, subs_id, kpi_id, sampling_interval_s, sampling_duration_s,
                                                start_timestamp, end_timestamp)

        # parse queue to append kpis into the list
        while True:
            while not subs_queue.empty():
                subs_response = SubsResponse()
                list = subs_queue.get_nowait()
                for item in list:
                    kpi = Kpi()
                    kpi.kpi_id.kpi_id.uuid = str(item[0])
                    kpi.timestamp.timestamp = timestamp_string_to_float(item[1])
                    kpi.kpi_value.floatVal = item[2]  # This must be improved
                    subs_response.kpi_list.kpi.append(kpi)
                subs_response.subs_id.subs_id.uuid = str(subs_id)
                yield subs_response
            if timestamp_utcnow_to_float() > end_timestamp:
                break
        # yield subs_response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetSubsDescriptor(self, request: SubscriptionID, grpc_context: grpc.ServicerContext) -> SubsDescriptor:
        subs_id = request.subs_id.uuid
        subs_db = self.management_db.get_subscription(int(request.subs_id.uuid))
        response = SubsDescriptor()
        if subs_db is None:
            LOGGER.info('GetSubsDescriptor error: SubsID({:s}): not found in database'.format(str(subs_id)))
        else:
            LOGGER.debug(subs_db)
            response.subs_id.subs_id.uuid = str(subs_db[0])
            response.kpi_id.kpi_id.uuid = str(subs_db[1])
            response.sampling_duration_s = subs_db[3]
            response.sampling_interval_s = subs_db[4]
            response.start_timestamp.timestamp = subs_db[5]
            response.end_timestamp.timestamp = subs_db[6]
        return response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetSubscriptions(self, request: Empty, grpc_context: grpc.ServicerContext) -> SubsList:
        response = SubsList()
        data = self.management_db.get_subscriptions()
        for subs_db in data:
            subs_descriptor = SubsDescriptor()
            subs_descriptor.subs_id.subs_id.uuid = str(subs_db[0])
            subs_descriptor.kpi_id.kpi_id.uuid = str(subs_db[1])
            subs_descriptor.sampling_duration_s = subs_db[3]
            subs_descriptor.sampling_interval_s = subs_db[4]
            subs_descriptor.start_timestamp.timestamp = subs_db[5]
            subs_descriptor.end_timestamp.timestamp = subs_db[6]
            response.subs_descriptor.append(subs_descriptor)
        return response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteSubscription(self, request: SubscriptionID, grpc_context: grpc.ServicerContext) -> Empty:
        subs_id = int(request.subs_id.uuid)
        subs_db = self.management_db.get_subscription(int(request.subs_id.uuid))
        if subs_db:
            self.management_db.delete_subscription(subs_id)
        else:
            LOGGER.info('DeleteSubscription error: SubsID({:s}): not found in database'.format(str(subs_id)))
        return Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetKpiAlarm(self, request: AlarmDescriptor, grpc_context: grpc.ServicerContext) -> AlarmResponse:
        response = AlarmID()
        alarm_description = request.alarm_description
        alarm_name = request.name
        kpi_id = request.kpi_id.kpi_id.uuid
        kpi_min_value = float(request.kpi_value_range.kpiMinValue.floatVal)
        kpi_max_value = float(request.kpi_value_range.kpiMaxValue.floatVal)
        in_range = request.kpi_value_range.inRange
        include_min_value = request.kpi_value_range.includeMinValue
        include_max_value = request.kpi_value_range.includeMaxValue
        timestamp = request.timestamp.timestamp
        LOGGER.debug(f"request.AlarmID: {request.alarm_id.alarm_id.uuid}")
        if request.alarm_id.alarm_id.uuid != "":
            alarm_id = request.alarm_id.alarm_id.uuid
            # Here the code to modify an existing alarm
        else:
            alarm_id = self.management_db.insert_alarm(alarm_description, alarm_name, kpi_id, kpi_min_value,
                                                        kpi_max_value,
                                                        in_range, include_min_value, include_max_value)
            LOGGER.debug(f"AlarmID: {alarm_id}")
        response.alarm_id.uuid = str(alarm_id)
        return response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetAlarms(self, request: Empty, grpc_context: grpc.ServicerContext) -> AlarmList:
        response = AlarmList()
        data = self.management_db.get_alarms()

        for alarm in data:
            alarm_descriptor = AlarmDescriptor()

            alarm_descriptor.alarm_id.alarm_id.uuid = str(alarm[0])
            alarm_descriptor.alarm_description = alarm[1]
            alarm_descriptor.name = alarm[2]
            alarm_descriptor.kpi_id.kpi_id.uuid = str(alarm[3])
            alarm_descriptor.kpi_value_range.kpiMinValue.floatVal = alarm[4]
            alarm_descriptor.kpi_value_range.kpiMaxValue.floatVal = alarm[5]
            alarm_descriptor.kpi_value_range.inRange = bool(alarm[6])
            alarm_descriptor.kpi_value_range.includeMinValue = bool(alarm[7])
            alarm_descriptor.kpi_value_range.includeMaxValue = bool(alarm[8])

            response.alarm_descriptor.append(alarm_descriptor)

        return response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetAlarmDescriptor(self, request: AlarmID, grpc_context: grpc.ServicerContext) -> AlarmDescriptor:
        alarm_id = request.alarm_id.uuid
        LOGGER.debug(alarm_id)
        alarm = self.management_db.get_alarm(alarm_id)
        response = AlarmDescriptor()

        if alarm:
            LOGGER.debug(f"{alarm}")
            response.alarm_id.alarm_id.uuid = str(alarm_id)
            response.alarm_description = alarm[1]
            response.name = alarm[2]
            response.kpi_id.kpi_id.uuid = str(alarm[3])
            response.kpi_value_range.kpiMinValue.floatVal = alarm[4]
            response.kpi_value_range.kpiMaxValue.floatVal = alarm[5]
            response.kpi_value_range.inRange = bool(alarm[6])
            response.kpi_value_range.includeMinValue = bool(alarm[7])
            response.kpi_value_range.includeMaxValue = bool(alarm[8])
        else:
            LOGGER.info('GetAlarmDescriptor error: AlarmID({:s}): not found in database'.format(str(alarm_id)))
            response.alarm_id.alarm_id.uuid = "NoID"
        return response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetAlarmResponseStream(
        self, request: AlarmSubscription, grpc_context: grpc.ServicerContext
    ) -> Iterator[AlarmResponse]:
        alarm_id = request.alarm_id.alarm_id.uuid
        alarm_data = self.management_db.get_alarm(alarm_id)
        real_start_time = timestamp_utcnow_to_float()

        if alarm_data:
            LOGGER.debug(f"{alarm_data}")
            alarm_queue = Queue()

            alarm_id = request.alarm_id.alarm_id.uuid
            kpi_id = alarm_data[3]
            kpiMinValue = alarm_data[4]
            kpiMaxValue = alarm_data[5]
            inRange = alarm_data[6]
            includeMinValue = alarm_data[7]
            includeMaxValue = alarm_data[8]
            subscription_frequency_ms = request.subscription_frequency_ms
            subscription_timeout_s = request.subscription_timeout_s

            end_timestamp = real_start_time + subscription_timeout_s

            self.alarm_manager.create_alarm(alarm_queue, alarm_id, kpi_id, kpiMinValue, kpiMaxValue, inRange,
                                            includeMinValue, includeMaxValue, subscription_frequency_ms,
                                            subscription_timeout_s)

            while True:
                while not alarm_queue.empty():
                    alarm_response = AlarmResponse()
                    list = alarm_queue.get_nowait()
                    size = len(list)
                    for item in list:
                        kpi = Kpi()
                        kpi.kpi_id.kpi_id.uuid = str(item[0])
                        kpi.timestamp.timestamp = timestamp_string_to_float(item[1])
                        kpi.kpi_value.floatVal = item[2]  # This must be improved
                        alarm_response.kpi_list.kpi.append(kpi)
                    alarm_response.alarm_id.alarm_id.uuid = alarm_id
                    yield alarm_response
                if timestamp_utcnow_to_float() > end_timestamp:
                    break
        else:
            LOGGER.info('GetAlarmResponseStream error: AlarmID({:s}): not found in database'.format(str(alarm_id)))
            alarm_response = AlarmResponse()
            alarm_response.alarm_id.alarm_id.uuid = "NoID"
            return alarm_response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteAlarm(self, request: AlarmID, grpc_context: grpc.ServicerContext) -> Empty:
        alarm_id = int(request.alarm_id.uuid)
        alarm = self.management_db.get_alarm(alarm_id)
        response = Empty()
        if alarm:
            self.alarm_manager.delete_alarm(alarm_id)
            self.management_db.delete_alarm(alarm_id)
        else:
            LOGGER.info('DeleteAlarm error: AlarmID({:s}): not found in database'.format(str(alarm_id)))
        return response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetStreamKpi(self, request: KpiId, grpc_context: grpc.ServicerContext) -> Iterator[Kpi]:
        kpi_id = request.kpi_id.uuid
        kpi_db = self.management_db.get_KPI(int(kpi_id))
        response = Kpi()
        if kpi_db is None:
            LOGGER.info('GetStreamKpi error: KpiID({:s}): not found in database'.format(str(kpi_id)))
            response.kpi_id.kpi_id.uuid = "NoID"
            return response
        else:
            yield response

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetInstantKpi(self, request: KpiId, grpc_context: grpc.ServicerContext) -> Kpi:
        kpi_id = request.kpi_id.uuid
        response = Kpi()
        if kpi_id == "":
            LOGGER.info('GetInstantKpi error: KpiID({:s}): not found in database'.format(str(kpi_id)))
            response.kpi_id.kpi_id.uuid = "NoID"
        else:
            query = f"SELECT kpi_id, timestamp, kpi_value FROM {METRICSDB_TABLE_MONITORING_KPIS} " \
                    f"WHERE kpi_id = '{kpi_id}' LATEST ON timestamp PARTITION BY kpi_id"
            data = self.metrics_db.run_query(query)
            LOGGER.debug(data)
            if len(data) == 0:
                response.kpi_id.kpi_id.uuid = request.kpi_id.uuid
            else:
                _data = data[0]
                response.kpi_id.kpi_id.uuid = str(_data[0])
                response.timestamp.timestamp = timestamp_string_to_float(_data[1])
                response.kpi_value.floatVal = _data[2]
        return response
