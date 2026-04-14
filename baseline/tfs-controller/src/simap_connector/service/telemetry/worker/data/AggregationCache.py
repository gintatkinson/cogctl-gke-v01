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


import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Set, Tuple


@dataclass
class LinkSample:
    network_id            : str
    link_id               : str
    bandwidth_utilization : float
    latency               : float
    related_service_ids   : Set[str] = field(default_factory=set)


@dataclass
class AggregatedLinkSample:
    timestamp             : datetime
    bandwidth_utilization : float     = field(default=0.0)
    latency               : float     = field(default=0.0)
    related_service_ids   : Set[str] = field(default_factory=set)


class AggregationCache:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._samples : Dict[Tuple[str, str], LinkSample] = dict()


    def update(self, link_sample : LinkSample) -> None:
        link_key = (link_sample.network_id, link_sample.link_id)
        with self._lock:
            self._samples[link_key] = link_sample


    def aggregate(self) -> AggregatedLinkSample:
        with self._lock:
            agg = AggregatedLinkSample(timestamp=datetime.utcnow())
            for sample in self._samples.values():
                agg.bandwidth_utilization = max(
                    agg.bandwidth_utilization, sample.bandwidth_utilization
                )
                agg.latency = agg.latency + sample.latency
                agg.related_service_ids = agg.related_service_ids.union(
                    sample.related_service_ids
                )
            return agg
