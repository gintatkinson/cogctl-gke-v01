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
from sqlalchemy import (
    CheckConstraint, Boolean, Column, DateTime, Enum, Float, ForeignKey,
    Integer, String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from common.proto.context_pb2 import LinkTypeEnum
from ._Base import _Base
from .enums.LinkType import ORM_LinkTypeEnum

class LinkModel(_Base):
    __tablename__ = 'link'

    link_uuid           = Column(UUID(as_uuid=False), primary_key=True)
    link_name           = Column(String, nullable=False)
    link_type           = Column(Enum(ORM_LinkTypeEnum), nullable=False)
    total_capacity_gbps = Column(Float, nullable=True)
    used_capacity_gbps  = Column(Float, nullable=True)
    is_bidirectional    = Column(Boolean, default=False)
    created_at          = Column(DateTime, nullable=False)
    updated_at          = Column(DateTime, nullable=False)

    #topology_links = relationship('TopologyLinkModel', back_populates='link')
    link_endpoints = relationship('LinkEndPointModel') # lazy='joined', back_populates='link'

    __table_args__ = (
        CheckConstraint(total_capacity_gbps >= 0, name='check_value_total_capacity_gbps'),
        CheckConstraint(used_capacity_gbps  >= 0, name='check_value_used_capacity_gbps' ),
    )

    def dump_id(self) -> Dict:
        return {'link_uuid': {'uuid': self.link_uuid}}

    def dump(self) -> Dict:
        result = {
            'link_id'          : self.dump_id(),
            'name'             : self.link_name,
            'link_type'        : self.link_type.value,
            'link_endpoint_ids': [
                link_endpoint.endpoint.dump_id()
                for link_endpoint in sorted(self.link_endpoints, key=operator.attrgetter('position'))
            ],
        }
        if self.link_type is None:
            self.link_type = LinkTypeEnum.LINKTYPE_UNKNOWN
        attributes : Dict = result.setdefault('attributes', dict())
        attributes.setdefault('is_bidirectional', self.is_bidirectional)
        if self.total_capacity_gbps is not None:
            attributes.setdefault('total_capacity_gbps', self.total_capacity_gbps)
        if self.used_capacity_gbps is not None:
            attributes.setdefault('used_capacity_gbps', self.used_capacity_gbps)
        return result

class LinkEndPointModel(_Base):
    __tablename__ = 'link_endpoint'

    link_uuid     = Column(ForeignKey('link.link_uuid',         ondelete='CASCADE' ), primary_key=True)
    endpoint_uuid = Column(ForeignKey('endpoint.endpoint_uuid', ondelete='RESTRICT'), primary_key=True, index=True)
    position      = Column(Integer, nullable=False)

    link     = relationship('LinkModel',     back_populates='link_endpoints') #, lazy='selectin'
    endpoint = relationship('EndPointModel', lazy='selectin') # back_populates='link_endpoints'

    __table_args__ = (
        CheckConstraint(position >= 0, name='check_position_value'),
    )
