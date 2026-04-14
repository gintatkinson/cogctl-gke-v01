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

import sqlite3
import logging

LOGGER = logging.getLogger(__name__)

class ManagementDB():
    def __init__(self, database):
        try:
            self.client = sqlite3.connect(database, check_same_thread=False)
            self.create_monitoring_table()
            self.create_subscription_table()
            self.create_alarm_table()
            LOGGER.info("ManagementDB initialized")
        except:
            LOGGER.info("ManagementDB cannot be initialized")
            raise Exception("Critical error in the monitoring component")
        
    def create_monitoring_table(self):
        try:
            result=self.client.execute("""
                CREATE TABLE IF NOT EXISTS kpi(
                    kpi_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kpi_description TEXT,
                    kpi_sample_type INTEGER,
                    device_id STRING,
                    endpoint_id STRING,
                    service_id STRING,
                    slice_id STRING,
                    connection_id STRING,
                    link_id STRING,
                    monitor_flag STRING
                );
            """)
            LOGGER.debug("KPI table created in the ManagementDB")
        except sqlite3.Error as e:
            LOGGER.debug(f"KPI table cannot be created in the ManagementD. {e}")
            raise Exception
    
    def create_subscription_table(self):
        try:
            result= self.client.execute("""
                CREATE TABLE IF NOT EXISTS subscription(
                    subs_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kpi_id INTEGER,
                    subscriber TEXT,
                    sampling_duration_s REAL,
                    sampling_interval_s REAL,
                    start_timestamp REAL,
                    end_timestamp REAL
                );
            """)
            LOGGER.info("Subscription table created in the ManagementDB")
        except sqlite3.Error as e:
            LOGGER.debug(f"Subscription table cannot be created in the ManagementDB. {e}")
            raise Exception

    def create_alarm_table(self):
        try:
            result=self.client.execute("""
                CREATE TABLE IF NOT EXISTS alarm(
                    alarm_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alarm_description TEXT,
                    alarm_name TEXT,
                    kpi_id INTEGER,
                    kpi_min_value REAL,
                    kpi_max_value REAL,
                    in_range INTEGER,
                    include_min_value INTEGER,
                    include_max_value INTEGER
                );
            """)
            LOGGER.info("Alarm table created in the ManagementDB")
        except sqlite3.Error as e:
            LOGGER.debug(f"Alarm table cannot be created in the ManagementDB. {e}")
            raise Exception

    def insert_KPI(self,kpi_description,kpi_sample_type,device_id,endpoint_id,service_id,slice_id,connection_id,link_id):
        try:
            c = self.client.cursor()
            c.execute("SELECT kpi_id FROM kpi WHERE device_id is ? AND kpi_sample_type is ? AND endpoint_id is ? AND service_id is ? AND slice_id is ? AND connection_id is ? AND link_id is ?",(device_id,kpi_sample_type,endpoint_id,service_id,slice_id,connection_id,link_id))
            data=c.fetchone()
            if data is None:
                c.execute("INSERT INTO kpi (kpi_description,kpi_sample_type,device_id,endpoint_id,service_id,slice_id,connection_id,link_id) VALUES (?,?,?,?,?,?,?,?)", (kpi_description,kpi_sample_type,device_id,endpoint_id,service_id,slice_id,connection_id,link_id))
                self.client.commit()
                kpi_id = c.lastrowid
                LOGGER.debug(f"KPI {kpi_id} succesfully inserted in the ManagementDB")
                return kpi_id
            else:
                kpi_id = data[0]
                LOGGER.debug(f"KPI {kpi_id} already exists")
                return kpi_id
        except sqlite3.Error as e:
            LOGGER.debug("KPI cannot be inserted in the ManagementDB: {e}")
            
    def insert_subscription(self,kpi_id,subscriber,sampling_duration_s,sampling_interval_s,start_timestamp, end_timestamp):
        try:
            c = self.client.cursor()
            c.execute("SELECT subs_id FROM subscription WHERE kpi_id is ? AND subscriber is ? AND sampling_duration_s is ? AND sampling_interval_s is ? AND start_timestamp is ? AND end_timestamp is ?",(kpi_id,subscriber,sampling_duration_s,sampling_interval_s,start_timestamp, end_timestamp))
            data=c.fetchone()
            if data is None:
                c.execute("INSERT INTO subscription (kpi_id,subscriber,sampling_duration_s,sampling_interval_s,start_timestamp, end_timestamp) VALUES (?,?,?,?,?,?)", (kpi_id,subscriber,sampling_duration_s,sampling_interval_s,start_timestamp, end_timestamp))
                self.client.commit()
                subs_id = c.lastrowid
                LOGGER.debug(f"Subscription {subs_id} succesfully inserted in the ManagementDB")
                return subs_id
            else:
                subs_id = data[0]
                LOGGER.debug(f"Subscription {subs_id} already exists")
                return subs_id
        except sqlite3.Error as e:
            LOGGER.debug("Subscription cannot be inserted in the ManagementDB: {e}")

    def insert_alarm(self,alarm_description,alarm_name,kpi_id,kpi_min_value,kpi_max_value,in_range,include_min_value,include_max_value):
        try:
            c = self.client.cursor()
            c.execute("SELECT alarm_id FROM alarm WHERE alarm_description is ? AND alarm_name is ? AND kpi_id is ? AND kpi_min_value is ? AND kpi_max_value is ? AND in_range is ? AND include_min_value is ? AND include_max_value is ?",(alarm_description,alarm_name,kpi_id,kpi_min_value,kpi_max_value,in_range,include_min_value,include_max_value))
            data=c.fetchone()
            if data is None:
                c.execute("INSERT INTO alarm (alarm_description, alarm_name, kpi_id, kpi_min_value, kpi_max_value, in_range, include_min_value, include_max_value) VALUES (?,?,?,?,?,?,?,?)", (alarm_description,alarm_name,kpi_id,kpi_min_value,kpi_max_value,in_range,include_min_value,include_max_value))
                self.client.commit()
                alarm_id=c.lastrowid
                LOGGER.debug(f"Alarm {alarm_id} succesfully inserted in the ManagementDB")
                return alarm_id
            else:
                alarm_id=data[0]
                LOGGER.debug(f"Alarm {alarm_id} already exists")
                return alarm_id
        except sqlite3.Error as e:
            LOGGER.debug(f"Alarm cannot be inserted in the ManagementDB: {e}")

    def delete_KPI(self,kpi_id):
        try:
            c = self.client.cursor()
            c.execute("SELECT * FROM kpi WHERE kpi_id is ?",(kpi_id,))       
            data=c.fetchone()
            if data is None:
                LOGGER.debug(f"KPI {kpi_id} does not exists")
                return False
            else:
                c.execute("DELETE FROM kpi WHERE kpi_id is ?",(kpi_id,))
                self.client.commit()
                LOGGER.debug(f"KPI {kpi_id} deleted from the ManagementDB")
                return True
        except sqlite3.Error as e:
            LOGGER.debug(f"KPI cannot be deleted from the ManagementDB: {e}")

    def delete_subscription(self,subs_id):
        try:
            c = self.client.cursor()
            c.execute("SELECT * FROM subscription WHERE subs_id is ?",(subs_id,))       
            data=c.fetchone()
            if data is None:
                LOGGER.debug(f"Subscription {subs_id} does not exists")
                return False
            else:
                c.execute("DELETE FROM subscription WHERE subs_id is ?",(subs_id,))
                self.client.commit()
                LOGGER.debug(f"Subscription {subs_id} deleted from the ManagementDB")
                return True
        except sqlite3.Error as e:
            LOGGER.debug(f"Subscription cannot be deleted from the ManagementDB: {e}")

    def delete_alarm(self,alarm_id):
        try:
            c = self.client.cursor()
            c.execute("SELECT * FROM alarm WHERE alarm_id is ?",(alarm_id,))       
            data=c.fetchone()
            if data is None:
                LOGGER.debug(f"Alarm {alarm_id} does not exists")
                return False
            else:
                c.execute("DELETE FROM alarm WHERE alarm_id is ?",(alarm_id,))
                self.client.commit()
                LOGGER.debug(f"Alarm {alarm_id} deleted from the ManagementDB")
                return True
        except sqlite3.Error as e:
            LOGGER.debug(f"Alarm cannot be deleted from the ManagementDB: {e}")

    def get_KPI(self,kpi_id):
        try:
            data = self.client.execute("SELECT * FROM kpi WHERE kpi_id is ?",(kpi_id,)).fetchone()
            if data:
                LOGGER.debug(f"KPI {kpi_id} succesfully retrieved from the ManagementDB")
                return data
            else:
                LOGGER.debug(f"KPI {kpi_id} does not exists")
                return data
        except sqlite3.Error as e:
            LOGGER.debug(f"KPI {kpi_id} cannot be retrieved from the ManagementDB: {e}")

    def get_subscription(self,subs_id):
        try:
            data = self.client.execute("SELECT * FROM subscription WHERE subs_id is ?",(subs_id,)).fetchone()
            if data:
                LOGGER.debug(f"Subscription {subs_id} succesfully retrieved from the ManagementDB")
                return data
            else:
                LOGGER.debug(f"Subscription {subs_id} does not exists")
                return data
        except sqlite3.Error as e:
            LOGGER.debug(f"Subscription {subs_id} cannot be retrieved from the ManagementDB: {e}")

    def get_alarm(self,alarm_id):
        try:
            data = self.client.execute("SELECT * FROM alarm WHERE alarm_id is ?",(alarm_id,)).fetchone()
            if data:
                LOGGER.debug(f"Alarm {alarm_id} succesfully retrieved from the ManagementDB")
                return data
            else:
                print(data)
                LOGGER.debug(f"Alarm {alarm_id} does not exists")
                return data
        except sqlite3.Error as e:
            LOGGER.debug(f"Alarm {alarm_id} cannot be retrieved from the ManagementDB: {e}")
        
    def get_KPIS(self):
        try:
            data = self.client.execute("SELECT * FROM kpi").fetchall()
            LOGGER.debug(f"KPIs succesfully retrieved from the ManagementDB")
            return data
        except sqlite3.Error as e:
            LOGGER.debug(f"KPIs cannot be retrieved from the ManagementDB: {e}")

    def get_subscriptions(self):
        try:
            data = self.client.execute("SELECT * FROM subscription").fetchall()
            LOGGER.debug(f"Subscriptions succesfully retrieved from the ManagementDB")
            return data
        except sqlite3.Error as e:
            LOGGER.debug(f"Subscriptions cannot be retrieved from the ManagementDB: {e}")

    def get_alarms(self):
        try:
            data = self.client.execute("SELECT * FROM alarm").fetchall()
            LOGGER.debug(f"Alarms succesfully retrieved from the ManagementDB")
            return data
        except sqlite3.Error as e:
            LOGGER.debug(f"Alarms cannot be retrieved from the ManagementDB: {e}")

    def check_monitoring_flag(self,kpi_id):
        try:
            c = self.client.cursor()
            c.execute("SELECT monitor_flag FROM kpi WHERE kpi_id is ?",(kpi_id,))
            data=c.fetchone()
            if data is None:
                LOGGER.debug(f"KPI {kpi_id} does not exists")
                return None
            else:
                if data[0] == 1:
                    return True
                elif data[0] == 0 or data[0] is None:
                    return False
                else:
                    LOGGER.debug(f"KPI {kpi_id} is wrong: {str(data)}")
                    return None
        except sqlite3.Error as e:
            LOGGER.debug(f"KPI {kpi_id} cannot be checked from the ManagementDB: {e}")


    def set_monitoring_flag(self,kpi_id,flag):
        try:
            c = self.client.cursor()
            data = c.execute("SELECT * FROM kpi WHERE kpi_id is ?",(kpi_id,)).fetchone()
            if data is None:
                LOGGER.debug(f"KPI {kpi_id} does not exists")
                return None
            else:
                if flag :
                    value = 1
                else:
                    value = 0
                c.execute("UPDATE kpi SET monitor_flag = ? WHERE kpi_id is ?",(value,kpi_id))
                return True
        except sqlite3.Error as e:
            LOGGER.debug(f"KPI {kpi_id} cannot be checked from the ManagementDB: {e}")