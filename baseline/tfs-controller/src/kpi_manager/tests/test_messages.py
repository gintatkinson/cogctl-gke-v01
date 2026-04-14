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

import uuid
from common.proto import kpi_manager_pb2
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.context_pb2 import DeviceId, LinkId, ServiceId, SliceId,\
                             ConnectionId, EndPointId


def create_kpi_id_request():
    _create_kpi_id = kpi_manager_pb2.KpiId()
    _create_kpi_id.kpi_id.uuid = str(uuid.uuid4())
    return _create_kpi_id

def create_kpi_descriptor_request(descriptor_name: str = "Test_name"):
    _create_kpi_request                                    = kpi_manager_pb2.KpiDescriptor()
    _create_kpi_request.kpi_id.kpi_id.uuid                 = str(uuid.uuid4())
    # _create_kpi_request.kpi_id.kpi_id.uuid                 = "6e22f180-ba28-4641-b190-2287bf448888"
    # _create_kpi_request.kpi_id.kpi_id.uuid                 = "f974b6cc-095f-4767-b8c1-3457b383fb99"
    _create_kpi_request.kpi_description                    = descriptor_name
    _create_kpi_request.kpi_sample_type                    = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.device_id.device_uuid.uuid         = str(uuid.uuid4())
    _create_kpi_request.service_id.service_uuid.uuid       = 'SERV2'
    _create_kpi_request.slice_id.slice_uuid.uuid           = 'SLC1'
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid     = str(uuid.uuid4())
    _create_kpi_request.connection_id.connection_uuid.uuid = 'CON1' 
    _create_kpi_request.link_id.link_uuid.uuid             = 'LNK1' 
    return _create_kpi_request

def create_kpi_descriptor_request_a(description: str = "Test Description"):
    _create_kpi_request                                    = kpi_manager_pb2.KpiDescriptor()
    _create_kpi_request.kpi_id.kpi_id.uuid                 = str(uuid.uuid4())
    _create_kpi_request.kpi_description                    = description
    _create_kpi_request.kpi_sample_type                    = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.device_id.device_uuid.uuid         = 'DEV4' 
    _create_kpi_request.service_id.service_uuid.uuid       = 'SERV3'
    _create_kpi_request.slice_id.slice_uuid.uuid           = 'SLC3' 
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid     = 'END2' 
    _create_kpi_request.connection_id.connection_uuid.uuid = 'CON2' 
    _create_kpi_request.link_id.link_uuid.uuid             = 'LNK2' 
    return _create_kpi_request

def create_kpi_filter_request():
    _create_kpi_filter_request = kpi_manager_pb2.KpiDescriptorFilter()
    _create_kpi_filter_request.kpi_sample_type.append(KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED)

    device_id_obj     = DeviceId()
    service_id_obj    = ServiceId()
    slice_id_obj      = SliceId()
    endpoint_id_obj   = EndPointId()
    connection_id_obj = ConnectionId()
    link_id_obj       = LinkId()

    device_id_obj.device_uuid.uuid         = "DEV2"
    service_id_obj.service_uuid.uuid       = "SERV2"
    slice_id_obj.slice_uuid.uuid           = "SLC1"
    endpoint_id_obj.endpoint_uuid.uuid     = "END1"
    connection_id_obj.connection_uuid.uuid = "CON1"
    link_id_obj.link_uuid.uuid             = "LNK1"

    _create_kpi_filter_request.device_id.append(device_id_obj)
    _create_kpi_filter_request.service_id.append(service_id_obj)
    _create_kpi_filter_request.slice_id.append(slice_id_obj)
    _create_kpi_filter_request.endpoint_id.append(endpoint_id_obj)
    _create_kpi_filter_request.connection_id.append(connection_id_obj)
    _create_kpi_filter_request.link_id.append(link_id_obj)

    return _create_kpi_filter_request
