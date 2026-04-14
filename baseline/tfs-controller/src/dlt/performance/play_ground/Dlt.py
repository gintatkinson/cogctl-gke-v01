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

import json, time
from typing import Dict, Union
from common.proto.context_pb2 import Device, Link, Service, Slice
from common.proto.dlt_gateway_pb2 import (
    DltRecord, DltRecordId, DltRecordOperationEnum, DltRecordStatus, DltRecordTypeEnum)
from common.tools.grpc.Tools import grpc_message_to_json_string
from dlt.connector.client.DltGatewayClient import DltGatewayClient
from .PerfPoint import PerfPoint

DLT_OPERATION_CREATE = DltRecordOperationEnum.DLTRECORDOPERATION_ADD
DLT_OPERATION_UPDATE = DltRecordOperationEnum.DLTRECORDOPERATION_UPDATE
DLT_OPERATION_DELETE = DltRecordOperationEnum.DLTRECORDOPERATION_DELETE

DLT_RECORD_TYPE_DEVICE  = DltRecordTypeEnum.DLTRECORDTYPE_DEVICE
DLT_RECORD_TYPE_LINK    = DltRecordTypeEnum.DLTRECORDTYPE_LINK
DLT_RECORD_TYPE_SERVICE = DltRecordTypeEnum.DLTRECORDTYPE_SERVICE
DLT_RECORD_TYPE_SLICE   = DltRecordTypeEnum.DLTRECORDTYPE_SLICE

def dlt_record_set(
    dltgateway_client : DltGatewayClient, perf_point : PerfPoint,
    operation : DltRecordOperationEnum, domain_uuid : str, objekt : Union[Device, Link, Service, Slice]
) -> DltRecordStatus:
    if isinstance(objekt, Device):
        record_type = DLT_RECORD_TYPE_DEVICE
        record_uuid = objekt.device_id.device_uuid.uuid
    elif isinstance(objekt, Link):
        record_type = DLT_RECORD_TYPE_LINK
        record_uuid = objekt.link_id.link_uuid.uuid
    elif isinstance(objekt, Service):
        record_type = DLT_RECORD_TYPE_SERVICE
        record_uuid = objekt.service_id.service_uuid.uuid
    elif isinstance(objekt, Slice):
        record_type = DLT_RECORD_TYPE_SLICE
        record_uuid = objekt.slice_id.slice_uuid.uuid
    else:
        raise NotImplementedError('Object({:s}) not supported'.format(str(type(objekt))))

    dlt_req = DltRecord()
    dlt_req.record_id.domain_uuid.uuid = domain_uuid    # pylint: disable=no-member
    dlt_req.record_id.type             = record_type    # pylint: disable=no-member
    dlt_req.record_id.record_uuid.uuid = record_uuid    # pylint: disable=no-member
    dlt_req.operation                  = operation
    dlt_req.data_json                  = grpc_message_to_json_string(objekt)

    perf_point.set_time_requested(time.time())
    reply = dltgateway_client.RecordToDlt(dlt_req)
    perf_point.set_time_replied(time.time())

    perf_point.set_size_bytes(len(dlt_req.data_json))   # pylint: disable=no-member
    if isinstance(objekt, Device):
        perf_point.set_num_config_rules(len(objekt.device_config.config_rules))
        perf_point.set_num_endpoints(len(objekt.device_endpoints))
    elif isinstance(objekt, Link):
        perf_point.set_num_endpoints(len(objekt.link_endpoint_ids))
    elif isinstance(objekt, Service):
        perf_point.set_num_config_rules(len(objekt.service_config.config_rules))
        perf_point.set_num_constraints(len(objekt.service_constraints))
        perf_point.set_num_endpoints(len(objekt.service_endpoint_ids))
    elif isinstance(objekt, Slice):
        perf_point.set_num_config_rules(len(objekt.slice_config.config_rules))
        perf_point.set_num_constraints(len(objekt.slice_constraints))
        perf_point.set_num_endpoints(len(objekt.slice_endpoint_ids))
        perf_point.set_num_sub_services(len(objekt.slice_service_ids))
        perf_point.set_num_sub_slices(len(objekt.slice_subslice_ids))
    else:
        raise NotImplementedError('Object({:s}) not supported'.format(str(type(objekt))))

    return reply

def dlt_record_found(record : DltRecord) -> bool:
    return all([
        len(record.record_id.domain_uuid.uuid) > 0,
        record.record_id.type != DltRecordTypeEnum.DLTRECORDTYPE_UNDEFINED,
        len(record.record_id.record_uuid.uuid) > 0,
        #record.operation != DltRecordOperationEnum.DLTRECORDOPERATION_UNDEFINED,
        len(record.data_json) > 0,
    ])

def dlt_record_get(
    dltgateway_client : DltGatewayClient, perf_point : PerfPoint,
    domain_uuid : str, record_type : DltRecordTypeEnum, record_uuid : str
) -> Dict:
    dlt_rec_id = DltRecordId()
    dlt_rec_id.domain_uuid.uuid = domain_uuid   # pylint: disable=no-member
    dlt_rec_id.type             = record_type
    dlt_rec_id.record_uuid.uuid = record_uuid   # pylint: disable=no-member

    perf_point.set_time_requested(time.time())
    dlt_rep = dltgateway_client.GetFromDlt(dlt_rec_id)
    perf_point.set_time_replied(time.time())

    if not dlt_record_found(dlt_rep):
        MSG = 'DltRecord({:s}/{:s}/{:s}) not found'
        str_record_type = DltRecordTypeEnum.Name(record_type)
        msg = MSG.format(str(domain_uuid), str_record_type, str(record_uuid))
        raise Exception(msg) # pylint: disable=broad-exception-raised

    data : Dict = json.loads(dlt_rep.data_json)

    perf_point.set_size_bytes(len(dlt_rep.data_json))
    if 'device_id' in data:
        perf_point.set_num_config_rules(len(data.get('device_config', {}).get('config_rules')))
        perf_point.set_num_endpoints(len(data.get('device_endpoints', [])))
    elif 'link_id' in data:
        perf_point.set_num_endpoints(len(data.get('link_endpoint_ids', [])))
    elif 'service_id' in data:
        perf_point.set_num_config_rules(len(data.get('service_config', []).get('config_rules')))
        perf_point.set_num_constraints(len(data.get('service_constraints', [])))
        perf_point.set_num_endpoints(len(data.get('service_endpoint_ids', [])))
    elif 'slice_id' in data:
        perf_point.set_num_config_rules(len(data.get('slice_config', []).get('config_rules')))
        perf_point.set_num_constraints(len(data.get('slice_constraints', [])))
        perf_point.set_num_endpoints(len(data.get('slice_endpoint_ids', [])))
        perf_point.set_num_sub_services(len(data.get('slice_service_ids', [])))
        perf_point.set_num_sub_slices(len(data.get('slice_subslice_ids', [])))
    else:
        raise NotImplementedError('Object({:s}) not supported'.format(str(data)))

    return data
