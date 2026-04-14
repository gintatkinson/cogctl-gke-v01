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

from typing import TYPE_CHECKING, Dict, Tuple
from common.DeviceTypes import DeviceTypeEnum
from common.method_wrappers.ServiceExceptions import OperationFailedException
from common.proto.context_pb2 import ConnectionId, Device
from common.tools.grpc.Tools import grpc_message_to_json_string
from service.service.service_handler_api.Tools import check_errors_deleteendpoint
from service.service.task_scheduler.TaskExecutor import TaskExecutor
from service.service.tools.EndpointIdFormatters import endpointids_to_raw
from service.service.tools.ObjectKeys import get_connection_key
from ._Task import _Task

if TYPE_CHECKING:
    from service.service.service_handler_api._ServiceHandler import _ServiceHandler

KEY_TEMPLATE = 'connection({connection_id:s}):deconfigure'

CONTROLLER_DEVICE_TYPES = {
    DeviceTypeEnum.TERAFLOWSDN_CONTROLLER,
    DeviceTypeEnum.NCE,
}

class Task_ConnectionDeconfigure(_Task):
    def __init__(self, task_executor : TaskExecutor, connection_id : ConnectionId) -> None:
        super().__init__(task_executor)
        self._connection_id = connection_id

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

        service_handler_settings = {}
        service_handlers : Dict[DeviceTypeEnum, Tuple['_ServiceHandler', Dict[str, Device]]] = \
            self._task_executor.get_service_handlers(connection, service, **service_handler_settings)

        connection_uuid = connection.connection_id.connection_uuid.uuid
        endpointids_to_delete = endpointids_to_raw(connection.path_hops_endpoint_ids)

        errors = list()
        for device_type, (service_handler, connection_devices) in service_handlers.items():
            if device_type in CONTROLLER_DEVICE_TYPES:
                _endpointids_to_delete = endpointids_to_delete
            else:
                _endpointids_to_delete = [
                    (device_uuid, endpoint_uuid, topology_uuid)
                    for device_uuid, endpoint_uuid, topology_uuid in endpointids_to_delete
                    if device_uuid in connection_devices
                ]
            results_deleteendpoint = service_handler.DeleteEndpoint(
                _endpointids_to_delete, connection_uuid=connection_uuid
            )
            errors.extend(check_errors_deleteendpoint(endpointids_to_delete, results_deleteendpoint))

        if len(errors) > 0:
            MSG = 'DeleteEndpoint for Connection({:s}) from Service({:s})'
            str_connection = grpc_message_to_json_string(connection)
            str_service = grpc_message_to_json_string(service)
            raise OperationFailedException(MSG.format(str_connection, str_service), extra_details=errors)

        self._task_executor.delete_connection(self._connection_id)
