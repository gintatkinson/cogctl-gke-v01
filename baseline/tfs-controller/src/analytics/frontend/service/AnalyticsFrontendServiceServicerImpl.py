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

import logging, grpc, json, queue

from typing          import Dict
from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import Producer as KafkaProducer
from confluent_kafka import KafkaError

from common.tools.kafka.Variables             import KafkaConfig, KafkaTopic
from common.proto.context_pb2                 import Empty
from common.method_wrappers.Decorator         import MetricsPool, safe_and_metered_rpc_method
from common.proto.analytics_frontend_pb2      import Analyzer, AnalyzerId, AnalyzerFilter, AnalyzerList
from common.proto.analytics_frontend_pb2_grpc import AnalyticsFrontendServiceServicer
from analytics.database.Analyzer_DB           import AnalyzerDB
from analytics.database.AnalyzerModel         import Analyzer as AnalyzerModel
from apscheduler.schedulers.background        import BackgroundScheduler
from apscheduler.triggers.interval            import IntervalTrigger

LOGGER           = logging.getLogger(__name__)
METRICS_POOL     = MetricsPool('AnalyticsFrontend', 'NBIgRPC')

class AnalyticsFrontendServiceServicerImpl(AnalyticsFrontendServiceServicer):
    def __init__(self):
        LOGGER.info('Init AnalyticsFrontendService')
        self.listener_topic = KafkaTopic.ANALYTICS_RESPONSE.value
        self.db_obj         = AnalyzerDB(AnalyzerModel)
        self.result_queue   = queue.Queue()
        self.scheduler      = BackgroundScheduler()
        self.kafka_producer = KafkaProducer({'bootstrap.servers' : KafkaConfig.get_kafka_address()})
        self.kafka_consumer = KafkaConsumer({'bootstrap.servers' : KafkaConfig.get_kafka_address(),
                                            'group.id'           : 'analytics-frontend',
                                            'auto.offset.reset'  : 'latest'})

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def StartAnalyzer(self, 
                       request : Analyzer, context: grpc.ServicerContext # type: ignore
                      ) -> AnalyzerId: # type: ignore
        LOGGER.info ("At Service gRPC message: {:}".format(request))
        response = AnalyzerId()

        self.db_obj.add_row_to_db(
            AnalyzerModel.ConvertAnalyzerToRow(request)
        )
        self.PublishStartRequestOnKafka(request)
        
        response.analyzer_id.uuid = request.analyzer_id.analyzer_id.uuid
        return response

    def PublishStartRequestOnKafka(self, analyzer_obj):
        """
        Method to generate analyzer request on Kafka.
        """
        analyzer_uuid = analyzer_obj.analyzer_id.analyzer_id.uuid
        analyzer_to_generate : Dict = {
            "algo_name"           : analyzer_obj.algorithm_name,
            "input_kpis"          : [k.kpi_id.uuid for k in analyzer_obj.input_kpi_ids],
            "output_kpis"         : [k.kpi_id.uuid for k in analyzer_obj.output_kpi_ids],
            "oper_mode"           : analyzer_obj.operation_mode,
            "duration"            : analyzer_obj.duration_s,
            "thresholds"          : json.loads(analyzer_obj.parameters["thresholds"]),
            "window_size"         : analyzer_obj.parameters["window_size"],     # slider window size in seconds (single batch execution time)
            "window_slider"       : analyzer_obj.parameters["window_slider"],   # slider shift in seconds
            "batch_size_min"      : analyzer_obj.batch_min_size,                # currently implemented
            "batch_size_max"      : analyzer_obj.batch_max_size,
            "batch_duration_min"  : analyzer_obj.batch_min_duration_s,          # currently implemented
            "batch_interval_max"  : analyzer_obj.batch_max_duration_s
        }
        self.kafka_producer.produce(
            KafkaTopic.ANALYTICS_REQUEST.value,
            key      = analyzer_uuid,
            value    = json.dumps(analyzer_to_generate),
            callback = self.delivery_callback
        )
        LOGGER.info("Analyzer Start Request Generated: Analyzer Id: {:}, Value: {:}".format(analyzer_uuid, analyzer_to_generate))
        self.kafka_producer.flush()
        

    def StartResponseListener(self, filter_key=None):
        """
        Start the Kafka response listener with APScheduler and return key-value pairs periodically.
        """
        LOGGER.info("Starting StartResponseListener")
        # Schedule the ResponseListener at fixed intervals
        self.scheduler.add_job(
            self.response_listener,
            trigger=IntervalTrigger(seconds=5),
            args=[filter_key], 
            id=f"response_listener_{self.listener_topic}",
            replace_existing=True
        )
        self.scheduler.start()
        LOGGER.info(f"Started Kafka listener for topic {self.listener_topic}...")
        try:
            while True:
                key, value = self.result_queue.get()
                yield key, value
        except KeyboardInterrupt:
            LOGGER.warning("Listener stopped manually.")
        finally:
            self.StopListener()

    def response_listener(self, filter_key=None):
        """
        Poll Kafka messages and put key-value pairs into the queue.
        """
        LOGGER.info(f"Polling Kafka topic {self.listener_topic}...")

        consumer = self.kafka_consumer
        consumer.subscribe([self.listener_topic])
        msg = consumer.poll(2.0)
        if msg is None:
            return
        elif msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                LOGGER.error(f"Kafka error: {msg.error()}")
            return

        try:
            key = msg.key().decode('utf-8') if msg.key() else None
            if filter_key is not None and key == filter_key:
                value = json.loads(msg.value().decode('utf-8'))
                LOGGER.info(f"Received key: {key}, value: {value}")
                self.result_queue.put((key, value))
            else:
                LOGGER.info(f"Skipping message with unmatched key: {key}")
        except Exception as e:
            LOGGER.error(f"Error processing Kafka message: {e}")

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def StopAnalyzer(self, 
                      request : AnalyzerId, context: grpc.ServicerContext # type: ignore
                     ) -> Empty:  # type: ignore
        LOGGER.info ("At Service gRPC message: {:}".format(request))
        try:
            analyzer_id_to_delete = request.analyzer_id.uuid
            self.db_obj.delete_db_row_by_id(
                AnalyzerModel, "analyzer_id", analyzer_id_to_delete
            )
            self.PublishStopRequestOnKafka(analyzer_id_to_delete)
        except Exception as e:
            LOGGER.error('Unable to delete analyzer. Error: {:}'.format(e))
        return Empty()

    def PublishStopRequestOnKafka(self, analyzer_uuid):
        """
        Method to generate stop analyzer request on Kafka.
        """
        # analyzer_uuid = analyzer_id.analyzer_id.uuid
        analyzer_to_stop :  Dict = {
            "algo_name"   : None,
            "input_kpis"  : [],
            "output_kpis" : [],
            "oper_mode"   : None
        }
        self.kafka_producer.produce(
            KafkaTopic.ANALYTICS_REQUEST.value,
            key      = analyzer_uuid,
            value    = json.dumps(analyzer_to_stop),
            callback = self.delivery_callback
        )
        LOGGER.info("Analyzer Stop Request Generated: Analyzer Id: {:}".format(analyzer_uuid))
        self.kafka_producer.flush()
        self.StopListener()

    def StopListener(self):
        """
        Gracefully stop the Kafka listener and the scheduler.
        """
        LOGGER.info("Stopping Kafka listener...")
        self.scheduler.shutdown()
        LOGGER.info("Kafka listener stopped.")

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SelectAnalyzers(self, 
                         filter : AnalyzerFilter, context: grpc.ServicerContext # type: ignore
                        ) -> AnalyzerList:  # type: ignore
        LOGGER.info("At Service gRPC message: {:}".format(filter))
        response = AnalyzerList()
        try:
            rows = self.db_obj.select_with_filter(AnalyzerModel, filter)
            try:
                for row in rows:
                    response.analyzer_list.append(
                        AnalyzerModel.ConvertRowToAnalyzer(row)
                    )
                return response
            except Exception as e:
                LOGGER.info('Unable to process filter response {:}'.format(e))
        except Exception as e:
            LOGGER.error('Unable to apply filter on table {:}. ERROR: {:}'.format(AnalyzerModel.__name__, e))
       

    def delivery_callback(self, err, msg):
        if err:
            LOGGER.debug('Message delivery failed: {:}'.format(err))
        else:
            LOGGER.debug('Message delivered to topic {:}'.format(msg.topic()))
