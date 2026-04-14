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

import logging, sys
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from slice.client.SliceClient import SliceClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def main():
    context_client = ContextClient()
    device_client = DeviceClient()
    service_client = ServiceClient()
    slice_client = SliceClient()

    LOGGER.info('Loading scenario...')
    descriptor_loader = DescriptorLoader(
        descriptors_file=sys.argv[1], context_client=context_client, device_client=device_client,
        service_client=service_client, slice_client=slice_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    descriptor_loader.validate()
    LOGGER.info('Done!')
    return 0

if __name__ == '__main__':
    sys.exit(main())
