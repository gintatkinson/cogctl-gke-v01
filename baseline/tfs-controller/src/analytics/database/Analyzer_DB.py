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
from common.method_wrappers.Decorator import MetricsPool
from common.tools.database.GenericDatabase import Database
from common.method_wrappers.ServiceExceptions import OperationFailedException

LOGGER       = logging.getLogger(__name__)
METRICS_POOL = MetricsPool('KpiManager', 'Database')

class AnalyzerDB(Database):
    def __init__(self, model) -> None:
        LOGGER.info('Init KpiManagerService')
        super().__init__(model)

    def select_with_filter(self, model, filter_object):
        """
        Generic method to create filters dynamically based on filter_object attributes.
        params:     model:         SQLAlchemy model class to query.
                    filter_object: Object that contains filtering criteria as attributes.
        return:     SQLAlchemy session, query and Model
        """
        session = self.Session()
        try:
            query = session.query(model)
            # Apply filters based on the filter_object
            if filter_object.analyzer_id:
                query = query.filter(model.analyzer_id.in_([a.analyzer_id.uuid for a in filter_object.analyzer_id]))

            if filter_object.algorithm_names:
                query = query.filter(model.algorithm_name.in_(filter_object.algorithm_names))

            if filter_object.input_kpi_ids:
                input_kpi_uuids = [k.kpi_id.uuid for k in filter_object.input_kpi_ids]
                query = query.filter(model.input_kpi_ids.op('&&')(input_kpi_uuids))

            if filter_object.output_kpi_ids:
                output_kpi_uuids = [k.kpi_id.uuid for k in filter_object.output_kpi_ids]
                query = query.filter(model.output_kpi_ids.op('&&')(output_kpi_uuids))
        except Exception as e:
            LOGGER.error(f"Error creating filter of {model.__name__} table. ERROR: {e}")
            raise OperationFailedException ("CreateKpiDescriptorFilter", extra_details=["unable to create the filter {:}".format(e)]) 
        
        return super().select_with_filter(query, session, model)
