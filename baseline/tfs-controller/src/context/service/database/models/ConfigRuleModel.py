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
from typing import Dict
from .enums.ConfigAction import ORM_ConfigActionEnum
from ._Base import _Base

# Enum values should match name of field in ConfigRule message
class ConfigRuleKindEnum(enum.Enum):
    CUSTOM   = 'custom'
    ACL      = 'acl'
    IP_LINK  = 'ip_link'
    IPOWDM   = 'ipowdm'
    TAPI_LSP = 'tapi_lsp'

class DeviceConfigRuleModel(_Base):
    __tablename__ = 'device_configrule'

    configrule_uuid = Column(UUID(as_uuid=False), primary_key=True)
    device_uuid     = Column(ForeignKey('device.device_uuid', ondelete='CASCADE'), nullable=False) #, index=True
    position        = Column(Integer, nullable=False)
    kind            = Column(Enum(ConfigRuleKindEnum), nullable=False)
    action          = Column(Enum(ORM_ConfigActionEnum), nullable=False)
    data            = Column(String, nullable=False)
    created_at      = Column(DateTime, nullable=False)
    updated_at      = Column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint(position >= 0, name='check_position_value'),
        #UniqueConstraint('device_uuid',  'position', name='unique_per_device' ),
    )

    def dump(self) -> Dict:
        return {
            'action': self.action.value,
            self.kind.value: json.loads(self.data),
        }

class ServiceConfigRuleModel(_Base):
    __tablename__ = 'service_configrule'

    configrule_uuid = Column(UUID(as_uuid=False), primary_key=True)
    service_uuid    = Column(ForeignKey('service.service_uuid', ondelete='CASCADE'), nullable=False) #, index=True
    position        = Column(Integer, nullable=False)
    kind            = Column(Enum(ConfigRuleKindEnum), nullable=False)
    action          = Column(Enum(ORM_ConfigActionEnum), nullable=False)
    data            = Column(String, nullable=False)
    created_at      = Column(DateTime, nullable=False)
    updated_at      = Column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint(position >= 0, name='check_position_value'),
        #UniqueConstraint('service_uuid', 'position', name='unique_per_service'),
    )

    def dump(self) -> Dict:
        return {
            'action': self.action.value,
            self.kind.value: json.loads(self.data),
        }

class SliceConfigRuleModel(_Base):
    __tablename__ = 'slice_configrule'

    configrule_uuid = Column(UUID(as_uuid=False), primary_key=True)
    slice_uuid      = Column(ForeignKey('slice.slice_uuid', ondelete='CASCADE'), nullable=False) #, index=True
    position        = Column(Integer, nullable=False)
    kind            = Column(Enum(ConfigRuleKindEnum), nullable=False)
    action          = Column(Enum(ORM_ConfigActionEnum), nullable=False)
    data            = Column(String, nullable=False)
    created_at      = Column(DateTime, nullable=False)
    updated_at      = Column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint(position >= 0, name='check_position_value'),
        #UniqueConstraint('slice_uuid',   'position', name='unique_per_slice'  ),
    )

    def dump(self) -> Dict:
        return {
            'action': self.action.value,
            self.kind.value: json.loads(self.data),
        }
