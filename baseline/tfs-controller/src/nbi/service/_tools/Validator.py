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

from typing import List
from flask.json import jsonify
from jsonschema import _utils
from jsonschema.validators import validator_for
from jsonschema.protocols import Validator
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from .HttpStatusCodes import HTTP_BADREQUEST

def validate_message(schema, message):
    validator_class = validator_for(schema)
    validator : Validator = validator_class(schema)
    errors : List[ValidationError] = sorted(validator.iter_errors(message), key=str)
    if len(errors) == 0: return
    response = jsonify([
        {'message': str(error.message), 'schema': str(error.schema), 'validator': str(error.validator),
         'where': str(_utils.format_as_index(container='message', indices=error.relative_path))}
        for error in errors
    ])
    response.status_code = HTTP_BADREQUEST
    raise BadRequest(response=response)
