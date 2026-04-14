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

import grpc, itertools, json, logging, time
from typing import Any, Dict, Iterator, Optional, Tuple
from common.tests.MockMessageBroker import Message, MockMessageBroker
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.proto.context_pb2 import EVENTTYPE_CREATE, EVENTTYPE_REMOVE, EVENTTYPE_UPDATE, Empty, TeraFlowController
from common.proto.dlt_gateway_pb2 import (
    DLTRECORDOPERATION_ADD, DLTRECORDOPERATION_DELETE, DLTRECORDOPERATION_UNDEFINED, DLTRECORDOPERATION_UPDATE,
    DLTRECORDSTATUS_FAILED, DLTRECORDSTATUS_SUCCEEDED, DLTRECORDTYPE_CONTEXT, DLTRECORDTYPE_DEVICE, DLTRECORDTYPE_LINK,
    DLTRECORDTYPE_SERVICE, DLTRECORDTYPE_SLICE, DLTRECORDTYPE_TOPOLOGY, DLTRECORDTYPE_UNDEFINED,
    DltPeerStatus, DltPeerStatusList, DltRecord, DltRecordEvent, DltRecordId, DltRecordOperationEnum, DltRecordStatus,
    DltRecordSubscription, DltRecordTypeEnum)
from common.proto.dlt_gateway_pb2_grpc import DltGatewayServiceServicer

LOGGER = logging.getLogger(__name__)

DltRecordKey  = Tuple[str, Any, str]            # domain_uuid, DltRecordOperationEnum, record_uuid
DltRecordDict = Dict[DltRecordKey, DltRecord]   # dlt_record_key => dlt_record

class AlreadyExistsException(Exception):
    pass

class DoesNotExistException(Exception):
    pass

MSG_NOT_EXISTS = 'RecordId({:s}, {:s}, {:s}) Does Not Exist'
MSG_ALREADY_EXISTS = 'RecordId({:s}, {:s}, {:s}) Already Exists'
MSG_OPERATION_NOT_IMPLEMENTED = 'DltRecordOperationEnum({:s}) Not Implemented'

class MockServicerImpl_DltGateway(DltGatewayServiceServicer):
    def __init__(self):
        LOGGER.info('[__init__] Creating Servicer...')
        self.records : DltRecordDict = {}
        self.msg_broker = MockMessageBroker()
        LOGGER.info('[__init__] Servicer Created')

    def __get_record(self, record_id : DltRecordId) -> Optional[Dict]:
        domain_uuid, record_uuid = record_id.domain_uuid.uuid, record_id.record_uuid.uuid
        str_type = DltRecordTypeEnum.Name(record_id.type).upper().replace('DLTRECORDTYPE_', '')
        records_domain : Dict[str, Dict] = self.records.setdefault(domain_uuid, {})
        records_type   : Dict[str, Dict] = records_domain.setdefault(str_type, {})
        record         : Optional[Dict] = records_type.get(record_uuid)
        return record

    def __set_record(self, record_id : DltRecordId, should_exist : bool, data_json : str) -> None:
        domain_uuid, record_uuid = record_id.domain_uuid.uuid, record_id.record_uuid.uuid
        str_type = DltRecordTypeEnum.Name(record_id.type).upper().replace('DLTRECORDTYPE_', '')
        records_domain : Dict[str, Dict] = self.records.setdefault(domain_uuid, {})
        records_type   : Dict[str, Dict] = records_domain.setdefault(str_type, {})
        record         : Optional[Dict] = records_type.get(record_uuid)
        if should_exist and record is None:
            raise DoesNotExistException(MSG_NOT_EXISTS.format(domain_uuid, str_type, record_uuid))
        elif not should_exist and record is not None:
            raise AlreadyExistsException(MSG_ALREADY_EXISTS.format(domain_uuid, str_type, record_uuid))
        records_type[record_uuid] = data_json

    def __del_record(self, record_id : DltRecordId) -> None:
        domain_uuid, record_uuid = record_id.domain_uuid.uuid, record_id.record_uuid.uuid
        str_type = DltRecordTypeEnum.Name(record_id.type).upper().replace('DLTRECORDTYPE_', '')
        records_domain : Dict[str, Dict] = self.records.setdefault(domain_uuid, {})
        records_type   : Dict[str, Dict] = records_domain.setdefault(str_type, {})
        record         : Optional[Dict] = records_type.get(record_uuid)
        if record is None:
            raise DoesNotExistException(MSG_NOT_EXISTS.format(domain_uuid, str_type, record_uuid))
        records_type.discard(record_uuid)

    def __publish(self, operation : DltRecordOperationEnum, record_id : DltRecordId) -> None:
        str_operation = DltRecordOperationEnum.Name(operation).upper().replace('DLTRECORDOPERATION_', '')
        str_type = DltRecordTypeEnum.Name(record_id.type).upper().replace('DLTRECORDTYPE_', '')
        topic = '{:s}:{:s}'.format(str_type, str_operation)
        event = DltRecordEvent()
        event.event.timestamp.timestamp = time.time()       # pylint: disable=no-member
        event.event.event_type = {                          # pylint: disable=no-member
            DLTRECORDOPERATION_ADD   : EVENTTYPE_CREATE,
            DLTRECORDOPERATION_UPDATE: EVENTTYPE_UPDATE,
            DLTRECORDOPERATION_DELETE: EVENTTYPE_REMOVE,
        }.get(operation)
        event.record_id.CopyFrom(record_id)                 # pylint: disable=no-member
        self.msg_broker.publish(Message(topic=topic, content=grpc_message_to_json_string(event)))

    def RecordToDlt(self, request : DltRecord, context : grpc.ServicerContext) -> DltRecordStatus:
        LOGGER.info('[RecordToDlt] request={:s}'.format(grpc_message_to_json_string(request)))
        record_id = request.record_id
        response = DltRecordStatus()
        response.record_id.CopyFrom(record_id)              # pylint: disable=no-member
        try:
            operation : DltRecordOperationEnum = request.operation
            if operation == DLTRECORDOPERATION_ADD:
                self.__set_record(record_id, False, json.loads(request.data_json))
            elif operation == DLTRECORDOPERATION_UPDATE:
                self.__set_record(record_id, True, json.loads(request.data_json))
            elif operation == DLTRECORDOPERATION_DELETE:
                self.__del_record(record_id)
            else:
                str_operation = DltRecordOperationEnum.Name(operation).upper().replace('DLTRECORDOPERATION_', '')
                raise NotImplementedError(MSG_OPERATION_NOT_IMPLEMENTED.format(str_operation))
            self.__publish(operation, record_id)
            response.status = DLTRECORDSTATUS_SUCCEEDED
        except Exception as e: # pylint: disable=broad-except
            response.status = DLTRECORDSTATUS_FAILED
            response.error_message = str(e)
        LOGGER.info('[RecordToDlt] response={:s}'.format(grpc_message_to_json_string(response)))
        return response

    def GetFromDlt(self, request : DltRecordId, context : grpc.ServicerContext) -> DltRecord:
        LOGGER.info('[GetFromDlt] request={:s}'.format(grpc_message_to_json_string(request)))
        record = self.__get_record(request)
        response = DltRecord()
        if record is not None:
            response.record_id.CopyFrom(request) # pylint: disable=no-member
            response.operation = DLTRECORDOPERATION_UNDEFINED
            response.data_json = json.dumps(record, sort_keys=True)
        LOGGER.info('[GetFromDlt] response={:s}'.format(grpc_message_to_json_string(response)))
        return response

    def SubscribeToDlt(
        self, request: DltRecordSubscription, context : grpc.ServicerContext
    ) -> Iterator[DltRecordEvent]:
        LOGGER.info('[SubscribeToDlt] request={:s}'.format(grpc_message_to_json_string(request)))
        types = request.type
        if len(types) == 0:
            types = [
                DLTRECORDTYPE_UNDEFINED, DLTRECORDTYPE_CONTEXT, DLTRECORDTYPE_TOPOLOGY, DLTRECORDTYPE_DEVICE,
                DLTRECORDTYPE_LINK, DLTRECORDTYPE_SERVICE, DLTRECORDTYPE_SLICE
            ]
        str_types = [
            DltRecordTypeEnum.Name(_type).upper().replace('DLTRECORDTYPE_', '')
            for _type in types
        ]
        operations = request.operation
        if len(operations) == 0:
            operations = [
                DLTRECORDOPERATION_UNDEFINED, DLTRECORDOPERATION_ADD, DLTRECORDOPERATION_UPDATE,
                DLTRECORDOPERATION_DELETE
            ]
        str_operations = [
            DltRecordOperationEnum.Name(_operation).upper().replace('DLTRECORDOPERATION_', '')
            for _operation in operations
        ]
        topics = {
            '{:s}:{:s}'.format(*type_operation)
            for type_operation in itertools.product(str_types, str_operations)
        }
        for message in self.msg_broker.consume(topics):
            yield DltRecordEvent(**json.loads(message.content))

    def GetDltStatus(self, request : TeraFlowController, context : grpc.ServicerContext) -> DltPeerStatus:
        LOGGER.info('[GetDltStatus] request={:s}'.format(grpc_message_to_json_string(request)))
        raise NotImplementedError()

    def GetDltPeers(self, request : Empty, context : grpc.ServicerContext) -> DltPeerStatusList:
        LOGGER.info('[GetDltPeers] request={:s}'.format(grpc_message_to_json_string(request)))
        raise NotImplementedError()
