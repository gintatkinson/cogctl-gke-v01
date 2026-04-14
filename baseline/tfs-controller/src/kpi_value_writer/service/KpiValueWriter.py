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
import logging
import threading

from confluent_kafka import KafkaError
from confluent_kafka import Consumer as KafkaConsumer

from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from common.proto.kpi_manager_pb2 import KpiDescriptor, KpiId
from common.Settings import get_service_port_grpc
from common.Constants import ServiceNameEnum
from common.tools.service.GenericGrpcService import GenericGrpcService

from kpi_manager.client.KpiManagerClient import KpiManagerClient
from .MetricWriterToPrometheus import MetricWriterToPrometheus


LOGGER = logging.getLogger(__name__)

class KpiValueWriter(GenericGrpcService):
    def __init__(self, cls_name : str = __name__) -> None:
        port = get_service_port_grpc(ServiceNameEnum.KPIVALUEWRITER)
        super().__init__(port, cls_name=cls_name)
        self.kafka_consumer = KafkaConsumer({'bootstrap.servers' : KafkaConfig.get_kafka_address(),
                                            'group.id'           : 'KpiValueWriter',
                                            'auto.offset.reset'  : 'latest'})

    def install_servicers(self):
        thread = threading.Thread(target=self.KafkaKpiConsumer, args=())
        thread.start()

    def KafkaKpiConsumer(self):
        kpi_manager_client = KpiManagerClient()
        metric_writer      = MetricWriterToPrometheus()

        consumer = self.kafka_consumer
        consumer.subscribe([KafkaTopic.VALUE.value])
        LOGGER.debug("Kafka Consumer start listenng on topic: {:}".format(KafkaTopic.VALUE.value))
        while True:
            raw_kpi = consumer.poll(1.0)
            if raw_kpi is None:
                continue
            elif raw_kpi.error():
                if raw_kpi.error().code() != KafkaError._PARTITION_EOF:
                    print("Consumer error: {}".format(raw_kpi.error()))
                continue
            try:
                kpi_value = json.loads(raw_kpi.value().decode('utf-8'))
                LOGGER.info("Received KPI : {:}".format(kpi_value))
                self.get_kpi_descriptor(kpi_value, kpi_manager_client, metric_writer)
            except:
                LOGGER.exception("Error detail: ")
                continue

    def get_kpi_descriptor(self, kpi_value: str, kpi_manager_client, metric_writer):
        kpi_id = KpiId()
        kpi_id.kpi_id.uuid = kpi_value['kpi_id']  # type: ignore
        try:
            kpi_descriptor_object = KpiDescriptor()
            kpi_descriptor_object = kpi_manager_client.GetKpiDescriptor(kpi_id)
            if kpi_descriptor_object.kpi_id.kpi_id.uuid == kpi_id.kpi_id.uuid:
                LOGGER.info("Extracted KpiDescriptor: {:}".format(kpi_descriptor_object))
                metric_writer.create_and_expose_cooked_kpi(kpi_descriptor_object, kpi_value)
            else:
                LOGGER.info("No KPI Descriptor found in Database for Kpi ID: {:}".format(kpi_id))
        except:
            LOGGER.exception("Unable to get KpiDescriptor")
