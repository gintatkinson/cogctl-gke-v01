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

import logging, signal, sys, threading
from .MockService_Dependencies import MockService_Dependencies
from .Config import BIND_ADDRESS, BIND_PORT, LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
)
LOGGER = logging.getLogger(__name__)
TERMINATE = threading.Event()

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name,unused-argument
    LOGGER.warning('Terminate signal received')
    TERMINATE.set()

def main():
    LOGGER.info('Starting...')
    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    grpc_service = MockService_Dependencies(BIND_PORT, bind_address=BIND_ADDRESS)
    grpc_service.start()

    # Wait for Ctrl+C or termination signal
    while not TERMINATE.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    grpc_service.stop()

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
