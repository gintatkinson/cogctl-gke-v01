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

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.base import JobLookupError
from datetime import datetime
import time
import logging

LOGGER = logging.getLogger(__name__)

class AlarmManager():
    def __init__(self, metrics_db):
        self.metrics_db = metrics_db
        self.scheduler = BackgroundScheduler(executors={'processpool': ProcessPoolExecutor(max_workers=20)})
        self.scheduler.start()
        LOGGER.info("Alarm Manager Initialized")

    def create_alarm(self, alarm_queue,alarm_id, kpi_id, kpiMinValue, kpiMaxValue, inRange, includeMinValue, includeMaxValue, subscription_frequency_ms, subscription_timeout_s=None):
        start_date=None
        end_date=None
        if subscription_timeout_s:
            start_timestamp=time.time()
            end_timestamp = start_timestamp + subscription_timeout_s
            start_date = datetime.utcfromtimestamp(start_timestamp).isoformat()
            end_date = datetime.utcfromtimestamp(end_timestamp).isoformat()

        job = self.scheduler.add_job(self.metrics_db.get_alarm_data,
                               args=(alarm_queue,kpi_id, kpiMinValue, kpiMaxValue, inRange, includeMinValue, includeMaxValue, subscription_frequency_ms),
                               trigger='interval', seconds=(subscription_frequency_ms/1000), start_date=start_date,
                               end_date=end_date,timezone=pytz.utc, id=str(alarm_id))
        LOGGER.debug(f"Alarm job {alarm_id} succesfully created")
        #job.remove()

    def delete_alarm(self, alarm_id):
        try:
            self.scheduler.remove_job(alarm_id)
            LOGGER.debug(f"Alarm job {alarm_id} succesfully deleted")
        except (Exception, JobLookupError) as e:
            LOGGER.debug(f"Alarm job {alarm_id} does not exists")
