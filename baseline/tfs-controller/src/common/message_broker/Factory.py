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

import logging, os
from typing import Optional, Union
from .backend._Backend import _Backend
from .backend.BackendEnum import BackendEnum
from .backend.inmemory.InMemoryBackend import InMemoryBackend
from .backend.nats.NatsBackend import NatsBackend
#from .backend.redis.RedisBackend import RedisBackend

LOGGER = logging.getLogger(__name__)

BACKENDS = {
    BackendEnum.INMEMORY.value: InMemoryBackend,
    BackendEnum.NATS.value: NatsBackend,
    #BackendEnum.REDIS.value: RedisBackend,
    #BackendEnum.KAFKA.value: KafkaBackend,
    #BackendEnum.RABBITMQ.value: RabbitMQBackend,
    #BackendEnum.ZEROMQ.value: ZeroMQBackend,
}

DEFAULT_MB_BACKEND = BackendEnum.INMEMORY

def get_messagebroker_backend(backend : Optional[Union[str, BackendEnum]] = None, **settings) -> _Backend:
    # return an instance of MessageBroker initialized with selected backend.
    # The backend is selected using following criteria (first that is not None is selected):
    # 1. user selected by parameter (backend=...)
    # 2. environment variable MB_BACKEND
    # 3. default backend: INMEMORY
    if backend is None: backend = os.environ.get('MB_BACKEND', DEFAULT_MB_BACKEND)
    if backend is None: raise Exception('MessageBroker Backend not specified')
    if isinstance(backend, BackendEnum): backend = backend.value
    backend_class = BACKENDS.get(backend)
    if backend_class is None: raise Exception('Unsupported MessageBrokerBackend({:s})'.format(backend))
    LOGGER.info('Selected MessageBroker Backend: {:s}'.format(backend))
    return backend_class(**settings)
