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


from functools import wraps
from flask import request
from .error import yang_error

def require_accept(allowed):
    def deco(fn):
        @wraps(fn)
        def _wrap(*args, **kwargs):
            accept = request.headers.get("Accept", "")
            if not any(a in accept or accept == "*/*" for a in allowed):
                return yang_error({"error-message": f"Accept not supported. Use one of {allowed}"}, status=406)
            return fn(*args, **kwargs)
        return _wrap
    return deco

def require_content_type(allowed):
    def deco(fn):
        @wraps(fn)
        def _wrap(*args, **kwargs):
            ctype = request.headers.get("Content-Type", "")
            if not any(a in ctype for a in allowed):
                return yang_error({"error-message": f"Content-Type not supported. Use one of {allowed}"}, status=415)
            return fn(*args, **kwargs)
        return _wrap
    return deco
