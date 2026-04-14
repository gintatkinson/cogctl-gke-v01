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

from common.proto.context_pb2 import ServiceId
from service.service.task_scheduler.TaskExecutor import TaskExecutor
from service.service.tools.ObjectKeys import get_service_key
from ._Task import _Task

KEY_TEMPLATE = 'optical_service({service_id:s}):delete'

class Task_OpticalServiceDelete(_Task):
    def __init__(
        self, task_executor : TaskExecutor, service_id : ServiceId,
        has_media_channel : bool, has_optical_band : bool
    ) -> None:
        super().__init__(task_executor)
        self._service_id = service_id
        self._has_media_channel = has_media_channel
        self._has_optical_band = has_optical_band

    @property
    def service_id(self) -> ServiceId: return self._service_id

    @staticmethod
    def build_key(service_id : ServiceId) -> str:   # pylint: disable=arguments-differ
        str_service_id = get_service_key(service_id)
        return KEY_TEMPLATE.format(service_id=str_service_id)

    @property
    def key(self) -> str: return self.build_key(self._service_id)

    def execute(self) -> None:
        if not self._has_media_channel or not self._has_optical_band:
            self._task_executor.delete_service(self._service_id)
