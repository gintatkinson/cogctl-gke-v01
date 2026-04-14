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

import logging, os, pytest, threading, time
from typing import List, Set
from common.message_broker.Factory import get_messagebroker_backend
from common.message_broker.Message import Message
from common.message_broker.MessageBroker import MessageBroker
from common.message_broker.backend.BackendEnum import BackendEnum
from common.message_broker.backend._Backend import _Backend

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DEFAULT_REDIS_SERVICE_HOST = '127.0.0.1'
DEFAULT_REDIS_SERVICE_PORT = 6379
DEFAULT_REDIS_DATABASE_ID  = 0

REDIS_CONFIG = {
    'REDIS_SERVICE_HOST': os.environ.get('REDIS_SERVICE_HOST', DEFAULT_REDIS_SERVICE_HOST),
    'REDIS_SERVICE_PORT': os.environ.get('REDIS_SERVICE_PORT', DEFAULT_REDIS_SERVICE_PORT),
    'REDIS_DATABASE_ID' : os.environ.get('REDIS_DATABASE_ID',  DEFAULT_REDIS_DATABASE_ID ),
}

SCENARIOS = [
    ('all_inmemory', BackendEnum.INMEMORY, {}          ),
    ('all_redis',    BackendEnum.REDIS,    REDIS_CONFIG),
]

CONSUME_TIMEOUT = 0.1 # seconds

TOPIC_DEVICES  = 'devices'
TOPIC_LINKS    = 'links'
TOPIC_SERVICES = 'services'

class Consumer(threading.Thread):
    def __init__(
        self, message_broker : MessageBroker, # pylint: disable=redefined-outer-name
        topic_names : Set[str], output_list : List[Message],
        consume_timeout=CONSUME_TIMEOUT) -> None:

        super().__init__(daemon=True)
        self._message_broker = message_broker
        self._topic_names = topic_names
        self._output_list = output_list
        self._consume_timeout = consume_timeout

    def run(self) -> None:
        LOGGER.info('{:s} subscribes to topics {:s}'.format(self.name, str(self._topic_names)))
        for message in self._message_broker.consume(self._topic_names, consume_timeout=self._consume_timeout):
            LOGGER.info('{:s} receives {:s}'.format(self.name, str(message)))
            self._output_list.append(message)
        LOGGER.info('{:s} terminates')

@pytest.fixture(scope='session', ids=[str(scenario[0]) for scenario in SCENARIOS], params=SCENARIOS)
def message_broker(request):
    name,mb_backend,mb_settings = request.param
    msg = 'Running scenario {:s} mb_backend={:s}, mb_settings={:s}...'
    LOGGER.info(msg.format(str(name), str(mb_backend.value), str(mb_settings)))
    _message_broker = MessageBroker(get_messagebroker_backend(backend=mb_backend, **mb_settings))
    yield _message_broker
    _message_broker.terminate()

def test_messagebroker_instantiation():
    with pytest.raises(AttributeError) as e:
        MessageBroker(None)
    str_class_path = '{}.{}'.format(_Backend.__module__, _Backend.__name__)
    assert str(e.value) == 'backend must inherit from {}'.format(str_class_path)

    assert MessageBroker(get_messagebroker_backend(BackendEnum.INMEMORY)) is not None

def test_messagebroker(message_broker : MessageBroker): # pylint: disable=redefined-outer-name
    output_list1 : List[Message] = []
    consumer1 = Consumer(message_broker, {TOPIC_DEVICES, TOPIC_LINKS}, output_list1)
    consumer1.start()

    output_list2 : List[Message] = []
    consumer2 = Consumer(message_broker, {TOPIC_DEVICES, TOPIC_SERVICES}, output_list2)
    consumer2.start()

    output_list3 : List[Message] = []
    consumer3 = Consumer(message_broker, {TOPIC_SERVICES}, output_list3)
    consumer3.start()

    LOGGER.info('delay')
    time.sleep(0.5)

    message = Message(topic=TOPIC_DEVICES, content='new-device-01')
    LOGGER.info('publish message={:s}'.format(str(message)))
    message_broker.publish(message)

    message = Message(topic=TOPIC_DEVICES, content='new-device-02')
    LOGGER.info('publish message={:s}'.format(str(message)))
    message_broker.publish(message)

    message = Message(topic=TOPIC_LINKS,   content='new-link-01-02')
    LOGGER.info('publish message={:s}'.format(str(message)))
    message_broker.publish(message)

    LOGGER.info('delay')
    time.sleep(0.1)

    message = Message(topic=TOPIC_DEVICES,  content='update-device-01')
    LOGGER.info('publish message={:s}'.format(str(message)))
    message_broker.publish(message)

    message = Message(topic=TOPIC_DEVICES,  content='update-device-02')
    LOGGER.info('publish message={:s}'.format(str(message)))
    message_broker.publish(message)

    message = Message(topic=TOPIC_SERVICES, content='new-service-01-02')
    LOGGER.info('publish message={:s}'.format(str(message)))
    message_broker.publish(message)

    LOGGER.info('delay')
    time.sleep(0.5)

    LOGGER.info('terminate')
    message_broker.terminate()

    LOGGER.info('join')
    consumer1.join()
    consumer2.join()
    consumer3.join()

    LOGGER.info('output_list1={:s}'.format(str(output_list1)))
    LOGGER.info('output_list2={:s}'.format(str(output_list2)))
    LOGGER.info('output_list3={:s}'.format(str(output_list3)))

    assert len(output_list1) == 5
    assert output_list1[0].topic == TOPIC_DEVICES
    assert output_list1[0].content == 'new-device-01'
    assert output_list1[1].topic == TOPIC_DEVICES
    assert output_list1[1].content == 'new-device-02'
    assert output_list1[2].topic == TOPIC_LINKS
    assert output_list1[2].content == 'new-link-01-02'
    assert output_list1[3].topic == TOPIC_DEVICES
    assert output_list1[3].content == 'update-device-01'
    assert output_list1[4].topic == TOPIC_DEVICES
    assert output_list1[4].content == 'update-device-02'

    assert len(output_list2) == 5
    assert output_list2[0].topic == TOPIC_DEVICES
    assert output_list2[0].content == 'new-device-01'
    assert output_list2[1].topic == TOPIC_DEVICES
    assert output_list2[1].content == 'new-device-02'
    assert output_list2[2].topic == TOPIC_DEVICES
    assert output_list2[2].content == 'update-device-01'
    assert output_list2[3].topic == TOPIC_DEVICES
    assert output_list2[3].content == 'update-device-02'
    assert output_list2[4].topic == TOPIC_SERVICES
    assert output_list2[4].content == 'new-service-01-02'

    assert len(output_list3) == 1
    assert output_list3[0].topic == TOPIC_SERVICES
    assert output_list3[0].content == 'new-service-01-02'
