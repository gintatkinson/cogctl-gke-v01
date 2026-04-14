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
from common.proto.pathcomp_pb2 import Algorithm_ShortestPath, PathCompRequest
from ._Algorithm import _Algorithm

class ShortestPathAlgorithm(_Algorithm):
    def __init__(self, algorithm : Algorithm_ShortestPath, class_name=__name__) -> None:
        super().__init__('SP', False, class_name=class_name)

    def add_service_requests(self, request : PathCompRequest) -> None:
        super().add_service_requests(request)
        for service_request in self.service_list:
            service_request['algId'    ] = self.algorithm_id
            service_request['syncPaths'] = self.sync_paths

    def _single_device_request(self) -> Optional[Dict]:
        if len(self.service_list) != 1: return None
        service = self.service_list[0]
        endpoint_ids = service['service_endpoints_ids']
        if len(endpoint_ids) != 2: return None
        if endpoint_ids[0]['device_id'] != endpoint_ids[-1]['device_id']: return None
        return {'response-list': [{
            'serviceId': service['serviceId'],
            'service_endpoints_ids': [endpoint_ids[0], endpoint_ids[-1]],
            'path': [{
                # not used by now
                #'path-capacity': {'total-size': {'value': 200, 'unit': 0}},
                #'path-latency': {'fixed-latency-characteristic': '2.000000'},
                #'path-cost': {'cost-name': '', 'cost-value': '1.000000', 'cost-algorithm': '0.000000'},
                'devices': [endpoint_ids[0], endpoint_ids[-1]]
            }]
        }]}

    def execute(self, dump_request_filename : Optional[str] = None, dump_reply_filename : Optional[str] = None) -> None:
        # if request is composed of a single service with single device (not supported by backend),
        # produce synthetic reply directly
        self.json_reply = self._single_device_request()
        if self.json_reply is None:
            # otherwise, follow normal logic through the backend
            return super().execute(dump_request_filename, dump_reply_filename)
