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

import logging, os, time
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, DeviceOperationalStatusEnum, Empty
from common.proto.monitoring_pb2 import KpiDescriptorList
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from monitoring.client.MonitoringClient import MonitoringClient
from tests.Fixtures import context_client, device_client, monitoring_client # pylint: disable=unused-import

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'descriptors_emulated.json')
ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))

def test_scenario_bootstrap(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    device_client : DeviceClient,   # pylint: disable=redefined-outer-name
) -> None:
    validate_empty_scenario(context_client)

    descriptor_loader = DescriptorLoader(
        descriptors_file=DESCRIPTOR_FILE, context_client=context_client, device_client=device_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    descriptor_loader.validate()

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

def test_scenario_devices_enabled(
    context_client : ContextClient,         # pylint: disable=redefined-outer-name
) -> None:
    """
    This test validates that the devices are enabled.
    """
    DEVICE_OP_STATUS_ENABLED = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED

    num_devices = -1
    num_devices_enabled, num_retry = 0, 0
    while (num_devices != num_devices_enabled) and (num_retry < 30):
        time.sleep(2.0)
        response = context_client.ListDevices(Empty())
        num_devices = len(response.devices)
        num_devices_enabled = 0
        for device in response.devices:
            if device.device_operational_status != DEVICE_OP_STATUS_ENABLED: continue
            num_devices_enabled += 1
        LOGGER.info('Num Devices enabled: {:d}/{:d}'.format(num_devices_enabled, num_devices))
        num_retry += 1
    assert num_devices_enabled == num_devices

def test_scenario_kpis_created(
    context_client : ContextClient,         # pylint: disable=redefined-outer-name
    monitoring_client: MonitoringClient,    # pylint: disable=redefined-outer-name
) -> None:
    """
    This test validates that KPIs related to the service/device/endpoint were created
    during the service creation process.
    """
    response = context_client.ListDevices(Empty())
    kpis_expected = set()
    for device in response.devices:
        device_uuid = device.device_id.device_uuid.uuid
        for endpoint in device.device_endpoints:
            endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
            for kpi_sample_type in endpoint.kpi_sample_types:
                kpis_expected.add((device_uuid, endpoint_uuid, kpi_sample_type))
    num_kpis_expected = len(kpis_expected)
    LOGGER.info('Num KPIs expected: {:d}'.format(num_kpis_expected))

    num_kpis_created, num_retry = 0, 0
    while (num_kpis_created != num_kpis_expected) and (num_retry < 30):
        time.sleep(2.0)
        response: KpiDescriptorList = monitoring_client.GetKpiDescriptorList(Empty())
        num_kpis_created = len(response.kpi_descriptor_list)
        LOGGER.info('Num KPIs created: {:d}'.format(num_kpis_created))
        num_retry += 1
    assert num_kpis_created == num_kpis_expected
