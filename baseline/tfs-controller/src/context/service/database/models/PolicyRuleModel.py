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

import enum, json
from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from .enums.PolicyRuleState import ORM_PolicyRuleStateEnum
from ._Base import _Base

# Enum values should match name of field in PolicyRule message
class PolicyRuleKindEnum(enum.Enum):
    DEVICE  = 'device'
    SERVICE = 'service'

class PolicyRuleModel(_Base):
    __tablename__ = 'policyrule'

    policyrule_uuid         = Column(UUID(as_uuid=False), primary_key=True)
    policyrule_kind         = Column(Enum(PolicyRuleKindEnum), nullable=False)
    policyrule_state        = Column(Enum(ORM_PolicyRuleStateEnum), nullable=False)
    policyrule_state_msg    = Column(String, nullable=False)
    policyrule_priority     = Column(Integer, nullable=False)
    policyrule_kpi_id       = Column(String, nullable=False)
    policyrule_service_uuid = Column(ForeignKey('service.service_uuid', ondelete='RESTRICT'), nullable=True, index=True)
    policyrule_eca_data     = Column(String, nullable=False)
    created_at              = Column(DateTime, nullable=False)
    updated_at              = Column(DateTime, nullable=False)

    policyrule_service = relationship('ServiceModel') # back_populates='policyrules'
    policyrule_devices = relationship('PolicyRuleDeviceModel' ) # back_populates='policyrule'

    __table_args__ = (
        CheckConstraint(policyrule_priority >= 0, name='check_priority_value'),
    )

    def dump_id(self) -> Dict:
        return {'uuid': {'uuid': self.policyrule_uuid}}

    def dump(self) -> Dict:
        # Load JSON-encoded Event-Condition-Action (ECA) model data and populate with policy basic details
        policyrule_basic = json.loads(self.policyrule_eca_data)
        policyrule_basic.update({
            'policyRuleId': self.dump_id(),
            'policyRuleState': {
                'policyRuleState': self.policyrule_state.value,
                'policyRuleStateMessage': self.policyrule_state_msg,
            },
            'priority': self.policyrule_priority,
            'kpiId': {'kpi_id': {'uuid': self.policyrule_kpi_id}},
        })
        result = {
            'policyRuleBasic': policyrule_basic,
            'deviceList': [{'device_uuid': {'uuid': pr_d.device_uuid}} for pr_d in self.policyrule_devices],
        }
        if self.policyrule_kind == PolicyRuleKindEnum.SERVICE:
            result['serviceId'] = self.policyrule_service.dump_id()
        return {self.policyrule_kind.value: result}

class PolicyRuleDeviceModel(_Base):
    __tablename__ = 'policyrule_device'

    policyrule_uuid = Column(ForeignKey('policyrule.policyrule_uuid', ondelete='RESTRICT'), primary_key=True)
    device_uuid     = Column(ForeignKey('device.device_uuid', ondelete='RESTRICT'), primary_key=True, index=True)

    #policyrule = relationship('PolicyRuleModel', lazy='joined') # back_populates='policyrule_devices'
    device     = relationship('DeviceModel',     lazy='selectin') # back_populates='policyrule_devices'
