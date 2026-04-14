#pylint: disable=invalid-name, missing-function-docstring, line-too-long, logging-fstring-interpolation, missing-class-docstring, missing-module-docstring
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

from typing import Dict, Union
import logging
from .cm_connection import CmConnection, ExternalError
from .constellation import Constellation
from .tf_service import TFService
from .transport_capacity import TransportCapacity
from .connection import Connection

LOGGER = logging.getLogger(__name__)

def _get_value_or_default(config: Dict[str, any], key: str, default_value: any) -> any:
    if key not in config:
        return default_value
    else:
        return config[key]

def _get_capacity(config) -> int:
    if "capacity_unit" not in config or "capacity_value" not in config:
        return 0
    if config["capacity_unit"] != "gigabit":
        return 0
    return config["capacity_value"]

def set_config_for_service(cm_connection: CmConnection, constellation: Constellation, uuid: str, config: Dict[str, any]) -> Union[bool, Exception]:
    try:
        service = TFService(uuid, config["input_sip_name"], config["output_sip_name"], _get_capacity(config))
        if constellation.is_vti_mode():
            desired_tc = TransportCapacity(from_tf_service=service)
            active_tc = cm_connection.get_transport_capacity_by_name(service.name())
            if desired_tc != active_tc:
                if active_tc:
                    LOGGER.info(f"set_config_for_service: Transport Capacity change for {uuid}, ({active_tc=}, {desired_tc=}), performing service impacting update")
                    # Remove previous connection (if any)
                    active_connection = cm_connection.get_connection_by_name(service.name())
                    if active_connection:
                        cm_connection.delete_connection(active_connection.href)
                    # Delete old TC
                    cm_connection.delete_transport_capacity(active_tc.href)
                if desired_tc:
                    href = cm_connection.create_transport_capacity(desired_tc)
                    if not href:
                        LOGGER.error(f"set_config_for_service: Failed to create Transport Capacity ({desired_tc=})")
                        return False
        connection = Connection(from_tf_service=service)
        try:
            href = cm_connection.create_or_update_connection(connection)
            if href:
                LOGGER.info(f"set_config_for_service: Created service {uuid} as {href} (connection={str(connection)})")
                return True
            else:
                LOGGER.error(f"set_config_for_service: Service creation failure for {uuid} (connection={str(connection)})")
                return False
        except ExternalError as e:
            LOGGER.error(f"set_config_for_service: Service creation failure for {uuid} (connection={str(connection)}): {str(e)}")
            return e
    # Intentionally catching all exceptions, as they are stored in a list as return values
    # by the caller
    # pylint: disable=broad-except
    except Exception as e:
        return e
