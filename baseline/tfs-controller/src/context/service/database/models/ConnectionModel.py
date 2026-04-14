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

import json, logging, operator
from sqlalchemy import Column, DateTime, ForeignKey, Integer, CheckConstraint, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from ._Base import _Base

LOGGER = logging.getLogger(__name__)

class ConnectionModel(_Base):
    __tablename__ = 'connection'

    connection_uuid = Column(UUID(as_uuid=False), primary_key=True)
    service_uuid    = Column(ForeignKey('service.service_uuid', ondelete='RESTRICT'), nullable=False, index=True)
    settings        = Column(String, nullable=False)
    created_at      = Column(DateTime, nullable=False)
    updated_at      = Column(DateTime, nullable=False)

    connection_service     = relationship('ServiceModel') # back_populates='connections'
    connection_endpoints   = relationship('ConnectionEndPointModel') # lazy='joined', back_populates='connection'
    connection_subservices = relationship('ConnectionSubServiceModel') # lazy='joined', back_populates='connection'

    def dump_id(self) -> Dict:
        return {'connection_uuid': {'uuid': self.connection_uuid}}

    def dump(self) -> Dict:
        return {
            'connection_id'         : self.dump_id(),
            'service_id'            : self.connection_service.dump_id(),
            'settings'              : json.loads(self.settings),
            'path_hops_endpoint_ids': [
                c_ep.endpoint.dump_id()
                for c_ep in sorted(self.connection_endpoints, key=operator.attrgetter('position'))
            ],
            'sub_service_ids'       : [
                c_ss.subservice.dump_id()
                for c_ss in self.connection_subservices
            ],
        }

class ConnectionEndPointModel(_Base):
    __tablename__ = 'connection_endpoint'

    connection_uuid = Column(ForeignKey('connection.connection_uuid', ondelete='CASCADE' ), primary_key=True)
    endpoint_uuid   = Column(ForeignKey('endpoint.endpoint_uuid', ondelete='RESTRICT'), primary_key=True, index=True)
    position        = Column(Integer, nullable=False)

    connection = relationship('ConnectionModel', back_populates='connection_endpoints') #, lazy='joined'
    endpoint   = relationship('EndPointModel',   lazy='selectin') # back_populates='connection_endpoints'

    __table_args__ = (
        CheckConstraint(position >= 0, name='check_position_value'),
    )

class ConnectionSubServiceModel(_Base):
    __tablename__ = 'connection_subservice'

    connection_uuid = Column(ForeignKey('connection.connection_uuid', ondelete='CASCADE' ), primary_key=True)
    subservice_uuid = Column(ForeignKey('service.service_uuid', ondelete='RESTRICT'), primary_key=True, index=True)

    connection = relationship('ConnectionModel', back_populates='connection_subservices') #, lazy='joined'
    subservice = relationship('ServiceModel',    lazy='selectin') # back_populates='connection_subservices'
