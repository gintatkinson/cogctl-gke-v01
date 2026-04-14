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

from ._Algorithm import _Algorithm
from .KDisjointPathAlgorithm import KDisjointPathAlgorithm
from .KShortestPathAlgorithm import KShortestPathAlgorithm
from .ShortestPathAlgorithm import ShortestPathAlgorithm

ALGORITHMS = {
    'shortest_path'  : ShortestPathAlgorithm,
    'k_shortest_path': KShortestPathAlgorithm,
    'k_disjoint_path': KDisjointPathAlgorithm,
}

def get_algorithm(request) -> _Algorithm:
    algorithm_name = request.WhichOneof('algorithm')
    algorithm_class = ALGORITHMS.get(algorithm_name)
    if algorithm_class is None:
        raise Exception('Algorithm({:s}) not supported'.format(str(algorithm_name)))
    algorithm_settings = getattr(request, algorithm_name)
    algorithm_instance = algorithm_class(algorithm_settings)
    return algorithm_instance
