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


from dask.distributed import Client, LocalCluster
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from confluent_kafka import Consumer, Producer

import logging
logger = logging.getLogger(__name__)


class AnalyzerHelper:
    def __init__(self):
        pass

    @staticmethod
    def initialize_dask_client(cluster_instance):
        """Initialize a local Dask client."""
        if cluster_instance is None:
            logger.error("Dask Cluster is not initialized. Exiting.")
            return None
        client = Client(cluster_instance)
        logger.info(f"Dask Client Initialized: {client}")
        return client

    @staticmethod
    def initialize_dask_cluster(n_workers=1, threads_per_worker=2):
        """Initialize a local Dask cluster"""
        cluster = LocalCluster(n_workers=n_workers, threads_per_worker=threads_per_worker)
        logger.info(f"Dask Cluster Initialized: {cluster}")
        return cluster

    @staticmethod
    def initialize_kafka_consumer():    # TODO: update to receive topic and group_id as parameters
        """Initialize the Kafka consumer."""
        consumer_conf = {
            'bootstrap.servers': KafkaConfig.get_kafka_address(),
            'group.id': 'analytics-backend',
            'auto.offset.reset': 'latest'
        }
        consumer = Consumer(consumer_conf)
        consumer.subscribe([KafkaTopic.VALUE.value])
        return consumer

    @staticmethod
    def initialize_kafka_producer():
        """Initialize the Kafka producer."""
        return Producer({'bootstrap.servers': KafkaConfig.get_kafka_address()})

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
