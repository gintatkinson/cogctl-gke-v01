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
from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict, List
from .enums.ServiceStatus import ORM_ServiceStatusEnum
from .enums.ServiceType import ORM_ServiceTypeEnum
from ._Base import _Base

class ServiceModel(_Base):
    __tablename__ = 'service'

    service_uuid   = Column(UUID(as_uuid=False), primary_key=True)
    context_uuid   = Column(ForeignKey('context.context_uuid'), nullable=False, index=True)
    service_name   = Column(String, nullable=False)
    service_type   = Column(Enum(ORM_ServiceTypeEnum), nullable=False)
    service_status = Column(Enum(ORM_ServiceStatusEnum), nullable=False)
    created_at     = Column(DateTime, nullable=False)
    updated_at     = Column(DateTime, nullable=False)

    context           = relationship('ContextModel', back_populates='services', lazy='selectin')
    service_endpoints = relationship('ServiceEndPointModel') # lazy='selectin', back_populates='service'
    constraints       = relationship('ServiceConstraintModel', passive_deletes=True) # lazy='selectin', back_populates='service'
    config_rules      = relationship('ServiceConfigRuleModel', passive_deletes=True) # lazy='selectin', back_populates='service'

    def dump_id(self) -> Dict:
        return {
            'context_id': self.context.dump_id(),
            'service_uuid': {'uuid': self.service_uuid},
        }

    def dump_endpoint_ids(self) -> List[Dict]:
        return [
            service_endpoint.endpoint.dump_id()
            for service_endpoint in sorted(self.service_endpoints, key=operator.attrgetter('position'))
        ]

    def dump_constraints(self) -> List[Dict]:
        return [
            constraint.dump()
            for constraint in sorted(self.constraints, key=operator.attrgetter('position'))
        ]

    def dump_config_rules(self) -> Dict:
        return {'config_rules': [
            config_rule.dump()
            for config_rule in sorted(self.config_rules, key=operator.attrgetter('position'))
        ]}

    def dump(
        self, include_endpoint_ids : bool = True, include_constraints : bool = True, include_config_rules : bool = True
    ) -> Dict:
        result = {
            'service_id'    : self.dump_id(),
            'name'          : self.service_name,
            'service_type'  : self.service_type.value,
            'service_status': {'service_status': self.service_status.value},
        }
        if include_endpoint_ids: result['service_endpoint_ids'] = self.dump_endpoint_ids()
        if include_constraints: result['service_constraints'] = self.dump_constraints()
        if include_config_rules: result['service_config'] = self.dump_config_rules()
        return result

class ServiceEndPointModel(_Base):
    __tablename__ = 'service_endpoint'

    service_uuid  = Column(ForeignKey('service.service_uuid',   ondelete='CASCADE' ), primary_key=True)
    endpoint_uuid = Column(ForeignKey('endpoint.endpoint_uuid', ondelete='RESTRICT'), primary_key=True, index=True)
    position      = Column(Integer, nullable=False)

    service  = relationship('ServiceModel',  back_populates='service_endpoints') # lazy='selectin'
    endpoint = relationship('EndPointModel', lazy='selectin') # back_populates='service_endpoints'

    __table_args__ = (
        CheckConstraint(position >= 0, name='check_position_value'),
    )
