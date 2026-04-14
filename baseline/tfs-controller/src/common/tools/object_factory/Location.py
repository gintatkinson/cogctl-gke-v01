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

import copy
from typing import Dict, Optional


def json_gps_position(latitude : float, longitude : float):
    return {'latitude': latitude, 'longitude': longitude}

def json_location(region : Optional[str] = None, gps_position : Optional[Dict] = None):
    if not region and not gps_position:
        raise Exception('One of "region" or "gps_position" arguments must be filled')
    if region:
        result = {'region': region}
    else:
        result = {'gps_position': copy.deepcopy(gps_position)}

    return result
