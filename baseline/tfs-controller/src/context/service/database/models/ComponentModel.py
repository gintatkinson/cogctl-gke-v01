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

import json
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from ._Base import _Base                                                

class ComponentModel(_Base):
    __tablename__ = 'device_component'
    
    component_uuid  = Column(UUID(as_uuid=False), primary_key=True)
    device_uuid     = Column(ForeignKey('device.device_uuid',ondelete='CASCADE' ), nullable=False, index=True)
    name            = Column(String, nullable=False)
    type            = Column(String, nullable=False)
    attributes      = Column(String, nullable=False)
    parent          = Column(String, nullable=False)
    created_at      = Column(DateTime, nullable=False)
    updated_at      = Column(DateTime, nullable=False)
    
    device           = relationship('DeviceModel', back_populates='components')
    def dump_id(self) -> Dict:
        return{
            'device_id'     : self.device.dump_id(),
            'component_uuid': {'uuid': self.component_uuid},
        }

    def dump(self) -> Dict:
        data = dict()
        data['attributes']     = json.loads(self.attributes)
        data['component_uuid'] = {'uuid': self.component_uuid}
        data['name']           = self.name
        data['type']           = self.type
        data['parent']         = self.parent
        return data

    def dump_name(self) -> Dict:
        return {
            'component_id'  : self.dump_id(),
            'device_name'   : self.device.device_name,
            'component_name': self.name,
        }
