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

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from ._Base import _Base

class TopologyModel(_Base):
    __tablename__ = 'topology'

    topology_uuid = Column(UUID(as_uuid=False), primary_key=True)
    context_uuid  = Column(ForeignKey('context.context_uuid'), nullable=False, index=True)
    topology_name = Column(String, nullable=False)
    created_at    = Column(DateTime, nullable=False)
    updated_at    = Column(DateTime, nullable=False)

    context                = relationship('ContextModel', back_populates='topologies', lazy='selectin')
    topology_devices       = relationship('TopologyDeviceModel') # back_populates='topology'
    topology_links         = relationship('TopologyLinkModel'  ) # back_populates='topology'
    topology_optical_links = relationship("TopologyOpticalLinkModel")

    def dump_id(self) -> Dict:
        return {
            'context_id': self.context.dump_id(),
            'topology_uuid': {'uuid': self.topology_uuid},
        }

    def dump(self) -> Dict:
        return {
            'topology_id'     : self.dump_id(),
            'name'            : self.topology_name,
            'device_ids'      : [{'device_uuid': {'uuid': td.device_uuid      }} for td in self.topology_devices      ],
            'link_ids'        : [{'link_uuid'  : {'uuid': tl.link_uuid        }} for tl in self.topology_links        ],
            'optical_link_ids': [{'link_uuid'  : {'uuid': to.optical_link_uuid}} for to in self.topology_optical_links],
        }

    def dump_details(self) -> Dict:
        devices = [
            td.device.dump(include_config_rules=False, include_components=False)
            for td in self.topology_devices
        ]
        links = [
            tl.link.dump()
            for tl in self.topology_links
        ]
        optical_links=[
            ol.optical_link.dump() 
            for ol in self.topology_optical_links
        ]
        return {
            'topology_id'  : self.dump_id(),
            'name'         : self.topology_name,
            'devices'      : devices,
            'links'        : links,
            'optical_links': optical_links,
        }

class TopologyDeviceModel(_Base):
    __tablename__ = 'topology_device'

    topology_uuid = Column(ForeignKey('topology.topology_uuid', ondelete='RESTRICT'), primary_key=True, index=True)
    device_uuid   = Column(ForeignKey('device.device_uuid',     ondelete='CASCADE' ), primary_key=True, index=True)

    topology = relationship('TopologyModel', lazy='selectin', viewonly=True) # back_populates='topology_devices'
    device   = relationship('DeviceModel',   lazy='selectin') # back_populates='topology_devices'

class TopologyLinkModel(_Base):
    __tablename__ = 'topology_link'

    topology_uuid = Column(ForeignKey('topology.topology_uuid', ondelete='RESTRICT'), primary_key=True, index=True)
    link_uuid     = Column(ForeignKey('link.link_uuid',         ondelete='CASCADE' ), primary_key=True, index=True)

    topology = relationship('TopologyModel', lazy='selectin', viewonly=True) # back_populates='topology_links'
    link     = relationship('LinkModel',     lazy='selectin') # back_populates='topology_links'

#---------------------------------------- Experimental ---------------------------------------

class TopologyOpticalLinkModel(_Base):
    __tablename__ = 'topology_optical_link'

    topology_uuid     = Column(ForeignKey('topology.topology_uuid',       ondelete='RESTRICT'), primary_key=True, index=True)
    optical_link_uuid = Column(ForeignKey('opticallink.opticallink_uuid', ondelete='CASCADE' ), primary_key=True, index=True)

    topology     = relationship('TopologyModel',    lazy='selectin', viewonly=True) # back_populates='topology_optical_links'
    optical_link = relationship('OpticalLinkModel', lazy='selectin') # back_populates='topology_optical_links'
