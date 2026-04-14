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
from sqlalchemy import delete
#from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Set
from common.proto.context_pb2 import Constraint
from common.tools.grpc.Tools import grpc_message_to_json_string
from .models.ConstraintModel import ConstraintKindEnum, ServiceConstraintModel, SliceConstraintModel
from .models.enums.ConstraintAction import ORM_ConstraintActionEnum, grpc_to_enum__constraint_action
from .uuids._Builder import get_uuid_from_string
from .uuids.EndPoint import endpoint_get_uuid

LOGGER = logging.getLogger(__name__)

def compose_constraints_data(
    constraints : List[Constraint], now : datetime.datetime,
    service_uuid : Optional[str] = None, slice_uuid : Optional[str] = None
) -> List[Dict]:
    dict_constraints : List[Dict] = list()
    for position,constraint in enumerate(constraints):
        str_kind = constraint.WhichOneof('constraint')
        kind = ConstraintKindEnum._member_map_.get(str_kind.upper()) # pylint: disable=no-member
        dict_constraint = {
            'position'  : position,
            'kind'      : kind,
            'action'    : grpc_to_enum__constraint_action(constraint.action),
            'data'      : grpc_message_to_json_string(getattr(constraint, str_kind, {})),
            'created_at': now,
            'updated_at': now,
        }

        parent_kind,parent_uuid = '',None
        if service_uuid is not None:
            dict_constraint['service_uuid'] = service_uuid
            parent_kind,parent_uuid = 'service',service_uuid
        elif slice_uuid is not None:
            dict_constraint['slice_uuid'] = slice_uuid
            parent_kind,parent_uuid = 'slice',slice_uuid
        else:
            MSG = 'Parent for Constraint({:s}) cannot be identified '+\
                  '(service_uuid={:s}, slice_uuid={:s})'
            str_constraint = grpc_message_to_json_string(constraint)
            raise Exception(MSG.format(str_constraint, str(service_uuid), str(slice_uuid)))

        constraint_name = None
        if kind == ConstraintKindEnum.CUSTOM:
            constraint_name = '{:s}:{:s}:{:s}'.format(parent_kind, kind.value, constraint.custom.constraint_type)
        elif kind == ConstraintKindEnum.ENDPOINT_LOCATION:
            _, _, endpoint_uuid = endpoint_get_uuid(constraint.endpoint_location.endpoint_id, allow_random=False)
            location_kind = constraint.endpoint_location.location.WhichOneof('location')
            constraint_name = '{:s}:{:s}:{:s}:{:s}'.format(parent_kind, kind.value, endpoint_uuid, location_kind)
        elif kind == ConstraintKindEnum.ENDPOINT_PRIORITY:
            _, _, endpoint_uuid = endpoint_get_uuid(constraint.endpoint_priority.endpoint_id, allow_random=False)
            constraint_name = '{:s}:{:s}:{:s}'.format(parent_kind, kind.value, endpoint_uuid)
        elif kind in {
            ConstraintKindEnum.SCHEDULE, ConstraintKindEnum.SLA_CAPACITY, ConstraintKindEnum.SLA_LATENCY,
            ConstraintKindEnum.SLA_AVAILABILITY, ConstraintKindEnum.SLA_ISOLATION, ConstraintKindEnum.EXCLUSIONS,
            ConstraintKindEnum.QOS_PROFILE
        }:
            constraint_name = '{:s}:{:s}:'.format(parent_kind, kind.value)
        else:
            MSG = 'Name for Constraint({:s}) cannot be inferred '+\
                  '(service_uuid={:s}, slice_uuid={:s})'
            str_constraint = grpc_message_to_json_string(constraint)
            raise Exception(MSG.format(str_constraint, str(service_uuid), str(slice_uuid)))

        constraint_uuid = get_uuid_from_string(constraint_name, prefix_for_name=parent_uuid)
        dict_constraint['constraint_uuid'] = constraint_uuid

        dict_constraints.append(dict_constraint)
    return dict_constraints

def upsert_constraints(
    session : Session, constraints : List[Dict], is_delete : bool = False,
    service_uuid : Optional[str] = None, slice_uuid : Optional[str] = None
) -> bool:
    if service_uuid is not None and slice_uuid is None:
        klass = ServiceConstraintModel
    elif service_uuid is None and slice_uuid is not None:
        klass = SliceConstraintModel
    else:
        MSG = 'DataModel cannot be identified (service_uuid={:s}, slice_uuid={:s})'
        raise Exception(MSG.format(str(service_uuid), str(slice_uuid)))
    uuids_to_delete : Set[str] = set()
    uuids_to_upsert : Dict[str, int] = dict()
    rules_to_upsert : List[Dict] = list()
    for constraint in constraints:
        constraint_uuid = constraint['constraint_uuid']
        constraint_action = constraint['action']
        if is_delete or constraint_action == ORM_ConstraintActionEnum.DELETE:
            uuids_to_delete.add(constraint_uuid)
        elif constraint_action == ORM_ConstraintActionEnum.SET:
            position = uuids_to_upsert.get(constraint_uuid)
            if position is None:
                # if not added, add it
                rules_to_upsert.append(constraint)
                uuids_to_upsert[constraint_uuid] = len(rules_to_upsert) - 1
            else:
                # if already added, update occurrence
                rules_to_upsert[position] = constraint
        else:
            MSG = 'Action for ConstraintRule({:s}) is not supported (service_uuid={:s}, slice_uuid={:s})'
            LOGGER.warning(MSG.format(str(constraint), str(service_uuid), str(slice_uuid)))
            # raise Exception(MSG.format(str_constraint, str(service_uuid), str(slice_uuid)))

    delete_affected = False
    if len(uuids_to_delete) > 0:
        stmt = delete(klass)
        if service_uuid is not None: stmt = stmt.where(klass.service_uuid == service_uuid)
        if slice_uuid   is not None: stmt = stmt.where(klass.slice_uuid   == slice_uuid  )
        stmt = stmt.where(klass.constraint_uuid.in_(uuids_to_delete))
        #str_stmt = stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
        #LOGGER.warning('delete stmt={:s}'.format(str(str_stmt)))
        constraint_deletes = session.execute(stmt)
        #LOGGER.warning('constraint_deletes.rowcount={:s}'.format(str(constraint_deletes.rowcount)))
        delete_affected = int(constraint_deletes.rowcount) > 0

    upsert_affected = False
    if not is_delete and len(constraints) > 0:
        stmt = insert(klass).values(constraints)
        stmt = stmt.on_conflict_do_update(
            index_elements=[klass.constraint_uuid],
            set_=dict(
                position   = stmt.excluded.position,
                action     = stmt.excluded.action,
                data       = stmt.excluded.data,
                updated_at = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(klass.created_at, klass.updated_at)
        #str_stmt = stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
        #LOGGER.warning('upsert stmt={:s}'.format(str(str_stmt)))
        constraint_updates = session.execute(stmt).fetchall()
        upsert_affected = any([(updated_at > created_at) for created_at,updated_at in constraint_updates])

    return delete_affected or upsert_affected
