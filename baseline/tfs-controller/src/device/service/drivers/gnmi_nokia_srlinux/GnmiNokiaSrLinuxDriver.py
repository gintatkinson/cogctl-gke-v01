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

import logging, queue, threading
from typing import Any, Iterator, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.type_checkers.Checkers import chk_type
from device.service.driver_api._Driver import _Driver
from .GnmiSessionHandler import GnmiSessionHandler

DRIVER_NAME = 'gnmi_nokiasrlinux'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class GnmiNokiaSrLinuxDriver(_Driver):
    def __init__(self, address : str, port : int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__logger = logging.getLogger('{:s}:[{:s}:{:s}]'.format(str(__name__), str(self.address), str(self.port)))
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        self.__handler = GnmiSessionHandler(self.address, self.port, settings, self.__logger)
        self.__out_samples = self.__handler.out_samples

    def Connect(self) -> bool:
        with self.__lock:
            if self.__started.is_set(): return True
            self.__handler.connect()
            self.__started.set()
            return True

    def Disconnect(self) -> bool:
        with self.__lock:
            # Trigger termination of loops and processes
            self.__terminate.set()
            # If not started, assume it is already disconnected
            if not self.__started.is_set(): return True
            self.__handler.disconnect()
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return []

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        with self.__lock:
            return self.__handler.get(resource_keys)

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        with self.__lock:
            return self.__handler.set(resources)

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        with self.__lock:
            return self.__handler.delete(resources)

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        chk_type('subscriptions', subscriptions, list)
        if len(subscriptions) == 0: return []
        with self.__lock:
            return self.__handler.subscribe(subscriptions)

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        chk_type('subscriptions', subscriptions, list)
        if len(subscriptions) == 0: return []
        with self.__lock:
            return self.__handler.unsubscribe(subscriptions)

    def GetState(self, blocking=False, terminate : Optional[threading.Event] = None) -> Iterator[Tuple[str, Any]]:
        while True:
            if self.__terminate.is_set(): break
            if terminate is not None and terminate.is_set(): break
            try:
                sample = self.__out_samples.get(block=blocking, timeout=0.1)
            except queue.Empty:
                if blocking: continue
                return
            if sample is None: continue
            yield sample
