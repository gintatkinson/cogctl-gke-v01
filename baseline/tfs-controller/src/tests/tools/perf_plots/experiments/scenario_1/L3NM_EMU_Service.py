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

# CEST times (UTC+2)
#
# 10:29 - 10:42: l3nm_emulated service setup
#     1000 requests
#     - service L3NM
#     off load: 50 erlang
#     hold time: 10 sec
#     inter arrival time: 0.2 sec
#     workers: 10 threads
#     1 replica per service
#     horizontal pod auto-scalers off

import datetime

EXPERIMENT_NAME = 'L3VPN with Emulated'
EXPERIMENT_ID   = 'scenario_1/emu-l3vpn-service/2023-05May-05'
TIME_START      = datetime.datetime(2023, 5, 5, 8, 29, 0, 0, tzinfo=datetime.timezone.utc)
TIME_END        = datetime.datetime(2023, 5, 5, 8, 42, 0, 0, tzinfo=datetime.timezone.utc)
