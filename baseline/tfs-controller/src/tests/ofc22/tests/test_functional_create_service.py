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

import logging, os, random
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, Empty, ServiceTypeEnum
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.descriptor.Loader import DescriptorLoader
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from monitoring.client.MonitoringClient import MonitoringClient
from tests.Fixtures import context_client, monitoring_client                    # pylint: disable=unused-import
from tests.tools.mock_osm.MockOSM import MockOSM
from .Fixtures import osm_wim                                                   # pylint: disable=unused-import
from .Objects import WIM_SERVICE_CONNECTION_POINTS, WIM_SERVICE_TYPE

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'descriptors_emulated.json')
ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))

def test_service_creation(context_client : ContextClient, osm_wim : MockOSM): # pylint: disable=redefined-outer-name
    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    descriptor_loader.validate()

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    # Create Connectivity Service
    service_uuid = osm_wim.create_connectivity_service(WIM_SERVICE_TYPE, WIM_SERVICE_CONNECTION_POINTS)
    osm_wim.get_connectivity_service_status(service_uuid)

    # Ensure slices and services are created
    response = context_client.ListSlices(ADMIN_CONTEXT_ID)
    LOGGER.info('Slices[{:d}] = {:s}'.format(len(response.slices), grpc_message_to_json_string(response)))
    assert len(response.slices) == 1 # OSM slice

    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.info('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
    assert len(response.services) == 2 # 1xL3NM + 1xTAPI

    for service in response.services:
        service_id = service.service_id
        response = context_client.ListConnections(service_id)
        LOGGER.info('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
            grpc_message_to_json_string(service_id), len(response.connections), grpc_message_to_json_string(response)))

        if service.service_type == ServiceTypeEnum.SERVICETYPE_L3NM:
            assert len(response.connections) == 1 # 1 connection per service
        elif service.service_type == ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE:
            assert len(response.connections) == 1 # 1 connection per service
        else:
            str_service = grpc_message_to_json_string(service)
            raise Exception('Unexpected ServiceType: {:s}'.format(str_service))


def test_scenario_kpi_values_created(
    monitoring_client: MonitoringClient,    # pylint: disable=redefined-outer-name
) -> None:
    """
    This test validates that KPI values have been inserted into the monitoring database.
    We short k KPI descriptors to test.
    """
    response = monitoring_client.GetKpiDescriptorList(Empty())
    assert len(response.kpi_descriptor_list) >= 2
    kpi_descriptors = random.choices(response.kpi_descriptor_list, k=2)

    for kpi_descriptor in kpi_descriptors:
        MSG = 'KPI(kpi_uuid={:s}, device_uuid={:s}, endpoint_uuid={:s}, service_uuid={:s}, kpi_sample_type={:s})...'
        LOGGER.info(MSG.format(
            str(kpi_descriptor.kpi_id.kpi_id.uuid), str(kpi_descriptor.device_id.device_uuid.uuid),
            str(kpi_descriptor.endpoint_id.endpoint_uuid.uuid), str(kpi_descriptor.service_id.service_uuid.uuid),
            str(KpiSampleType.Name(kpi_descriptor.kpi_sample_type))))
        response = monitoring_client.GetInstantKpi(kpi_descriptor.kpi_id)
        kpi_uuid = response.kpi_id.kpi_id.uuid
        assert kpi_uuid == kpi_descriptor.kpi_id.kpi_id.uuid
        kpi_value_type = response.kpi_value.WhichOneof('value')
        if kpi_value_type is None:
            MSG = '  KPI({:s}): No instant value found'
            LOGGER.warning(MSG.format(str(kpi_uuid)))
        else:
            kpi_timestamp = response.timestamp.timestamp
            assert kpi_timestamp > 0
            assert kpi_value_type == 'floatVal'
            kpi_value = getattr(response.kpi_value, kpi_value_type)
            MSG = '  KPI({:s}): timestamp={:s} value_type={:s} value={:s}'
            LOGGER.info(MSG.format(str(kpi_uuid), str(kpi_timestamp), str(kpi_value_type), str(kpi_value)))
