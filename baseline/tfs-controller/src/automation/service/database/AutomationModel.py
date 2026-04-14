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
from .models._Base import _Base
from common.proto.automation_pb2 import ZSMService

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class AutomationModel(_Base):
    __tablename__ = 'automation'

    zsm_id          = Column(UUID(as_uuid=False), primary_key=True)
    zsm_description = Column(Text               , nullable=False)

    # helps in logging the information
    def __repr__(self):
        return (f"<Automation(zsm_id='{self.zsm_id}', zsm_description='{self.zsm_description}'>")

    @classmethod
    def convert_Automation_to_row(cls, uuid , zsm_description):
        """
        Create an instance of Automation from a request object.
        Args:    request: The request object containing the data.
        Returns: An instance of Automation initialized with data from the request.
        """
        return cls(
            zsm_id          = uuid,
            zsm_description = zsm_description
        )

    @classmethod
    def convert_row_to_Automation(cls, row):
        """
        Create and return a dictionary representation of a Automation instance.
        Args:   row: The Automation instance (row) containing the data.
        Returns: Automation object
        """
        response = ZSMService()
        response.zsmServiceId.uuid.uuid               = row.zsm_id
        return response
