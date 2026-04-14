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

import logging, os, time, json, socket, re
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, DeviceOperationalStatusEnum, Empty
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from tests.Fixtures import context_client, device_client # pylint: disable=unused-import

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# Update the path to your QKD descriptor file
DESCRIPTOR_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'descriptorQKD_links.json')
ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))

def load_descriptor_with_runtime_ip(descriptor_file_path):
    """
    Load the descriptor file and replace placeholder IP with the machine's IP address.
    """
    with open(descriptor_file_path, 'r') as descriptor_file:
        descriptor = descriptor_file.read()

    # Get the current machine's IP address
    try:
        # Use socket to get the local IP address directly from the network interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        current_ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        raise Exception(f"Unable to get the IP address: {str(e)}")

    # Replace all occurrences of <YOUR_MACHINE_IP> with the current IP
    updated_descriptor = re.sub(r"<YOUR_MACHINE_IP>", current_ip, descriptor)

    # Write updated descriptor back
    with open(descriptor_file_path, 'w') as descriptor_file:
        descriptor_file.write(updated_descriptor)

    return json.loads(updated_descriptor)

def load_and_process_descriptor(context_client, device_client, descriptor_file_path):
    """
    Function to load and process descriptor programmatically, similar to what WebUI does.
    """
    print(f"Loading descriptor from file: {descriptor_file_path}")
    try:
        # Update the descriptor with the runtime IP address
        descriptor = load_descriptor_with_runtime_ip(descriptor_file_path)

        # Initialize DescriptorLoader with the updated descriptor file
        descriptor_loader = DescriptorLoader(
            descriptors_file=descriptor_file_path, context_client=context_client, device_client=device_client
        )

        # Process and validate the descriptor
        print("Processing the descriptor...")
        results = descriptor_loader.process()
        print(f"Descriptor processing results: {results}")

        print("Checking descriptor load results...")
        check_descriptor_load_results(results, descriptor_loader)

        print("Validating descriptor...")
        descriptor_loader.validate()
        print("Descriptor validated successfully.")
    except Exception as e:
        LOGGER.error(f"Failed to load and process descriptor: {e}")
        raise e

def test_qkd_scenario_bootstrap(
    context_client: ContextClient,  # pylint: disable=redefined-outer-name
    device_client: DeviceClient,    # pylint: disable=redefined-outer-name
) -> None:
    """
    This test validates that the QKD scenario is correctly bootstrapped.
    """
    print("Starting QKD scenario bootstrap test...")

    # Check if context_client and device_client are instantiated
    if context_client is None:
        print("Error: context_client is not instantiated!")
    else:
        print(f"context_client is instantiated: {context_client}")

    if device_client is None:
        print("Error: device_client is not instantiated!")
    else:
        print(f"device_client is instantiated: {device_client}")

    # Validate empty scenario
    print("Validating empty scenario...")
    validate_empty_scenario(context_client)

    # Load the descriptor
    load_and_process_descriptor(context_client, device_client, DESCRIPTOR_FILE_PATH)

def test_qkd_devices_enabled(
    context_client: ContextClient,  # pylint: disable=redefined-outer-name
) -> None:
    """
    This test validates that the QKD devices are enabled.
    """
    print("Starting QKD devices enabled test...")

    # Check if context_client is instantiated
    if context_client is None:
        print("Error: context_client is not instantiated!")
    else:
        print(f"context_client is instantiated: {context_client}")

    DEVICE_OP_STATUS_ENABLED = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED

    num_devices = -1
    num_devices_enabled, num_retry = 0, 0

    while (num_devices != num_devices_enabled) and (num_retry < 10):
        print(f"Attempt {num_retry + 1}: Checking device status...")

        time.sleep(1.0)  # Add a delay to allow for device enablement

        response = context_client.ListDevices(Empty())
        num_devices = len(response.devices)
        print(f"Total devices found: {num_devices}")

        num_devices_enabled = 0
        for device in response.devices:
            if device.device_operational_status == DEVICE_OP_STATUS_ENABLED:
                num_devices_enabled += 1
        
        print(f"Devices enabled: {num_devices_enabled}/{num_devices}")
        num_retry += 1

    # Final check to ensure all devices are enabled
    print(f"Final device status: {num_devices_enabled}/{num_devices} devices enabled.")
    assert num_devices_enabled == num_devices
    print("QKD devices enabled test completed.")