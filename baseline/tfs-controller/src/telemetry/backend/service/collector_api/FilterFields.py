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

from enum import Enum
from typing import Any, Dict, Optional
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import Device, DeviceDriverEnum

class FilterFieldEnum(Enum):
    DEVICE_TYPE   = 'device_type'
    DRIVER        = 'driver'
    VENDOR        = 'vendor'
    MODEL         = 'model'
    SERIAL_NUMBER = 'serial_number'

# Map allowed filter fields to allowed values per Filter field. If no restriction (free text) None is specified
FILTER_FIELD_ALLOWED_VALUES = {
    FilterFieldEnum.DEVICE_TYPE.value   : {i.value for i in DeviceTypeEnum},
    FilterFieldEnum.DRIVER.value        : set(DeviceDriverEnum.values()),
    FilterFieldEnum.VENDOR.value        : None,
    FilterFieldEnum.MODEL.value         : None,
    FilterFieldEnum.SERIAL_NUMBER.value : None,
}

def get_device_driver_filter_fields(device : Optional[Device]) -> Dict[FilterFieldEnum, Any]:
    if device is None: return {}
    return {
        FilterFieldEnum.DEVICE_TYPE: device.device_type,
        FilterFieldEnum.DRIVER     : [driver for driver in device.device_drivers],
    }
