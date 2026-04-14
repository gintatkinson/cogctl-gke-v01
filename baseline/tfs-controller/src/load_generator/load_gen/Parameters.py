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

from typing import List, Optional
from load_generator.load_gen.Constants import (
    DEFAULT_AVAILABILITY_RANGES, DEFAULT_CAPACITY_GBPS_RANGES, DEFAULT_E2E_LATENCY_MS_RANGES, DEFAULT_MAX_WORKERS)
from load_generator.tools.ListScalarRange import Type_ListScalarRange


class Parameters:
    def __init__(
        self,
        num_requests : int,
        request_types : List[str],
        device_regex : Optional[str] = None,
        endpoint_regex : Optional[str] = None,
        offered_load : Optional[float] = None,
        inter_arrival_time : Optional[float] = None,
        holding_time : Optional[float] = None,
        availability_ranges : Type_ListScalarRange = DEFAULT_AVAILABILITY_RANGES,
        capacity_gbps_ranges : Type_ListScalarRange = DEFAULT_CAPACITY_GBPS_RANGES,
        e2e_latency_ms_ranges : Type_ListScalarRange = DEFAULT_E2E_LATENCY_MS_RANGES,
        max_workers : int = DEFAULT_MAX_WORKERS,
        do_teardown : bool = True,
        dry_mode : bool = False,
        record_to_dlt : bool = False,
        dlt_domain_id : Optional[str] = None
    ) -> None:
        self._num_requests = num_requests
        self._request_types = request_types
        self._device_regex = r'.*' if (device_regex is None or len(device_regex) == 0) else device_regex
        self._endpoint_regex = r'.*' if (endpoint_regex is None or len(endpoint_regex) == 0) else endpoint_regex
        self._offered_load = offered_load
        self._inter_arrival_time = inter_arrival_time
        self._holding_time = holding_time
        self._availability_ranges = availability_ranges
        self._capacity_gbps_ranges = capacity_gbps_ranges
        self._e2e_latency_ms_ranges = e2e_latency_ms_ranges
        self._max_workers = max_workers
        self._do_teardown = do_teardown
        self._dry_mode = dry_mode
        self._record_to_dlt = record_to_dlt
        self._dlt_domain_id = dlt_domain_id

        if self._offered_load is None and self._holding_time is not None and self._inter_arrival_time is not None:
            self._offered_load = self._holding_time / self._inter_arrival_time
        elif self._offered_load is not None and self._holding_time is not None and self._inter_arrival_time is None:
            self._inter_arrival_time = self._holding_time / self._offered_load
        elif self._offered_load is not None and self._holding_time is None and self._inter_arrival_time is not None:
            self._holding_time = self._offered_load * self._inter_arrival_time
        else:
            MSG = 'Exactly two of offered_load({:s}), inter_arrival_time({:s}), holding_time({:s}) must be specified.'
            raise Exception(MSG.format(str(self._offered_load), str(self._inter_arrival_time), str(self._holding_time)))

        if self._record_to_dlt and self._dlt_domain_id is None:
            MSG = 'Parameter dlt_domain_id({:s}) must be specified with record_to_dlt({:s}).'
            raise Exception(MSG.format(str(self._dlt_domain_id), str(self._record_to_dlt)))

    @property
    def num_requests(self): return self._num_requests

    @property
    def request_types(self): return self._request_types

    @property
    def device_regex(self): return self._device_regex

    @property
    def endpoint_regex(self): return self._endpoint_regex

    @property
    def offered_load(self): return self._offered_load

    @property
    def inter_arrival_time(self): return self._inter_arrival_time

    @property
    def holding_time(self): return self._holding_time

    @property
    def availability_ranges(self): return self._availability_ranges

    @property
    def capacity_gbps_ranges(self): return self._capacity_gbps_ranges

    @property
    def e2e_latency_ms_ranges(self): return self._e2e_latency_ms_ranges

    @property
    def max_workers(self): return self._max_workers

    @property
    def do_teardown(self): return self._do_teardown

    @property
    def dry_mode(self): return self._dry_mode

    @property
    def record_to_dlt(self): return self._record_to_dlt

    @property
    def dlt_domain_id(self): return self._dlt_domain_id
