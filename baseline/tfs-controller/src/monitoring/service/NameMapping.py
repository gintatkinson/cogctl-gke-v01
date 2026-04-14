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

import threading
from typing import Dict, Optional

class NameMapping:
    def __init__(self) -> None:
        self.__lock = threading.Lock()
        self.__device_to_name   : Dict[str, str] = dict()
        self.__endpoint_to_name : Dict[str, str] = dict()

    def get_device_name(self, device_uuid : str) -> Optional[str]:
        with self.__lock:
            return self.__device_to_name.get(device_uuid)

    def get_endpoint_name(self, endpoint_uuid : str) -> Optional[str]:
        with self.__lock:
            return self.__endpoint_to_name.get(endpoint_uuid)

    def set_device_name(self, device_uuid : str, device_name : str) -> None:
        with self.__lock:
            self.__device_to_name[device_uuid] = device_name

    def set_endpoint_name(self, endpoint_uuid : str, endpoint_name : str) -> None:
        with self.__lock:
            self.__endpoint_to_name[endpoint_uuid] = endpoint_name

    def delete_device_name(self, device_uuid : str) -> None:
        with self.__lock:
            self.__device_to_name.pop(device_uuid, None)

    def delete_endpoint_name(self, endpoint_uuid : str) -> None:
        with self.__lock:
            self.__endpoint_to_name.pop(endpoint_uuid, None)
