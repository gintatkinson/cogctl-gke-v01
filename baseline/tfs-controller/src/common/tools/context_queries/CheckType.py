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

from typing import Union
from common.DeviceTypes import DeviceTypeEnum

def device_type_is_datacenter(device_type : Union[str, DeviceTypeEnum]) -> bool:
    return device_type in {
        DeviceTypeEnum.DATACENTER, DeviceTypeEnum.DATACENTER.value,
        DeviceTypeEnum.EMULATED_DATACENTER, DeviceTypeEnum.EMULATED_DATACENTER.value
    }

def device_type_is_network(device_type : Union[str, DeviceTypeEnum]) -> bool:
    return device_type in {DeviceTypeEnum.NETWORK, DeviceTypeEnum.NETWORK.value}

def endpoint_type_is_border(endpoint_type : str) -> bool:
    return str(endpoint_type).endswith('/border')
