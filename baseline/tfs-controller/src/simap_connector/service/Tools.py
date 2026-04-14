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


import logging, re
from dataclasses import dataclass, field
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import BrokerResponseError
from typing import List, Optional
from common.proto.monitoring_pb2 import (
    SSEMonitoringSubscriptionConfig, SSEMonitoringSubscriptionResponse
)
from common.tools.kafka.Variables import KafkaConfig
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from device.client.DeviceClient import DeviceClient


LOGGER = logging.getLogger(__name__)


XPATH_LINK_TEMPLATE = '/ietf-network:networks/network={:s}/ietf-network-topology:link={:s}'
SIMAP_TELEMETRY_SUFFIX = '/simap-telemetry:simap-telemetry'

RE_XPATH_LINK = re.compile(
    r'^/ietf-network:networks/network=([^/]+)/ietf-network-topology:link=([^/]+)/?.*$'
)


@dataclass
class Link:
    network_id : str
    link_id    : str

    def get_xpath_filter(self, add_simap_telemetry : bool = True) -> str:
        xpath_filter = XPATH_LINK_TEMPLATE.format(self.network_id, self.link_id)
        if add_simap_telemetry: xpath_filter += SIMAP_TELEMETRY_SUFFIX
        return xpath_filter


@dataclass
class LinkDetails:
    link             : Link
    supporting_links : List[Link] = field(default_factory=list)


def discover_link_details(restconf_client : RestConfClient, xpath_filter : str) -> LinkDetails:
    link_xpath_match = RE_XPATH_LINK.match(xpath_filter)
    if link_xpath_match is None:
        raise Exception('Unsupported xpath_filter({:s})'.format(str(xpath_filter)))

    network_id, link_id = link_xpath_match.groups()
    link_details = LinkDetails(Link(network_id, link_id))

    xpath_filter = link_details.link.get_xpath_filter(add_simap_telemetry=False)
    xpath_data = restconf_client.get(xpath_filter)
    if not xpath_data:
        raise Exception('Resource({:s}) not found in SIMAP Server'.format(str(xpath_filter)))

    links = xpath_data.get('ietf-network-topology:link', list())
    if len(links) == 0:
        raise Exception('Link({:s}) not found'.format(str(xpath_filter)))
    if len(links) >  1:
        raise Exception('Multiple occurrences for Link({:s})'.format(str(xpath_filter)))
    link = links[0]
    if link['link-id'] != link_id:
        MSG = 'Retieved Link({:s}) does not match xpath_filter({:s})'
        raise Exception(MSG.format(str(link), str(xpath_filter)))
    supporting_links = link.get('supporting-link', list())
    if len(supporting_links) == 0:
        MSG = 'No supporting links found for Resource({:s}, {:s})'
        raise Exception(MSG.format(str(xpath_filter), str(xpath_data)))

    for sup_link in supporting_links:
        link_details.supporting_links.append(Link(
            sup_link['network-ref'], sup_link['link-ref']
        ))
    return link_details


#def compose_establish_subscription(datastore : str, xpath_filter : str, period : float) -> Dict:
#    return {
#        'ietf-subscribed-notifications:input': {
#            'datastore': datastore,
#            'ietf-yang-push:datastore-xpath-filter': xpath_filter,
#            'ietf-yang-push:periodic': {
#                'ietf-yang-push:period': period,
#            }
#        }
#    }


CONTROLLER_MAP = {
    'e2e'      : 'TFS-E2E',
    'agg'      : 'TFS-AGG',
    'trans-pkt': 'TFS-IP',
    'trans-opt': 'NCE-T',
    'access'   : 'NCE-FAN',
    'admin'    : None,          # controller-less
}

def get_controller_id(network_id : str) -> Optional[str]:
    # TODO: Future improvement: infer controller based on topology data
    if network_id not in CONTROLLER_MAP:
        MSG = 'Unable to identify controller for SimapNetwork({:s})'
        raise Exception(MSG.format(str(network_id)))
    return CONTROLLER_MAP[network_id]


@dataclass
class UnderlaySubscriptionId:
    subscription_id  : int
    subscription_uri : str

    @classmethod
    def from_reply(cls, sse_sub_rep : SSEMonitoringSubscriptionResponse) -> 'UnderlaySubscriptionId':
        return cls(
            subscription_id  = sse_sub_rep.identifier,
            subscription_uri = sse_sub_rep.uri,
        )

def establish_underlay_subscription(
    device_client : DeviceClient, controller_uuid : str, xpath_filter : str,
    sampling_interval : float
) -> UnderlaySubscriptionId:
    sse_sub_req = SSEMonitoringSubscriptionConfig()
    sse_sub_req.device_id.device_uuid.uuid = controller_uuid
    sse_sub_req.config_type = SSEMonitoringSubscriptionConfig.Subscribe
    sse_sub_req.uri = xpath_filter
    sse_sub_req.sampling_interval = str(sampling_interval)
    sse_sub_rep = device_client.SSETelemetrySubscribe(sse_sub_req)
    return UnderlaySubscriptionId.from_reply(sse_sub_rep)

def delete_underlay_subscription(
    device_client : DeviceClient, controller_uuid : str, subscription_id : int
) -> None:
    sse_unsub_req = SSEMonitoringSubscriptionConfig()
    sse_unsub_req.device_id.device_uuid.uuid = controller_uuid
    sse_unsub_req.config_type = SSEMonitoringSubscriptionConfig.Unsubscribe
    sse_unsub_req.identifier = str(subscription_id)
    device_client.SSETelemetrySubscribe(sse_unsub_req)


KAFKA_BOOT_SERVERS = KafkaConfig.get_kafka_address()

def create_kafka_topic(topic : str) -> None:
    try:
        kafka_admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOT_SERVERS)
        existing_topics = set(kafka_admin.list_topics())
        if topic in existing_topics: return
        to_create = [NewTopic(topic, num_partitions=3, replication_factor=1)]
        kafka_admin.create_topics(to_create, validate_only=False)
    except BrokerResponseError:
        MSG = 'Error creating Topic({:s})'
        LOGGER.exception(MSG.format(str(topic)))

def delete_kafka_topic(topic : str) -> None:
    try:
        kafka_admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOT_SERVERS)
        existing_topics = set(kafka_admin.list_topics())
        if topic not in existing_topics: return
        kafka_admin.delete_topics([topic])
    except BrokerResponseError:
        MSG = 'Error deleting Topic({:s})'
        LOGGER.exception(MSG.format(str(topic)))
