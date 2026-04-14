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
    Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from ._Base import _Base
from .Slot import C_Slot, S_Slot, L_Slot

class OpticalLinkModel(_Base):
    __tablename__ = 'opticallink'

    opticallink_uuid          = Column(UUID(as_uuid=False), primary_key=True)
    name                      = Column(String, nullable=False)
    created_at                = Column(DateTime, nullable=False)
    updated_at                = Column(DateTime, nullable=False)
    length                    = Column(Integer, nullable=True)
    src_port                  = Column(String, nullable=True)
    dst_port                  = Column(String, nullable=True)
    local_peer_port           = Column(String, nullable=True)
    remote_peer_port          = Column(String, nullable=True)
    used                      = Column(Boolean ,nullable=True)
    c_slots                   = Column (C_Slot,nullable=True)
    l_slots                   = Column (L_Slot,nullable=True)
    s_slots                   = Column (S_Slot,nullable=True)
    opticallink_endpoints     = relationship('OpticalLinkEndPointModel')
    topology_optical_links    = relationship('TopologyOpticalLinkModel', back_populates='optical_link')

    def dump_id(self) -> Dict:
        return {'link_uuid': {'uuid': self.opticallink_uuid}}

    def dump(self) -> Dict:
        result = {
            'link_id'            : self.dump_id(),
            'name'               : self.name,
            'optical_details'    : {
                'length'           : self.length,
                'src_port'         : self.src_port,
                'dst_port'         : self.dst_port,
                'local_peer_port'  : self.local_peer_port,
                'remote_peer_port' : self.remote_peer_port,
                'used'             : self.used,
                'c_slots'          : self.c_slots if self.c_slots is not None else {},
                'l_slots'          : self.l_slots if self.l_slots is not None else {},
                's_slots'          : self.s_slots if self.s_slots is not None else {},
            },
            'link_endpoint_ids' : [
                optical_endpoint.endpoint.dump_id()
                for optical_endpoint in sorted(self.opticallink_endpoints, key=operator.attrgetter('position'))
            ],
        }
        return result

class OpticalLinkEndPointModel(_Base):
    __tablename__ = 'opticallink_endpoint'

    link_uuid     = Column(ForeignKey('opticallink.opticallink_uuid', ondelete='CASCADE' ), primary_key=True)
    endpoint_uuid = Column(ForeignKey('endpoint.endpoint_uuid',       ondelete='RESTRICT'), primary_key=True, index=True)
    position      = Column(Integer, nullable=False)

    optical_link  = relationship('OpticalLinkModel', back_populates='opticallink_endpoints')
    endpoint      = relationship('EndPointModel',    lazy='selectin')

    __table_args__ = (
        CheckConstraint(position >= 0, name='check_position_value'),
    )
