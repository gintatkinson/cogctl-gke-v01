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

import logging, pandas
from typing import List, Optional

LOGGER = logging.getLogger(__name__)

class InMemoryTimeSeriesDatabase:
    def __init__(self) -> None:
        self._data = pandas.DataFrame(columns=['timestamp', 'kpi_uuid', 'value'])

    def filter(
        self, kpi_uuids : List[str] = [], start_timestamp : Optional[float] = None,
        end_timestamp : Optional[float] = None
    ) -> pandas.DataFrame:
        data = self._data

        if len(kpi_uuids) > 0:
            data = data[data.kpi_uuid.isin(kpi_uuids)]

        if start_timestamp is not None:
            start_datetime = pandas.to_datetime(start_timestamp, unit='s')
            data = data[data.timestamp >= start_datetime]

        if end_timestamp is not None:
            end_datetime = pandas.to_datetime(end_timestamp, unit='s')
            data = data[data.timestamp <= end_datetime]

        return data
