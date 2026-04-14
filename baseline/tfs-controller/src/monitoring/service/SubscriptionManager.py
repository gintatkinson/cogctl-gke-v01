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

import pytz
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime
import time


LOGGER = logging.getLogger(__name__)

class SubscriptionManager():
    def __init__(self, metrics_db):
        self.metrics_db = metrics_db
        self.scheduler = BackgroundScheduler(executors={'processpool': ProcessPoolExecutor(max_workers=20)})
        self.scheduler.start()
        
    def create_subscription(self,subs_queue, subscription_id, kpi_id, sampling_interval_s, sampling_duration_s=None, start_timestamp=None, end_timestamp=None):
        start_date = None
        end_date = None
        if sampling_duration_s:
            if not start_timestamp:
                start_timestamp = time.time()
            end_timestamp = start_timestamp + sampling_duration_s
        if start_timestamp:
            start_date = datetime.utcfromtimestamp(start_timestamp).isoformat()
        if end_timestamp:
            end_date = datetime.utcfromtimestamp(end_timestamp).isoformat()

        job = self.scheduler.add_job(self.metrics_db.get_subscription_data, args=(subs_queue,kpi_id, sampling_interval_s),
                               trigger='interval', seconds=sampling_interval_s, start_date=start_date,
                               end_date=end_date, timezone=pytz.utc, id=str(subscription_id))
        LOGGER.debug(f"Subscrition job {subscription_id} succesfully created")
        #job.remove()

    def delete_subscription(self, subscription_id):
        self.scheduler.remove_job(subscription_id)
        LOGGER.debug(f"Subscription job {subscription_id} succesfully deleted")