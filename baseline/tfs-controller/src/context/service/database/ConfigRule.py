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
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Set
from common.proto.context_pb2 import ConfigRule, ServiceConfigRule, Empty
from common.tools.grpc.Tools import grpc_message_to_json_string
from .models.enums.ConfigAction import ORM_ConfigActionEnum, grpc_to_enum__config_action
from .models.ConfigRuleModel import (
    ConfigRuleKindEnum, DeviceConfigRuleModel, ServiceConfigRuleModel, SliceConfigRuleModel)
from .uuids._Builder import get_uuid_from_string
from .uuids.EndPoint import endpoint_get_uuid
from sqlalchemy_cockroachdb import run_transaction
from sqlalchemy.orm import Session, sessionmaker

LOGGER = logging.getLogger(__name__)

def compose_config_rules_data(
    config_rules : List[ConfigRule], now : datetime.datetime,
    device_uuid : Optional[str] = None, service_uuid : Optional[str] = None, slice_uuid : Optional[str] = None
) -> List[Dict]:
    dict_config_rules : List[Dict] = list()
    for position,config_rule in enumerate(config_rules):
        str_kind = config_rule.WhichOneof('config_rule')
        kind = ConfigRuleKindEnum._member_map_.get(str_kind.upper()) # pylint: disable=no-member
        dict_config_rule = {
            'position'  : position,
            'kind'      : kind,
            'action'    : grpc_to_enum__config_action(config_rule.action),
            'data'      : grpc_message_to_json_string(getattr(config_rule, str_kind, {})),
            'created_at': now,
            'updated_at': now,
        }

        parent_kind,parent_uuid = '',None
        if device_uuid is not None:
            dict_config_rule['device_uuid'] = device_uuid
            parent_kind,parent_uuid = 'device',device_uuid
        elif service_uuid is not None:
            dict_config_rule['service_uuid'] = service_uuid
            parent_kind,parent_uuid = 'service',service_uuid
        elif slice_uuid is not None:
            dict_config_rule['slice_uuid'] = slice_uuid
            parent_kind,parent_uuid = 'slice',slice_uuid
        else:
            MSG = 'Parent for ConfigRule({:s}) cannot be identified '+\
                  '(device_uuid={:s}, service_uuid={:s}, slice_uuid={:s})'
            str_config_rule = grpc_message_to_json_string(config_rule)
            raise Exception(MSG.format(str_config_rule, str(device_uuid), str(service_uuid), str(slice_uuid)))

        configrule_name = None
        if kind == ConfigRuleKindEnum.CUSTOM:
            configrule_name = '{:s}:{:s}:{:s}'.format(parent_kind, kind.value, config_rule.custom.resource_key)
        elif kind == ConfigRuleKindEnum.ACL:
            _, _, endpoint_uuid = endpoint_get_uuid(config_rule.acl.endpoint_id, allow_random=False)
            rule_set_name = config_rule.acl.rule_set.name
            configrule_name = '{:s}:{:s}:{:s}:{:s}'.format(parent_kind, kind.value, endpoint_uuid, rule_set_name)
        elif kind == ConfigRuleKindEnum.IP_LINK:
            _, _, endpoint_uuid = endpoint_get_uuid(config_rule.ip_link.endpoint_id, allow_random=False)
        elif kind == ConfigRuleKindEnum.IPOWDM:
            _, _, endpoint_uuid = endpoint_get_uuid(config_rule.ipowdm.endpoint_id, allow_random=False)
            configrule_name = '{:s}:{:s}:{:s}'.format(parent_kind, kind.value, endpoint_uuid)
        elif kind == ConfigRuleKindEnum.TAPI_LSP:
            _, _, endpoint_uuid = endpoint_get_uuid(config_rule.tapi_lsp.endpoint_id, allow_random=False)
            configrule_name = '{:s}:{:s}:{:s}'.format(parent_kind, kind.value, endpoint_uuid)
        else:
            MSG = 'Name for ConfigRule({:s}) cannot be inferred '+\
                  '(device_uuid={:s}, service_uuid={:s}, slice_uuid={:s})'
            str_config_rule = grpc_message_to_json_string(config_rule)
            raise Exception(MSG.format(str_config_rule, str(device_uuid), str(service_uuid), str(slice_uuid)))

        configrule_uuid = get_uuid_from_string(configrule_name, prefix_for_name=parent_uuid)
        dict_config_rule['configrule_uuid'] = configrule_uuid

        dict_config_rules.append(dict_config_rule)
    return dict_config_rules

def upsert_config_rules(
    session : Session, config_rules : List[Dict], is_delete : bool = False,
    device_uuid : Optional[str] = None, service_uuid : Optional[str] = None, slice_uuid : Optional[str] = None,
) -> bool:
    if device_uuid is not None and service_uuid is None and slice_uuid is None:
        klass = DeviceConfigRuleModel
    elif device_uuid is None and service_uuid is not None and slice_uuid is None:
        klass = ServiceConfigRuleModel
    elif device_uuid is None and service_uuid is None and slice_uuid is not None:
        klass = SliceConfigRuleModel
    else:
        MSG = 'DataModel cannot be identified (device_uuid={:s}, service_uuid={:s}, slice_uuid={:s})'
        raise Exception(MSG.format(str(device_uuid), str(service_uuid), str(slice_uuid)))

    uuids_to_delete : Set[str] = set()
    uuids_to_upsert : Dict[str, int] = dict()
    rules_to_upsert : List[Dict] = list()
    for config_rule in config_rules:
        configrule_uuid = config_rule['configrule_uuid']
        configrule_action = config_rule['action']
        if is_delete or configrule_action == ORM_ConfigActionEnum.DELETE:
            uuids_to_delete.add(configrule_uuid)
        elif configrule_action == ORM_ConfigActionEnum.SET:
            position = uuids_to_upsert.get(configrule_uuid)
            if position is None:
                # if not added, add it
                rules_to_upsert.append(config_rule)
                uuids_to_upsert[configrule_uuid] = len(rules_to_upsert) - 1
            else:
                # if already added, update occurrence
                rules_to_upsert[position] = config_rule
        else:
            MSG = 'Action for ConfigRule({:s}) is not supported '+\
                  '(device_uuid={:s}, service_uuid={:s}, slice_uuid={:s})'
            str_config_rule = json.dumps(config_rule)
            raise Exception(MSG.format(str_config_rule, str(device_uuid), str(service_uuid), str(slice_uuid)))

    delete_affected = False
    if len(uuids_to_delete) > 0:
        stmt = delete(klass)
        if device_uuid  is not None: stmt = stmt.where(klass.device_uuid  == device_uuid )
        if service_uuid is not None: stmt = stmt.where(klass.service_uuid == service_uuid)
        if slice_uuid   is not None: stmt = stmt.where(klass.slice_uuid   == slice_uuid  )
        stmt = stmt.where(klass.configrule_uuid.in_(uuids_to_delete))
        #str_stmt = stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
        #LOGGER.warning('delete stmt={:s}'.format(str(str_stmt)))
        configrule_deletes = session.execute(stmt)
        #LOGGER.warning('configrule_deletes.rowcount={:s}'.format(str(configrule_deletes.rowcount)))
        delete_affected = int(configrule_deletes.rowcount) > 0

    upsert_affected = False
    if len(rules_to_upsert) > 0:
        stmt = insert(klass).values(rules_to_upsert)
        stmt = stmt.on_conflict_do_update(
            index_elements=[klass.configrule_uuid],
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
        configrule_updates = session.execute(stmt).fetchall()
        upsert_affected = any([(updated_at > created_at) for created_at,updated_at in configrule_updates])

    return delete_affected or upsert_affected


def delete_config_rule(db_engine : Engine, request : ServiceConfigRule):
    config_rule = request.configrule_custom
    service_id  = request.service_id
    parent_uuid = service_id.service_uuid.uuid
    configrule_name = 'service:custom:{:s}'.format( config_rule.resource_key)
    configrule_uuid = get_uuid_from_string(configrule_name, prefix_for_name=parent_uuid)
    def callback(session : Session) -> bool:
        num_deleted = session.query(ServiceConfigRuleModel).filter_by(configrule_uuid=configrule_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    return Empty()
