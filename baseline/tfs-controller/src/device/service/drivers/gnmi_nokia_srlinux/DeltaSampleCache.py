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
from typing import Any, Dict, Tuple, Union

class DeltaSampleCache:
    def __init__(self) -> None:
        self._previous_samples : Dict[str, Tuple[float, Union[int, float]]] = dict()

    def get_delta(self, path : str, current_timestamp : float, current_value : Any) -> None:
        previous_sample = copy.deepcopy(self._previous_samples.get(path))
        self._previous_samples[path] = current_timestamp, current_value

        if not isinstance(current_value, (int, float)): return None
        if previous_sample is None: return current_timestamp, 0
        previous_timestamp, previous_value = previous_sample
        if not isinstance(previous_value, (int, float)): return None

        delta_value = max(0, current_value - previous_value)
        delay = current_timestamp - previous_timestamp
        delta_sample = current_timestamp, delta_value / delay

        return delta_sample
