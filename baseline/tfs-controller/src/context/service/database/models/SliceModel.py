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
from .enums.SliceStatus import ORM_SliceStatusEnum
from ._Base import _Base

class SliceModel(_Base):
    __tablename__ = 'slice'

    slice_uuid         = Column(UUID(as_uuid=False), primary_key=True)
    context_uuid       = Column(ForeignKey('context.context_uuid'), nullable=False, index=True)
    slice_name         = Column(String, nullable=True)
    slice_status       = Column(Enum(ORM_SliceStatusEnum), nullable=False)
    slice_owner_uuid   = Column(String, nullable=True)
    slice_owner_string = Column(String, nullable=True)
    created_at         = Column(DateTime, nullable=False)
    updated_at         = Column(DateTime, nullable=False)

    context         = relationship('ContextModel', back_populates='slices', lazy='selectin')
    slice_endpoints = relationship('SliceEndPointModel') # lazy='selectin', back_populates='slice'
    slice_services  = relationship('SliceServiceModel') # lazy='selectin', back_populates='slice'
    slice_subslices = relationship(
        'SliceSubSliceModel', primaryjoin='slice.c.slice_uuid == slice_subslice.c.slice_uuid')
    constraints     = relationship('SliceConstraintModel', passive_deletes=True) # lazy='selectin', back_populates='slice'
    config_rules    = relationship('SliceConfigRuleModel', passive_deletes=True) # lazy='selectin', back_populates='slice'

    def dump_id(self) -> Dict:
        return {
            'context_id': self.context.dump_id(),
            'slice_uuid': {'uuid': self.slice_uuid},
        }

    def dump_endpoint_ids(self) -> List[Dict]:
        return [
            slice_endpoint.endpoint.dump_id()
            for slice_endpoint in sorted(self.slice_endpoints, key=operator.attrgetter('position'))
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

    def dump_service_ids(self) -> List[Dict]:
        return [
            slice_service.service.dump_id()
            for slice_service in self.slice_services
        ]

    def dump_subslice_ids(self) -> List[Dict]:
        return [
            slice_subslice.subslice.dump_id()
            for slice_subslice in self.slice_subslices
        ]

    def dump_owner_id(self) -> Dict:
        return {
            'owner_uuid': {'uuid': self.slice_owner_uuid},
            'owner_string': self.slice_owner_string
        }

    def dump(
        self, include_endpoint_ids : bool = True, include_constraints : bool = True, include_service_ids : bool = True,
        include_subslice_ids : bool = True, include_config_rules : bool = True
    ) -> Dict:
        result = {
            'slice_id'    : self.dump_id(),
            'name'        : self.slice_name,
            'slice_status': {'slice_status': self.slice_status.value},
            'slice_owner' : self.dump_owner_id()
        }
        if include_endpoint_ids: result['slice_endpoint_ids'] = self.dump_endpoint_ids()
        if include_constraints : result['slice_constraints' ] = self.dump_constraints()
        if include_service_ids : result['slice_service_ids' ] = self.dump_service_ids()
        if include_subslice_ids: result['slice_subslice_ids'] = self.dump_subslice_ids()
        if include_config_rules: result['slice_config'      ] = self.dump_config_rules()
        return result

class SliceEndPointModel(_Base):
    __tablename__ = 'slice_endpoint'

    slice_uuid    = Column(ForeignKey('slice.slice_uuid',       ondelete='CASCADE' ), primary_key=True)
    endpoint_uuid = Column(ForeignKey('endpoint.endpoint_uuid', ondelete='RESTRICT'), primary_key=True, index=True)
    position      = Column(Integer, nullable=False)

    slice    = relationship('SliceModel', back_populates='slice_endpoints') #, lazy='selectin'
    endpoint = relationship('EndPointModel', lazy='selectin') # back_populates='slice_endpoints'

    __table_args__ = (
        CheckConstraint(position >= 0, name='check_position_value'),
    )

class SliceServiceModel(_Base):
    __tablename__ = 'slice_service'

    slice_uuid   = Column(ForeignKey('slice.slice_uuid',     ondelete='CASCADE' ), primary_key=True)
    service_uuid = Column(ForeignKey('service.service_uuid', ondelete='RESTRICT'), primary_key=True, index=True)

    slice   = relationship('SliceModel', back_populates='slice_services') # , lazy='selectin'
    service = relationship('ServiceModel', lazy='selectin') # back_populates='slice_services'

class SliceSubSliceModel(_Base):
    __tablename__ = 'slice_subslice'

    slice_uuid    = Column(ForeignKey('slice.slice_uuid', ondelete='CASCADE'), primary_key=True, index=True)
    subslice_uuid = Column(ForeignKey('slice.slice_uuid', ondelete='CASCADE'), primary_key=True, index=True)

    slice    = relationship(
        'SliceModel', foreign_keys='SliceSubSliceModel.slice_uuid', back_populates='slice_subslices') #, lazy='selectin'
    subslice = relationship('SliceModel', foreign_keys='SliceSubSliceModel.subslice_uuid', lazy='selectin')
