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
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from context.service.database.models._Base import _Base

class OpticalConfigModel(_Base):
    __tablename__ = 'optical_config'
    opticalconfig_uuid = Column(String,        primary_key = True)
    channel_namespace  = Column(String,        nullable    = True)
    endpoints          = Column(ARRAY(String), nullable    = True)
    type               = Column(String,        nullable    = False)

    # transcievers   = Column(ARRAY(String), nullable=True)
    # interfaces     = Column(String, nullable=True)
    # channels       = relationship("OpticalChannelModel")
    transponders   = relationship("TransponderTypeModel")
    roadms         = relationship("RoadmTypeModel")

    device_uuid = Column(ForeignKey("device.device_uuid",ondelete="CASCADE"),index=True ,nullable=False)
    device = relationship("DeviceModel",  back_populates='optical_config')

    def dump_id (self ):
        return {
            "opticalconfig_uuid":self.opticalconfig_uuid,
            "device_uuid" :self.device_uuid
        }

    def dump(self):
        obj={
            # "channels"          : [channel.dump() for channel in self.channels],
            # "transceivers"      : {"transceiver": [transciever for transciever in self.transcievers]},
            # "interfaces"        : {"interface":json.loads(self.interfaces) if self.interfaces else ''},
            "channel_namespace" : self.channel_namespace,
            "endpoints"         : [json.loads(endpoint) for endpoint in self.endpoints if endpoint],
            "device_name"       : self.device.device_name,
            "type"              : self.type
        }
        if self.type =="optical-transponder" :
            channels = [transponer.dump() for transponer in self.transponders][0]
            obj['channels'       ] = channels.get('channels',        None)
            obj['transceivers'   ] = channels.get('transceivers',    None)
            obj['interfaces'     ] = channels.get('interfaces',      None)
            obj['trasponder_uuid'] = channels.get('trasponder_uuid', None)
            
        if self.type =="optical-roadm" :
            dev = [roadms.dump() for roadms in self.roadms][0]
            obj['channels'  ] = dev.get('channels',   None)
            obj['roadm_uuid'] = dev.get('roadm_uuid', None)

        if self.type =="openroadm" :
            dev = [roadms.dump() for roadms in self.roadms][0]
            obj['interfaces'] = dev.get('interfaces', None)
            obj['roadm_uuid'] = dev.get('roadm_uuid', None)

        return obj
