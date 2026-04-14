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
from typing import Any, Dict, Optional, Union
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.proto.context_pb2 import (
    Connection, ConnectionId, Device, DeviceId, Service
)
from service.service.tools.ObjectKeys import get_connection_key, get_device_key

LOGGER = logging.getLogger(__name__)

CacheableObject = Union[Connection, Device, Service]

class CacheableObjectType(Enum):
    CONNECTION = 'connection'
    DEVICE     = 'device'
    SERVICE    = 'service'

class MockTaskExecutor:
    def __init__(self) -> None:
        self._grpc_objects_cache : Dict[str, CacheableObject] = dict()

    # ----- Common methods ---------------------------------------------------------------------------------------------

    def _load_grpc_object(self, object_type : CacheableObjectType, object_key : str) -> Optional[CacheableObject]:
        object_key = '{:s}:{:s}'.format(object_type.value, object_key)
        return self._grpc_objects_cache.get(object_key)

    def _store_grpc_object(self, object_type : CacheableObjectType, object_key : str, grpc_object) -> None:
        object_key = '{:s}:{:s}'.format(object_type.value, object_key)
        self._grpc_objects_cache[object_key] = grpc_object
    
    def _delete_grpc_object(self, object_type : CacheableObjectType, object_key : str) -> None:
        object_key = '{:s}:{:s}'.format(object_type.value, object_key)
        self._grpc_objects_cache.pop(object_key, None)

    def _store_editable_grpc_object(
        self, object_type : CacheableObjectType, object_key : str, grpc_class, grpc_ro_object
    ) -> Any:
        grpc_rw_object = grpc_class()
        grpc_rw_object.CopyFrom(grpc_ro_object)
        self._store_grpc_object(object_type, object_key, grpc_rw_object)
        return grpc_rw_object

    # ----- Connection-related methods ---------------------------------------------------------------------------------

    def get_connection(self, connection_id : ConnectionId) -> Connection:
        connection_key = get_connection_key(connection_id)
        connection = self._load_grpc_object(CacheableObjectType.CONNECTION, connection_key)
        if connection is None: raise NotFoundException('Connection', connection_key)
        return connection

    def set_connection(self, connection : Connection) -> None:
        connection_key = get_connection_key(connection.connection_id)
        self._store_grpc_object(CacheableObjectType.CONNECTION, connection_key, connection)

    def delete_connection(self, connection_id : ConnectionId) -> None:
        connection_key = get_connection_key(connection_id)
        self._delete_grpc_object(CacheableObjectType.CONNECTION, connection_key)

    # ----- Device-related methods -------------------------------------------------------------------------------------

    def get_device(self, device_id : DeviceId) -> Device:
        device_key = get_device_key(device_id)
        device = self._load_grpc_object(CacheableObjectType.DEVICE, device_key)
        if device is None: raise NotFoundException('Device', device_key)
        return device

    def configure_device(self, device : Device) -> None:
        device_key = get_device_key(device.device_id)
        self._store_grpc_object(CacheableObjectType.DEVICE, device_key, device)
