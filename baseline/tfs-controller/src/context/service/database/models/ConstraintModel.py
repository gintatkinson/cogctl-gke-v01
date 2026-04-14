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
from .enums.ConstraintAction import ORM_ConstraintActionEnum
from ._Base import _Base

# Enum values should match name of field in Constraint message
# - enum item name should be Constraint message type in upper case
# - enum item value should be Constraint message type as it is in the proto files
class ConstraintKindEnum(enum.Enum):
    CUSTOM            = 'custom'
    SCHEDULE          = 'schedule'
    ENDPOINT_LOCATION = 'endpoint_location'
    ENDPOINT_PRIORITY = 'endpoint_priority'
    SLA_CAPACITY      = 'sla_capacity'
    SLA_LATENCY       = 'sla_latency'
    SLA_AVAILABILITY  = 'sla_availability'
    SLA_ISOLATION     = 'sla_isolation'
    QOS_PROFILE       = 'qos_profile'
    EXCLUSIONS        = 'exclusions'

class ServiceConstraintModel(_Base):
    __tablename__ = 'service_constraint'

    constraint_uuid = Column(UUID(as_uuid=False), primary_key=True)
    service_uuid    = Column(ForeignKey('service.service_uuid', ondelete='CASCADE'), nullable=False) #, index=True
    position        = Column(Integer, nullable=False)
    kind            = Column(Enum(ConstraintKindEnum), nullable=False)
    action          = Column(Enum(ORM_ConstraintActionEnum), nullable=False)
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

class SliceConstraintModel(_Base):
    __tablename__ = 'slice_constraint'

    constraint_uuid = Column(UUID(as_uuid=False), primary_key=True)
    slice_uuid      = Column(ForeignKey('slice.slice_uuid', ondelete='CASCADE'), nullable=False) #, index=True
    position        = Column(Integer, nullable=False)
    kind            = Column(Enum(ConstraintKindEnum), nullable=False)
    action          = Column(Enum(ORM_ConstraintActionEnum), nullable=False)
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
