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

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from ._Base import _Base

class ContextModel(_Base):
    __tablename__ = 'context'

    context_uuid = Column(UUID(as_uuid=False), primary_key=True)
    context_name = Column(String, nullable=False)
    created_at   = Column(DateTime, nullable=False)
    updated_at   = Column(DateTime, nullable=False)

    topologies = relationship('TopologyModel', back_populates='context')
    services   = relationship('ServiceModel',  back_populates='context')
    slices     = relationship('SliceModel',    back_populates='context')

    def dump_id(self) -> Dict:
        return {'context_uuid': {'uuid': self.context_uuid}}

    def dump(self) -> Dict:
        return {
            'context_id'  : self.dump_id(),
            'name'        : self.context_name,
            'topology_ids': [obj.dump_id() for obj in self.topologies],
            'service_ids' : [obj.dump_id() for obj in self.services  ],
            'slice_ids'   : [obj.dump_id() for obj in self.slices    ],
        }
