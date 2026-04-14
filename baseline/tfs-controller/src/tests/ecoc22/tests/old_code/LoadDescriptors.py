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

import json, logging, sys
from common.Settings import get_setting
from context.client.ContextClient import ContextClient
from common.proto.context_pb2 import Context, Device, Link, Topology
from device.client.DeviceClient import DeviceClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def main():
    context_client = ContextClient()
    device_client  = DeviceClient()

    with open('tests/ecoc22/descriptors.json', 'r', encoding='UTF-8') as f:
        descriptors = json.loads(f.read())

    for context  in descriptors['contexts'  ]: context_client.SetContext (Context (**context ))
    for topology in descriptors['topologies']: context_client.SetTopology(Topology(**topology))
    for device   in descriptors['devices'   ]: device_client .AddDevice  (Device  (**device  ))
    for link     in descriptors['links'     ]: context_client.SetLink    (Link    (**link    ))
    return 0

if __name__ == '__main__':
    sys.exit(main())
