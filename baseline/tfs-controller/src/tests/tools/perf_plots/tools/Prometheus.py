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

import json, requests, time
from datetime import datetime
from typing import Dict, List, Optional

def get_prometheus_series_names(
    address : str, port : int, metric_match : str, time_start : datetime, time_end : datetime, timeout : int = 10,
    raw_json_filepath : Optional[str] = None
) -> List[str]:
    str_url = 'http://{:s}:{:d}/api/v1/label/__name__/values'.format(address, port)
    params = {
        'match[]': '{{__name__=~"{:s}"}}'.format(metric_match),
        'start': time.mktime(time_start.timetuple()),
        'end'  : time.mktime(time_end.timetuple()),
    }
    response = requests.get(str_url, params=params, timeout=timeout)
    results = response.json()
    if raw_json_filepath is not None:
        with open(raw_json_filepath, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(results, sort_keys=True))
    assert results['status'] == 'success'
    return results['data']

def get_prometheus_range(
    address : str, port : int, metric_name : str, labels : Dict[str, str], time_start : datetime, time_end : datetime,
    time_step : str, timeout : int = 10, raw_json_filepath : Optional[str] = None
) -> List[Dict]:
    str_url = 'http://{:s}:{:d}/api/v1/query_range'.format(address, port)
    str_query = metric_name
    if len(labels) > 0:
        str_labels = ', '.join(['{:s}="{:s}"'.format(name, value) for name,value in labels.items()])
        str_query += '{{{:s}}}'.format(str_labels)
    params = {
        'query': str_query,
        'start': time.mktime(time_start.timetuple()),
        'end'  : time.mktime(time_end.timetuple()),
        'step' : time_step,
    }
    response = requests.get(str_url, params=params, timeout=timeout)
    results = response.json()
    if raw_json_filepath is not None:
        with open(raw_json_filepath, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(results, sort_keys=True))
    assert results['status'] == 'success'
    assert results['data']['resultType'] == 'matrix'
    return results['data']['result']
