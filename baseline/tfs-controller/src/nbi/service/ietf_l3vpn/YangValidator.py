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

import libyang, os
from typing import Dict, Optional

YANG_DIR = os.path.join(os.path.dirname(__file__), 'yang')

class YangValidator:
    def __init__(self, module_name : str) -> None:
        self._yang_context = libyang.Context(YANG_DIR)
        self._yang_module  = self._yang_context.load_module(module_name)
        self._yang_module.feature_enable_all()

    def parse_to_dict(self, message : Dict) -> Dict:
        dnode : Optional[libyang.DNode] = self._yang_module.parse_data_dict(
            message, validate_present=True, validate=True, strict=True
        )
        if dnode is None: raise Exception('Unable to parse Message({:s})'.format(str(message)))
        message = dnode.print_dict()
        dnode.free()
        return message

    def destroy(self) -> None:
        self._yang_context.destroy()
