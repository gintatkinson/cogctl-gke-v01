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


import grpc, logging, sqlalchemy
from typing import Optional
from common.proto.context_pb2 import Empty
from common.proto.simap_connector_pb2 import Affectation, Subscription, SubscriptionId
from common.proto.simap_connector_pb2_grpc import SimapConnectorServiceServicer
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from device.client.DeviceClient import DeviceClient
from simap_connector.service.telemetry.worker.SynthesizerWorker import SynthesizerWorker
from simap_connector.service.telemetry.worker._Worker import WorkerTypeEnum
from .database.Subscription import subscription_get, subscription_set, subscription_delete
from .database.SubSubscription import (
    sub_subscription_list, sub_subscription_set, sub_subscription_delete
)
from .telemetry.worker.data.AggregationCache import AggregationCache
from .telemetry.TelemetryPool import TelemetryPool
from .Tools import (
    LinkDetails, create_kafka_topic, delete_kafka_topic, delete_underlay_subscription,
    discover_link_details, establish_underlay_subscription, get_controller_id
)

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('SimapConnector', 'RPC')


class SimapConnectorServiceServicerImpl(SimapConnectorServiceServicer):
    def __init__(
        self, db_engine : sqlalchemy.engine.Engine, restconf_client : RestConfClient,
        telemetry_pool : TelemetryPool
    ) -> None:
        LOGGER.debug('Creating Servicer...')
        self._db_engine = db_engine
        self._restconf_client = restconf_client
        self._telemetry_pool = telemetry_pool
        LOGGER.debug('Servicer Created')


    def _get_metrics(self) -> MetricsPool: return METRICS_POOL


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def EstablishSubscription(
        self, request : Subscription, context : grpc.ServicerContext
    ) -> SubscriptionId:
        datastore    = request.datastore
        xpath_filter = request.xpath_filter
        period       = request.period
        link_details : LinkDetails = discover_link_details(
            self._restconf_client, xpath_filter
        )
        xpath_filter = link_details.link.get_xpath_filter(add_simap_telemetry=True)

        parent_subscription_uuid, parent_subscription_id = subscription_set(
            self._db_engine, datastore, xpath_filter, period
        )

        aggregation_cache = AggregationCache()

        device_client = DeviceClient()
        for supporting_link in link_details.supporting_links:
            controller_id = get_controller_id(supporting_link.network_id)
            sup_link_xpath_filter = supporting_link.get_xpath_filter(add_simap_telemetry=True)

            if controller_id is None:
                collector_name = '{:d}:SIMAP:{:s}:{:s}'.format(
                    parent_subscription_id, str(supporting_link.network_id),
                    str(supporting_link.link_id)
                )
                target_uri = sup_link_xpath_filter
                underlay_subscription_id = 0
            else:
                underlay_sub_id = establish_underlay_subscription(
                    device_client, controller_id, sup_link_xpath_filter, period
                )
                collector_name = '{:d}:{:s}:{:s}'.format(
                    parent_subscription_id, controller_id,
                    str(underlay_sub_id.subscription_id)
                )
                target_uri = underlay_sub_id.subscription_uri
                underlay_subscription_id = underlay_sub_id.subscription_id

            self._telemetry_pool.start_collector(
                collector_name, controller_id, supporting_link.network_id,
                supporting_link.link_id, target_uri, aggregation_cache, period
            )

            sub_request = Subscription()
            sub_request.datastore    = datastore
            sub_request.xpath_filter = sup_link_xpath_filter
            sub_request.period       = period
            sub_subscription_set(
                self._db_engine, parent_subscription_uuid, controller_id, datastore,
                sup_link_xpath_filter, period, underlay_subscription_id, target_uri,
                collector_name
            )

        topic = 'subscription.{:d}'.format(parent_subscription_id)
        create_kafka_topic(topic)

        aggregator_name = str(parent_subscription_id)
        network_id = link_details.link.network_id
        link_id    = link_details.link.link_id
        self._telemetry_pool.start_aggregator(
            aggregator_name, network_id, link_id, parent_subscription_id,
            aggregation_cache, topic, period
        )

        return SubscriptionId(subscription_id=parent_subscription_id)


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteSubscription(
        self, request : SubscriptionId, context : grpc.ServicerContext
    ) -> Empty:
        parent_subscription_id = request.subscription_id
        subscription = subscription_get(self._db_engine, parent_subscription_id)
        if subscription is None: return Empty()

        aggregator_name = str(parent_subscription_id)
        self._telemetry_pool.stop_worker(WorkerTypeEnum.AGGREGATOR, aggregator_name)

        device_client = DeviceClient()
        parent_subscription_uuid = subscription['subscription_uuid']
        sub_subscriptions = sub_subscription_list(self._db_engine, parent_subscription_uuid)
        for sub_subscription in sub_subscriptions:
            sub_subscription_id = sub_subscription['sub_subscription_id']
            controller_id       = sub_subscription['controller_uuid'    ]
            collector_name      = sub_subscription['collector_name'     ]

            self._telemetry_pool.stop_worker(WorkerTypeEnum.COLLECTOR, collector_name)

            if controller_id is not None and len(controller_id) > 0:
                delete_underlay_subscription(device_client, controller_id, sub_subscription_id)

            sub_subscription_delete(self._db_engine, parent_subscription_uuid, sub_subscription_id)

        topic = 'subscription.{:d}'.format(parent_subscription_id)
        delete_kafka_topic(topic)

        subscription_delete(self._db_engine, parent_subscription_id)
        return Empty()


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def AffectSampleSynthesizer(
        self, request : Affectation, context : grpc.ServicerContext
    ) -> Empty:
        network_id       = request.network_id
        link_id          = request.link_id
        bandwidth_factor = request.bandwidth_factor
        latency_factor   = request.latency_factor

        synthesizer_name = '{:s}:{:s}'.format(network_id, link_id)
        synthesizer : Optional[SynthesizerWorker] = self._telemetry_pool.get_worker(
            WorkerTypeEnum.SYNTHESIZER, synthesizer_name
        )
        if synthesizer is None:
            MSG = 'Synthesizer({:s}) not found'
            raise Exception(MSG.format(synthesizer_name))
        synthesizer.change_resources(bandwidth_factor, latency_factor)
        return Empty()
