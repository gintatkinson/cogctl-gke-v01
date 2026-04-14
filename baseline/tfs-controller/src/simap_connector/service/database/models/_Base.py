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

import sqlalchemy
#from typing import Any, List
#from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import declarative_base
#from sqlalchemy.sql import text
#from sqlalchemy_cockroachdb import run_transaction

_Base = declarative_base()

#def create_performance_enhancers(db_engine : sqlalchemy.engine.Engine) -> None:
#    def index_storing(
#        index_name : str, table_name : str, index_fields : List[str], storing_fields : List[str]
#    ) -> Any:
#        str_index_fields = ','.join(['"{:s}"'.format(index_field) for index_field in index_fields])
#        str_storing_fields = ','.join(['"{:s}"'.format(storing_field) for storing_field in storing_fields])
#        INDEX_STORING = 'CREATE INDEX IF NOT EXISTS {:s} ON "{:s}" ({:s}) STORING ({:s});'
#        return text(INDEX_STORING.format(index_name, table_name, str_index_fields, str_storing_fields))
#
#    statements = [
#    ]
#    def callback(session : Session) -> bool:
#        for stmt in statements: session.execute(stmt)
#    run_transaction(sessionmaker(bind=db_engine), callback)

def rebuild_database(db_engine : sqlalchemy.engine.Engine, drop_if_exists : bool = False):
    if drop_if_exists: _Base.metadata.drop_all(db_engine)
    _Base.metadata.create_all(db_engine)
    #create_performance_enhancers(db_engine)
