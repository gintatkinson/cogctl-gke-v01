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
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from tests.Fixtures import context_client, device_client   # pylint: disable=unused-import
from tests.tools.test_tools_p4 import (
    ADMIN_CONTEXT_ID,
    DESC_FILE_RULES_DELETE_ALL,
    DEV_NB,
    CONNECTION_RULES,
    ENDPOINT_RULES,
    DATAPLANE_RULES_NB_INT_B1,
    DATAPLANE_RULES_NB_INT_B2,
    DATAPLANE_RULES_NB_INT_B3,
    DATAPLANE_RULES_NB_RT_WEST,
    DATAPLANE_RULES_NB_RT_EAST,
    DATAPLANE_RULES_NB_ACL,
    DATAPLANE_RULES_NB_TOT,
    verify_number_of_rules
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def test_initial_context(
    context_client : ContextClient # pylint: disable=redefined-outer-name
) -> None:
    # Verify the scenario has 0 service and 0 slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    # Check there are no slices
    response = context_client.ListSlices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Slices[{:d}] = {:s}'.format(len(response.slices), grpc_message_to_json_string(response)))
    assert len(response.slices) == 0

    # Check there is 0 service
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
    assert len(response.services) == 0

    # Check there are 3 devices
    response = context_client.ListDevices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Devices[{:d}] = {:s}'.format(len(response.devices), grpc_message_to_json_string(response)))
    assert len(response.devices) == DEV_NB

def test_rules_before_removal(
    context_client : ContextClient # pylint: disable=redefined-outer-name
) -> None:
    response = context_client.ListDevices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Devices[{:d}] = {:s}'.format(len(response.devices), grpc_message_to_json_string(response)))
    assert len(response.devices) == DEV_NB

    # Verify that the following rules are in place
    desired_rules_nb = \
        CONNECTION_RULES + \
        ENDPOINT_RULES + \
        DATAPLANE_RULES_NB_INT_B1 + \
        DATAPLANE_RULES_NB_INT_B2 + \
        DATAPLANE_RULES_NB_INT_B3 + \
        DATAPLANE_RULES_NB_RT_WEST + \
        DATAPLANE_RULES_NB_RT_EAST + \
        DATAPLANE_RULES_NB_ACL
    assert desired_rules_nb == CONNECTION_RULES + ENDPOINT_RULES + DATAPLANE_RULES_NB_TOT
    verify_number_of_rules(response.devices, desired_rules_nb)

def test_rules_removal(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    device_client : DeviceClient    # pylint: disable=redefined-outer-name
) -> None:
    # Load dataplane rules for removal
    descriptor_loader = DescriptorLoader(
        descriptors_file=DESC_FILE_RULES_DELETE_ALL, context_client=context_client, device_client=device_client
    )
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)

def test_rules_after_removal(
    context_client : ContextClient # pylint: disable=redefined-outer-name
) -> None:
    # State **after** removing all dataplane rules
    # Still 3 devices
    response = context_client.ListDevices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Devices[{:d}] = {:s}'.format(len(response.devices), grpc_message_to_json_string(response)))
    assert len(response.devices) == DEV_NB

    # Only connection and endpoint rules must be in place
    desired_rules_nb = \
        CONNECTION_RULES + \
        ENDPOINT_RULES
    verify_number_of_rules(response.devices, desired_rules_nb)
