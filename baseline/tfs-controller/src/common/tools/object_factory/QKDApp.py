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
from typing import Dict, List, Optional
from common.Constants import DEFAULT_CONTEXT_NAME
from common.tools.object_factory.Context import json_context_id


def json_app_id(app_uuid : str, context_id : Optional[Dict] = None) -> Dict:
    result = {'app_uuid': {'uuid': app_uuid}}
    if context_id is not None: result['context_id'] = copy.deepcopy(context_id)
    return result
