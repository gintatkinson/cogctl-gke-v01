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

from typing import Any, Dict, List, Tuple

class _Handler:
    def get_resource_key(self) -> str:
        # Retrieve the TeraFlowSDN resource_key path schema used to point this handler
        raise NotImplementedError()

    def get_path(self) -> str:
        # Retrieve the Nokia path schema used to interrogate the device
        raise NotImplementedError()

    def compose(self, resource_key : str, resource_value : Dict, delete : bool = False) -> Tuple[str, str]:
        # Compose a Set/Delete message based on the resource_key/resource_value fields, and the delete flag
        raise NotImplementedError()

    def parse(self, json_data : Dict) -> List[Tuple[str, Dict[str, Any]]]:
        # Parse a Reply from the device and return a list of resource_key/resource_value pairs
        raise NotImplementedError()
