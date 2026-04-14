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

# Scalability
#     13:02 - 13:19 CEST times (UTC+2)
#     1000 requests
#     L2 svc + L2 slc + L3 svc + L3 slc
#     hold time: 10 sec
#     horizontal pod auto-scalers on
#     max 100 replica per service (context, service, pathcomp, slice)
#     off load [erlang]: see ERLANGS
#     max threads: see TENANTS

import datetime

TENANTS = 80
ERLANGS = 400

EXPERIMENT_NAME = 'Scalability ({:d} Tenants, {:d} Erlangs)'.format(TENANTS, ERLANGS)
EXPERIMENT_ID   = 'scenario_2/scalability/2023-05May-29/scal_{:03d}tnt_{:03d}erl'.format(TENANTS, ERLANGS)

TIME_START      = datetime.datetime(2023, 5, 29, 11,  2, 0, 0, tzinfo=datetime.timezone.utc)
TIME_END        = datetime.datetime(2023, 5, 29, 11, 19, 0, 0, tzinfo=datetime.timezone.utc)
