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

import logging
from common.tools.descriptor.Loader import DescriptorLoader, validate_empty_scenario
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from tests.Fixtures import context_client, device_client # pylint: disable=unused-import
from tests.tools.test_tools_p4 import ADMIN_CONTEXT_ID, DESC_TOPO

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def test_scenario_cleanup(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    device_client : DeviceClient    # pylint: disable=redefined-outer-name
) -> None:
    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    # Unload topology and validate empty scenario
    descriptor_loader = DescriptorLoader(
        descriptors_file=DESC_TOPO, context_client=context_client, device_client=device_client)
    descriptor_loader.validate()
    descriptor_loader.unload()
    validate_empty_scenario(context_client)
