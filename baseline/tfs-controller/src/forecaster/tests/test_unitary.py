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

import logging, pandas, pytest #, json
from typing import Dict, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import ContextId, TopologyId
from common.proto.forecaster_pb2 import ForecastLinkCapacityRequest, ForecastTopologyCapacityRequest
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.monitoring_pb2 import KpiDescriptor
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from forecaster.client.ForecasterClient import ForecasterClient
from forecaster.tests.Tools import compose_descriptors, read_csv
from monitoring.client.MonitoringClient import MonitoringClient
from .MockService_Dependencies import MockService_Dependencies
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    mock_service, forecaster_service, context_client, monitoring_client, forecaster_client)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
logging.getLogger('common.tests.InMemoryObjectDatabase').setLevel(logging.INFO)
logging.getLogger('common.tests.InMemoryTimeSeriesDatabase').setLevel(logging.INFO)
logging.getLogger('common.tests.MockServicerImpl_Context').setLevel(logging.INFO)
logging.getLogger('common.tests.MockServicerImpl_Monitoring').setLevel(logging.INFO)
logging.getLogger('context.client.ContextClient').setLevel(logging.INFO)
logging.getLogger('monitoring.client.MonitoringClient').setLevel(logging.INFO)

JSON_ADMIN_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
ADMIN_CONTEXT_ID = ContextId(**JSON_ADMIN_CONTEXT_ID)
ADMIN_TOPOLOGY_ID = TopologyId(**json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=JSON_ADMIN_CONTEXT_ID))

CSV_DATA_FILE = 'forecaster/tests/data/dataset.csv'
#DESC_DATS_FILE = 'forecaster/tests/data/descriptor.json'

@pytest.fixture(scope='session')
def scenario() -> Tuple[pandas.DataFrame, Dict]:
    df = read_csv(CSV_DATA_FILE)
    descriptors = compose_descriptors(df)
    #with open(DESC_DATS_FILE, 'w', encoding='UTF-8') as f:
    #    f.write(json.dumps(descriptors))
    yield df, descriptors

def test_prepare_environment(
    context_client : ContextClient,             # pylint: disable=redefined-outer-name
    monitoring_client : MonitoringClient,       # pylint: disable=redefined-outer-name
    mock_service : MockService_Dependencies,    # pylint: disable=redefined-outer-name
    scenario : Tuple[pandas.DataFrame, Dict]    # pylint: disable=redefined-outer-name
) -> None:
    df, descriptors = scenario

    validate_empty_scenario(context_client)
    descriptor_loader = DescriptorLoader(descriptors=descriptors, context_client=context_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    descriptor_loader.validate()

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    for link in descriptors['links']:
        link_uuid = link['link_id']['link_uuid']['uuid']
        kpi_descriptor = KpiDescriptor()
        kpi_descriptor.kpi_id.kpi_id.uuid     = link_uuid   # pylint: disable=no-member
        kpi_descriptor.kpi_description        = 'Used Capacity in Link: {:s}'.format(link_uuid)
        kpi_descriptor.kpi_sample_type        = KpiSampleType.KPISAMPLETYPE_LINK_USED_CAPACITY_GBPS
        kpi_descriptor.link_id.link_uuid.uuid = link_uuid   # pylint: disable=no-member
        monitoring_client.SetKpi(kpi_descriptor)

    mock_service.monitoring_servicer.ts_db._data = df.rename(columns={
        'link_id': 'kpi_uuid',
        'used_capacity_gbps': 'value'
    })

def test_forecast_link(
    context_client : ContextClient,
    forecaster_client : ForecasterClient,
):  # pylint: disable=redefined-outer-name
    topology = context_client.GetTopology(ADMIN_TOPOLOGY_ID)
    link_id = topology.link_ids[0]
    forecast_request = ForecastLinkCapacityRequest()
    forecast_request.link_id.CopyFrom(link_id)                  # pylint: disable=no-member
    forecast_request.forecast_window_seconds = 10 * 24 * 60 * 60 # 10 days in seconds
    forecast_reply = forecaster_client.ForecastLinkCapacity(forecast_request)
    assert forecast_reply.link_id == link_id
    assert forecast_reply.total_capacity_gbps >= forecast_reply.current_used_capacity_gbps
    # TODO: validate forecasted values; might be increasing or decreasing

def test_forecast_topology(
    context_client : ContextClient,
    forecaster_client : ForecasterClient,
):  # pylint: disable=redefined-outer-name
    forecast_request = ForecastTopologyCapacityRequest()
    forecast_request.topology_id.CopyFrom(ADMIN_TOPOLOGY_ID)    # pylint: disable=no-member
    forecast_request.forecast_window_seconds = 10 * 24 * 60 * 60 # 10 days in seconds
    forecast_reply = forecaster_client.ForecastTopologyCapacity(forecast_request)

    topology = context_client.GetTopology(ADMIN_TOPOLOGY_ID)
    assert len(forecast_reply.link_capacities) == len(topology.link_ids)
    reply_link_uuid__to__link_capacity = {
        link_capacity.link_id.link_uuid.uuid : link_capacity
        for link_capacity in forecast_reply.link_capacities
    }
    for link_id in topology.link_ids:
        link_uuid = link_id.link_uuid.uuid
        assert link_uuid in reply_link_uuid__to__link_capacity
        link_capacity_forecast = reply_link_uuid__to__link_capacity[link_uuid]
        assert link_capacity_forecast.link_id == link_id
        assert link_capacity_forecast.total_capacity_gbps >= link_capacity_forecast.current_used_capacity_gbps
        # TODO: validate forecasted values; might be increasing or decreasing

def test_cleanup_environment(
    context_client : ContextClient,             # pylint: disable=redefined-outer-name
    scenario : Tuple[pandas.DataFrame, Dict]    # pylint: disable=redefined-outer-name
) -> None:
    _, descriptors = scenario

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(descriptors=descriptors, context_client=context_client)
    descriptor_loader.validate()
    descriptor_loader.unload()
    validate_empty_scenario(context_client)
