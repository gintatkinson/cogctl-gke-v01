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

from nbi.service.NbiApplication import NbiApplication
from .Hardware import Hardware
from .HardwareMultipleDevices import HardwareMultipleDevices

URL_PREFIX = '/restconf/data'

def register_ietf_hardware(nbi_app : NbiApplication):
    nbi_app.add_rest_api_resource(
        Hardware,
        URL_PREFIX + '/device=<path:device_uuid>/ietf-network-hardware-inventory:network-hardware-inventory'
    )
    nbi_app.add_rest_api_resource(
        HardwareMultipleDevices,
        URL_PREFIX + '/ietf-network-hardware-inventory:network-hardware-inventory'
    )
