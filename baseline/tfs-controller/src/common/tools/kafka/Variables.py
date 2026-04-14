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
from enum import Enum
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from common.Settings import get_setting


LOGGER = logging.getLogger(__name__)
KFK_SERVER_ADDRESS_TEMPLATE = 'kafka-public.{:s}.svc.cluster.local:{:s}'

KAFKA_TOPIC_NUM_PARTITIONS         = 1
KAFKA_TOPIC_REPLICATION_FACTOR     = 1
#KAFKA_TOPIC_LIST_TIMEOUT           = 5
KAFKA_TOPIC_CREATE_REQUEST_TIMEOUT = 60_000 # ms
KAFKA_TOPIC_CREATE_WAIT_ITERATIONS = 10
KAFKA_TOPIC_CREATE_WAIT_TIME       = 1

class KafkaConfig(Enum):

    @staticmethod
    def get_kafka_address() -> str:
        kafka_server_address = get_setting('KFK_SERVER_ADDRESS', default=None)
        if kafka_server_address is None:
            KFK_NAMESPACE = get_setting('KFK_NAMESPACE', default='kafka')
            KFK_PORT      = get_setting('KFK_SERVER_PORT', default='9092')
            kafka_server_address = KFK_SERVER_ADDRESS_TEMPLATE.format(KFK_NAMESPACE, KFK_PORT)
        return kafka_server_address

    @staticmethod
    def get_admin_client():
        SERVER_ADDRESS = KafkaConfig.get_kafka_address()
        ADMIN_CLIENT   = KafkaAdminClient(bootstrap_servers=SERVER_ADDRESS)
        return ADMIN_CLIENT


class KafkaTopic(Enum):
    # TODO: Later to be populated from ENV variable.
    TELEMETRY_REQUEST    = 'topic_telemetry_request'
    TELEMETRY_RESPONSE   = 'topic_telemetry_response'
    RAW                  = 'topic_raw'                  # TODO: Update name to telemetry_raw
    LABELED              = 'topic_labeled'              # TODO: Update name to telemetry_labeled
    VALUE                = 'topic_value'                # TODO: Update name to telemetry_value
    ALARMS               = 'topic_alarms'               # TODO: Update name to telemetry_alarms
    ANALYTICS_REQUEST    = 'topic_analytics_request'
    ANALYTICS_RESPONSE   = 'topic_analytics_response'
    VNTMANAGER_REQUEST   = 'topic_vntmanager_request'
    VNTMANAGER_RESPONSE  = 'topic_vntmanager_response'
    NBI_SOCKETIO_WORKERS = 'tfs_nbi_socketio'

    @staticmethod
    def create_all_topics() -> bool:
        '''
            Method to create Kafka topics defined as class members
        '''
        LOGGER.debug('Kafka server address: {:s}'.format(str(KafkaConfig.get_kafka_address())))
        kafka_admin_client = KafkaConfig.get_admin_client()

        #topic_metadata = kafka_admin_client.list_topics(timeout=KAFKA_TOPIC_LIST_TIMEOUT)
        #existing_topics = set(topic_metadata.topics.keys())
        existing_topics = set(kafka_admin_client.list_topics())
        LOGGER.debug('Existing Kafka topics: {:s}'.format(str(existing_topics)))

        missing_topics = [
            NewTopic(topic.value, KAFKA_TOPIC_NUM_PARTITIONS, KAFKA_TOPIC_REPLICATION_FACTOR)
            for topic in KafkaTopic
            if topic.value not in existing_topics
        ]
        LOGGER.debug('Missing Kafka topics: {:s}'.format(str(missing_topics)))

        if len(missing_topics) == 0:
            LOGGER.debug('All topics already existed.')
            return True

        #create_topic_future_map = kafka_admin_client.create_topics(missing_topics, request_timeout=5*60)
        #LOGGER.debug('create_topic_future_map: {:s}'.format(str(create_topic_future_map)))
        try:
            topics_result = kafka_admin_client.create_topics(
                new_topics=missing_topics, timeout_ms=KAFKA_TOPIC_CREATE_REQUEST_TIMEOUT,
                validate_only=False
            )
            LOGGER.debug('topics_result={:s}'.format(str(topics_result)))

            failed_topic_creations = set()
            #for topic, future in create_topic_future_map.items():
            #    try:
            #        LOGGER.info('Waiting for Topic({:s})...'.format(str(topic)))
            #        future.result()  # Blocks until topic is created or raises an exception
            #        LOGGER.info('Topic({:s}) successfully created.'.format(str(topic)))
            #    except: # pylint: disable=bare-except
            #        LOGGER.exception('Failed to create Topic({:s})'.format(str(topic)))
            #        failed_topic_creations.add(topic)
            for topic_name, error_code, error_message in topics_result.topic_errors:
                if error_code == 0 and error_message is None:
                    MSG = 'Topic({:s}) successfully created.'
                    LOGGER.info(MSG.format(str(topic_name)))
                else:
                    MSG = 'Failed to create Topic({:s}): error_code={:s} error_message={:s}'
                    LOGGER.error(MSG.format(str(topic_name), str(error_code), str(error_message)))
                    failed_topic_creations.add(topic_name)

            if len(failed_topic_creations) > 0: return False
            LOGGER.debug('All topics created.')

        except TopicAlreadyExistsError:
            LOGGER.debug('Some topics already exists.')

        # Wait until topics appear in metadata
        desired_topics = {topic.value for topic in KafkaTopic}
        missing_topics = set()
        for _ in range(KAFKA_TOPIC_CREATE_WAIT_ITERATIONS):
            #topic_metadata = kafka_admin_client.list_topics(timeout=KAFKA_TOPIC_LIST_TIMEOUT)
            #existing_topics = set(topic_metadata.topics.keys())
            existing_topics = set(kafka_admin_client.list_topics())
            LOGGER.debug('existing_topics={:s}'.format(str(existing_topics)))
            missing_topics = desired_topics.difference(existing_topics)
            if len(missing_topics) == 0: break
            MSG = 'Waiting for Topics({:s}) to appear in metadata...'
            LOGGER.debug(MSG.format(str(missing_topics)))
            time.sleep(KAFKA_TOPIC_CREATE_WAIT_TIME)

        if len(missing_topics) > 0:
            MSG = 'Something went wrong... Topics({:s}) does not appear in metadata'
            LOGGER.error(MSG.format(str(missing_topics)))
            return False
        else:
            LOGGER.debug('All topics created and available.')
            return True


if __name__ == '__main__':
    import os
    if 'KFK_SERVER_ADDRESS' not in os.environ:
        os.environ['KFK_SERVER_ADDRESS'] = 'kafka-service.kafka.svc.cluster.local:9092'
    KafkaTopic.create_all_topics()
