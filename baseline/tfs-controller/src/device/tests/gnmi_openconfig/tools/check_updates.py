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

from typing import Iterable, List, Tuple

def check_updates(results : Iterable[Tuple[str, bool]], format_str : str, item_ids : List[Tuple]) -> None:
    results = set(results)
    assert len(results) == len(item_ids)
    for item_id_fields in item_ids:
        if isinstance(item_id_fields, (str, int, float, bool)): item_id_fields = (item_id_fields,)
        assert (format_str.format(*item_id_fields), True) in results
