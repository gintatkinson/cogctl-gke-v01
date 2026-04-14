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
import enum

from sqlalchemy     import Column, String, Float, Enum, BigInteger, JSON
from sqlalchemy.orm import registry
from common.proto   import analytics_frontend_pb2
from common.proto   import kpi_manager_pb2

from sqlalchemy.dialects.postgresql import UUID, ARRAY


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Create a base class for declarative models
Base = registry().generate_base()

class AnalyzerOperationMode (enum.Enum):
    BATCH     = analytics_frontend_pb2.AnalyzerOperationMode.ANALYZEROPERATIONMODE_BATCH
    STREAMING = analytics_frontend_pb2.AnalyzerOperationMode.ANALYZEROPERATIONMODE_STREAMING

class Analyzer(Base):
    __tablename__ = 'analyzer'

    analyzer_id           = Column( UUID(as_uuid=False)        , primary_key=True)
    algorithm_name        = Column( String                     , nullable=False  )
    input_kpi_ids         = Column( ARRAY(UUID(as_uuid=False)) , nullable=False  )
    output_kpi_ids        = Column( ARRAY(UUID(as_uuid=False)) , nullable=False  )
    operation_mode        = Column( Enum(AnalyzerOperationMode), nullable=False  )
    parameters            = Column( JSON                       , nullable=True   )
    batch_min_duration_s  = Column( Float                      , nullable=False  )
    batch_max_duration_s  = Column( Float                      , nullable=False  )
    batch_min_size        = Column( BigInteger                 , nullable=False  )
    batch_max_size        = Column( BigInteger                 , nullable=False  )

    # helps in logging the information
    def __repr__(self):
            return (f"<Analyzer(analyzer_id='{self.analyzer_id}'       , algorithm_name='{self.algorithm_name}', "
                    f"input_kpi_ids={self.input_kpi_ids}               , output_kpi_ids={self.output_kpi_ids}, "
                    f"operation_mode='{self.operation_mode}'           , parameters={self.parameters}, "
                    f"batch_min_duration_s={self.batch_min_duration_s} , batch_max_duration_s={self.batch_max_duration_s}, "
                    f"batch_min_size={self.batch_min_size}             , batch_max_size={self.batch_max_size})>")


    @classmethod
    def ConvertAnalyzerToRow(cls, request):
        """
        Create an instance of Analyzer table rows from a request object.
        Args:    request: The request object containing analyzer gRPC message.
        Returns: A row (an instance of Analyzer table) initialized with content of the request.
        """
        return cls(
            analyzer_id          = request.analyzer_id.analyzer_id.uuid,
            algorithm_name       = request.algorithm_name,
            input_kpi_ids        = [k.kpi_id.uuid for k in request.input_kpi_ids],
            output_kpi_ids       = [k.kpi_id.uuid for k in request.output_kpi_ids],
            operation_mode       = AnalyzerOperationMode(request.operation_mode),   # converts integer to coresponding Enum class member
            parameters           = dict(request.parameters),
            batch_min_duration_s = request.batch_min_duration_s,
            batch_max_duration_s = request.batch_max_duration_s,
            batch_min_size       = request.batch_min_size,
            batch_max_size       = request.batch_max_size
        )

    @classmethod
    def ConvertRowToAnalyzer(cls, row):
        """
        Create and return an Analyzer gRPC message initialized with the content of a row.
        Args: row: The Analyzer table instance (row) containing the data.
        Returns:   An Analyzer gRPC message initialized with the content of the row.
        """
        # Create an instance of the Analyzer message
        response                              = analytics_frontend_pb2.Analyzer()
        response.analyzer_id.analyzer_id.uuid = row.analyzer_id
        response.algorithm_name               = row.algorithm_name
        response.operation_mode               = row.operation_mode.value
        response.parameters.update(row.parameters)
        
        for input_kpi_id in row.input_kpi_ids:
            _kpi_id = kpi_manager_pb2.KpiId()
            _kpi_id.kpi_id.uuid = input_kpi_id
            response.input_kpi_ids.append(_kpi_id)
        for output_kpi_id in row.output_kpi_ids:
            _kpi_id = kpi_manager_pb2.KpiId()
            _kpi_id.kpi_id.uuid = output_kpi_id
            response.output_kpi_ids.append(_kpi_id)

        response.batch_min_duration_s = row.batch_min_duration_s
        response.batch_max_duration_s = row.batch_max_duration_s
        response.batch_min_size       = row.batch_min_size
        response.batch_max_size       = row.batch_max_size
        return response
