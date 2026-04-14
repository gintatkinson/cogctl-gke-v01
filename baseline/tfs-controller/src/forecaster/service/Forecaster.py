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

import math, pandas
from datetime import datetime, timezone
from statistics import mean
from sklearn.ensemble import RandomForestRegressor
from common.proto.monitoring_pb2 import KpiId
from forecaster.Config import FORECAST_TO_HISTORY_RATIO

def compute_forecast(samples : pandas.DataFrame, kpi_id : KpiId) -> float:
    kpi_uuid = kpi_id.kpi_id.uuid
    samples = samples[samples.kpi_id == kpi_uuid].copy()

    num_samples = samples.shape[0]
    if num_samples <= 0:
        MSG = 'KpiId({:s}): Wrong number of samples: {:d}'
        raise Exception(MSG.format(kpi_uuid, num_samples))

    num_samples_test = math.ceil(num_samples / FORECAST_TO_HISTORY_RATIO)
    if num_samples_test  <= 0:
        MSG = 'KpiId({:s}): Wrong number of test samples: {:d}'
        raise Exception(MSG.format(kpi_uuid, num_samples_test ))

    num_samples_train = num_samples - num_samples_test
    if num_samples_train <= 0:
        MSG = 'KpiId({:s}): Wrong number of train samples: {:d}'
        raise Exception(MSG.format(kpi_uuid, num_samples_train))

    samples['timestamp'] = pandas.to_datetime(samples['timestamp']) - datetime(1970, 1, 1, tzinfo=timezone.utc)
    samples['timestamp'] = samples['timestamp'].dt.total_seconds()

    train_set = samples[0:num_samples_train]
    test_set  = samples[num_samples_train:num_samples]

    rfr = RandomForestRegressor(n_estimators=600, random_state=42)
    rfr.fit(train_set.drop(['kpi_id', 'value'], axis=1), train_set['value'])
    forecast = rfr.predict(test_set.drop(['kpi_id', 'value'], axis=1))
    avg_forecast = round(mean(forecast), 2)
    return avg_forecast
