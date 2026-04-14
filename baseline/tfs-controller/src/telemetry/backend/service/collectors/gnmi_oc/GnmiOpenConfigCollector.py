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


import logging, pytz, queue
from datetime import datetime
from typing import Dict, Optional, Tuple, List, Union, Any, Iterator
from pygnmi.client import gNMIclient
from telemetry.backend.service.collector_api._Collector import _Collector
from .PathMapper import PathMapper
from .SubscriptionNew import Subscription

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)8s [%(name)s - %(funcName)s()]: %(message)s",
)

class GNMIOpenConfigCollector(_Collector):
    """
    GNMI OpenConfig Collector
    =========================
    Lightweight wrapper around *pygnmi* with subscribe / get / unsubscribe helpers.
    """
    def __init__(self, address: str = '', port: int = -1, **setting ) -> None:
        
        super().__init__('gNMI_openconfig_collector', address, port, **setting)
        self._subscriptions : Dict[str, Subscription] = {}

        self.username = setting.get('username', 'admin')
        self.password = setting.get('password', 'admin')
        self.insecure = setting.get('insecure', True)
        # self.username = username
        # self.password = password
        # self.insecure = insecure

        self.connected = False          # To track connection state
        self.client: Optional[gNMIclient] = None
        self._output_queue = queue.Queue()  # Queue for telemetry updates

        self.logger    = logging.getLogger(__name__)
        self.logger.debug("GNMICollector instantiated.")


    def Connect(self) -> bool:
        """
        Connect to the gNMI target device.
        """
        if not self.connected:
            self.client = gNMIclient(
                target=(self.address, self.port),
                username=self.username,
                password=self.password,
                insecure=self.insecure
            )
            # self.logger.info("Connecting to gNMI target %s:%s with %s and %s", self.address, self.port, self.username, self.password)
            self.client.connect()           # type: ignore
            self.connected = True
            self.logger.info("Connected to gNMI target %s:%s", self.address, self.port)
            return True
        else:
            self.logger.warning("Already connected to gNMI target %s:%s", self.address, self.port)
            return True

    def Disconnect(self) -> bool:
        """
        Disconnect from the gNMI target device.
        """
        if self.connected and self.client:
            self.client.close()
            self.connected = False
            self.logger.info("Disconnected from gNMI target %s:%s", self.address, self.port)
            return True
        else:
            self.logger.warning("Not connected to any gNMI target.")
            return True

    def SubscribeState(self, subscriptions: List[Tuple[str, dict, float, float]]
                  ) -> List[Union[bool, Exception]]:
        response = []
        for subscription in subscriptions:
            try:
                # Validate subscription format
                if len(subscription) != 4:
                    raise ValueError(f"Expected 4 elements, got {len(subscription)}")
                sub_id, sub_endpoint, duration, interval = subscription

                if not isinstance(sub_endpoint, dict):
                    raise TypeError("Endpoint must be a dictionary.")
                if sub_endpoint.get('endpoint') is None:
                    raise KeyError("Endpoint dictionary must contain 'endpoint' key.")
                if sub_endpoint.get('kpi') is None:
                    raise KeyError("Endpoint dictionary must contain 'kpi' key.")
                if sub_endpoint.get('resource') is None:
                    raise KeyError("Endpoint dictionary must contain 'resource' key.")

                paths = PathMapper.build(
                                endpoint=sub_endpoint['endpoint'],
                                kpi=sub_endpoint['kpi'],
                                resource=sub_endpoint['resource'],
                )

                self._subscriptions[sub_id] = Subscription(
                    sub_id                = sub_id,
                    gnmi_client           = self.client,                   # type: ignore
                    path_list             = paths,                         # <- list of paths
                    metric_queue          = self._output_queue,
                    mode                  = 'stream',                      # Default mode
                    sample_interval_ns    = int(interval * 1_000_000_000), # Convert seconds to nanoseconds
                    heartbeat_interval_ns = int(duration * 1_000_000_000), # Convert seconds to nanoseconds
                    encoding              = 'json_ietf',                   # Default encoding
                )

                self.logger.info("Subscribing to %s with job_id %s ...", sub_endpoint, sub_id)
                response.append(True)
            except:
                self.logger.exception("Invalid subscription format: %s", subscription)
                response.append(False)
        return response

    def UnsubscribeState(self, resource_key: str) -> bool:
        """Stop the given subscription."""
        sub = self._subscriptions.pop(resource_key, None)
        if not sub:
            self.logger.error("Attempt to unsubscribe unknown id=%s", resource_key)
            # raise KeyError(f"Unknown subscription id '{resource_key}'.")
            return False
        try: sub.stop()
        except:
            self.logger.exception("Error stopping subscription %s. ", resource_key)
            return False
        self.logger.info("Unsubscribed from state: %s", resource_key)
        return True

    def GetState(self, duration : float, blocking : bool = True, terminate: Optional[queue.Queue] = None
                 ) -> Iterator[Tuple[float, str, Any]]:
        """
        Pull a single telemetry update from the queue.
        Returns an iterator that yields (timestamp, resource_key, data).
        """
        logging.debug("GetState called with duration=%s, blocking=%s", duration, blocking)
        start_time = datetime.now(pytz.utc)
        while True:
            logging.debug("GetState loop started at %s", start_time)
            try:
                if terminate and not terminate.empty():
                    self.logger.info("Termination signal received, stopping GetState")
                    break

                elapsed_time = (datetime.now(pytz.utc) - start_time).total_seconds()
                if elapsed_time >= duration:
                    self.logger.info("Duration expired, stopping GetState")
                    break

                sample = self._output_queue.get(block=blocking, timeout=1 if blocking else 0.1)
                self.logger.info(f"Retrieved state sample: {sample}")
                yield sample
            except queue.Empty:
                if not blocking:
                    self.logger.info("No more samples in queue, exiting GetState")
                    return None
        # sample = self._output_queue.get(block=blocking, timeout=duration if blocking else 0.1)
        # yield sample

        # return self._output_queue.get(timeout=duration) if blocking else self._output_queue.get_nowait()
        # Note: This method will block until an item is available or the timeout is reached.
