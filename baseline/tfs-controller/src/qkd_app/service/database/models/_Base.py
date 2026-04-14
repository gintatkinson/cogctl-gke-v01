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
from sqlalchemy.orm import declarative_base

_Base = declarative_base()

def rebuild_database(db_engine: sqlalchemy.engine.Engine, drop_if_exists: bool = False):
    """
    Rebuild the database schema for the QKD application. Optionally drop the existing schema if specified.
    
    :param db_engine: SQLAlchemy engine instance.
    :param drop_if_exists: Boolean indicating if the schema should be dropped before rebuilding.
    """
    if drop_if_exists:
        _Base.metadata.drop_all(db_engine)
    _Base.metadata.create_all(db_engine)
