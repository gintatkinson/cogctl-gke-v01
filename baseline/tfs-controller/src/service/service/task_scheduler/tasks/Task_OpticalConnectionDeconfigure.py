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

from common.method_wrappers.ServiceExceptions import OperationFailedException
from common.proto.context_pb2 import ConnectionId
from common.tools.grpc.Tools import grpc_message_to_json_string
from service.service.service_handler_api.Tools import check_errors_deleteendpoint
from service.service.task_scheduler.TaskExecutor import TaskExecutor
from service.service.tools.EndpointIdFormatters import endpointids_to_raw
from service.service.tools.ObjectKeys import get_connection_key
from service.service.service_handlers.oc.OCServiceHandler import OCServiceHandler

from ._Task import _Task


KEY_TEMPLATE       = 'optical_connection({connection_id:s}):deconfigure'
SUPPORTED_HANDLERS = (OCServiceHandler,)

class Task_OpticalConnectionDeconfigure(_Task):
    def __init__(
        self, task_executor : TaskExecutor, connection_id : ConnectionId,
        has_media_channel : bool
    ) -> None:
        super().__init__(task_executor)
        self._connection_id = connection_id
        self._has_media_channel = has_media_channel

    @property
    def connection_id(self) -> ConnectionId: return self._connection_id

    @staticmethod
    def build_key(connection_id : ConnectionId) -> str: # pylint: disable=arguments-differ
        str_connection_id = get_connection_key(connection_id)
        return KEY_TEMPLATE.format(connection_id=str_connection_id)

    @property
    def key(self) -> str: return self.build_key(self._connection_id)

    def execute(self) -> None:
        connection = self._task_executor.get_connection(self._connection_id)
        service = self._task_executor.get_service(connection.service_id)
        errors = []
        service_handler_settings = {}

        service_handlers = self._task_executor.get_service_handlers(connection, service, **service_handler_settings)
        for _, (service_handler, connection_devices) in service_handlers.items():
            endpointids_to_delete = endpointids_to_raw(connection.path_hops_endpoint_ids)
            connection_uuid = connection.connection_id.connection_uuid.uuid
            if self._has_media_channel:
                if isinstance(service_handler, SUPPORTED_HANDLERS):
                    is_media_channel = True
                else:
                    is_media_channel = service_handler.check_media_channel(connection_uuid)
                if is_media_channel:
                    results_deleteendpoint = service_handler.DeleteEndpoint(endpointids_to_delete, connection_uuid=connection_uuid)
                    errors = check_errors_deleteendpoint(endpointids_to_delete, results_deleteendpoint)
                if len(errors) > 0:
                    MSG = 'DeleteEndpoint for OpticalConnection({:s}) from Service({:s})'
                    str_connection = grpc_message_to_json_string(connection)
                    str_service = grpc_message_to_json_string(service)
                    raise OperationFailedException(MSG.format(str_connection, str_service), extra_details=errors)
                if is_media_channel:
                    self._task_executor.delete_connection(self._connection_id)
            else:
                results_deleteendpoint = service_handler.DeleteEndpoint(endpointids_to_delete, connection_uuid=connection_uuid)
                errors = check_errors_deleteendpoint(endpointids_to_delete, results_deleteendpoint)
                if len(errors) > 0:
                    MSG = 'DeleteEndpoint for OpticalConnection({:s}) from Service({:s})'
                    str_connection = grpc_message_to_json_string(connection)
                    str_service = grpc_message_to_json_string(service)
                    raise OperationFailedException(MSG.format(str_connection, str_service), extra_details=errors)
                self._task_executor.delete_connection(self._connection_id)
