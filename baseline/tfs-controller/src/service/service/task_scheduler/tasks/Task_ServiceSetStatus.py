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

from common.proto.context_pb2 import ServiceId, ServiceStatusEnum
from service.service.task_scheduler.TaskExecutor import TaskExecutor
from service.service.tools.ObjectKeys import get_service_key
from ._Task import _Task

KEY_TEMPLATE = 'service({service_id:s}):set_status({new_status:s})'

class Task_ServiceSetStatus(_Task):
    def __init__(self, task_executor : TaskExecutor, service_id : ServiceId, new_status : ServiceStatusEnum) -> None:
        super().__init__(task_executor)
        self._service_id = service_id
        self._new_status = new_status

    @property
    def service_id(self) -> ServiceId: return self._service_id

    @property
    def new_status(self) -> ServiceStatusEnum: return self._new_status

    @staticmethod
    def build_key(service_id : ServiceId, new_status : ServiceStatusEnum) -> str:   # pylint: disable=arguments-differ
        str_service_id = get_service_key(service_id)
        str_new_status = ServiceStatusEnum.Name(new_status)
        return KEY_TEMPLATE.format(service_id=str_service_id, new_status=str_new_status)

    @property
    def key(self) -> str: return self.build_key(self._service_id, self._new_status)

    def execute(self) -> None:
        service = self._task_executor.get_service(self._service_id)
        service.service_status.service_status = self._new_status
        self._task_executor.set_service(service)
