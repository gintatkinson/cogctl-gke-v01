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


import logging
from flask import Response, abort, jsonify, request
from flask_restful import Resource
from .Callbacks import CallbackDispatcher
from .HttpStatusCodesEnum import HttpStatusCodesEnum
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

class RestConfDispatchOperations(Resource):
    def __init__(
        self, yang_handler : YangHandler, callback_dispatcher : CallbackDispatcher
    ) -> None:
        super().__init__()
        self._yang_handler = yang_handler
        self._callback_dispatcher = callback_dispatcher

    def post(self, subpath : str) -> Response:
        try:
            payload = request.get_json(force=True)
        except Exception:
            LOGGER.exception('Invalid JSON')
            abort(HttpStatusCodesEnum.CLI_ERR_BAD_REQUEST.value, desctiption='Invalid JSON')

        output_data = self._callback_dispatcher.dispatch_operation(
            '/restconf/operations/' + subpath, input_data=payload
        )

        LOGGER.info('[POST] {:s} {:s} => {:s}'.format(subpath, str(payload), str(output_data)))

        response = jsonify(output_data)
        response.status_code = HttpStatusCodesEnum.SUCCESS_OK.value
        return response
