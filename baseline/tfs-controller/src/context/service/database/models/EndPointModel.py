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
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from typing import Dict
from .enums.KpiSampleType import ORM_KpiSampleTypeEnum
from ._Base import _Base

class EndPointModel(_Base):
    __tablename__ = 'endpoint'

    endpoint_uuid     = Column(UUID(as_uuid=False), primary_key=True)
    device_uuid       = Column(ForeignKey('device.device_uuid',     ondelete='CASCADE' ), nullable=False, index=True)
    topology_uuid     = Column(ForeignKey('topology.topology_uuid', ondelete='RESTRICT'), nullable=False, index=True)
    name              = Column(String, nullable=False)
    endpoint_type     = Column(String, nullable=False)
    kpi_sample_types  = Column(ARRAY(Enum(ORM_KpiSampleTypeEnum), dimensions=1))
    created_at        = Column(DateTime, nullable=False)
    updated_at        = Column(DateTime, nullable=False)
    endpoint_location = Column(String, nullable=True)

    device                 = relationship('DeviceModel',              back_populates='endpoints') # lazy='selectin'
    topology               = relationship('TopologyModel',            lazy='selectin')
    optical_link_endpoints = relationship('OpticalLinkEndPointModel', back_populates='endpoint' )
    #link_endpoints    = relationship('LinkEndPointModel',    back_populates='endpoint' )
    #service_endpoints = relationship('ServiceEndPointModel', back_populates='endpoint' )

    def dump_id(self) -> Dict:
        result = {
            'topology_id'  : self.topology.dump_id(),
            'device_id'    : self.device.dump_id(),
            'endpoint_uuid': {'uuid': self.endpoint_uuid},
        }
        return result

    def dump(self) -> Dict:
        return {
            'endpoint_id'      : self.dump_id(),
            'name'             : self.name,
            'endpoint_type'    : self.endpoint_type,
            'kpi_sample_types' : [kst.value for kst in self.kpi_sample_types],
            'endpoint_location': json.loads(self.endpoint_location)
        }

    def dump_name(self) -> Dict:
        return {
            'endpoint_id'  : self.dump_id(),
            'device_name'  : self.device.device_name,
            'endpoint_name': self.name,
            'endpoint_type': self.endpoint_type,
        }
