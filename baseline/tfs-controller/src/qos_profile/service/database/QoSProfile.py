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

import logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from typing import List, Optional

from common.proto.context_pb2 import Empty, Uuid, QoSProfileId
from common.proto.qos_profile_pb2 import QoSProfileValueUnitPair, QoSProfile
from common.tools.grpc.Tools import grpc_message_to_json
from .models.QoSProfile import QoSProfileModel

LOGGER = logging.getLogger(__name__)

def grpc_message_to_qos_table_data(message: QoSProfile) -> dict:
    return {
    'qos_profile_id'            : message.qos_profile_id.qos_profile_id.uuid,
    'name'                      : message.name,
    'description'               : message.description,
    'status'                    : message.status,
    'targetMinUpstreamRate'     : grpc_message_to_json(message.targetMinUpstreamRate),
    'maxUpstreamRate'           : grpc_message_to_json(message.maxUpstreamRate),
    'maxUpstreamBurstRate'      : grpc_message_to_json(message.maxUpstreamBurstRate),
    'targetMinDownstreamRate'   : grpc_message_to_json(message.targetMinDownstreamRate),
    'maxDownstreamRate'         : grpc_message_to_json(message.maxDownstreamRate),
    'maxDownstreamBurstRate'    : grpc_message_to_json(message.maxDownstreamBurstRate),
    'minDuration'               : grpc_message_to_json(message.minDuration),
    'maxDuration'               : grpc_message_to_json(message.maxDuration),
    'priority'                  : message.priority,
    'packetDelayBudget'         : grpc_message_to_json(message.packetDelayBudget),
    'jitter'                    : grpc_message_to_json(message.jitter),
    'packetErrorLossRate'       : message.packetErrorLossRate,
    }

def qos_table_data_to_grpc_message(data: QoSProfileModel) -> QoSProfile:
    return QoSProfile(
    qos_profile_id            = QoSProfileId(qos_profile_id=Uuid(uuid=data.qos_profile_id)),
    name                      = data.name,
    description               = data.description,
    status                    = data.status,
    targetMinUpstreamRate     = QoSProfileValueUnitPair(**data.targetMinUpstreamRate),
    maxUpstreamRate           = QoSProfileValueUnitPair(**data.maxUpstreamRate),
    maxUpstreamBurstRate      = QoSProfileValueUnitPair(**data.maxUpstreamBurstRate),
    targetMinDownstreamRate   = QoSProfileValueUnitPair(**data.targetMinDownstreamRate),
    maxDownstreamRate         = QoSProfileValueUnitPair(**data.maxDownstreamRate),
    maxDownstreamBurstRate    = QoSProfileValueUnitPair(**data.maxDownstreamBurstRate),
    minDuration               = QoSProfileValueUnitPair(**data.minDuration),
    maxDuration               = QoSProfileValueUnitPair(**data.maxDuration),
    priority                  = data.priority,
    packetDelayBudget         = QoSProfileValueUnitPair(**data.packetDelayBudget),
    jitter                    = QoSProfileValueUnitPair(**data.jitter),
    packetErrorLossRate       = data.packetErrorLossRate
    )

def set_qos_profile(db_engine : Engine, request : QoSProfile) -> QoSProfile:
    qos_profile_data = grpc_message_to_qos_table_data(request)
    def callback(session : Session) -> bool:
        stmt = insert(QoSProfileModel).values([qos_profile_data])
        stmt = stmt.on_conflict_do_update(index_elements=[QoSProfileModel.qos_profile_id],
            set_=dict(

                    name                      = stmt.excluded.name,
                    description               = stmt.excluded.description,
                    status                    = stmt.excluded.status,
                    targetMinUpstreamRate     = stmt.excluded.targetMinUpstreamRate,
                    maxUpstreamRate           = stmt.excluded.maxUpstreamRate,
                    maxUpstreamBurstRate      = stmt.excluded.maxUpstreamBurstRate,
                    targetMinDownstreamRate   = stmt.excluded.targetMinDownstreamRate,
                    maxDownstreamRate         = stmt.excluded.maxDownstreamRate,
                    maxDownstreamBurstRate    = stmt.excluded.maxDownstreamBurstRate,
                    minDuration               = stmt.excluded.minDuration,
                    maxDuration               = stmt.excluded.maxDuration,
                    priority                  = stmt.excluded.priority,
                    packetDelayBudget         = stmt.excluded.packetDelayBudget,
                    jitter                    = stmt.excluded.jitter,
                    packetErrorLossRate       = stmt.excluded.packetErrorLossRate,
                )
        )
        stmt = stmt.returning(QoSProfileModel)
        qos_profile = session.execute(stmt).fetchall()
        return qos_profile[0]
    qos_profile_row = run_transaction(sessionmaker(bind=db_engine), callback)
    return qos_table_data_to_grpc_message(qos_profile_row)

def delete_qos_profile(db_engine : Engine, request : str) -> Empty:
    def callback(session : Session) -> bool:
        num_deleted = session.query(QoSProfileModel).filter_by(qos_profile_id=request).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    return Empty()

def get_qos_profile(db_engine : Engine, request : str) -> Optional[QoSProfile]:
    def callback(session : Session) -> Optional[QoSProfile]:
        obj : Optional[QoSProfileModel] = session.query(QoSProfileModel).filter_by(qos_profile_id=request).one_or_none()
        return None if obj is None else qos_table_data_to_grpc_message(obj)
    return run_transaction(sessionmaker(bind=db_engine), callback)

def get_qos_profiles(db_engine : Engine, request : Empty) -> List[QoSProfile]:
    def callback(session : Session) -> List[QoSProfile]:
        obj_list : List[QoSProfileModel] = session.query(QoSProfileModel).all()
        return [qos_table_data_to_grpc_message(obj) for obj in obj_list]
    return run_transaction(sessionmaker(bind=db_engine), callback)
