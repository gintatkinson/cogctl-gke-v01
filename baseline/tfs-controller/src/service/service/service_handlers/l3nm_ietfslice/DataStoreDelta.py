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
from deepdiff import DeepDiff
from typing import Dict, Optional
from common.proto.context_pb2 import Service


RUNNING_RESOURCE_KEY   = 'running_ietf_slice'
CANDIDATE_RESOURCE_KEY = 'candidate_ietf_slice'


class DataStoreDelta:
    def __init__(self, service : Service):
        self._service = service
        self._service_config = service.service_config
        self._candidate_data = self._get_datastore_data(CANDIDATE_RESOURCE_KEY)
        self._running_data   = self._get_datastore_data(RUNNING_RESOURCE_KEY  )

    def _get_datastore_data(self, resource_key : str) -> Optional[Dict]:
        for cr in self._service_config.config_rules:
            if cr.WhichOneof('config_rule') != 'custom': continue
            if cr.custom.resource_key != resource_key: continue
            resource_value = json.loads(cr.custom.resource_value)
            return resource_value.get('network-slice-services', dict()).get('slice-service')
        return None

    @property
    def candidate_data(self): return self._candidate_data

    @property
    def running_data(self): return self._running_data

    def get_diff(self) -> Dict:
        return DeepDiff(self._running_data, self._candidate_data)
