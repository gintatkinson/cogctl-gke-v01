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

import datetime, json, logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, selectinload, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from typing import Dict, List, Optional, Set
from common.proto.context_pb2 import Empty, EventTypeEnum
from common.proto.policy_pb2 import PolicyRule, PolicyRuleId, PolicyRuleIdList, PolicyRuleList
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.PolicyRule import json_policyrule_id
from context.service.database.uuids.Device import device_get_uuid
from .models.enums.PolicyRuleState import grpc_to_enum__policyrule_state
from .models.PolicyRuleModel import PolicyRuleDeviceModel, PolicyRuleKindEnum, PolicyRuleModel
from .uuids.PolicuRule import policyrule_get_uuid
from .uuids.Service import service_get_uuid
from .Events import notify_event_policy_rule

LOGGER = logging.getLogger(__name__)

def policyrule_list_ids(db_engine : Engine) -> PolicyRuleIdList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[PolicyRuleModel] = session.query(PolicyRuleModel).all()
        return [obj.dump_id() for obj in obj_list]
    policy_rule_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    return PolicyRuleIdList(policyRuleIdList=policy_rule_ids)

def policyrule_list_objs(db_engine : Engine) -> PolicyRuleList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[PolicyRuleModel] = session.query(PolicyRuleModel)\
            .options(selectinload(PolicyRuleModel.policyrule_service))\
            .options(selectinload(PolicyRuleModel.policyrule_devices))\
            .all()
        return [obj.dump() for obj in obj_list]
    policy_rules = run_transaction(sessionmaker(bind=db_engine), callback)
    return PolicyRuleList(policyRules=policy_rules)

def policyrule_get(db_engine : Engine, request : PolicyRuleId) -> PolicyRule:
    policyrule_uuid = policyrule_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[PolicyRuleModel] = session.query(PolicyRuleModel)\
            .options(selectinload(PolicyRuleModel.policyrule_service))\
            .options(selectinload(PolicyRuleModel.policyrule_devices))\
            .filter_by(policyrule_uuid=policyrule_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        raw_policyrule_uuid = request.uuid.uuid
        raise NotFoundException('PolicyRule', raw_policyrule_uuid, extra_details=[
            'policyrule_uuid generated was: {:s}'.format(policyrule_uuid)
        ])
    return PolicyRule(**obj)

def policyrule_set(db_engine : Engine, messagebroker : MessageBroker, request : PolicyRule) -> PolicyRuleId:
    policyrule_kind = request.WhichOneof('policy_rule')
    policyrule_spec = getattr(request, policyrule_kind)
    policyrule_basic = policyrule_spec.policyRuleBasic
    policyrule_id = policyrule_basic.policyRuleId
    policyrule_uuid = policyrule_get_uuid(policyrule_id, allow_random=False)

    policyrule_kind  = PolicyRuleKindEnum._member_map_.get(policyrule_kind.upper()) # pylint: disable=no-member
    policyrule_state = grpc_to_enum__policyrule_state(policyrule_basic.policyRuleState.policyRuleState)
    policyrule_state_msg = policyrule_basic.policyRuleState.policyRuleStateMessage

    json_policyrule_basic = grpc_message_to_json(policyrule_basic)
    policyrule_eca_data = json.dumps({
        'actionList': json_policyrule_basic.get('actionList', []),
    }, sort_keys=True)

    now = datetime.datetime.now(datetime.timezone.utc)

    policyrule_data = [{
        'policyrule_uuid'     : policyrule_uuid,
        'policyrule_kind'     : policyrule_kind,
        'policyrule_state'    : policyrule_state,
        'policyrule_state_msg': policyrule_state_msg,
        'policyrule_priority' : policyrule_basic.priority,
        'policyrule_kpi_id'   : policyrule_basic.kpiId.kpi_id.uuid,
        'policyrule_eca_data' : policyrule_eca_data,
        'created_at'          : now,
        'updated_at'          : now,
    }]

    policyrule_service_uuid = None
    if policyrule_kind == PolicyRuleKindEnum.SERVICE:
        _,policyrule_service_uuid = service_get_uuid(policyrule_spec.serviceId, allow_random=False)
        policyrule_data[0]['policyrule_service_uuid'] = policyrule_service_uuid

    device_uuids : Set[str] = set()
    related_devices : List[Dict] = list()
    for device_id in policyrule_spec.deviceList:
        device_uuid = device_get_uuid(device_id, allow_random=False)
        if device_uuid in device_uuids: continue
        related_devices.append({
            'policyrule_uuid': policyrule_uuid,
            'device_uuid'    : device_uuid,
        })
        device_uuids.add(device_uuid)

    def callback(session : Session) -> bool:
        stmt = insert(PolicyRuleModel).values(policyrule_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[PolicyRuleModel.policyrule_uuid],
            set_=dict(
                policyrule_state     = stmt.excluded.policyrule_state,
                policyrule_state_msg = stmt.excluded.policyrule_state_msg,
                policyrule_priority  = stmt.excluded.policyrule_priority,
                policyrule_kpi_id    = stmt.excluded.policyrule_kpi_id,
                policyrule_eca_data  = stmt.excluded.policyrule_eca_data,
                updated_at           = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(PolicyRuleModel.created_at, PolicyRuleModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()
        updated = updated_at > created_at

        if len(related_devices) > 0:
            session.execute(insert(PolicyRuleDeviceModel).values(related_devices).on_conflict_do_nothing(
                index_elements=[PolicyRuleDeviceModel.policyrule_uuid, PolicyRuleDeviceModel.device_uuid]
            ))

        return updated

    updated = run_transaction(sessionmaker(bind=db_engine), callback)
    policyrule_id = json_policyrule_id(policyrule_uuid)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    notify_event_policy_rule(messagebroker, event_type, policyrule_id)
    return PolicyRuleId(**policyrule_id)

def policyrule_delete(db_engine : Engine, messagebroker : MessageBroker, request : PolicyRuleId) -> Empty:
    policyrule_uuid = policyrule_get_uuid(request, allow_random=False)
    def callback(session : Session) -> bool:
        num_deleted = session.query(PolicyRuleModel).filter_by(policyrule_uuid=policyrule_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    policyrule_id = json_policyrule_id(policyrule_uuid)
    if deleted:
        notify_event_policy_rule(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, policyrule_id)
    return Empty()
