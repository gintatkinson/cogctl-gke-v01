# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pip install grpcio==1.47.0 grpcio-tools==1.47.0 protobuf==3.20.1
# PYTHONPATH=./src python
# PYTHONPATH=/home/cttc/teraflow/src python -m dlt.connector.tests.basic

import logging, sys, time
from common.proto.context_pb2 import DEVICEOPERATIONALSTATUS_ENABLED, Device
from common.proto.dlt_gateway_pb2 import (
    DLTRECORDOPERATION_ADD, DLTRECORDOPERATION_UNDEFINED, DLTRECORDOPERATION_UPDATE, DLTRECORDTYPE_DEVICE,
    DLTRECORDTYPE_UNDEFINED, DltRecord, DltRecordId)
from common.tools.object_factory.Device import json_device
from common.tools.grpc.Tools import grpc_message_to_json_string
from ..client.DltGatewayClient import DltGatewayClient
from ..client.DltEventsCollector import DltEventsCollector

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DLT_GATEWAY_HOST = '127.0.0.1'
DLT_GATEWAY_PORT = 30551 #50051

def record_found(record : DltRecord) -> bool:
    found = True
    found = found and (len(record.record_id.domain_uuid.uuid) > 0)
    found = found and (record.record_id.type != DLTRECORDTYPE_UNDEFINED)
    found = found and (len(record.record_id.record_uuid.uuid) > 0)
    #found = found and (record.operation != DLTRECORDOPERATION_UNDEFINED)
    found = found and (len(record.data_json) > 0)
    return found

def main():
    dltgateway_client = DltGatewayClient(host=DLT_GATEWAY_HOST, port=DLT_GATEWAY_PORT)
    dltgateway_collector = DltEventsCollector(dltgateway_client, log_events_received=True)
    dltgateway_collector.start()

    time.sleep(3)

    # Check record exists
    dri = DltRecordId()
    dri.domain_uuid.uuid = 'non-existing-domain'
    dri.record_uuid.uuid = 'non-existing-record'
    dri.type = DLTRECORDTYPE_DEVICE
    reply = dltgateway_client.GetFromDlt(dri)
    assert not record_found(reply), 'Record should not exist'

    device = Device(**json_device('dev-1', 'packet-router', DEVICEOPERATIONALSTATUS_ENABLED))

    r2dlt_req = DltRecord()
    r2dlt_req.record_id.domain_uuid.uuid = 'tfs-a'
    r2dlt_req.record_id.type             = DLTRECORDTYPE_DEVICE
    r2dlt_req.record_id.record_uuid.uuid = device.device_id.device_uuid.uuid
    r2dlt_req.operation                  = DLTRECORDOPERATION_ADD
    r2dlt_req.data_json                  = grpc_message_to_json_string(device)
    LOGGER.info('r2dlt_req = {:s}'.format(grpc_message_to_json_string(r2dlt_req)))
    r2dlt_rep = dltgateway_client.RecordToDlt(r2dlt_req)
    LOGGER.info('r2dlt_rep = {:s}'.format(grpc_message_to_json_string(r2dlt_rep)))

    dlt2r_req = r2dlt_req.record_id
    LOGGER.info('dlt2r_req = {:s}'.format(grpc_message_to_json_string(dlt2r_req)))
    dlt2r_rep = dltgateway_client.GetFromDlt(dlt2r_req)
    LOGGER.info('dlt2r_rep = {:s}'.format(grpc_message_to_json_string(dlt2r_rep)))

    dltgateway_collector.stop()
    return 0

if __name__ == '__main__':
    sys.exit(main())
