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
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from common.tools.context_queries.Device import get_device, get_devices
from common.tools.context_queries.Link import get_link, get_links
from common.tools.context_queries.Topology import get_topology, get_topologies
from common.tools.context_queries.Service import get_service_by_uuid, get_services
from context.client.ContextClient import ContextClient


LOGGER = logging.getLogger(__name__)


class CachedEntities(Enum):
    TOPOLOGY   = 'topology'
    DEVICE     = 'device'
    ENDPOINT   = 'endpoint'
    LINK       = 'link'
    SERVICE    = 'service'
    CONNECTION = 'connection'


KEY_LENGTHS = {
    CachedEntities.TOPOLOGY   : 1,
    CachedEntities.DEVICE     : 1,
    CachedEntities.ENDPOINT   : 2,
    CachedEntities.LINK       : 1,
    CachedEntities.SERVICE    : 1,
    CachedEntities.CONNECTION : 3,
}


def compose_object_key(entity : CachedEntities, *object_uuids : str) -> Tuple[str, ...]:
    expected_length = KEY_LENGTHS.get(entity)
    entity_name = str(entity.value)
    if expected_length is None:
        MSG = 'Unsupported ({:s}, {:s})'
        raise Exception(MSG.format(entity_name.title(), str(object_uuids)))

    if len(object_uuids) == expected_length:
        return (entity_name, *object_uuids)

    MSG = 'Invalid Key ({:s}, {:s})'
    raise Exception(MSG.format(entity_name.title(), str(object_uuids)))


class ObjectCache:
    def __init__(self, context_client : ContextClient):
        self._context_client = context_client
        self._object_cache : Dict[Tuple[str, str], Any] = dict()

    def get(
        self, entity : CachedEntities, *object_uuids : str,
        auto_retrieve : bool = True, force_update : bool = False
    ) -> Optional[Any]:
        if force_update: self._update(entity, *object_uuids)

        object_key = compose_object_key(entity, *object_uuids)
        if object_key in self._object_cache:
            return self._object_cache[object_key]

        if not auto_retrieve: return None
        return self._update(entity, *object_uuids)

    def get_all(
        self, entity : CachedEntities, fresh : bool = False
    ) -> List[Any]:
        if fresh: self._update_all(entity)
        entity_name = str(entity.value)
        return [
            obj
            for obj_key, obj in self._object_cache.items()
            if obj_key[0] == entity_name
        ]

    def set(self, entity : CachedEntities, object_inst : Any, *object_uuids : str) -> None:
        object_key = compose_object_key(entity, *object_uuids)
        self._object_cache[object_key] = object_inst

    def _update(self, entity : CachedEntities, *object_uuids : str) -> Optional[Any]:
        if entity == CachedEntities.TOPOLOGY:
            object_inst = get_topology(
                self._context_client, object_uuids[0], rw_copy=False
            )
        elif entity == CachedEntities.DEVICE:
            object_inst = get_device(
                self._context_client, object_uuids[0], rw_copy=False, include_endpoints=True,
                include_components=False, include_config_rules=False,
            )
        elif entity == CachedEntities.ENDPOINT:
            # Endpoints are only updated when updating a Device
            return None
        elif entity == CachedEntities.LINK:
            object_inst = get_link(
                self._context_client, object_uuids[0], rw_copy=False
            )
        elif entity == CachedEntities.SERVICE:
            object_inst = get_service_by_uuid(
                self._context_client, object_uuids[0], rw_copy=False
            )
        else:
            MSG = 'Not Supported ({:s}, {:s})'
            LOGGER.warning(MSG.format(str(entity.value).title(), str(object_uuids)))
            return None

        if object_inst is None:
            MSG = 'Not Found ({:s}, {:s})'
            LOGGER.warning(MSG.format(str(entity.value).title(), str(object_uuids)))
            return None

        self.set(entity, object_inst, object_uuids[0])
        self.set(entity, object_inst, object_inst.name)

        if entity == CachedEntities.DEVICE:
            device_uuid = object_inst.device_id.device_uuid.uuid
            device_name = object_inst.name

            for endpoint in object_inst.device_endpoints:
                endpoint_device_uuid = endpoint.endpoint_id.device_id.device_uuid.uuid
                if device_uuid != endpoint_device_uuid:
                    MSG = 'DeviceUUID({:s}) != Endpoint.DeviceUUID({:s})'
                    raise Exception(str(device_uuid), str(endpoint_device_uuid))

                endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
                endpoint_name = endpoint.name
                self.set(CachedEntities.ENDPOINT, endpoint, device_uuid, endpoint_uuid)
                self.set(CachedEntities.ENDPOINT, endpoint, device_uuid, endpoint_name)
                self.set(CachedEntities.ENDPOINT, endpoint, device_name, endpoint_uuid)
                self.set(CachedEntities.ENDPOINT, endpoint, device_name, endpoint_name)

        return object_inst

    def _update_all(self, entity : CachedEntities) -> None:
        if entity == CachedEntities.TOPOLOGY:
            objects = get_topologies(self._context_client)
            objects = {
                (t.topology_id.topology_uuid.uuid, t.name) : t
                for t in objects
            }
        elif entity == CachedEntities.DEVICE:
            objects = get_devices(self._context_client)
            objects = {
                (d.device_id.device_uuid.uuid, d.name) : d
                for d in objects
            }
        elif entity == CachedEntities.ENDPOINT:
            # Endpoints are only updated when updating a Device
            return None
        elif entity == CachedEntities.LINK:
            objects = get_links(self._context_client)
            objects = {
                (l.link_id.link_uuid.uuid, l.name) : l
                for l in objects
            }
        elif entity == CachedEntities.SERVICE:
            objects = get_services(self._context_client)
            objects = {
                (s.service_id.service_uuid.uuid, s.name) : s
                for s in objects
            }
        else:
            MSG = 'Not Supported ({:s})'
            LOGGER.warning(MSG.format(str(entity.value).title()))
            return None

        for (object_uuid, object_name), object_inst in objects.items():
            self.set(entity, object_inst, object_uuid)
            self.set(entity, object_inst, object_name)

            if entity == CachedEntities.DEVICE:
                for endpoint in object_inst.device_endpoints:
                    endpoint_device_uuid = endpoint.endpoint_id.device_id.device_uuid.uuid
                    if object_uuid != endpoint_device_uuid:
                        MSG = 'DeviceUUID({:s}) != Endpoint.DeviceUUID({:s})'
                        raise Exception(str(object_uuid), str(endpoint_device_uuid))

                    endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
                    endpoint_name = endpoint.name
                    self.set(CachedEntities.ENDPOINT, endpoint, object_uuid, endpoint_uuid)
                    self.set(CachedEntities.ENDPOINT, endpoint, object_uuid, endpoint_name)
                    self.set(CachedEntities.ENDPOINT, endpoint, object_name, endpoint_uuid)
                    self.set(CachedEntities.ENDPOINT, endpoint, object_name, endpoint_name)

    def delete(self, entity : CachedEntities, *object_uuids : str) -> None:
        object_key = compose_object_key(entity, *object_uuids)
        self._object_cache.pop(object_key, None)
