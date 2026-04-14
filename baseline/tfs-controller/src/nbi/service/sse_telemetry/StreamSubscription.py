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


import logging, time
from typing import Dict, List
from flask import Response
from flask_restful import Resource
from kafka import KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.consumer.fetcher import ConsumerRecord
from kafka.errors import TopicAlreadyExistsError
from common.tools.kafka.Variables import KafkaConfig
from nbi.service._tools.Authentication import HTTP_AUTH


LOGGER = logging.getLogger(__name__)


KAFKA_BOOT_SERVERS = KafkaConfig.get_kafka_address()


class StreamSubscription(Resource):
    @HTTP_AUTH.login_required
    def get(self, subscription_id : int):
        LOGGER.debug('[get] begin')

        def event_stream():
            LOGGER.debug('[stream:event_stream] begin')
            topic = 'subscription.{:s}'.format(str(subscription_id))

            LOGGER.info('[stream:event_stream] Checking Topics...')
            kafka_admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOT_SERVERS)
            existing_topics = set(kafka_admin.list_topics())
            LOGGER.info('[stream:event_stream] existing_topics={:s}'.format(str(existing_topics)))
            if topic not in existing_topics:
                LOGGER.info('[stream:event_stream] Creating Topic...')
                to_create = [NewTopic(topic, num_partitions=3, replication_factor=1)]
                try:
                    kafka_admin.create_topics(to_create, validate_only=False)
                    LOGGER.info('[stream:event_stream] Topic Created')
                except TopicAlreadyExistsError:
                    pass

            LOGGER.info('[stream:event_stream] Connecting Consumer...')
            kafka_consumer = KafkaConsumer(
                bootstrap_servers = KAFKA_BOOT_SERVERS,
                group_id          = None, # consumer dispatch all messages sent to subscribed topics
                auto_offset_reset = 'latest',
            )
            LOGGER.info('[stream:event_stream] Subscribing topic={:s}...'.format(str(topic)))
            kafka_consumer.subscribe(topics=[topic])
            LOGGER.info('[stream:event_stream] Subscribed')

            while True:
                #LOGGER.debug('[stream:event_stream] Waiting...')
                topic_records : Dict[TopicPartition, List[ConsumerRecord]] = \
                    kafka_consumer.poll(timeout_ms=1000, max_records=1)
                if len(topic_records) == 0:
                    time.sleep(0.5)
                    continue    # no pending records

                #LOGGER.info('[stream:event_stream] topic_records={:s}'.format(str(topic_records)))
                for _topic, records in topic_records.items():
                    if _topic.topic != topic: continue
                    for record in records:
                        #message_key   = record.key.decode('utf-8')
                        message_value = record.value.decode('utf-8')

                        #MSG = '[stream:event_stream] message_key={:s} message_value={:s}'
                        #LOGGER.debug(MSG.format(str(message_key), str(message_value)))
                        yield message_value
                        #LOGGER.debug('[stream:event_stream] Sent')

            LOGGER.info('[stream:event_stream] Closing...')
            kafka_consumer.close()

        LOGGER.info('[stream] Ready to stream...')
        return Response(event_stream(), mimetype='text/event-stream')
