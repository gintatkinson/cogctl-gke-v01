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


import dateutil.parser, math
from datetime import datetime, timezone

def timestamp_datetime_to_float(dt_timestamp : datetime) -> int:
    return math.floor(dt_timestamp.timestamp())

def timestamp_datetime_to_int(dt_timestamp : datetime) -> int:
    return math.floor(timestamp_datetime_to_float(dt_timestamp))

def timestamp_string_to_float(str_timestamp : str) -> float:
    return timestamp_datetime_to_float(dateutil.parser.isoparse(str_timestamp))

def timestamp_float_to_string(flt_timestamp : float) -> str:
    return datetime.utcfromtimestamp(flt_timestamp).isoformat() + 'Z'

def timestamp_utcnow_to_datetime() -> datetime:
    return datetime.now(tz=timezone.utc)

def timestamp_utcnow_to_float() -> float:
    return timestamp_datetime_to_float(timestamp_utcnow_to_datetime())
