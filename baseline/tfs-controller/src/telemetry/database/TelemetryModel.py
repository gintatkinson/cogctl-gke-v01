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
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import registry
from common.proto import telemetry_frontend_pb2

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Create a base class for declarative models
Base = registry().generate_base()
    
class Collector(Base):
    __tablename__ = 'collector'

    collector_id         = Column(UUID(as_uuid=False), primary_key=True)
    kpi_id               = Column(UUID(as_uuid=False), nullable=False)
    sampling_duration_s  = Column(Float              , nullable=False)
    sampling_interval_s  = Column(Float              , nullable=False)
    start_timestamp      = Column(Float              , nullable=False)
    end_timestamp        = Column(Float              , nullable=False)

    # helps in logging the information
    def __repr__(self):
        return (f"<Collector(collector_id='{self.collector_id}'   , kpi_id='{self.kpi_id}', "
                f"sampling_duration_s='{self.sampling_duration_s}', sampling_interval_s='{self.sampling_interval_s}',"
                f"start_timestamp='{self.start_timestamp}'        , end_timestamp='{self.end_timestamp}')>")

    @classmethod
    def ConvertCollectorToRow(cls, request):
        """
        Create an instance of Collector table rows from a request object.
        Args:    request: The request object containing collector gRPC message.
        Returns: A row (an instance of Collector table) initialized with content of the request.
        """
        return cls(
            collector_id         = request.collector_id.collector_id.uuid,
            kpi_id               = request.kpi_id.kpi_id.uuid,
            sampling_duration_s  = request.duration_s,
            sampling_interval_s  = request.interval_s,
            start_timestamp      = request.start_time.timestamp,
            end_timestamp        = request.end_time.timestamp
        )

    @classmethod
    def ConvertRowToCollector(cls, row):
        """
        Create and return a dictionary representation of a Collector table instance.       
        Args:   row: The Collector table instance (row) containing the data.
        Returns: collector gRPC message initialized with the content of a row.
        """
        response                                = telemetry_frontend_pb2.Collector()
        response.collector_id.collector_id.uuid = row.collector_id
        response.kpi_id.kpi_id.uuid             = row.kpi_id
        response.duration_s                     = row.sampling_duration_s
        response.interval_s                     = row.sampling_interval_s
        response.start_time.timestamp           = row.start_timestamp
        response.end_time.timestamp             = row.end_timestamp
        return response
