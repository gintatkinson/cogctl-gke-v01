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
import time
import logging
import threading

from .HelperMethods   import get_collector_by_kpi_id, get_subscription_parameters
from common.Constants import ServiceNameEnum
from common.Settings  import get_service_port_grpc
from confluent_kafka  import Consumer as KafkaConsumer
from confluent_kafka  import KafkaError
from confluent_kafka  import Producer as KafkaProducer
from datetime         import datetime, timezone
from typing           import Any, Dict

from .collector_api._Collector               import _Collector
from .collector_api.DriverInstanceCache      import DriverInstanceCache, get_driver
from .collectors.emulated.EmulatedCollector  import EmulatedCollector
from common.method_wrappers.Decorator        import MetricsPool
from common.proto.kpi_manager_pb2            import KpiId
from common.tools.context_queries.Device     import get_device
from common.tools.kafka.Variables            import KafkaConfig, KafkaTopic
from common.tools.service.GenericGrpcService import GenericGrpcService
from context.client.ContextClient            import ContextClient
from kpi_manager.client.KpiManagerClient     import KpiManagerClient


LOGGER = logging.getLogger(__name__)
METRICS_POOL = MetricsPool('TelemetryBackend', 'backendService')

class TelemetryBackendService(GenericGrpcService):
    """
    Class listens for request on Kafka topic, fetches requested metrics from device.
    Produces metrics on both TELEMETRY_RESPONSE and VALUE kafka topics.
    """
    def __init__(self, driver_instance_cache : DriverInstanceCache, cls_name : str = __name__) -> None:
        LOGGER.info('Init TelemetryBackendService')
        port = get_service_port_grpc(ServiceNameEnum.TELEMETRYBACKEND)
        super().__init__(port, cls_name=cls_name)
        self.kafka_producer = KafkaProducer({'bootstrap.servers' : KafkaConfig.get_kafka_address()})
        self.kafka_consumer = KafkaConsumer({'bootstrap.servers' : KafkaConfig.get_kafka_address(),
                                            'group.id'           : 'backend',
                                            'auto.offset.reset'  : 'latest'})
        self.driver_instance_cache = driver_instance_cache
        self.device_collector      = None
        self.collector             = None           # This should be replaced with device_collector (later to be removed)
        self.context_client        = ContextClient()
        self.kpi_manager_client    = KpiManagerClient()
        self.active_jobs = {}

    def install_servicers(self):
        threading.Thread(target=self.RequestListener).start()

    def RequestListener(self):
        """
        listener for requests on Kafka topic.
        """
        LOGGER.info('Telemetry backend request listener is running ...')
        # print      ('Telemetry backend request listener is running ...')
        consumer = self.kafka_consumer
        consumer.subscribe([KafkaTopic.TELEMETRY_REQUEST.value])
        while True:
            receive_msg = consumer.poll(1.0)
            if receive_msg is None:
                continue
            elif receive_msg.error():
                if receive_msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                elif receive_msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    LOGGER.warning(
                        f"Subscribed topic {receive_msg.topic()} does not exist or topic does not have any messages.")
                    continue
                else:
                    LOGGER.error("Consumer error: {}".format(receive_msg.error()))
                    break
            try: 
                collector = json.loads(receive_msg.value().decode('utf-8'))
                collector_id = receive_msg.key().decode('utf-8')
                LOGGER.debug('Recevied Collector: {:} - {:}'.format(collector_id, collector))

                duration = collector.get('duration', 0)
                if duration == -1 and collector['interval'] == -1:
                    self.TerminateCollector(collector_id)
                else:
                    LOGGER.info("Received Collector ID: {:} - Scheduling...".format(collector_id))
                    if collector_id not in self.active_jobs:
                        stop_event = threading.Event()
                        self.active_jobs[collector_id] = stop_event
                        threading.Thread(target=self.GenericCollectorHandler,
                                         args=(
                                             collector_id,
                                             collector['kpi_id'],
                                             duration,
                                             collector['interval'],
                                             collector['interface'],      # for INT collector
                                             collector['transport_port'], # for INT collector
                                             collector['service_id'],     # for INT collector
                                             collector['context_id'],     # for INT collector
                                             stop_event
                                         )).start()
                        # Stop the Collector after the given duration
                        if duration > 0:
                            def stop_after_duration(completion_time, stop_event):
                                time.sleep(completion_time)
                                if not stop_event.is_set():
                                    LOGGER.warning(
                                        f"Execution duration ({completion_time}) completed of Collector: {collector_id}")
                                    self.TerminateCollector(collector_id)

                            duration_thread = threading.Thread(
                                target=stop_after_duration, daemon=True, name=f"stop_after_duration_{collector_id}",
                                args=(duration, stop_event)
                            )
                            duration_thread.start()
                    else:
                        LOGGER.warning("Collector ID: {:} - Already scheduled or running".format(collector_id))
            except Exception as e:
                LOGGER.warning(
                    "Unable to consume message from topic: {:}. ERROR: {:}".format(KafkaTopic.TELEMETRY_REQUEST.value, e))

    def GenericCollectorHandler(self, collector_id, kpi_id, duration, interval, interface , port , service_id , context_id , stop_event ):
        """
        Method to handle collector request.
        """
        # CONFIRM: The method (get_collector_by_kpi_id) is working correctly. testcase in integration tests.
        self.device_collector = get_collector_by_kpi_id(
            kpi_id, self.kpi_manager_client, self.context_client, self.driver_instance_cache)

        if not self.device_collector:
            LOGGER.warning(f"KPI ID: {kpi_id} - Collector not found. Skipping...")
            raise Exception(f"KPI ID: {kpi_id} - Collector not found.")
        LOGGER.info(("----- Number done -----"))

        # CONFIRM: The method (get_subscription_parameters) is working correctly. testcase in telemetery backend tests.
        resource_to_subscribe = get_subscription_parameters(
            kpi_id, self.kpi_manager_client, self.context_client, duration, interval
        )
        if not resource_to_subscribe:
            LOGGER.warning(f"KPI ID: {kpi_id} - Resource to subscribe not found. Skipping...")
            raise Exception(f"KPI ID: {kpi_id} - Resource to subscribe not found.")
        LOGGER.info("------ Number done 2 -----")

        responses = self.device_collector.SubscribeState(resource_to_subscribe)

        for status in responses:
            if isinstance(status, Exception):
                LOGGER.error(f"Subscription failed for KPI ID: {kpi_id} - Error: {status}")
                raise status
            else:
                LOGGER.info(f"Subscription successful for KPI ID: {kpi_id} - Status: {status}")
        LOGGER.info("------ Number done 3 -----")

        for samples in self.device_collector.GetState(duration=duration, blocking=True):
            LOGGER.info(f"KPI ID: {kpi_id} - Samples: {samples}")
            self.GenerateKpiValue(collector_id, kpi_id, samples)

        LOGGER.info("------ Number done 4 -----")
        self.device_collector.Disconnect()
        # TODO: Stop_event should be managed here is this method because there will be no more specific collector.

# --- START: Kept for INT compatibility, to be removed later ---
    def INTCollectorHandler(self, subscription, duration, collector_id, kpi_id, interface, port, service_id, context_id , stop_event):
        self.collector = INTCollector(
            collector_id=collector_id ,
            address="127.0.0.1",
            interface=interface,
            port=port,
            kpi_id=kpi_id,
            service_id=service_id,
            context_id=context_id
        )
        self.collector.Connect()
        if stop_event.is_set():
            self.collector.Disconnect()
# --- END: Kept for INT compatibility, to be removed later ---

    def GenerateKpiValue(self, collector_id: str, kpi_id: str, measured_kpi_value: Any):
        """
        Method to write kpi value on VALUE Kafka topic
        """
        producer = self.kafka_producer
        kpi_value: Dict = {
            "time_stamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "kpi_id": kpi_id,
            "kpi_value": measured_kpi_value
        }
        producer.produce(
            KafkaTopic.VALUE.value,
            key=collector_id,
            value=json.dumps(kpi_value),
            callback=self.delivery_callback
        )
        producer.flush()

    def delivery_callback(self, err, msg):
        if err: 
            LOGGER.error('Message delivery failed: {:s}'.format(str(err)))

    def TerminateCollector(self, job_id):
        LOGGER.debug("Terminating collector backend...")
        try:
            if job_id not in self.active_jobs:
                self.logger.warning(f"No active jobs found for {job_id}. It might have already terminated.")
            else:
                LOGGER.info(f"Terminating job: {job_id}")
                stop_event = self.active_jobs.pop(job_id, None)
                if stop_event:
                    stop_event.set()
                    LOGGER.info(f"Job {job_id} terminated.")
                    if self.collector.UnsubscribeState(job_id):
                        LOGGER.info(f"Unsubscribed from collector: {job_id}")
                    else:
                        LOGGER.warning(f"Failed to unsubscribe from collector: {job_id}")
                else:
                    LOGGER.warning(f"Job {job_id} not found in active jobs.")
        except:
            LOGGER.exception("Error terminating job: {:}".format(job_id))

