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

from datetime import datetime
import logging, grpc, json, queue
from typing import Dict
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from confluent_kafka import KafkaError

from common.proto.context_pb2 import Empty
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.kpi_manager_pb2 import KpiDescriptor, KpiId
from common.proto.kpi_value_api_pb2_grpc import KpiValueAPIServiceServicer
from common.proto.kpi_value_api_pb2 import KpiAlarms, KpiValueList, KpiValueFilter, KpiValue, KpiValueType
from apscheduler.schedulers.background        import BackgroundScheduler
from apscheduler.triggers.interval            import IntervalTrigger
from confluent_kafka import Producer as KafkaProducer
from confluent_kafka import Consumer as KafkaConsumer

from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime

from kpi_manager.client.KpiManagerClient import KpiManagerClient

LOGGER       = logging.getLogger(__name__)
METRICS_POOL = MetricsPool('KpiValueAPI', 'NBIgRPC')
PROM_URL     = "http://prometheus-k8s.monitoring.svc.cluster.local:9090"    # TODO: updated with the env variables

class KpiValueApiServiceServicerImpl(KpiValueAPIServiceServicer):
    def __init__(self):
        LOGGER.debug('Init KpiValueApiService')
        self.listener_topic = KafkaTopic.ALARMS.value
        self.result_queue   = queue.Queue()
        self.scheduler      = BackgroundScheduler()
        self.kafka_producer = KafkaProducer({'bootstrap.servers' : KafkaConfig.get_kafka_address()})
        self.kafka_consumer = KafkaConsumer({'bootstrap.servers' : KafkaConfig.get_kafka_address(),
                                            'group.id'           : 'kpi-value-api-frontend',
                                            'auto.offset.reset'  : 'latest'})
        
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def StoreKpiValues(self, request: KpiValueList, grpc_context: grpc.ServicerContext
                       ) -> Empty:
        LOGGER.debug('StoreKpiValues: Received gRPC message object: {:}'.format(request))

        producer = self.kafka_producer
        for kpi_value in request.kpi_value_list:
            kpi_value_to_produce : Dict  = {
                "kpi_uuid"       : kpi_value.kpi_id.kpi_id.uuid,            
                "timestamp"      : kpi_value.timestamp.timestamp,                
                "kpi_value_type" : self.ExtractKpiValueByType(kpi_value.kpi_value_type)       
            }
            LOGGER.debug('KPI to produce is {:}'.format(kpi_value_to_produce))
            msg_key = "gRPC-kpivalueapi"        # str(__class__.__name__) can be used
        
            producer.produce(
                KafkaTopic.VALUE.value, 
                key      = msg_key,
                value    = json.dumps(kpi_value_to_produce),
                callback = self.delivery_callback
            )
            producer.flush()
        return Empty()

    def ExtractKpiValueByType(self, value):
        attributes = [ 'floatVal' , 'int32Val' , 'uint32Val','int64Val', 
                       'uint64Val', 'stringVal', 'boolVal']
        for attr in attributes:
            try:
                return getattr(value, attr)
            except (ValueError, TypeError, AttributeError):
                continue
        return None

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SelectKpiValues(self, request: KpiValueFilter, grpc_context: grpc.ServicerContext
                        ) -> KpiValueList:
        LOGGER.debug('StoreKpiValues: Received gRPC message object: {:}'.format(request))
        response = KpiValueList()
        
        kpi_manager_client = KpiManagerClient()
        prom_connect       = PrometheusConnect(url=PROM_URL)

        metrics          = [self.GetKpiSampleType(kpi, kpi_manager_client) for kpi       in request.kpi_id]
        start_timestamps = [parse_datetime(timestamp)                      for timestamp in request.start_timestamp]
        end_timestamps   = [parse_datetime(timestamp)                      for timestamp in request.end_timestamp]

        prom_response = []
        for start_time, end_time in zip(start_timestamps, end_timestamps):
            for metric in metrics:
                print(start_time, end_time, metric)
                LOGGER.debug(">>> Query: {:}".format(metric))
                prom_response.append(
                    prom_connect.custom_query_range(
                    query      = metric,        # this is the metric name and label config
                    start_time = start_time,
                    end_time   = end_time,
                    step       = 30,            # or any other step value (missing in gRPC Filter request)
                    )
                )
        
        for single_resposne in prom_response:
            # print ("{:}".format(single_resposne))
            for record in single_resposne:
                # print("Record >>> kpi: {:} >>> time & values set: {:}".format(record['metric']['__name__'], record['values']))
                for value in record['values']:
                    # print("{:} - {:}".format(record['metric']['__name__'], value))
                    kpi_value = KpiValue()
                    kpi_value.kpi_id.kpi_id  = record['metric']['__name__'],      
                    kpi_value.timestamp      = value[0],      
                    kpi_value.kpi_value_type.CopyFrom(self.ConverValueToKpiValueType(value['kpi_value']))
                    response.kpi_value_list.append(kpi_value)
        return response
    
    def GetKpiSampleType(self, kpi_value: str, kpi_manager_client):
        kpi_id = KpiId()
        kpi_id.kpi_id.uuid = kpi_value.kpi_id.kpi_id.uuid
        # print("KpiId generated: {:}".format(kpi_id))
        try:
            kpi_descriptor_object = KpiDescriptor()
            kpi_descriptor_object = kpi_manager_client.GetKpiDescriptor(kpi_id)
            # TODO: why kpi_descriptor_object recevies a KpiDescriptor type object not Empty type object???
            if kpi_descriptor_object.kpi_id.kpi_id.uuid == kpi_id.kpi_id.uuid:
                LOGGER.info("Extracted KpiDescriptor: {:}".format(kpi_descriptor_object))
                print("Extracted KpiDescriptor: {:}".format(kpi_descriptor_object))
                return KpiSampleType.Name(kpi_descriptor_object.kpi_sample_type)    # extract and return the name of KpiSampleType
            else:
                LOGGER.info("No KPI Descriptor found in DB for Kpi ID: {:}".format(kpi_id))
                print("No KPI Descriptor found in DB for Kpi ID: {:}".format(kpi_id))
        except Exception as e:
            LOGGER.info("Unable to get KpiDescriptor. Error: {:}".format(e))
            print ("Unable to get KpiDescriptor. Error: {:}".format(e))

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetKpiAlarms(self, request: KpiId, grpc_context: grpc.ServicerContext) -> KpiAlarms: # type: ignore
        """
        Get Alarms from Kafka return Alrams periodically.
        """
        LOGGER.debug('GetKpiAlarms: {:}'.format(request))
        response = KpiAlarms()

        for alarm_key, value in self.StartResponseListener(request.kpi_id.uuid):
            response.start_timestamp.timestamp = datetime.strptime(
                value["window_start"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
            response.kpi_id.kpi_id.uuid  = value['kpi_id']
            for key, threshold in value.items():
                if key not in ['kpi_id', 'window']:
                    response.alarms[key] = threshold

            yield response

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
                LOGGER.info("entering while...")
                key, value = self.result_queue.get()  # Wait until a result is available
                LOGGER.info("In while true ...")
                yield key, value  # Yield the result to the calling function
        except Exception as e:
            LOGGER.warning("Listener stopped. Error: {:}".format(e))
        finally:
            self.scheduler.shutdown()

    def response_listener(self, filter_key=None):
        """
        Poll Kafka messages and put key-value pairs into the queue.
        """
        LOGGER.info(f"Polling Kafka topic {self.listener_topic}...")

        consumer = self.kafka_consumer
        consumer.subscribe([self.listener_topic])
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            elif msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    LOGGER.error(f"Kafka error: {msg.error()}")
                break
            try:
                key = msg.key().decode('utf-8') if msg.key() else None
                if filter_key is not None and key == filter_key:
                    value = json.loads(msg.value().decode('utf-8'))
                    LOGGER.info(f"Received key: {key}, value: {value}")
                    self.result_queue.put((key, value))
                else:
                    LOGGER.warning(f"Skipping message with unmatched key: {key} - {filter_key}")
            except Exception as e:
                LOGGER.error(f"Error processing Kafka message: {e}")

    def delivery_callback(self, err, msg):
        if err: LOGGER.debug('Message delivery failed: {:}'.format(err))
        else:   LOGGER.debug('Message delivered to topic {:}'.format(msg.topic()))

    def ConverValueToKpiValueType(self, value):
        kpi_value_type = KpiValueType()
        if isinstance(value, int):
            kpi_value_type.int32Val = value
        elif isinstance(value, float):
            kpi_value_type.floatVal = value
        elif isinstance(value, str):
            kpi_value_type.stringVal = value
        elif isinstance(value, bool):
            kpi_value_type.boolVal = value
        # Add other checks for different types as needed
        return kpi_value_type
