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

import datetime, logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from typing import Dict, List, Optional, Tuple
from common.method_wrappers.ServiceExceptions import NotFoundException
from .models.SubSubscriptionModel import SubSubscriptionModel


LOGGER = logging.getLogger(__name__)


def sub_subscription_list(db_engine : Engine, parent_subscription_uuid : str) -> List[Dict]:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[SubSubscriptionModel] = (
            session
            .query(SubSubscriptionModel)
            .filter_by(parent=parent_subscription_uuid)
            .all()
        )
        return [obj.dump() for obj in obj_list]
    return run_transaction(sessionmaker(bind=db_engine), callback)


def sub_subscription_get(
    db_engine : Engine, parent_subscription_uuid : str, sub_subscription_id : int
) -> Dict:
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[SubSubscriptionModel] = (
            session
            .query(SubSubscriptionModel)
            .filter_by(parent=parent_subscription_uuid, sub_subscription_id=sub_subscription_id)
            .one_or_none()
        )
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        sub_sub_key = '{:s}/{:s}'.format(str(parent_subscription_uuid), str(sub_subscription_id))
        raise NotFoundException('SubSubscription', sub_sub_key)
    return obj


def sub_subscription_set(
    db_engine : Engine, parent_subscription_uuid : str, controller_uuid : str, datastore : str,
    xpath_filter : str, period : float, sub_subscription_id : int, sub_subscription_uri : str,
    collector_name : str
) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    if controller_uuid is None: controller_uuid = ''
    sub_subscription_data = {
        'parent'              : parent_subscription_uuid,
        'controller_uuid'     : controller_uuid,
        'datastore'           : datastore,
        'xpath_filter'        : xpath_filter,
        'period'              : period,
        'sub_subscription_id' : sub_subscription_id,
        'sub_subscription_uri': sub_subscription_uri,
        'collector_name'      : collector_name,
        'created_at'          : now,
        'updated_at'          : now,
    }

    def callback(session : Session) -> Tuple[bool, str]:
        stmt = insert(SubSubscriptionModel).values([sub_subscription_data])
        stmt = stmt.on_conflict_do_update(
            index_elements=[
                SubSubscriptionModel.parent,
                SubSubscriptionModel.sub_subscription_uuid,
            ],
            set_=dict(
                controller_uuid      = stmt.excluded.controller_uuid,
                datastore            = stmt.excluded.datastore,
                xpath_filter         = stmt.excluded.xpath_filter,
                period               = stmt.excluded.period,
                sub_subscription_id  = stmt.excluded.sub_subscription_id,
                sub_subscription_uri = stmt.excluded.sub_subscription_uri,
                collector_name       = stmt.excluded.collector_name,
                updated_at           = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(
            SubSubscriptionModel.created_at, SubSubscriptionModel.updated_at,
            SubSubscriptionModel.sub_subscription_uuid
        )
        return_values = session.execute(stmt).fetchone()
        created_at,updated_at,subscription_uuid = return_values
        return updated_at > created_at, subscription_uuid

    _, subscription_uuid = run_transaction(sessionmaker(bind=db_engine), callback)
    return subscription_uuid


def sub_subscription_delete(
    db_engine : Engine, parent_subscription_uuid : str, sub_subscription_id : int
) -> bool:
    def callback(session : Session) -> bool:
        num_deleted = (
            session
            .query(SubSubscriptionModel)
            .filter_by(parent=parent_subscription_uuid, sub_subscription_id=sub_subscription_id)
            .delete()
        )
        return num_deleted > 0
    return run_transaction(sessionmaker(bind=db_engine), callback)
