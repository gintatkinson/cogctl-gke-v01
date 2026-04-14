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

import logging, os, pandas, pytest
from typing import Dict, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import ContextId, TopologyId
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.monitoring_pb2 import KpiDescriptor
from common.proto.pathcomp_pb2 import PathCompRequest
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.Constraint import (
    json_constraint_schedule, json_constraint_sla_capacity, json_constraint_sla_latency)
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from common.tools.object_factory.Service import get_service_uuid, json_service_l3nm_planned
from common.tools.timestamp.Converters import timestamp_utcnow_to_float
from context.client.ContextClient import ContextClient
from forecaster.tests.Tools import compose_descriptors, read_csv
from monitoring.client.MonitoringClient import MonitoringClient
from pathcomp.frontend.client.PathCompClient import PathCompClient
from .MockService_Dependencies import MockService_Dependencies

# configure backend environment variables before overwriting them with fixtures to use real backend pathcomp
DEFAULT_PATHCOMP_BACKEND_SCHEME  = 'http'
DEFAULT_PATHCOMP_BACKEND_HOST    = '127.0.0.1'
DEFAULT_PATHCOMP_BACKEND_PORT    = '8081'
DEFAULT_PATHCOMP_BACKEND_BASEURL = '/pathComp/api/v1/compRoute'

os.environ['PATHCOMP_BACKEND_SCHEME'] = os.environ.get('PATHCOMP_BACKEND_SCHEME', DEFAULT_PATHCOMP_BACKEND_SCHEME)
os.environ['PATHCOMP_BACKEND_BASEURL'] = os.environ.get('PATHCOMP_BACKEND_BASEURL', DEFAULT_PATHCOMP_BACKEND_BASEURL)

# Find IP:port of backend container as follows:
# - first check env vars PATHCOMP_BACKEND_HOST & PATHCOMP_BACKEND_PORT
# - if not set, check env vars PATHCOMPSERVICE_SERVICE_HOST & PATHCOMPSERVICE_SERVICE_PORT_HTTP
# - if not set, use DEFAULT_PATHCOMP_BACKEND_HOST & DEFAULT_PATHCOMP_BACKEND_PORT
backend_host = DEFAULT_PATHCOMP_BACKEND_HOST
backend_host = os.environ.get('PATHCOMPSERVICE_SERVICE_HOST', backend_host)
os.environ['PATHCOMP_BACKEND_HOST'] = os.environ.get('PATHCOMP_BACKEND_HOST', backend_host)

backend_port = DEFAULT_PATHCOMP_BACKEND_PORT
backend_port = os.environ.get('PATHCOMPSERVICE_SERVICE_PORT_HTTP', backend_port)
os.environ['PATHCOMP_BACKEND_PORT'] = os.environ.get('PATHCOMP_BACKEND_PORT', backend_port)

from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    mock_service, context_client, monitoring_client,
    forecaster_service, forecaster_client, pathcomp_service, pathcomp_client)

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
    descriptors = compose_descriptors(df, num_client_endpoints=5)
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

def test_request_service_shortestpath_forecast(
    pathcomp_client : PathCompClient,               # pylint: disable=redefined-outer-name
) -> None:
    
    start_timestamp = timestamp_utcnow_to_float()
    duration_days = 1.5

    endpoint_id_a = json_endpoint_id(json_device_id('pt1.pt'), 'client:1')
    endpoint_id_z = json_endpoint_id(json_device_id('gr1.gr'), 'client:3')
    context_uuid = DEFAULT_CONTEXT_NAME
    service_uuid = get_service_uuid(endpoint_id_a, endpoint_id_z)
    request_service = json_service_l3nm_planned(
        service_uuid,
        context_uuid=context_uuid,
        endpoint_ids=[endpoint_id_a, endpoint_id_z],
        constraints=[
            json_constraint_sla_capacity(25.0),
            json_constraint_sla_latency(20.0),
            json_constraint_schedule(start_timestamp, duration_days),
        ]
    )

    pathcomp_request = PathCompRequest(services=[request_service])
    pathcomp_request.shortest_path.Clear()  # hack to select the shortest path algorithm that has no attributes

    pathcomp_reply = pathcomp_client.Compute(pathcomp_request)

    pathcomp_reply = grpc_message_to_json(pathcomp_reply)
    reply_services = pathcomp_reply['services']
    reply_connections = pathcomp_reply['connections']
    assert len(reply_services) >= 1
    reply_service_ids = {
        '{:s}/{:s}'.format(
            svc['service_id']['context_id']['context_uuid']['uuid'],
            svc['service_id']['service_uuid']['uuid']
        )
        for svc in reply_services
    }
    # Assert requested service has a reply
    # It permits having other services not requested (i.e., sub-services)
    context_service_uuid = '{:s}/{:s}'.format(context_uuid, service_uuid)
    assert context_service_uuid in reply_service_ids

    reply_connection_service_ids = {
        '{:s}/{:s}'.format(
            conn['service_id']['context_id']['context_uuid']['uuid'],
            conn['service_id']['service_uuid']['uuid']
        )
        for conn in reply_connections
    }
    # Assert requested service has a connection associated
    # It permits having other connections not requested (i.e., connections for sub-services)
    assert context_service_uuid in reply_connection_service_ids

    # TODO: implement other checks. examples:
    # - request service and reply service endpoints match
    # - request service and reply connection endpoints match
    # - reply sub-service and reply sub-connection endpoints match
    # - others?
    #for json_service,json_connection in zip(json_services, json_connections):

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
