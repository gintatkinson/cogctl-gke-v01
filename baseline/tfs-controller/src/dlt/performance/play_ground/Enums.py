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

import enum
from common.proto.context_pb2 import EventTypeEnum
from common.proto.dlt_gateway_pb2 import DltRecordTypeEnum

class ActionEnum(enum.Enum):
    CREATE = 'create'
    GET    = 'get'
    UPDATE = 'update'
    DELETE = 'delete'

class RecordTypeEnum(enum.Enum):
    DEVICE  = 'device'
    LINK    = 'link'
    SERVICE = 'service'
    SLICE   = 'slice'

CONTEXT_EVENT_TYPE_TO_ACTION = {
    EventTypeEnum.EVENTTYPE_CREATE : ActionEnum.CREATE,
    EventTypeEnum.EVENTTYPE_UPDATE : ActionEnum.UPDATE,
    EventTypeEnum.EVENTTYPE_REMOVE : ActionEnum.DELETE,
}

RECORD_TYPE_TO_ENUM = {
    DltRecordTypeEnum.DLTRECORDTYPE_DEVICE  : RecordTypeEnum.DEVICE,
    DltRecordTypeEnum.DLTRECORDTYPE_LINK    : RecordTypeEnum.LINK,
    DltRecordTypeEnum.DLTRECORDTYPE_SERVICE : RecordTypeEnum.SERVICE,
    DltRecordTypeEnum.DLTRECORDTYPE_SLICE   : RecordTypeEnum.SLICE,
}
