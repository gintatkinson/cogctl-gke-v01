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

import pandas as pd
from analytics.backend.service.AnalyzerHandlers import Handlers

def get_input_kpi_list():
    return ["1e22f180-ba28-4641-b190-2287bf446666", "6e22f180-ba28-4641-b190-2287bf448888", 'kpi_3']

def get_output_kpi_list():
    return ["1e22f180-ba28-4641-b190-2287bf441616", "6e22f180-ba28-4641-b190-2287bf181818", 'kpi_4']

def get_thresholds():
    return {
        "task_type": Handlers.AGGREGATION_HANDLER.value,
        "task_parameter": [
            {"last":  [40, 80], "variance": [300, 500]},
            {"count": [2,  4],  "max":      [70,  100]},
            {"min":   [10, 20], "avg":      [50,  70]},
        ],
    }

def get_duration():
    return 90

def get_batch_duration():
    return 30

def get_windows_size():
    return None

def get_batch_size():
    return 5

def get_interval():
    return 5

def get_batch():
    return [
        {"time_stamp": "2025-01-13T08:44:10Z", "kpi_id": "6e22f180-ba28-4641-b190-2287bf448888", "kpi_value": 46.72},
        {"time_stamp": "2025-01-13T08:44:12Z", "kpi_id": "6e22f180-ba28-4641-b190-2287bf448888", "kpi_value": 65.22},
        {"time_stamp": "2025-01-13T08:44:14Z", "kpi_id": "1e22f180-ba28-4641-b190-2287bf446666", "kpi_value": 54.24},
        {"time_stamp": "2025-01-13T08:44:16Z", "kpi_id": "1e22f180-ba28-4641-b190-2287bf446666", "kpi_value": 57.67},
        {"time_stamp": "2025-01-13T08:44:18Z", "kpi_id": "1e22f180-ba28-4641-b190-2287bf446666", "kpi_value": 38.6},
        {"time_stamp": "2025-01-13T08:44:20Z", "kpi_id": "6e22f180-ba28-4641-b190-2287bf448888", "kpi_value": 38.9},
        {"time_stamp": "2025-01-13T08:44:22Z", "kpi_id": "6e22f180-ba28-4641-b190-2287bf448888", "kpi_value": 52.44},
        {"time_stamp": "2025-01-13T08:44:24Z", "kpi_id": "6e22f180-ba28-4641-b190-2287bf448888", "kpi_value": 47.76},
        {"time_stamp": "2025-01-13T08:44:26Z", "kpi_id": "efef4d95-1cf1-43c4-9742-95c283ddd7a6", "kpi_value": 33.71},
        {"time_stamp": "2025-01-13T08:44:28Z", "kpi_id": "efef4d95-1cf1-43c4-9742-95c283ddd7a6", "kpi_value": 64.44},
    ]

def get_agg_df():
    data = [ 
        {"kpi_id": "1e22f180-ba28-4641-b190-2287bf441616", "last": 47.76, "variance": 970.41},
    ]
    return pd.DataFrame(data)
