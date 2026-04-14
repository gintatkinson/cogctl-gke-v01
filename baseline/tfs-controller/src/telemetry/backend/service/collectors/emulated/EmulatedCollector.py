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

import pytz
import queue
import logging
from anytree import Node, Resolver
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Any, Iterator, List, Tuple, Union, Optional
from telemetry.backend.service.collector_api._Collector import _Collector
from .EmulatedHelper import EmulatedCollectorHelper
from .SyntheticMetricsGenerator import SyntheticMetricsGenerator


class EmulatedCollector(_Collector):
    """
    EmulatedCollector is a class that simulates a network collector for testing purposes.
    It provides functionalities to manage configurations, state subscriptions, and synthetic data generation.
    """
    def __init__(self, address: str, port: int, **settings):
        super().__init__('emulated_collector', address, port, **settings)
        self._out_samples    = queue.Queue()                # Queue to hold synthetic state samples
        self._synthetic_data = SyntheticMetricsGenerator(metric_queue=self._out_samples)  # Placeholder for synthetic data generator
        self._scheduler      = BackgroundScheduler(daemon=True)
        self._scheduler.configure(
            jobstores = {'default': MemoryJobStore()},
            executors = {'default': ThreadPoolExecutor(max_workers=1)},
            timezone  = pytz.utc
        )
        # self._scheduler.add_listener(self._listener_job_added_to_subscription_tree,     EVENT_JOB_ADDED)
        # self._scheduler.add_listener(self._listener_job_removed_from_subscription_tree, EVENT_JOB_REMOVED)
        self._helper_methods = EmulatedCollectorHelper()

        self.logger    = logging.getLogger(__name__)
        self.connected = False          # To track connection state
        self.logger.info("EmulatedCollector initialized")

    def Connect(self) -> bool:
        self.logger.info(f"Connecting to {self.address}:{self.port}")
        self.connected = True
        self._scheduler.start()
        self.logger.info(f"Successfully connected to {self.address}:{self.port}")
        return True

    def Disconnect(self) -> bool:
        self.logger.info(f"Disconnecting from {self.address}:{self.port}")
        if not self.connected:
            self.logger.warning("Collector is not connected. Nothing to disconnect.")
            return False
        self._scheduler.shutdown()
        self.connected = False
        self.logger.info(f"Successfully disconnected from {self.address}:{self.port}")
        return True

    def _require_connection(self):
        if not self.connected:
            raise RuntimeError("Collector is not connected. Please connect before performing operations.")

    def SubscribeState(self, subscriptions: List[Tuple[str, dict, float, float]]) -> bool:
        self._require_connection()
        try:
            job_id, endpoint, duration, interval = subscriptions
        except:
            self.logger.exception(f"Invalid subscription format: {subscriptions}")
            return False
        if endpoint:
            self.logger.info(f"Subscribing to {endpoint} with duration {duration}s and interval {interval}s")
            try:
                sample_type_ids = endpoint['sample_types']   # type: ignore
                resource_name   = endpoint['name']           # type: ignore
                # Add the job to the scheduler
                self._scheduler.add_job(
                    self._generate_sample,
                    'interval',
                    seconds=interval,
                    args=[resource_name, sample_type_ids],
                    id=f"{job_id}",
                    replace_existing=True,
                    end_date=datetime.now(pytz.utc) + timedelta(seconds=duration)
                )
                self.logger.info(f"Job added to scheduler for resource key {resource_name} with duration {duration}s and interval {interval}s")
                return True
            except:
                self.logger.exception(f"Failed to verify resource key or add job:")
                return False
        else:
            self.logger.warning(f"No sample types found for {endpoint}. Skipping subscription.")
            return False

    def UnsubscribeState(self, resource_key: str) -> bool:
        self._require_connection()
        try: 
            # Check if job exists
            job_ids = [job.id for job in self._scheduler.get_jobs() if resource_key in job.id]
            if not job_ids:
                self.logger.warning(f"No active jobs found for {resource_key}. It might have already terminated.")
                return False
            for job_id in job_ids:
                self._scheduler.remove_job(job_id)
            self.logger.info(f"Unsubscribed from {resource_key} with job IDs: {job_ids}")
            return True
        except:
            self.logger.exception(f"Failed to unsubscribe from {resource_key}")
            return False

    def GetState(self, duration : int, blocking: bool = False, terminate: Optional[queue.Queue] = None) -> Iterator[Tuple[float, str, Any]]:
        self._require_connection()
        start_time = datetime.now(pytz.utc)
        while True:
            try:
                if terminate and not terminate.empty():
                    self.logger.info("Termination signal received, stopping GetState")
                    break

                elapsed_time = (datetime.now(pytz.utc) - start_time).total_seconds()
                if elapsed_time >= duration:
                    self.logger.info("Duration expired, stopping GetState")
                    break

                sample = self._out_samples.get(block=blocking, timeout=1 if blocking else 0.1)
                self.logger.info(f"Retrieved state sample: {sample}")
                yield sample
            except queue.Empty:
                if not blocking:
                    self.logger.info("No more samples in queue, exiting GetState")
                    return None

    def _generate_sample(self, resource_key: str, sample_type_ids : List[int]):
        # Simulate generating a sample for the resource key
        self.logger.debug(f"Executing _generate_sample for resource: {resource_key}")
        sample = self._synthetic_data.generate_synthetic_data_point(resource_key, sample_type_ids)
        self._out_samples.put(sample)
