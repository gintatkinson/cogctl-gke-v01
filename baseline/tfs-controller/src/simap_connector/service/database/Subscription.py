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
from typing import Dict, Optional, Tuple
from common.method_wrappers.ServiceExceptions import NotFoundException
from .models.SubscriptionModel import SubscriptionModel


LOGGER = logging.getLogger(__name__)


def subscription_get(db_engine : Engine, subscription_id : int) -> Dict:
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[SubscriptionModel] = (
            session
            .query(SubscriptionModel)
            .filter_by(subscription_id=subscription_id)
            .one_or_none()
        )
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        raise NotFoundException('Subscription', str(subscription_id))
    return obj


def subscription_set(
    db_engine : Engine, datastore : str, xpath_filter : str, period : float
) -> Tuple[str, int]:
    now = datetime.datetime.now(datetime.timezone.utc)
    subscription_data = {
        'datastore'    : datastore,
        'xpath_filter' : xpath_filter,
        'period'       : period,
        'created_at'   : now,
        'updated_at'   : now,
    }

    def callback(session : Session) -> Tuple[bool, str, int]:
        stmt = insert(SubscriptionModel).values([subscription_data])
        stmt = stmt.on_conflict_do_update(
            index_elements=[SubscriptionModel.subscription_uuid],
            set_=dict(
                datastore    = stmt.excluded.datastore,
                xpath_filter = stmt.excluded.xpath_filter,
                period       = stmt.excluded.period,
                updated_at   = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(
            SubscriptionModel.created_at, SubscriptionModel.updated_at,
            SubscriptionModel.subscription_uuid, SubscriptionModel.subscription_id
        )
        return_values = session.execute(stmt).fetchone()
        created_at,updated_at,subscription_uuid,subscription_id = return_values
        return updated_at > created_at, subscription_uuid, subscription_id

    _, subscription_uuid, subscription_id = run_transaction(sessionmaker(bind=db_engine), callback)
    return subscription_uuid, subscription_id


def subscription_delete(db_engine : Engine, subscription_id : int) -> bool:
    def callback(session : Session) -> bool:
        num_deleted = (
            session
            .query(SubscriptionModel)
            .filter_by(subscription_id=subscription_id)
            .delete()
        )
        return num_deleted > 0
    return run_transaction(sessionmaker(bind=db_engine), callback)
