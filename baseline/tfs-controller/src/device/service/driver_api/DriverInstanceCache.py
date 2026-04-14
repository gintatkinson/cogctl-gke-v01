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

import json, logging, threading
from typing import Any, Dict, Optional
from common.method_wrappers.ServiceExceptions import InvalidArgumentException
from common.proto.context_pb2 import Device, Empty
from context.client.ContextClient import ContextClient
from device.service.Tools import get_connect_rules
from ._Driver import _Driver
from .DriverFactory import DriverFactory
from .Exceptions import DriverInstanceCacheTerminatedException
from .FilterFields import FilterFieldEnum, get_device_driver_filter_fields

LOGGER = logging.getLogger(__name__)

class DriverInstanceCache:
    def __init__(self, driver_factory : DriverFactory) -> None:
        self._lock = threading.Lock()
        self._terminate = threading.Event()
        self._device_uuid__to__driver_instance : Dict[str, _Driver] = {}
        self._driver_factory = driver_factory

    def get(
        self, device_uuid : str, filter_fields : Dict[FilterFieldEnum, Any] = {}, address : Optional[str] = None,
        port : Optional[int] = None, settings : Dict[str, Any] = {}
    ) -> _Driver:

        if self._terminate.is_set():
            raise DriverInstanceCacheTerminatedException()

        filter_fields = {k.value:v for k,v in filter_fields.items()}

        with self._lock:
            driver_instance = self._device_uuid__to__driver_instance.get(device_uuid)
            if driver_instance is not None: return driver_instance

            if len(filter_fields) == 0: return None
            MSG = 'Selecting driver for device({:s}) with filter_fields({:s})...'
            LOGGER.info(MSG.format(str(device_uuid), str(filter_fields)))
            driver_class = self._driver_factory.get_driver_class(**filter_fields)
            MSG = 'Driver({:s}) selected for device({:s}) with filter_fields({:s})...'
            LOGGER.info(MSG.format(str(driver_class.__name__), str(device_uuid), str(filter_fields)))

            if driver_class.__name__ == "OCDriver" or driver_class.__name__ == "OpenROADMDriver":
                driver_instance : _Driver = driver_class(address, port, device_uuid=device_uuid, **settings)
            else:
                driver_instance : _Driver = driver_class(address, port, **settings)

            self._device_uuid__to__driver_instance[device_uuid] = driver_instance
            return driver_instance

    def delete(self, device_uuid : str) -> None:
        with self._lock:
            device_driver = self._device_uuid__to__driver_instance.pop(device_uuid, None)
            if device_driver is None: return
            device_driver.Disconnect()

    def terminate(self) -> None:
        self._terminate.set()
        with self._lock:
            while len(self._device_uuid__to__driver_instance) > 0:
                device_uuid,device_driver = self._device_uuid__to__driver_instance.popitem()
                try:
                    device_driver.Disconnect()
                except: # pylint: disable=bare-except
                    msg = 'Error disconnecting Driver({:s}) from device. Will retry later...'
                    LOGGER.exception(msg.format(device_uuid))
                    # re-adding to retry disconnect
                    self._device_uuid__to__driver_instance[device_uuid] = device_driver

def get_driver(driver_instance_cache : DriverInstanceCache, device : Device) -> _Driver:
    device_uuid = device.device_id.device_uuid.uuid

    driver : _Driver = driver_instance_cache.get(device_uuid)
    if driver is not None: return driver

    driver_filter_fields = get_device_driver_filter_fields(device)
    connect_rules = get_connect_rules(device.device_config)

    #LOGGER.info('[get_driver] connect_rules = {:s}'.format(str(connect_rules)))
    address  = connect_rules.get('address',  '127.0.0.1')
    port     = connect_rules.get('port',     '0')
    settings = connect_rules.get('settings', '{}')

    try:
        settings = json.loads(settings)
    except ValueError as e:
        raise InvalidArgumentException(
            'device.device_config.config_rules[settings]', settings,
            extra_details='_connect/settings Config Rules provided cannot be decoded as JSON dictionary.'
        ) from e

    driver : _Driver = driver_instance_cache.get(
        device_uuid, filter_fields=driver_filter_fields, address=address, port=port, settings=settings)
    driver.Connect()

    return driver

def preload_drivers(driver_instance_cache : DriverInstanceCache) -> None:
    context_client = ContextClient()
    devices = context_client.ListDevices(Empty())
    for device in devices.devices: get_driver(driver_instance_cache, device)
