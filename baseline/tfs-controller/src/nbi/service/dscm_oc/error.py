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
from flask import Response

YANG_JSON = "application/yang-data+json"
ERR_JSON  = "application/yang-errors+json"


def yang_json(data, status=200):
    return Response(json.dumps(data, ensure_ascii=False), status=status, mimetype=YANG_JSON)

def yang_error(err_dict, status=400):
    body = {"errors": {"error": [err_dict]}}
    return Response(json.dumps(body, ensure_ascii=False), status=status, mimetype=ERR_JSON)

def _bad_request(msg, path=None):
    return yang_error({"error-type": "protocol", "error-tag": "operation-failed",
                       "error-message": msg, **({"error-path": path} if path else {})}, status=400)

def _not_found(msg, path=None):
    return yang_error({"error-type": "application", "error-tag": "data-missing",
                       "error-message": msg, **({"error-path": path} if path else {})}, status=404)
