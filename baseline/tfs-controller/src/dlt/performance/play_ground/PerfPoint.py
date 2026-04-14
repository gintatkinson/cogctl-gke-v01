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

from typing import Dict, Optional
from .Enums import ActionEnum, RecordTypeEnum

class PerfPoint:
    def __init__(self, action : ActionEnum, record_type : RecordTypeEnum, record_uuid : str) -> None:
        self.action           : ActionEnum      = action
        self.record_type      : RecordTypeEnum  = record_type
        self.record_uuid      : str             = record_uuid
        self.size_bytes       : Optional[int  ] = None
        self.num_endpoints    : Optional[int  ] = None
        self.num_config_rules : Optional[int  ] = None
        self.num_constraints  : Optional[int  ] = None
        self.num_sub_services : Optional[int  ] = None
        self.num_sub_slices   : Optional[int  ] = None
        self.time_requested   : Optional[float] = None
        self.time_replied     : Optional[float] = None
        self.time_notified    : Optional[float] = None

    def set_size_bytes      (self, size_bytes       : int) -> None: self.size_bytes       = size_bytes
    def set_num_endpoints   (self, num_endpoints    : int) -> None: self.num_endpoints    = num_endpoints
    def set_num_config_rules(self, num_config_rules : int) -> None: self.num_config_rules = num_config_rules
    def set_num_constraints (self, num_constraints  : int) -> None: self.num_constraints  = num_constraints
    def set_num_sub_services(self, num_sub_services : int) -> None: self.num_sub_services = num_sub_services
    def set_num_sub_slices  (self, num_sub_slices   : int) -> None: self.num_sub_slices   = num_sub_slices

    def set_time_requested(self, timestamp : float) -> None: self.time_requested = timestamp
    def set_time_replied  (self, timestamp : float) -> None: self.time_replied   = timestamp
    def set_time_notified (self, timestamp : float) -> None: self.time_notified  = timestamp

    def to_dict(self) -> Dict:
        exec_time, event_delay = None, None
        if self.time_replied is not None and self.time_requested is not None:
            exec_time = self.time_replied - self.time_requested
            if self.time_notified is not None:
                event_delay = self.time_notified - self.time_requested

        return {
            'action'          : self.action.value,
            'record_type'     : self.record_type.value,
            'record_uuid'     : self.record_uuid,
            'size_bytes'      : self.size_bytes,
            'num_endpoints'   : self.num_endpoints,
            'num_config_rules': self.num_config_rules,
            'num_constraints' : self.num_constraints,
            'num_sub_services': self.num_sub_services,
            'num_sub_slices'  : self.num_sub_slices,
            'time_requested'  : self.time_requested,
            'time_replied'    : self.time_replied,
            'time_notified'   : self.time_notified,
            'exec_time'       : exec_time,
            'event_delay'     : event_delay,
        }
