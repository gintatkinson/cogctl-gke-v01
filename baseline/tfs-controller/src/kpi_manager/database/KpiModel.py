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
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import registry
from common.proto.kpi_manager_pb2 import KpiDescriptor

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Create a base class for declarative models
Base = registry().generate_base()

class Kpi(Base):
    __tablename__ = 'kpi'

    kpi_id          = Column(UUID(as_uuid=False), primary_key=True)
    kpi_description = Column(Text               , nullable=False)
    kpi_sample_type = Column(Integer            , nullable=False)
    device_id       = Column(String             , nullable=False)
    endpoint_id     = Column(String             , nullable=False)
    service_id      = Column(String             , nullable=False)
    slice_id        = Column(String             , nullable=False)
    connection_id   = Column(String             , nullable=False)
    link_id         = Column(String             , nullable=False)

    # helps in logging the information
    def __repr__(self):
        return (f"<Kpi(kpi_id='{self.kpi_id}', kpi_description='{self.kpi_description}', "
                f"kpi_sample_type='{self.kpi_sample_type}', device_id='{self.device_id}', "
                f"endpoint_id='{self.endpoint_id}', service_id='{self.service_id}', "
                f"slice_id='{self.slice_id}', connection_id='{self.connection_id}', "
                f"link_id='{self.link_id}')>")

    @classmethod
    def convert_KpiDescriptor_to_row(cls, request):
        """
        Create an instance of Kpi from a request object.
        Args:    request: The request object containing the data.
        Returns: An instance of Kpi initialized with data from the request.
        """
        return cls(
            kpi_id          = request.kpi_id.kpi_id.uuid,
            kpi_description = request.kpi_description,
            kpi_sample_type = request.kpi_sample_type,
            device_id       = request.device_id.device_uuid.uuid,
            endpoint_id     = request.endpoint_id.endpoint_uuid.uuid,
            service_id      = request.service_id.service_uuid.uuid,
            slice_id        = request.slice_id.slice_uuid.uuid,
            connection_id   = request.connection_id.connection_uuid.uuid,
            link_id         = request.link_id.link_uuid.uuid
        )
    
    @classmethod
    def convert_row_to_KpiDescriptor(cls, row):
        """
        Create and return a dictionary representation of a Kpi instance.       
        Args:   row: The Kpi instance (row) containing the data.
        Returns: KpiDescriptor object
        """
        response = KpiDescriptor()
        response.kpi_id.kpi_id.uuid                 = row.kpi_id
        response.kpi_description                    = row.kpi_description
        response.kpi_sample_type                    = row.kpi_sample_type
        response.service_id.service_uuid.uuid       = row.service_id
        response.device_id.device_uuid.uuid         = row.device_id
        response.slice_id.slice_uuid.uuid           = row.slice_id
        response.endpoint_id.endpoint_uuid.uuid     = row.endpoint_id
        response.connection_id.connection_uuid.uuid = row.connection_id
        response.link_id.link_uuid.uuid             = row.link_id
        return response
