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

import json
from typing import Any, Dict
import grpc
import logging

from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from common.proto.context_pb2 import Empty
from common.proto.telemetry_frontend_pb2 import CollectorId, Collector, CollectorFilter, CollectorList
from common.proto.telemetry_frontend_pb2_grpc import TelemetryFrontendServiceServicer

from telemetry.database.TelemetryModel import Collector as CollectorModel
from telemetry.database.Telemetry_DB import TelemetryDB

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import Producer as KafkaProducer


LOGGER            = logging.getLogger(__name__)
METRICS_POOL      = MetricsPool('TelemetryFrontend', 'NBIgRPC')
ACTIVE_COLLECTORS = []       # keep and can be populated from DB


class TelemetryFrontendServiceServicerImpl(TelemetryFrontendServiceServicer):
    def __init__(self):
        LOGGER.info('Init TelemetryFrontendService')
        self.tele_db_obj = TelemetryDB(CollectorModel)
        self.kafka_producer = KafkaProducer({'bootstrap.servers' : KafkaConfig.get_kafka_address()})
        self.kafka_consumer = KafkaConsumer({'bootstrap.servers' : KafkaConfig.get_kafka_address(),
                                            'group.id'           : 'frontend',
                                            'auto.offset.reset'  : 'latest'})

   
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def StartCollector(self, 
                       request : Collector, context: grpc.ServicerContext # type: ignore
                      ) -> CollectorId: # type: ignore
        LOGGER.info ("gRPC message: {:}".format(request))
        response = CollectorId()

        # INFO: If kpi_uuid is already in the DB, it will raise an exception.
        self.tele_db_obj.add_row_to_db(
            CollectorModel.ConvertCollectorToRow(request)
        )
        self.PublishStartRequestOnKafka(request)
        
        response.collector_id.uuid = request.collector_id.collector_id.uuid
        return response

    def PublishStartRequestOnKafka(self, collector_obj):
        """
        Method to generate collector request on Kafka.
        """
        collector_uuid = collector_obj.collector_id.collector_id.uuid
        collector_to_generate :  Dict = {
            "kpi_id"  : collector_obj.kpi_id.kpi_id.uuid,
            "duration": collector_obj.duration_s,
            "interval": collector_obj.interval_s,
            "interface": collector_obj.int_collector.interface,
            "transport_port": collector_obj.int_collector.transport_port,
            "service_id": collector_obj.int_collector.service_id,
            "context_id": collector_obj.int_collector.context_id
        }
        self.kafka_producer.produce(
            KafkaTopic.TELEMETRY_REQUEST.value,
            key      = collector_uuid,
            value    = json.dumps(collector_to_generate),
            callback = self.delivery_callback
        )
        LOGGER.info("Collector Request Generated: Collector Id: {:}, Value: {:}".format(collector_uuid, collector_to_generate))
        ACTIVE_COLLECTORS.append(collector_uuid)
        self.kafka_producer.flush()


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def StopCollector(self, 
                      request : CollectorId, context: grpc.ServicerContext # type: ignore
                     ) -> Empty:  # type: ignore
        LOGGER.info ("gRPC message: {:}".format(request))
        try:
            collector_to_delete = request.collector_id.uuid
            self.tele_db_obj.delete_db_row_by_id(
                CollectorModel, "collector_id", collector_to_delete
            )
            self.PublishStopRequestOnKafka(request)
        except Exception as e:
            LOGGER.error('Unable to delete collector. Error: {:}'.format(e))
        return Empty()

    def PublishStopRequestOnKafka(self, collector_id):
        """
        Method to generate stop collector request on Kafka.
        """
        collector_uuid = collector_id.collector_id.uuid
        collector_to_stop :  Dict = {
            "kpi_id"  : collector_uuid,
            "duration": -1,
            "interval": -1
        }
        self.kafka_producer.produce(
            KafkaTopic.TELEMETRY_REQUEST.value,
            key      = collector_uuid,
            value    = json.dumps(collector_to_stop),
            callback = self.delivery_callback
        )
        LOGGER.info("Collector Stop Request Generated: Collector Id: {:}, Value: {:}".format(collector_uuid, collector_to_stop))
        try:
            ACTIVE_COLLECTORS.remove(collector_uuid)
        except ValueError:
            LOGGER.warning('Collector ID {:} not found in active collector list'.format(collector_uuid))
        self.kafka_producer.flush()


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SelectCollectors(self, 
                         request : CollectorFilter, context: grpc.ServicerContext # type: ignore
                        ) -> CollectorList:  # type: ignore
        LOGGER.info("gRPC message: {:}".format(request))
        response = CollectorList()

        try:
            rows = self.tele_db_obj.select_with_filter(CollectorModel, request)
        except Exception as e:
            LOGGER.info('Unable to apply filter on kpi descriptor. {:}'.format(e))
        try:
            for row in rows:    # TODO: Tackle this warning.
                collector_obj = CollectorModel.ConvertRowToCollector(row)
                response.collector_list.append(collector_obj)
            return response
        except Exception as e:
            LOGGER.info('Unable to process filter response {:}'.format(e))


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def delivery_callback(self, err, msg):
        if err:
            LOGGER.debug('Message delivery failed: {:}'.format(err))

