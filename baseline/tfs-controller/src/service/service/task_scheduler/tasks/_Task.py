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

from service.service.task_scheduler.TaskExecutor import TaskExecutor

class _Task:
    def __init__(self, task_executor : TaskExecutor) -> None:
        self._task_executor = task_executor

    @staticmethod
    def build_key() -> str:
        raise NotImplementedError('Task:build_key() not implemented')

    @property
    def key(self) -> str:
        raise NotImplementedError('Task:key() not implemented')

    def execute(self) -> bool:
        raise NotImplementedError('Task:execute() not implemented')
