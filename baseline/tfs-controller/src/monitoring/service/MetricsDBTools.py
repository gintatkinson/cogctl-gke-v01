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

import time
import math
from random import random

from questdb.ingress import Sender, IngressError
import requests
import json
import logging
import datetime
from common.tools.timestamp.Converters import timestamp_float_to_string, timestamp_utcnow_to_float
import psycopg2

from monitoring.service.NameMapping import NameMapping

LOGGER = logging.getLogger(__name__)


class MetricsDB():
    def __init__(self, host, name_mapping : NameMapping, ilp_port=9009, rest_port=9000, table="monitoring",
                 commit_lag_ms=1000, retries=10, postgre=False, postgre_port=8812, postgre_user='admin',
                 postgre_password='quest'):
        try:
            self.host = host
            self.name_mapping = name_mapping
            self.ilp_port = int(ilp_port)
            self.rest_port = rest_port
            self.table = table
            self.commit_lag_ms = commit_lag_ms
            self.retries = retries
            self.postgre = postgre
            self.postgre_port = postgre_port
            self.postgre_user = postgre_user
            self.postgre_password = postgre_password
            self.create_table()
            LOGGER.info("MetricsDB initialized")
        except:
            LOGGER.info("MetricsDB cannot be initialized")
            raise Exception("Critical error in the monitoring component")

    def is_postgre_enabled(self):
        LOGGER.info(f"PostgreSQL is {self.postgre}")
        return self.postgre

    def get_retry_number(self):
        LOGGER.info(f"Retry number is {self.retries}")
        return self.retries

    def get_commit_lag(self):
        LOGGER.info(f"Commit lag of monitoring queries is {self.commit_lag_ms} ms")
        return self.commit_lag_ms

    def enable_postgre_mode(self):
        self.postgre = True
        LOGGER.info("MetricsDB PostgreSQL query mode enabled")

    def disable_postgre_mode(self):
        self.postgre = False
        LOGGER.info("MetricsDB REST query mode enabled")

    def set_postgre_credentials(self, user, password):
        self.postgre_user = user
        self.postgre_password = password
        LOGGER.info("MetricsDB PostgreSQL credentials changed")

    def set_retry_number(self, retries):
        self.retries = retries
        LOGGER.info(f"Retriy number changed to {retries}")

    def set_commit_lag(self, commit_lag_ms):
        self.commit_lag_ms = commit_lag_ms
        LOGGER.info(f"Commit lag of monitoring queries changed to {commit_lag_ms} ms")

    def create_table(self):
        try:
            query = f'CREATE TABLE IF NOT EXISTS {self.table}' \
                    '(kpi_id SYMBOL,' \
                    'kpi_sample_type SYMBOL,' \
                    'device_id SYMBOL,' \
                    'device_name SYMBOL,' \
                    'endpoint_id SYMBOL,' \
                    'endpoint_name SYMBOL,' \
                    'service_id SYMBOL,' \
                    'slice_id SYMBOL,' \
                    'connection_id SYMBOL,' \
                    'link_id SYMBOL,' \
                    'timestamp TIMESTAMP,' \
                    'kpi_value DOUBLE)' \
                    'TIMESTAMP(timestamp);'
            result = self.run_query(query)
            if (result == True):
                LOGGER.info(f"Table {self.table} created")
        except (Exception) as e:
            LOGGER.debug(f"Table {self.table} cannot be created. {e}")
            raise Exception

    def write_KPI(self, time, kpi_id, kpi_sample_type, device_id, endpoint_id, service_id, slice_id, connection_id, link_id, kpi_value):
        device_name = self.name_mapping.get_device_name(device_id) or ''
        endpoint_name = self.name_mapping.get_endpoint_name(endpoint_id) or ''

        counter = 0
        while (counter < self.retries):
            try:
                with Sender(self.host, self.ilp_port) as sender:
                    sender.row(
                        self.table,
                        symbols={
                            'kpi_id': kpi_id,
                            'kpi_sample_type': kpi_sample_type,
                            'device_id': device_id,
                            'device_name': device_name,
                            'endpoint_id': endpoint_id,
                            'endpoint_name': endpoint_name,
                            'service_id': service_id,
                            'slice_id': slice_id,
                            'connection_id': connection_id,
                            'link_id': link_id,
                        },
                        columns={
                            'kpi_value': kpi_value},
                        at=datetime.datetime.fromtimestamp(time))
                    sender.flush()
                counter = self.retries
                LOGGER.debug(f"KPI written in the MetricsDB")
            except (Exception, IngressError) as e:
                counter = counter + 1
                if counter == self.retries:
                    raise Exception(f"Maximum number of retries achieved: {self.retries}")

    def run_query(self, sql_query):
        counter = 0
        while (counter < self.retries):
            try:
                query_params = {'query': sql_query, 'fmt': 'json'}
                url = f"http://{self.host}:{self.rest_port}/exec"
                response = requests.get(url, params=query_params)
                json_response = json.loads(response.text)
                if ('ddl' in json_response):
                    LOGGER.debug(f"REST query executed succesfully, result: {json_response['ddl']}")
                    counter = self.retries
                    return True
                elif ('dataset' in json_response):
                    LOGGER.debug(f"REST query executed, result: {json_response['dataset']}")
                    counter = self.retries
                    return json_response['dataset']
            except (Exception, requests.exceptions.RequestException) as e:
                counter = counter + 1
                if counter == self.retries:
                    raise Exception(f"Maximum number of retries achieved: {self.retries}")

    def run_query_postgre(self, postgre_sql_query):
        connection = None
        cursor = None
        counter = 0
        while (counter < self.retries):
            try:
                connection = psycopg2.connect(
                    user=self.postgre_user,
                    password=self.postgre_password,
                    host=self.host,
                    port=self.postgre_port,
                    database=self.table)
                cursor = connection.cursor()
                cursor.execute(postgre_sql_query)
                result = cursor.fetchall()
                LOGGER.debug(f"PostgreSQL query executed, result: {result}")
                counter = self.retries
                return result
            except (Exception, psycopg2.Error) as e:
                counter = counter + 1
                if counter == self.retries:
                    raise Exception(f"Maximum number of retries achieved: {self.retries}")
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

    def get_raw_kpi_list(self, kpi_id, monitoring_window_s, last_n_samples, start_timestamp, end_timestamp):
        try:
            query_root  = f"SELECT timestamp, kpi_value FROM {self.table} WHERE kpi_id = '{kpi_id}' "
            query       = query_root
            start_date  = float()
            end_date    = float()
            if last_n_samples:
                query = query + f"ORDER BY timestamp DESC limit {last_n_samples}"
            elif monitoring_window_s or start_timestamp or end_timestamp:
                if start_timestamp and end_timestamp:
                    start_date  = start_timestamp
                    end_date    = end_timestamp
                elif monitoring_window_s:
                    if start_timestamp and not end_timestamp:
                        start_date  = start_timestamp
                        end_date    = start_date + monitoring_window_s
                    elif end_timestamp and not start_timestamp:
                        end_date    = end_timestamp
                        start_date  = end_date - monitoring_window_s
                    elif not start_timestamp and not end_timestamp:
                        end_date    = timestamp_utcnow_to_float()
                        start_date  = end_date - monitoring_window_s
                query = query + f"AND (timestamp BETWEEN '{timestamp_float_to_string(start_date)}' AND '{timestamp_float_to_string(end_date)}')"
            else:
                LOGGER.debug(f"Wrong parameters settings")

            LOGGER.debug(query)

            if self.postgre:
                kpi_list = self.run_query_postgre(query)
                LOGGER.debug(f"kpi_list postgre: {kpi_list}")
            else:
                kpi_list = self.run_query(query)
                LOGGER.debug(f"kpi_list influx: {kpi_list}")
            if kpi_list:
                LOGGER.debug(f"New data received for subscription to KPI {kpi_id}")
                return kpi_list
            else:
                LOGGER.debug(f"No new data for the subscription to KPI {kpi_id}")
        except (Exception) as e:
            LOGGER.debug(f"Subscription data cannot be retrieved. {e}")

    def get_subscription_data(self,subs_queue, kpi_id, sampling_interval_s=1):
        try:
            end_date = timestamp_utcnow_to_float() - self.commit_lag_ms / 1000
            start_date = end_date - sampling_interval_s
            query = f"SELECT kpi_id, timestamp, kpi_value FROM {self.table} WHERE kpi_id = '{kpi_id}' AND (timestamp BETWEEN '{timestamp_float_to_string(start_date)}' AND '{timestamp_float_to_string(end_date)}')"
            LOGGER.debug(query)
            if self.postgre:
                kpi_list = self.run_query_postgre(query)
                LOGGER.debug(f"kpi_list postgre: {kpi_list}")
            else:
                kpi_list = self.run_query(query)
                LOGGER.debug(f"kpi_list influx: {kpi_list}")
            if kpi_list:
                subs_queue.put_nowait(kpi_list)
                LOGGER.debug(f"New data received for subscription to KPI {kpi_id}")
            else:
                LOGGER.debug(f"No new data for the subscription to KPI {kpi_id}")
        except (Exception) as e:
            LOGGER.debug(f"Subscription data cannot be retrieved. {e}")

    def get_alarm_data(self, alarm_queue, kpi_id, kpiMinValue, kpiMaxValue, inRange=True, includeMinValue=True, includeMaxValue=True,
                       subscription_frequency_ms=1000):
        try:
            end_date = timestamp_utcnow_to_float() - self.commit_lag_ms / 1000
            start_date = end_date - subscription_frequency_ms / 1000
            query = f"SELECT kpi_id, timestamp, kpi_value FROM {self.table} WHERE kpi_id = '{kpi_id}' AND (timestamp BETWEEN '{timestamp_float_to_string(start_date)}' AND '{timestamp_float_to_string(end_date)}')"
            if self.postgre:
                kpi_list = self.run_query_postgre(query)
            else:
                kpi_list = self.run_query(query)
            if kpi_list:
                LOGGER.debug(f"New data received for alarm of KPI {kpi_id}")
                LOGGER.info(kpi_list)
                valid_kpi_list = []
                for kpi in kpi_list:
                    alarm = False
                    kpi_value = kpi[2]
                    kpiMinIsNone = ((kpiMinValue is None) or math.isnan(kpiMinValue))
                    kpiMaxIsNone = ((kpiMaxValue is None) or math.isnan(kpiMaxValue))
                    if (kpiMinValue == kpi_value and kpiMaxValue == kpi_value and inRange):
                        alarm = True
                    elif (inRange and not kpiMinIsNone and not kpiMaxIsNone and includeMinValue and includeMaxValue):
                        if (kpi_value >= kpiMinValue and kpi_value <= kpiMaxValue):
                            alarm = True
                    elif (inRange and not kpiMinIsNone and not kpiMaxIsNone and includeMinValue and not includeMaxValue):
                        if (kpi_value >= kpiMinValue and kpi_value < kpiMaxValue):
                            alarm = True
                    elif (inRange and not kpiMinIsNone and not kpiMaxIsNone and not includeMinValue and includeMaxValue):
                        if (kpi_value > kpiMinValue and kpi_value <= kpiMaxValue):
                            alarm = True
                    elif (inRange and not kpiMinIsNone and not kpiMaxIsNone and not includeMinValue and not includeMaxValue):
                        if (kpi_value > kpiMinValue and kpi_value < kpiMaxValue):
                            alarm = True
                    elif (not inRange and not kpiMinIsNone and not kpiMaxIsNone and includeMinValue and includeMaxValue):
                        if (kpi_value <= kpiMinValue or kpi_value >= kpiMaxValue):
                            alarm = True
                    elif (not inRange and not kpiMinIsNone and not kpiMaxIsNone and includeMinValue and not includeMaxValue):
                        if (kpi_value <= kpiMinValue or kpi_value > kpiMaxValue):
                            alarm = True
                    elif (not inRange and not kpiMinIsNone and not kpiMaxIsNone and not includeMinValue and includeMaxValue):
                        if (kpi_value < kpiMinValue or kpi_value >= kpiMaxValue):
                            alarm = True
                    elif (not inRange and not kpiMinIsNone and not kpiMaxIsNone and not includeMinValue and not includeMaxValue):
                        if (kpi_value < kpiMinValue or kpi_value > kpiMaxValue):
                            alarm = True
                    elif (inRange and not kpiMinIsNone and kpiMaxIsNone and includeMinValue):
                        if (kpi_value >= kpiMinValue):
                            alarm = True
                    elif (inRange and not kpiMinIsNone and kpiMaxIsNone and not includeMinValue):
                        if (kpi_value > kpiMinValue):
                            alarm = True
                    elif (not inRange and not kpiMinIsNone and kpiMaxIsNone and includeMinValue):
                        if (kpi_value <= kpiMinValue):
                            alarm = True
                    elif (not inRange and not kpiMinIsNone and kpiMaxIsNone and not includeMinValue):
                        if (kpi_value < kpiMinValue):
                            alarm = True
                    elif (inRange and kpiMinIsNone and not kpiMaxIsNone and includeMaxValue):
                        if (kpi_value <= kpiMaxValue):
                            alarm = True
                    elif (inRange and kpiMinIsNone and not kpiMaxIsNone and not includeMaxValue):
                        if (kpi_value < kpiMaxValue):
                            alarm = True
                    elif (not inRange and kpiMinIsNone and not kpiMaxIsNone and includeMaxValue):
                        if (kpi_value >= kpiMaxValue):
                            alarm = True
                    elif (not inRange and kpiMinIsNone and not kpiMaxIsNone and not includeMaxValue):
                        if (kpi_value > kpiMaxValue):
                            alarm = True

                    if alarm:
                        valid_kpi_list.append(kpi)
                if valid_kpi_list:
                    alarm_queue.put_nowait(valid_kpi_list)
                    LOGGER.debug(f"Alarm of KPI {kpi_id} triggered -> kpi_value:{kpi[2]}, timestamp:{kpi[1]}")
                else:
                    LOGGER.debug(f"No new alarms triggered for the alarm of KPI {kpi_id}")
            else:
                LOGGER.debug(f"No new data for the alarm of KPI {kpi_id}")
        except (Exception) as e:
            LOGGER.debug(f"Alarm data cannot be retrieved. {e}")
