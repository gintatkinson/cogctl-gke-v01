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

import time
import json
import logging
import threading

from common.tools.service.GenericGrpcService import GenericGrpcService
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from confluent_kafka import Consumer
from confluent_kafka import KafkaError, KafkaException
from common.Constants import ServiceNameEnum
from common.Settings import get_service_port_grpc
from analytics.backend.service.Streamer import DaskStreamer
from analytics.backend.service.AnalyzerHelper import AnalyzerHelper


LOGGER = logging.getLogger(__name__)

class AnalyticsBackendService(GenericGrpcService):
    """
    AnalyticsBackendService class is responsible for handling the requests from the AnalyticsFrontendService.
    It listens to the Kafka topic for the requests to start and stop the Streamer accordingly.
    It also initializes the Kafka producer and Dask cluster for the streamer.
    """
    def __init__(self, cls_name : str = __name__, n_workers=1, threads_per_worker=1
                 ) -> None:
        LOGGER.info('Init AnalyticsBackendService')
        port = get_service_port_grpc(ServiceNameEnum.ANALYTICSBACKEND)
        super().__init__(port, cls_name=cls_name)
        self.active_streamers = {}
        self.central_producer = AnalyzerHelper.initialize_kafka_producer()  # Multi-threaded producer
        self.cluster          = AnalyzerHelper.initialize_dask_cluster(
                                        n_workers, threads_per_worker) # Local cluster
        self.request_consumer = Consumer({
            'bootstrap.servers' : KafkaConfig.get_kafka_address(),
            'group.id'          : 'analytics-backend',
            'auto.offset.reset' : 'latest',
            })


    def install_servicers(self):
        threading.Thread(
            target=self.RequestListener,
            args=()
        ).start()

    def RequestListener(self):
        """
        listener for requests on Kafka topic.
        """
        LOGGER.info("Request Listener is initiated ...")
        consumer = self.request_consumer
        consumer.subscribe([KafkaTopic.ANALYTICS_REQUEST.value])
        while True:
            message = consumer.poll(2.0)
            if message is None:
                continue
            elif message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        LOGGER.warning(f"Consumer reached end of topic {message.topic()}/{message.partition()}")
                        break
                    elif message.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                        LOGGER.error(f"Subscribed topic {message.topic()} does not exist. May be topic does not have any messages.")
                        continue
                    elif message.error():
                        raise KafkaException(message.error())
            try:
                analyzer      = json.loads(message.value().decode('utf-8'))
                analyzer_uuid = message.key().decode('utf-8')
                LOGGER.info('Recevied Analyzer: {:} - {:}'.format(analyzer_uuid, analyzer))

                if analyzer["algo_name"] is None and analyzer["oper_mode"] is None:
                    if self.StopStreamer(analyzer_uuid):
                        LOGGER.info("Dask Streamer stopped.")
                    else:
                        LOGGER.warning("Failed to stop Dask Streamer. May be already terminated...")
                else:
                    if self.StartStreamer(analyzer_uuid, analyzer):
                        LOGGER.info("Dask Streamer started.")
                    else:
                        LOGGER.warning("Failed to start Dask Streamer.")
            except Exception as e:
                LOGGER.warning("Unable to consume message from topic: {:}. ERROR: {:}".format(KafkaTopic.ANALYTICS_REQUEST.value, e))


    def StartStreamer(self, analyzer_uuid : str, analyzer : dict):
        """
        Start the DaskStreamer with the given parameters.
        """
        if analyzer_uuid in self.active_streamers:
            LOGGER.warning("Dask Streamer already running with the given analyzer_uuid: {:}".format(analyzer_uuid))
            return False
        try:
            streamer = DaskStreamer(
                key               = analyzer_uuid,
                input_kpis        = analyzer['input_kpis'        ],
                output_kpis       = analyzer['output_kpis'       ],
                thresholds        = analyzer['thresholds'        ],
                batch_size        = analyzer['batch_size_min'    ],
                batch_duration    = analyzer['batch_duration_min'],
                window_size       = analyzer['window_size'       ],
                cluster_instance  = self.cluster,
                producer_instance = self.central_producer,
            )
            streamer.start()
            LOGGER.info(f"Streamer started with analyzer Id: {analyzer_uuid}")

            # Stop the streamer after the given duration
            duration = analyzer['duration']
            if duration > 0:
                def stop_after_duration():
                    time.sleep(duration)
                    LOGGER.warning(f"Execution duration ({duration}) completed of Analyzer: {analyzer_uuid}")
                    if not self.StopStreamer(analyzer_uuid):
                        LOGGER.warning("Failed to stop Dask Streamer. Streamer may be already terminated.")

                duration_thread = threading.Thread(
                    target=stop_after_duration, daemon=True, name=f"stop_after_duration_{analyzer_uuid}"
                    )
                duration_thread.start()

            self.active_streamers[analyzer_uuid] = streamer
            return True
        except Exception as e:
            LOGGER.error("Failed to start Dask Streamer. ERROR: {:}".format(e))
            return False

    def StopStreamer(self, analyzer_uuid : str):
        """
        Stop the DaskStreamer with the given analyzer_uuid.
        """
        try:
            if analyzer_uuid not in self.active_streamers:
                LOGGER.warning("Dask Streamer not found with the given analyzer_uuid: {:}".format(analyzer_uuid))
                return True
            LOGGER.info(f"Terminating streamer with Analyzer Id: {analyzer_uuid}")
            streamer = self.active_streamers[analyzer_uuid]
            streamer.stop()
            streamer.join()
            del self.active_streamers[analyzer_uuid]
            LOGGER.info(f"Streamer with analyzer_uuid '{analyzer_uuid}' has been trerminated sucessfully.")
            return True
        except:
            LOGGER.exception("Failed to stop Dask Streamer.")
            return False

    def close(self):
        """
        Close the producer and cluster cleanly.
        """
        if self.central_producer:
            try:
                self.central_producer.flush()
                LOGGER.info("Kafka producer flushed and closed.")
            except:
                LOGGER.exception("Error closing Kafka producer")
        if self.cluster:
            try:
                self.cluster.close()
                LOGGER.info("Dask cluster closed.")
            except:
                LOGGER.exception("Error closing Dask cluster")

    def stop(self):
        self.close()
        return super().stop()
