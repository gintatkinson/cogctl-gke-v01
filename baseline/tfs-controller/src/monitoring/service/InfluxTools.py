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

from influxdb import InfluxDBClient

class Influx():
  def __init__(self, host, port, username, password, database):
      self.client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

  def write_KPI(self,time,kpi_id,kpi_sample_type,device_id,endpoint_id,service_id,kpi_value):
    data = [{
      "measurement": "samples",
      "time": time,
      "tags": {
          "kpi_id" : kpi_id,
          "kpi_sample_type": kpi_sample_type,
          "device_id"  : device_id,
          "endpoint_id" : endpoint_id,
          "service_id" : service_id
      },
      "fields": {
          "kpi_value": kpi_value
      }
    }]
    self.client.write_points(data)

  def read_KPI_points(self):
      results = self.client.query('select * from samples;')
      print(results.raw)

      points = results.get_points(tags={'kpi_id' : '1','device_id': '1', 'kpi_sample_type': '101'})
      for point in points:
          print("Time: %s, Value: %i" % (point['time'], point['kpi_value']))

      return points

