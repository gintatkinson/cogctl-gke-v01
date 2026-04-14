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

import json, logging, socketio, threading
from typing import Dict, List
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from kafka import KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord
from .Constants import SIO_NAMESPACE, SIO_ROOM

LOGGER = logging.getLogger(__name__)

class VntRecommThread(threading.Thread):
    def __init__(self, namespace : socketio.Namespace):
        super().__init__(daemon=True)
        self._terminate = threading.Event()
        self._namespace = namespace

    def start(self):
        self._terminate.clear()
        return super().start()

    def stop(self) -> None:
        self._terminate.set()

    def run(self):
        LOGGER.info('[run] Starting...')
        try:
            kafka_consumer = KafkaConsumer(
                bootstrap_servers = KafkaConfig.get_kafka_address(),
                group_id          = None, # consumer dispatch all messages sent to subscribed topics
                auto_offset_reset = 'latest',
            )

            LOGGER.info('[run] Subscribing...')
            kafka_consumer.subscribe(topics=[KafkaTopic.VNTMANAGER_REQUEST.value])
            LOGGER.info('[run] Subscribed')

            while not self._terminate.is_set():
                topic_records : Dict[TopicPartition, List[ConsumerRecord]] = \
                    kafka_consumer.poll(timeout_ms=1000, max_records=1)
                if len(topic_records) == 0: continue    # no pending records
                self.process_topic_records(topic_records)

            LOGGER.info('[run] Closing...')
            kafka_consumer.close()
        except: # pylint: disable=bare-except
            LOGGER.exception('[run] Unexpected Thread Exception')
        LOGGER.info('[run] Terminated')

    def process_topic_records(
        self, topic_records : Dict[TopicPartition, List[ConsumerRecord]]
    ) -> None:
        MSG = '[process_topic_records] topic_records={:s}'
        LOGGER.debug(MSG.format(str(topic_records)))
        for topic, records in topic_records.items():
            if topic.topic == KafkaTopic.VNTMANAGER_REQUEST.value:
                for record in records: self.emit_recommendation(record)

    def emit_recommendation(self, record : ConsumerRecord) -> None:
        message_key   = record.key.decode('utf-8')
        message_value = record.value.decode('utf-8')
        message_value = json.loads(message_value)
        message_event = message_value.pop('event')
        message_data  = json.loads(message_value['data'])
        message_data['_request_key'] = message_key
        message_data = json.dumps(message_data)

        MSG = '[emit_recommendation] Recommendation: event={:s} data={:s}'
        LOGGER.debug(MSG.format(str(message_event), str(message_data)))

        LOGGER.debug('[emit_recommendation] checking server namespace...')
        server : socketio.Server = self._namespace.server
        if server is None: return
        LOGGER.debug('[emit_recommendation] emitting recommendation...')
        server.emit(message_event, message_data, namespace=SIO_NAMESPACE, to=SIO_ROOM)
        LOGGER.debug('[emit_recommendation] emitted')
