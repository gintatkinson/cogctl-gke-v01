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

import grpc #, logging
from typing import Any, Dict, List, Set

#LOGGER = logging.getLogger(__name__)

class InMemoryObjectDatabase:
    def __init__(self) -> None:
        self._database : Dict[str, Dict[str, Any]] = dict()

    def _get_container(self, container_name : str) -> Dict[str, Any]:
        return self._database.setdefault(container_name, {})

    def get_entries(self, container_name : str) -> List[Any]:
        container = self._get_container(container_name)
        return [container[entry_uuid] for entry_uuid in sorted(container.keys())]

    def has_entry(self, container_name : str, entry_uuid : str) -> Any:
        #LOGGER.debug('[has_entry] BEFORE database={:s}'.format(str(self._database)))
        container = self._get_container(container_name)
        return entry_uuid in container

    def get_entry(self, container_name : str, entry_uuid : str, context : grpc.ServicerContext) -> Any:
        #LOGGER.debug('[get_entry] BEFORE database={:s}'.format(str(self._database)))
        container = self._get_container(container_name)
        if entry_uuid not in container:
            MSG = '{:s}({:s}) not found; available({:s})'
            msg = str(MSG.format(container_name, entry_uuid, str(container.keys())))
            context.abort(grpc.StatusCode.NOT_FOUND, msg)
        return container[entry_uuid]

    def set_entry(self, container_name : str, entry_uuid : str, entry : Any) -> Any:
        container = self._get_container(container_name)
        #LOGGER.debug('[set_entry] BEFORE database={:s}'.format(str(self._database)))
        container[entry_uuid] = entry
        #LOGGER.debug('[set_entry] AFTER database={:s}'.format(str(self._database)))
        return entry

    def del_entry(self, container_name : str, entry_uuid : str, context : grpc.ServicerContext) -> None:
        container = self._get_container(container_name)
        #LOGGER.debug('[del_entry] BEFORE database={:s}'.format(str(self._database)))
        if entry_uuid not in container:
            context.abort(grpc.StatusCode.NOT_FOUND, str('{:s}({:s}) not found'.format(container_name, entry_uuid)))
        del container[entry_uuid]
        #LOGGER.debug('[del_entry] AFTER database={:s}'.format(str(self._database)))

    def select_entries(self, container_name : str, entry_uuids : Set[str]) -> List[Any]:
        if len(entry_uuids) == 0: return self.get_entries(container_name)
        container = self._get_container(container_name)
        return [
            container[entry_uuid]
            for entry_uuid in sorted(container.keys())
            if entry_uuid in entry_uuids
        ]
