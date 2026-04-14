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


from dataclasses import dataclass, field
from typing import List
from simap_connector.service.simap_updater.SimapClient import SimapClient
from .SyntheticSamplers import SyntheticSampler


@dataclass
class ResourceNode:
    domain_name             : str
    node_name               : str
    cpu_utilization_sampler : SyntheticSampler
    related_service_ids     : List[str] = field(default_factory=list)

    def generate_samples(self, simap_client : SimapClient) -> None:
        cpu_utilization = self.cpu_utilization_sampler.get_sample()
        simap_node = simap_client.network(self.domain_name).node(self.node_name)
        simap_node.telemetry.update(
            cpu_utilization.value, related_service_ids=self.related_service_ids
        )


@dataclass
class ResourceLink:
    domain_name                   : str
    link_name                     : str
    bandwidth_utilization_sampler : SyntheticSampler
    latency_sampler               : SyntheticSampler
    related_service_ids           : List[str] = field(default_factory=list)

    def generate_samples(self, simap_client : SimapClient) -> None:
        bandwidth_utilization = self.bandwidth_utilization_sampler.get_sample()
        latency               = self.latency_sampler.get_sample()
        simap_link = simap_client.network(self.domain_name).link(self.link_name)
        simap_link.telemetry.update(
            bandwidth_utilization.value, latency.value,
            related_service_ids=self.related_service_ids
        )


@dataclass
class Resources:
    nodes : List[ResourceNode] = field(default_factory=list)
    links : List[ResourceLink] = field(default_factory=list)

    def generate_samples(self, simap_client : SimapClient) -> None:
        for resource in self.nodes:
            resource.generate_samples(simap_client)

        for resource in self.links:
            resource.generate_samples(simap_client)
