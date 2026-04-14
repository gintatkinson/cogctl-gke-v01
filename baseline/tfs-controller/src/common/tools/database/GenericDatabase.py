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
import sqlalchemy_utils
from .GenericEngine import Engine
from sqlalchemy     import inspect
from sqlalchemy.orm import sessionmaker
from common.Settings import get_setting

from common.method_wrappers.ServiceExceptions import (OperationFailedException, AlreadyExistsException)

LOGGER = logging.getLogger(__name__)

class Database:
    def __init__(self, model):
        self.db_engine = Engine.get_engine()
        if self.db_engine is None:
            LOGGER.error('Unable to get SQLAlchemy DB Engine...')
            raise Exception('Failed to initialize the database engine.')
        self.db_model = model
        self.db_table = model.__name__
        self.Session  = sessionmaker(bind=self.db_engine)
    
    def create_database(self):
        if not sqlalchemy_utils.database_exists(self.db_engine.url):
            LOGGER.debug("Database created. {:}".format(self.db_engine.url))
            sqlalchemy_utils.create_database(self.db_engine.url)

    def drop_database(self) -> None:
        if sqlalchemy_utils.database_exists(self.db_engine.url):
            sqlalchemy_utils.drop_database(self.db_engine.url)

    def create_tables(self):
        try:
            self.db_model.metadata.create_all(self.db_engine)
            LOGGER.debug("Tables created in the database: {:}".format(self.db_table))
        except Exception as e:
            LOGGER.debug("Tables cannot be created in the database. {:s}".format(str(e)))
            raise OperationFailedException ("Tables can't be created", extra_details=["unable to create table {:}".format(e)])

    def verify_tables(self):
        try:
            inspect_object = inspect(self.db_engine)
            if(inspect_object.has_table(self.db_table , None)):
                LOGGER.info("Table exists in DB: {:}".format(self.db_name))
        except Exception as e:
            LOGGER.info("Unable to fetch Table names. {:s}".format(str(e)))    

# ----------------- DB OPERATIONS ---------------------

    def add_row_to_db(self, row):
        session = self.Session()
        try:
            session.add(row)
            session.commit()
            LOGGER.debug(f"Row inserted into {row.__class__.__name__} table.")
            return True
        except Exception as e:
            session.rollback()
            if "psycopg2.errors.UniqueViolation" in str(e):
                LOGGER.error(f"Unique key voilation: {row.__class__.__name__} table. {str(e)}")
                raise AlreadyExistsException(row.__class__.__name__, row,
                                             extra_details=["Unique key voilation: {:}".format(e)] )
            else:
                LOGGER.error(f"Failed to insert new row into {row.__class__.__name__} table. {str(e)}")
                raise OperationFailedException ("Deletion by column id", extra_details=["unable to delete row {:}".format(e)])
        finally:
            session.close()
    
    def search_db_row_by_id(self, model, col_name, id_to_search):
        session = self.Session()
        try:
            entity = session.query(model).filter_by(**{col_name: id_to_search}).first()
            if entity:
                # LOGGER.debug(f"{model.__name__} ID found: {str(entity)}")
                return entity
            else:
                LOGGER.debug(f"{model.__name__} ID not found, No matching row: {str(id_to_search)}")
                print("{:} ID not found, No matching row: {:}".format(model.__name__, id_to_search))
                return None
        except Exception as e:
            session.rollback()
            LOGGER.debug(f"Failed to retrieve {model.__name__} ID. {str(e)}")
            raise OperationFailedException ("search by column id", extra_details=["unable to search row {:}".format(e)])
        finally:
            session.close()
    
    def delete_db_row_by_id(self, model, col_name, id_to_search):
        session = self.Session()
        try:
            record = session.query(model).filter_by(**{col_name: id_to_search}).first()
            if record:
                session.delete(record)
                session.commit()
                LOGGER.debug("Deleted %s with %s: %s", model.__name__, col_name, id_to_search)
            else:
                LOGGER.debug("%s with %s %s not found", model.__name__, col_name, id_to_search)
                return None
        except Exception as e:
            session.rollback()
            LOGGER.error("Error deleting %s with %s %s: %s", model.__name__, col_name, id_to_search, e)
            raise OperationFailedException ("Deletion by column id", extra_details=["unable to delete row {:}".format(e)])
        finally:
            session.close()

    def select_with_filter(self, query_object, session, model):
        """
        Generic method to apply filters dynamically based on filter.
        params:     model_name:    SQLAlchemy model class name.
                    query_object : Object that contains query with applied filters.
                    session:       session of the query.
        return:     List of filtered records.
        """
        try:
            result = query_object.all()
            # Log result and handle empty case
            if result:
                LOGGER.debug(f"Fetched filtered rows from {model.__name__} with filters: {query_object}")
            else:
                LOGGER.warning(f"No matching rows found in {model.__name__} with filters: {query_object}")
            return result
        except Exception as e:
            LOGGER.error(f"Error fetching filtered rows from {model.__name__} with filters {query_object} ::: {e}")
            raise OperationFailedException("Select by filter", extra_details=[f"Unable to apply the filter: {e}"])
        finally:
            session.close()
