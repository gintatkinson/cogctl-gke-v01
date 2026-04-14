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

import base64, json
from typing import Any
from ..gnmi.gnmi_pb2 import TypedValue

def decode_value(value : TypedValue) -> Any:
    encoding = value.WhichOneof('value')
    if encoding == 'json_val':
        value = value.json_val
        #mdl, cls = self._classes[className]
        #obj = json.loads(strObj)
        #if isinstance(obj, (list,)):
        #    obj = map(lambda n: pybindJSON.loads(n, mdl, cls.__name__), obj)
        #    data = map(lambda n: json.loads(pybindJSON.dumps(n, mode='default')), obj)
        #else:
        #    obj = pybindJSON.loads(obj, mdl, cls.__name__)
        #    data = json.loads(pybindJSON.dumps(obj, mode='default'))
        raise NotImplementedError()
        #return value
    elif encoding == 'json_ietf_val':
        value : str = value.json_ietf_val
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            # Assume is Base64-encoded
            b_b64_value = value.encode('UTF-8')
            b_value = base64.b64decode(b_b64_value, validate=True)
            value = b_value.decode('UTF-8')
            return json.loads(value)
    else:
        MSG = 'Unsupported Encoding({:s}) in Value({:s})'
        # pylint: disable=broad-exception-raised
        raise Exception(MSG.format(str(encoding), str(value)))

def value_exists(value) -> bool:
    if value is None: return False
    if isinstance(value, Exception): return False
    if issubclass(type(value), Exception): return False
    return True
