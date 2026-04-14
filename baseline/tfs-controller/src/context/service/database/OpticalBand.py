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
from sqlalchemy.dialects.postgresql import insert
from common.method_wrappers.ServiceExceptions import NotFoundException
from typing import Dict, List
from common.proto.context_pb2 import OpticalBand,OpticalBandId,OpticalBandList
from .models.OpticalConfig.OpticalBandModel import OpticalBandModel


LOGGER = logging.getLogger(__name__)



def get_optical_band(db_engine : Engine):
    def callback(session:Session):
        results = session.query(OpticalBandModel).all()
        
        return [obj.dump() for obj in results]
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    return obj


def select_optical_band( db_engine : Engine ,request:OpticalBandId):
    ob_uuid = request.opticalband_uuid.uuid
    def callback(session : Session) -> OpticalBand:
        stmt = session.query(OpticalBandModel)
        stmt = stmt.filter_by(ob_uuid=ob_uuid)
        obj = stmt.first()
        if obj is not None:
          
            return obj.dump()
        return None
    result= run_transaction(sessionmaker(bind=db_engine, expire_on_commit=False), callback)
    if result is None : 
       return result
    return OpticalBand(**result)
         

def set_optical_band(db_engine : Engine, ob_data ):
  
    def callback(session : Session) -> List[Dict]:
        if len(ob_data) > 0:
                stmt = insert(OpticalBandModel).values(ob_data)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[OpticalBandModel.ob_uuid],
                    set_=dict(
                        connection_uuid = stmt.excluded.connection_uuid
                    )
                )
                stmt = stmt.returning(OpticalBandModel.ob_uuid)
                ob_id = session.execute(stmt).fetchone()
                
    ob_id = run_transaction(sessionmaker(bind=db_engine), callback)
    return {'ob_id': ob_id}            
