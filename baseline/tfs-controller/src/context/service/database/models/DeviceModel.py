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

import operator
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from typing import Dict, List
from .enums.DeviceDriver import ORM_DeviceDriverEnum
from .enums.DeviceOperationalStatus import ORM_DeviceOperationalStatusEnum
from ._Base import _Base

class DeviceModel(_Base):
    __tablename__ = 'device'

    device_uuid               = Column(UUID(as_uuid=False), primary_key=True)
    device_name               = Column(String, nullable=False)
    device_type               = Column(String, nullable=False)
    device_operational_status = Column(Enum(ORM_DeviceOperationalStatusEnum), nullable=False)
    device_drivers            = Column(ARRAY(Enum(ORM_DeviceDriverEnum), dimensions=1))
    controller_uuid           = Column(UUID(as_uuid=False), ForeignKey('device.device_uuid'), nullable=True)
    created_at                = Column(DateTime, nullable=False)
    updated_at                = Column(DateTime, nullable=False)

    #topology_devices = relationship('TopologyDeviceModel', back_populates='device')
    config_rules   = relationship('DeviceConfigRuleModel', passive_deletes=True) # lazy='joined', back_populates='device'
    endpoints      = relationship('EndPointModel', passive_deletes=True) # lazy='joined', back_populates='device'
    components     = relationship('ComponentModel', passive_deletes=True) # lazy='joined', back_populates='device' 
    controller     = relationship('DeviceModel', remote_side=[device_uuid], passive_deletes=True) # lazy='joined', back_populates='device'
    optical_config = relationship('OpticalConfigModel', passive_deletes=True)

    def dump_id(self) -> Dict:
        return {'device_uuid': {'uuid': self.device_uuid}}

    def dump_controller(self) -> Dict:
        if self.controller is None: return {}
        return self.controller.dump_id()

    def dump_endpoints(self) -> List[Dict]:
        return [endpoint.dump() for endpoint in self.endpoints]

    def dump_config_rules(self) -> Dict:
        return {'config_rules': [
            config_rule.dump()
            for config_rule in sorted(self.config_rules, key=operator.attrgetter('position'))
        ]}

    def dump_components(self) -> List[Dict]:
        return [component.dump() for component in self.components]

    def dump(self,
        include_endpoints : bool = True, include_config_rules : bool = True, include_components : bool = True,
    ) -> Dict:
        result = {
            'device_id'                : self.dump_id(),
            'name'                     : self.device_name,
            'device_type'              : self.device_type,
            'device_operational_status': self.device_operational_status.value,
            'device_drivers'           : [driver.value for driver in self.device_drivers],
            'controller_id'            : self.dump_controller(),
        }
        if include_endpoints: result['device_endpoints'] = self.dump_endpoints()
        if include_config_rules: result['device_config'] = self.dump_config_rules()
        if include_components: result['components'] = self.dump_components()
        return result
