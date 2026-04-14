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
from random import random

from common.proto import monitoring_pb2
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.timestamp.Converters import timestamp_utcnow_to_float

def kpi_id():
    _kpi_id             = monitoring_pb2.KpiId()
    _kpi_id.kpi_id.uuid = str(1)            # pylint: disable=maybe-no-member
    return _kpi_id

def create_kpi_request(kpi_id_str):
    _create_kpi_request                                     = monitoring_pb2.KpiDescriptor()
    _create_kpi_request.kpi_description                     = 'KPI Description Test'
    _create_kpi_request.kpi_sample_type                     = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.device_id.device_uuid.uuid          = 'DEV' + str(kpi_id_str)
    _create_kpi_request.service_id.service_uuid.uuid        = 'SERV' + str(kpi_id_str)
    _create_kpi_request.slice_id.slice_uuid.uuid            = 'SLC' + str(kpi_id_str)
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid      = 'END' + str(kpi_id_str)
    _create_kpi_request.connection_id.connection_uuid.uuid  = 'CON' + str(kpi_id_str)
    return _create_kpi_request

def create_kpi_request_b():
    _create_kpi_request                                = monitoring_pb2.KpiDescriptor()
    _create_kpi_request.kpi_description                = 'KPI Description Test'
    _create_kpi_request.kpi_sample_type                = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.device_id.device_uuid.uuid     = 'DEV2'     # pylint: disable=maybe-no-member
    _create_kpi_request.service_id.service_uuid.uuid   = 'SERV2'    # pylint: disable=maybe-no-member
    _create_kpi_request.slice_id.slice_uuid.uuid       = 'SLC2'  # pylint: disable=maybe-no-member
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid = 'END2'     # pylint: disable=maybe-no-member
    _create_kpi_request.connection_id.connection_uuid.uuid = 'CON2'  # pylint: disable=maybe-no-member
    return _create_kpi_request

def create_kpi_request_c():
    _create_kpi_request                                = monitoring_pb2.KpiDescriptor()
    _create_kpi_request.kpi_description                = 'KPI Description Test'
    _create_kpi_request.kpi_sample_type                = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.device_id.device_uuid.uuid     = 'DEV3'     # pylint: disable=maybe-no-member
    _create_kpi_request.service_id.service_uuid.uuid   = 'SERV3'    # pylint: disable=maybe-no-member
    _create_kpi_request.slice_id.slice_uuid.uuid       = 'SLC3'  # pylint: disable=maybe-no-member
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid = 'END3'     # pylint: disable=maybe-no-member
    _create_kpi_request.connection_id.connection_uuid.uuid = 'CON3'  # pylint: disable=maybe-no-member
    return _create_kpi_request

def create_kpi_request_d():
    _create_kpi_request                                = monitoring_pb2.KpiDescriptor()
    _create_kpi_request.kpi_description                = 'KPI Description Test'
    _create_kpi_request.kpi_sample_type                = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.device_id.device_uuid.uuid     = 'DEV4'     # pylint: disable=maybe-no-member
    _create_kpi_request.service_id.service_uuid.uuid   = 'SERV4'    # pylint: disable=maybe-no-member
    _create_kpi_request.slice_id.slice_uuid.uuid       = 'SLC4'  # pylint: disable=maybe-no-member
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid = 'END4'     # pylint: disable=maybe-no-member
    _create_kpi_request.connection_id.connection_uuid.uuid = 'CON4'  # pylint: disable=maybe-no-member
    return _create_kpi_request

def monitor_kpi_request(kpi_uuid, monitoring_window_s, sampling_rate_s):
    _monitor_kpi_request                     = monitoring_pb2.MonitorKpiRequest()
    _monitor_kpi_request.kpi_id.kpi_id.uuid  = kpi_uuid   # pylint: disable=maybe-no-member
    _monitor_kpi_request.monitoring_window_s = monitoring_window_s
    _monitor_kpi_request.sampling_rate_s     = sampling_rate_s
    return _monitor_kpi_request

def include_kpi_request(kpi_id):
    _include_kpi_request                        = monitoring_pb2.Kpi()
    _include_kpi_request.kpi_id.kpi_id.uuid     = kpi_id.kpi_id.uuid
    _include_kpi_request.timestamp.timestamp    = timestamp_utcnow_to_float()
    _include_kpi_request.kpi_value.floatVal     = 500*random()       # pylint: disable=maybe-no-member
    return _include_kpi_request

def kpi_descriptor_list():
    _kpi_descriptor_list = monitoring_pb2.KpiDescriptorList()

    return _kpi_descriptor_list

def kpi_query(kpi_id_list):
    _kpi_query = monitoring_pb2.KpiQuery()

    _kpi_query.kpi_ids.extend(kpi_id_list)
    # _kpi_query.monitoring_window_s          = 10
    # _kpi_query.last_n_samples               = 2
    _kpi_query.start_timestamp.timestamp    = timestamp_utcnow_to_float() - 10
    _kpi_query.end_timestamp.timestamp      = timestamp_utcnow_to_float()

    return _kpi_query

def subs_descriptor(kpi_id):
    _subs_descriptor = monitoring_pb2.SubsDescriptor()

    sampling_duration_s = 10
    sampling_interval_s = 3
    real_start_time     = timestamp_utcnow_to_float()
    start_timestamp     = real_start_time
    end_timestamp       = start_timestamp + sampling_duration_s

    _subs_descriptor.subs_id.subs_id.uuid       = ""
    _subs_descriptor.kpi_id.kpi_id.uuid         = kpi_id.kpi_id.uuid
    _subs_descriptor.sampling_duration_s        = sampling_duration_s
    _subs_descriptor.sampling_interval_s        = sampling_interval_s
    _subs_descriptor.start_timestamp.timestamp  = start_timestamp
    _subs_descriptor.end_timestamp.timestamp    = end_timestamp

    return _subs_descriptor

def subs_id():
    _subs_id = monitoring_pb2.SubsDescriptor()

    return _subs_id

def alarm_descriptor(kpi_id):
    _alarm_descriptor = monitoring_pb2.AlarmDescriptor()

    _alarm_descriptor.alarm_description                     = "Alarm Description"
    _alarm_descriptor.name                                  = "Alarm Name"
    _alarm_descriptor.kpi_id.kpi_id.uuid                    = kpi_id.kpi_id.uuid
    _alarm_descriptor.kpi_value_range.kpiMinValue.floatVal  = 0.0
    _alarm_descriptor.kpi_value_range.kpiMaxValue.floatVal  = 250.0
    _alarm_descriptor.kpi_value_range.inRange               = True
    _alarm_descriptor.kpi_value_range.includeMinValue       = False
    _alarm_descriptor.kpi_value_range.includeMaxValue       = True

    return _alarm_descriptor

def alarm_descriptor_b():
    _alarm_descriptor = monitoring_pb2.AlarmDescriptor()

    _alarm_descriptor.kpi_id.kpi_id.uuid = "2"

    return _alarm_descriptor

def alarm_subscription(alarm_id):
    _alarm_subscription = monitoring_pb2.AlarmSubscription()

    subscription_timeout_s = 10
    subscription_frequency_ms = 1000

    _alarm_subscription.alarm_id.alarm_id.uuid      = str(alarm_id.alarm_id.uuid)
    _alarm_subscription.subscription_timeout_s      = subscription_timeout_s
    _alarm_subscription.subscription_frequency_ms   = subscription_frequency_ms

    return _alarm_subscription


def alarm_id():
    _alarm_id = monitoring_pb2.AlarmID()

    return _alarm_id