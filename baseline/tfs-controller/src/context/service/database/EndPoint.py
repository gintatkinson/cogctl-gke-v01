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
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, selectinload, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from typing import Dict, List
from common.proto.context_pb2 import EndPointIdList, EndPointNameList
from .models.EndPointModel import EndPointModel
from .uuids.EndPoint import endpoint_get_uuid

LOGGER = logging.getLogger(__name__)

def endpoint_list_names(db_engine : Engine, request : EndPointIdList) -> EndPointNameList:
    endpoint_uuids = {
        endpoint_get_uuid(endpoint_id, allow_random=False)[-1]
        for endpoint_id in request.endpoint_ids
    }
    def callback(session : Session) -> List[Dict]:
        obj_list : List[EndPointModel] = session.query(EndPointModel)\
            .options(selectinload(EndPointModel.device))\
            .filter(EndPointModel.endpoint_uuid.in_(endpoint_uuids)).all()
        return [obj.dump_name() for obj in obj_list]
    endpoint_names = run_transaction(sessionmaker(bind=db_engine), callback)
    return EndPointNameList(endpoint_names=endpoint_names)
