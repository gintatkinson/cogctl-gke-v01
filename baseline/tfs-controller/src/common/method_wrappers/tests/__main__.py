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

import logging, random
from prometheus_client import start_http_server
from .DummyDeviceDriver import DummyDeviceDriver

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

def main():
    # Start up the server to expose the metrics
    start_http_server(8000)

    ddd = DummyDeviceDriver()
    while True:
        func = random.choice([ddd.get_config, ddd.set_config, ddd.del_config])
        func()

if __name__ == '__main__':
    main()
