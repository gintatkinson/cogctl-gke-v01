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

from common.proto.pathcomp_pb2 import Algorithm_KShortestPath
from ._Algorithm import _Algorithm

class KShortestPathAlgorithm(_Algorithm):
    def __init__(self, algorithm : Algorithm_KShortestPath, class_name=__name__) -> None:
        super().__init__('KSP', False, class_name=class_name)
        self.k_inspection = algorithm.k_inspection
        self.k_return = algorithm.k_return

    def add_service_requests(self, requested_services) -> None:
        super().add_service_requests(requested_services)
        for service_request in self.service_list:
            service_request['algId'    ] = self.algorithm_id
            service_request['syncPaths'] = self.sync_paths
            service_request['kPaths_inspection'] = self.k_inspection
            service_request['kPaths_return'    ] = self.k_return
