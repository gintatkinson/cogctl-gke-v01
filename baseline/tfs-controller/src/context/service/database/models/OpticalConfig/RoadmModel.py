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

import logging
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from context.service.database.models._Base import _Base

class RoadmTypeModel(_Base):
    __tablename__      = 'roadm_type'
    roadm_uuid         = Column(String, primary_key=True)
    circuits           = Column(String, nullable=True)
    opticalconfig_uuid = Column(ForeignKey('optical_config.opticalconfig_uuid', ondelete='CASCADE'), index=True, nullable=False)
    channels           = relationship("ChannelModel")
    opticalconfig      = relationship('OpticalConfigModel', back_populates='roadms')
    interfaces         = relationship("ORInterfaceModel")

    def dump_id (self): 
        return {
            "roadm_uuid" : self.roadm_uuid
        }

    def dump (self):
        return {
            "channels"   : [channel.dump() for channel in self.channels],
            "roadm_uuid" : self.dump_id(),
            "interfaces" : [interface.dump() for interface in self.interfaces]
        }

class ChannelModel(_Base):
    __tablename__ = 'channel'

    channel_uuid        = Column(String,  primary_key=True)
    band_name           = Column(String,  nullable=True)
    lower_frequency     = Column(Integer, nullable=True)
    upper_frequency     = Column(Integer, nullable=True)
    channel_index       = Column(String,  nullable=True)
    status              = Column(String,  nullable=True)
    src_port            = Column(String,  nullable=True)
    dest_port           = Column(String,  nullable=True)
    type                = Column(String,  nullable=False)
    optical_band_parent = Column(String,  nullable=True)
    roadm_uuid          = Column(ForeignKey('roadm_type.roadm_uuid', ondelete='CASCADE'), nullable=False)
    roadm               = relationship('RoadmTypeModel',back_populates='channels')

    # opticalconfig_uuid = Column(ForeignKey('optical_config.opticalconfig_uuid', ondelete='CASCADE'), primary_key=True)
    # opticalconfig      = relationship('OpticalConfigModel', back_populates='channels')

    def dump_id (self ):
        return {
            "channel_uuid": {"uuid":self.channel_uuid}
        }

    def dump(self):
        return {
            "band_name"           : self.band_name,
            "lower_frequency"     : self.lower_frequency,
            "upper_frequency"     : self.upper_frequency,
            "type"                : self.type,
            "src_port"            : self.src_port,
            "dest_port"           : self.dest_port,
            "status"              : self.status,
            "optical_band_parent" : self.optical_band_parent,
            "channel_index"       : self.channel_index,
        }

class ORInterfaceModel (_Base): 
    __tablename__        =  'open_roadm_interface'

    interface_uuid       =  Column(String,  primary_key = True)
    name                 =  Column(String,  nullable = False)
    type                 =  Column(String,  nullable = True)
    administrative_state =  Column(String,  nullable = True)
    circuit_pack_name    =  Column(String,  nullable = True)
    port                 =  Column(String,  nullable = True)
    interface_list       =  Column(String,  nullable = True)
    frequency            =  Column(Float,   nullable = True)
    width                =  Column(Integer, nullable = True)
    roadm_uuid           =  Column(ForeignKey('roadm_type.roadm_uuid', ondelete='CASCADE'), nullable=False)
    roadm                =  relationship('RoadmTypeModel', back_populates='interfaces')

    def dump_id (self ):
        return {
            "interface_uuid": self.interface_uuid
        }

    def dump(self):
        return {
            "name"                : self.name,
            "type"                : self.type,
            "administrative_state": self.administrative_state,
            "circuit_pack_name"   : self.circuit_pack_name,
            "port"                : self.port,
            "interface_list"      : self.interface_list,
            "frequency"           : self.frequency,
            "width"               : self.width
        }
