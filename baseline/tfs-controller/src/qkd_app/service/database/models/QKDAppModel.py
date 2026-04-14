# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy import Column, DateTime, String, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from typing import Dict
from ._Base import _Base
from .enums.QKDAppStatus import ORM_QKDAppStatusEnum
from .enums.QKDAppTypes import ORM_QKDAppTypesEnum


class AppModel(_Base):
    """
    ORM model representing a QKD (Quantum Key Distribution) Application.
    This model stores information about the QKD app status, type, and related device and 
    backing QKD links. It is stored in the 'qkd_app' table.
    """
    __tablename__ = 'qkd_app'

    # Primary Key
    app_uuid = Column(UUID(as_uuid=False), primary_key=True, nullable=False, doc="Unique identifier for the QKD app.")
    
    # Foreign Key-like field (context)
    context_uuid = Column(UUID(as_uuid=False), nullable=False, doc="Foreign key linking to the application's context.")

    # Status and type
    app_status = Column(Enum(ORM_QKDAppStatusEnum), nullable=False, doc="Current status of the QKD app.")
    app_type = Column(Enum(ORM_QKDAppTypesEnum), nullable=False, doc="Type of the QKD app (internal or client).")

    # Application IDs
    server_app_id = Column(String, nullable=False, doc="ID of the server-side QKD application.")
    client_app_id = Column(ARRAY(String), nullable=False, doc="List of client-side QKD application IDs.")

    # Backing QKD links and devices
    backing_qkdl_uuid = Column(ARRAY(UUID(as_uuid=False)), nullable=False, doc="List of UUIDs of the backing QKD links.")
    local_device_uuid = Column(UUID(as_uuid=False), nullable=False, doc="UUID of the local QKD device.")
    remote_device_uuid = Column(UUID(as_uuid=False), nullable=True, doc="UUID of the remote QKD device (nullable).")

    # Timestamps
    created_at = Column(DateTime, nullable=False, doc="Timestamp when the QKD app record was created.")
    updated_at = Column(DateTime, nullable=False, doc="Timestamp when the QKD app record was last updated.")

    def dump_id(self) -> Dict:
        """
        Serializes the primary key fields (context and app UUID) into a dictionary.

        :return: A dictionary with 'context_id' and 'app_uuid' keys.
        """
        return {
            'context_id': {'context_uuid': {'uuid': self.context_uuid}},
            'app_uuid': {'uuid': self.app_uuid}
        }

    def dump(self) -> Dict:
        """
        Serializes the entire QKD app model into a dictionary, including app status, type, IDs, 
        device info, and backing QKD links.

        :return: A dictionary representation of the QKD app.
        """
        return {
            'app_id': self.dump_id(),
            'app_status': self.app_status.value,
            'app_type': self.app_type.value,
            'server_app_id': self.server_app_id,
            'client_app_id': self.client_app_id,
            'backing_qkdl_id': [{'qkdl_uuid': {'uuid': qkdl_id}} for qkdl_id in self.backing_qkdl_uuid],
            'local_device_id': {'device_uuid': {'uuid': self.local_device_uuid}},
            'remote_device_id': {'device_uuid': {'uuid': self.remote_device_uuid}} if self.remote_device_uuid else None,
        }
