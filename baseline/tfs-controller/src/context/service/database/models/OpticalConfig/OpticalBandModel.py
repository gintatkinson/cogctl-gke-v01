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
from context.service.database.models._Base import _Base

LOGGER = logging.getLogger(__name__)

class OpticalBandModel(_Base):
    __tablename__ = 'opticalband'

    ob_uuid = Column(UUID(as_uuid=False), primary_key=True)
    connection_uuid     = Column(ForeignKey('connection.connection_uuid', ondelete='CASCADE'), nullable=False)
    channel_uuid        = Column(ForeignKey('channel.channel_uuid', ondelete='CASCADE'), nullable=False)
    created_at          = Column(DateTime, nullable=False)
    ob_channel          = relationship('ChannelModel') # back_populates='connections'
    ob_connection       = relationship('ConnectionModel') # lazy='joined', back_populates='connection'
   
    def dump_id(self) -> Dict:
        return {'opticalband_uuid': {'uuid': self.ob_uuid}}

    def dump(self) -> Dict:
        return {
            'opticalband_id': self.dump_id(),
            'channel_id'    : self.ob_channel.dump_id(),
            'connection_id' : self.ob_connection.dump_id(),
            'service_id'    : self.ob_connection.connection_service.dump_id(),
            'channel'       : json.dumps(self.ob_channel.dump()),
            'connection'    : self.ob_connection.dump(),
            "service"       : self.ob_connection.connection_service.dump()
            
        }

