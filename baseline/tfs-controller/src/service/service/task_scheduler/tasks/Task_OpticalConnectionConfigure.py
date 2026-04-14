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
from common.method_wrappers.ServiceExceptions import OperationFailedException
from common.proto.context_pb2 import ConnectionId, ServiceTypeEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from service.service.service_handler_api.Tools import check_errors_setendpoint
from service.service.task_scheduler.TaskExecutor import TaskExecutor
from service.service.tools.EndpointIdFormatters import endpointids_to_raw
from service.service.tools.ObjectKeys import get_connection_key
from service.service.service_handlers.oc.OCServiceHandler import OCServiceHandler

from ._Task import _Task


KEY_TEMPLATE       = 'optical_connection({connection_id:s}):configure'
SUPPORTED_HANDLERS = (OCServiceHandler,)


class Task_OpticalConnectionConfigure(_Task):
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
        service_handler = None
        service_handlers = self._task_executor.get_service_handlers(connection, service, **service_handler_settings)
        for _, (handler, connection_devices) in service_handlers.items():
             if service_handler is None : service_handler=handler
             else :
                logging.info(f"type_servicehandler {handler} and {service_handler}")
                if type(handler) != type(service_handler) : 
                    if  service.service_type == ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY:
                       if isinstance(handler, SUPPORTED_HANDLERS) and isinstance(service_handler, SUPPORTED_HANDLERS):
                          break

                    raise Exception("Devices are not compatible ")

        connection_uuid = connection.connection_id.connection_uuid.uuid
        endpointids_to_set = endpointids_to_raw(connection.path_hops_endpoint_ids)
        errors = list()

        connection_uuid = connection.connection_id.connection_uuid.uuid

        results_setendpoint = service_handler.SetEndpoint(endpointids_to_set, connection_uuid=connection_uuid)
        errors.extend(check_errors_setendpoint(endpointids_to_set, results_setendpoint))

        if len(errors) > 0:
            MSG = 'SetEndpoint for Connection({:s}) from Service({:s})'
            str_connection = grpc_message_to_json_string(connection)
            str_service = grpc_message_to_json_string(service)
            raise OperationFailedException(MSG.format(str_connection, str_service), extra_details=errors)

        self._task_executor.set_connection(connection)

        results_setendOpticalConfigs = service_handler.SetOpticalConfig(
                endpointids_to_set, connection_uuid=connection_uuid
            )
        errors.extend(check_errors_setendpoint(endpointids_to_set, results_setendOpticalConfigs))

        if len(errors) > 0:
            MSG = 'SetOpticalConfigs for Optical Connection({:s}) from Optical Service({:s})'
            str_connection = grpc_message_to_json_string(connection)
            str_service = grpc_message_to_json_string(service)
            raise OperationFailedException(MSG.format(str_connection, str_service), extra_details=errors)
