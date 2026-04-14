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

import json
from sqlalchemy import Column, String, Integer , ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from context.service.database.models._Base import _Base

class TransponderTypeModel (_Base):
    __tablename__ = 'transponder_type'

    transponder_uuid   = Column(String, primary_key=True)
    transcievers       = Column(ARRAY(String), nullable=True)
  
    opticalconfig_uuid = Column(ForeignKey('optical_config.opticalconfig_uuid', ondelete='CASCADE'), index=True, nullable=False)
    
    interfaces         =   relationship("TransponderInterfaceModel")
    channels           = relationship("OpticalChannelModel")
    opticalconfig      = relationship('OpticalConfigModel', back_populates='transponders')

    def dump_id (self): 
        return {
            "transponder_uuid": self.transponder_uuid
        }

    def dump (self):
        return {
            "channels"        : [channel.dump() for channel in self.channels],
            "transceivers"    : {"transceiver": [transciever for transciever in self.transcievers]},
            "interfaces"        : [interface.dump() for interface in self.interfaces],
            "trasponder_uuid" : self.dump_id()
        }

class OpticalChannelModel(_Base):
    __tablename__ = 'optical_channel'

    channel_uuid        = Column(String,  primary_key=True)
    channel_name        = Column(String,  nullable=True)
    frequency           = Column(Integer, nullable=True)
    operational_mode    = Column(Integer, nullable=True)
    status              = Column(String,  nullable=True)
    target_output_power = Column(String,  nullable=True)
    transponder_uuid    = Column(ForeignKey('transponder_type.transponder_uuid', ondelete='CASCADE'), nullable=False)
    transponder         = relationship('TransponderTypeModel', back_populates='channels')

    # opticalconfig_uuid = Column(ForeignKey('optical_config.opticalconfig_uuid', ondelete='CASCADE'), primary_key=True)
    # opticalconfig      = relationship('OpticalConfigModel', back_populates='channels')

    def dump_id (self ):
        return {
            "channel_uuid": self.channel_uuid
        }

    def dump(self):
        return {
            "name"                : {'index':self.channel_name},
            "frequency"           : self.frequency,
            "target-output-power" : self.target_output_power,
            "operational-mode"    : self.operational_mode,
            "status"              : self.status,
        }


class TransponderInterfaceModel(_Base):
    __tablename__           =      'transponder_interface'
    interface_uuid          =       Column(String, primary_key=True)
    
    name                    =       Column (String,nullable=True)
    status                  =       Column(String , nullable=True)
    operation_status        =       Column(String , nullable=True)
    ifindex                 =       Column(Integer, nullable=True)
    in_octets               =       Column(Integer, nullable=True)
    in_pkts                 =       Column(Integer, nullable=True)
    in_unicast_pkts         =       Column(Integer, nullable=True)
    in_broadcast_pkts       =       Column(Integer, nullable=True)
    in_multicast_pkts       =       Column(Integer, nullable=True)
    out_discards            =       Column(Integer, nullable=True)
    out_errors              =       Column(Integer, nullable=True)
    in_discards            =       Column(Integer, nullable=True)
    in_errors              =       Column(Integer, nullable=True)
    out_octets              =       Column(Integer, nullable=True)
    out_pkts                =       Column(Integer, nullable=True)
    out_unicast_pkts        =       Column(Integer, nullable=True)
    out_broadcast_pkts      =       Column(Integer, nullable=True)
    out_multicast_pkts      =       Column(Integer, nullable=True)
   
   
    last_clear              =       Column(Integer, nullable=True)
   
    
    transponder_uuid      =       Column(ForeignKey('transponder_type.transponder_uuid', ondelete='CASCADE' ),nullable=False)
    transponder           =       relationship('TransponderTypeModel',back_populates='interfaces')
    # opticalconfig_uuid        = Column(ForeignKey('optical_config.opticalconfig_uuid',         ondelete='CASCADE' ), primary_key=True)
    # opticalconfig             = relationship('OpticalConfigModel',     back_populates='channels')
    def dump_id (self ):
        return {
            "interface_uuid":self.interface_uuid
        }

    def dump(self):
        return {
            "name"      :self.name,
           "status":self.status,
            "operation_status":self.operation_status,
            "ifindex":self.ifindex,
            "in_octets":self.in_octets,
            "in_pkts":self.in_pkts,
            "in_unicast_pkts":self.in_unicast_pkts,
            "in_broadcast_pkts":self.in_broadcast_pkts,
            "in_multicast_pkts":self.in_multicast_pkts,
            "in_discards":self.in_discards,
            "in_errors":self.in_errors,
            "out_discards":self.out_discards,
            "out_errors":self.out_errors,
            "out_octets":self.out_octets,
            "out_pkts":self.out_pkts,
            "out_unicast_pkts":self.out_unicast_pkts,
            "out_broadcast_pkts":self.out_broadcast_pkts,
            "out_multicast_pkts":self.out_multicast_pkts,
            "last_clear":self.last_clear
        }
