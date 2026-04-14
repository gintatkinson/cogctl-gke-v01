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


import deepdiff, json, logging
from flask import Response, abort, jsonify, request
from flask_restful import Resource
from .Callbacks import CallbackDispatcher
from .HttpStatusCodesEnum import HttpStatusCodesEnum
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

class RestConfDispatchData(Resource):
    def __init__(
        self, yang_handler : YangHandler, callback_dispatcher : CallbackDispatcher
    ) -> None:
        super().__init__()
        self._yang_handler = yang_handler
        self._callback_dispatcher = callback_dispatcher

    def get(self, subpath : str = '/') -> Response:
        data = self._yang_handler.get(subpath)
        self._callback_dispatcher.dispatch_data_pre_get(
            '/restconf/data/' + subpath, old_data=data
        )

        data = self._yang_handler.get(subpath)
        if data is None:
            abort(
                HttpStatusCodesEnum.CLI_ERR_NOT_FOUND.value,
                description='Path({:s}) not found'.format(str(subpath))
            )

        LOGGER.info('[GET] {:s} => {:s}'.format(subpath, str(data)))

        response = jsonify(json.loads(data))
        response.status_code = HttpStatusCodesEnum.SUCCESS_OK.value
        return response

    def post(self, subpath : str) -> Response:
        # TODO: client should not provide identifier of element to be created, add it to subpath
        try:
            payload = request.get_json(force=True)
        except Exception:
            LOGGER.exception('Invalid JSON')
            abort(HttpStatusCodesEnum.CLI_ERR_BAD_REQUEST.value, desctiption='Invalid JSON')

        data = self._yang_handler.get(subpath)
        if data is not None:
            abort(
                HttpStatusCodesEnum.CLI_ERR_CONFLICT.value,
                description='Path({:s}) already exists'.format(str(subpath))
            )

        try:
            json_data = self._yang_handler.create(subpath, payload)
        except Exception as e:
            LOGGER.exception('Create failed')
            abort(
                HttpStatusCodesEnum.CLI_ERR_NOT_ACCEPTABLE.value,
                description=str(e)
            )

        LOGGER.info('[POST] {:s} {:s} => {:s}'.format(subpath, str(payload), str(json_data)))

        self._callback_dispatcher.dispatch_data_update(
            '/restconf/data/' + subpath, old_data=None, new_data=json_data
        )

        response = jsonify({'status': 'created'})
        response.status_code = HttpStatusCodesEnum.SUCCESS_CREATED.value
        return response

    def put(self, subpath : str) -> Response:
        # NOTE: client should provide identifier of element to be created/replaced
        try:
            payload = request.get_json(force=True)
        except Exception:
            LOGGER.exception('Invalid JSON')
            abort(HttpStatusCodesEnum.CLI_ERR_BAD_REQUEST.value, desctiption='Invalid JSON')

        old_data = self._yang_handler.get(subpath)

        try:
            new_data = self._yang_handler.update(subpath, payload)
        except Exception as e:
            LOGGER.exception('Update failed')
            abort(
                HttpStatusCodesEnum.CLI_ERR_NOT_ACCEPTABLE.value,
                description=str(e)
            )

        LOGGER.info('[PUT] {:s} {:s} => {:s}'.format(subpath, str(payload), str(new_data)))

        diff_data = deepdiff.DeepDiff(old_data, new_data)
        updated = len(diff_data) > 0

        self._callback_dispatcher.dispatch_data_update(
            '/restconf/data/' + subpath, old_data=old_data, new_data=new_data
        )

        response = jsonify({'status': (
            'updated' if updated else 'created'
        )})
        response.status_code = (
            HttpStatusCodesEnum.SUCCESS_NO_CONTENT.value
            if updated else
            HttpStatusCodesEnum.SUCCESS_CREATED.value
        )
        return response

    def patch(self, subpath : str) -> Response:
        # NOTE: client should provide identifier of element to be patched
        try:
            payload = request.get_json(force=True)
        except Exception:
            LOGGER.exception('Invalid JSON')
            abort(HttpStatusCodesEnum.CLI_ERR_BAD_REQUEST.value, desctiption='Invalid JSON')

        old_data = self._yang_handler.get(subpath)

        try:
            new_data = self._yang_handler.update(subpath, payload)
        except Exception as e:
            LOGGER.exception('Update failed')
            abort(
                HttpStatusCodesEnum.CLI_ERR_NOT_ACCEPTABLE.value,
                description=str(e)
            )

        LOGGER.info('[PATCH] {:s} {:s} => {:s}'.format(subpath, str(payload), str(new_data)))

        #diff_data = deepdiff.DeepDiff(old_data, new_data)
        #updated = len(diff_data) > 0

        self._callback_dispatcher.dispatch_data_update(
            '/restconf/data/' + subpath, old_data=old_data, new_data=new_data
        )

        response = jsonify({'status': 'patched'})
        response.status_code = HttpStatusCodesEnum.SUCCESS_NO_CONTENT.value
        return response

    def delete(self, subpath : str) -> Response:
        # NOTE: client should provide identifier of element to be patched

        old_data = self._yang_handler.get(subpath)

        try:
            deleted_node = self._yang_handler.delete(subpath)
        except Exception as e:
            LOGGER.exception('Delete failed')
            abort(
                HttpStatusCodesEnum.CLI_ERR_NOT_ACCEPTABLE.value,
                description=str(e)
            )

        LOGGER.info('[DELETE] {:s} => {:s}'.format(subpath, str(deleted_node)))

        if deleted_node is None:
            abort(
                HttpStatusCodesEnum.CLI_ERR_NOT_FOUND.value,
                description='Path({:s}) not found'.format(str(subpath))
            )

        self._callback_dispatcher.dispatch_data_update(
            '/restconf/data/' + subpath, old_data=old_data, new_data=None
        )

        response = jsonify({})
        response.status_code = HttpStatusCodesEnum.SUCCESS_NO_CONTENT.value
        return response
