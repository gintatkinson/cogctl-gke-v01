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

import copy, logging, os
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId
from common.proto.pathcomp_pb2 import PathCompRequest
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.Constraint import (
    json_constraint_custom, json_constraint_endpoint_location_region, json_constraint_endpoint_priority,
    json_constraint_sla_availability, json_constraint_sla_capacity, json_constraint_sla_latency)
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from common.tools.object_factory.Service import json_service_l3nm_planned
from context.client.ContextClient import ContextClient
from pathcomp.frontend.client.PathCompClient import PathCompClient

# Scenarios:
#from .Objects_A_B_C import CONTEXTS, DEVICES, LINKS, SERVICES, TOPOLOGIES
#from .Objects_DC_CSGW_TN import CONTEXTS, DEVICES, LINKS, SERVICES, TOPOLOGIES
from .Objects_DC_CSGW_TN_OLS import CONTEXTS, DEVICES, LINKS, SERVICES, TOPOLOGIES

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

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))
DESCRIPTORS = {
    'dummy_mode': True,
    'contexts'  : CONTEXTS,
    'topologies': TOPOLOGIES,
    'devices'   : DEVICES,
    'links'     : LINKS,
}

def test_prepare_environment(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
) -> None:
    validate_empty_scenario(context_client)

    descriptor_loader = DescriptorLoader(descriptors=DESCRIPTORS, context_client=context_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    descriptor_loader.validate()

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

def test_request_service_shortestpath(
    pathcomp_client : PathCompClient):  # pylint: disable=redefined-outer-name

    request_services = copy.deepcopy(SERVICES)
    #request_services[0]['service_constraints'] = [
    #    json_constraint_sla_capacity(1000.0),
    #    json_constraint_sla_latency(1200.0),
    #]
    pathcomp_request = PathCompRequest(services=request_services)
    pathcomp_request.shortest_path.Clear()  # hack to select the shortest path algorithm that has no attributes

    pathcomp_reply = pathcomp_client.Compute(pathcomp_request)

    pathcomp_reply = grpc_message_to_json(pathcomp_reply)
    reply_services = pathcomp_reply['services']
    reply_connections = pathcomp_reply['connections']
    assert len(request_services) <= len(reply_services)
    request_service_ids = {
        '{:s}/{:s}'.format(
            svc['service_id']['context_id']['context_uuid']['uuid'],
            svc['service_id']['service_uuid']['uuid']
        )
        for svc in request_services
    }
    reply_service_ids = {
        '{:s}/{:s}'.format(
            svc['service_id']['context_id']['context_uuid']['uuid'],
            svc['service_id']['service_uuid']['uuid']
        )
        for svc in reply_services
    }
    # Assert all requested services have a reply
    # It permits having other services not requested (i.e., sub-services)
    assert len(request_service_ids.difference(reply_service_ids)) == 0

    reply_connection_service_ids = {
        '{:s}/{:s}'.format(
            conn['service_id']['context_id']['context_uuid']['uuid'],
            conn['service_id']['service_uuid']['uuid']
        )
        for conn in reply_connections
    }
    # Assert all requested services have a connection associated
    # It permits having other connections not requested (i.e., connections for sub-services)
    assert len(request_service_ids.difference(reply_connection_service_ids)) == 0

    # TODO: implement other checks. examples:
    # - request service and reply service endpoints match
    # - request service and reply connection endpoints match
    # - reply sub-service and reply sub-connection endpoints match
    # - others?
    #for json_service,json_connection in zip(json_services, json_connections):


def test_request_service_kshortestpath(
    pathcomp_client : PathCompClient):  # pylint: disable=redefined-outer-name

    request_services = SERVICES
    pathcomp_request = PathCompRequest(services=request_services)
    pathcomp_request.k_shortest_path.k_inspection = 2   #pylint: disable=no-member
    pathcomp_request.k_shortest_path.k_return = 2       #pylint: disable=no-member

    pathcomp_reply = pathcomp_client.Compute(pathcomp_request)

    pathcomp_reply = grpc_message_to_json(pathcomp_reply)
    reply_services = pathcomp_reply['services']
    reply_connections = pathcomp_reply['connections']
    assert len(request_services) <= len(reply_services)
    request_service_ids = {
        '{:s}/{:s}'.format(
            svc['service_id']['context_id']['context_uuid']['uuid'],
            svc['service_id']['service_uuid']['uuid']
        )
        for svc in request_services
    }
    reply_service_ids = {
        '{:s}/{:s}'.format(
            svc['service_id']['context_id']['context_uuid']['uuid'],
            svc['service_id']['service_uuid']['uuid']
        )
        for svc in reply_services
    }
    # Assert all requested services have a reply
    # It permits having other services not requested (i.e., sub-services)
    assert len(request_service_ids.difference(reply_service_ids)) == 0

    reply_connection_service_ids = {
        '{:s}/{:s}'.format(
            conn['service_id']['context_id']['context_uuid']['uuid'],
            conn['service_id']['service_uuid']['uuid']
        )
        for conn in reply_connections
    }
    # Assert all requested services have a connection associated
    # It permits having other connections not requested (i.e., connections for sub-services)
    assert len(request_service_ids.difference(reply_connection_service_ids)) == 0

    # TODO: implement other checks. examples:
    # - request service and reply service endpoints match
    # - request service and reply connection endpoints match
    # - reply sub-service and reply sub-connection endpoints match
    # - others?
    #for json_service,json_connection in zip(json_services, json_connections):


def test_request_service_kdisjointpath(
    pathcomp_client : PathCompClient):  # pylint: disable=redefined-outer-name

    service_uuid = 'DC1-DC2'
    raw_endpoints = [
        ('CS1-GW1', '10/1', 'DC1', 10),
        ('CS1-GW2', '10/1', 'DC1', 20),
        ('CS2-GW1', '10/1', 'DC2', 10),
        ('CS2-GW2', '10/1', 'DC2', 20),
    ]
    
    endpoint_ids, constraints = [], [
        json_constraint_sla_capacity(10.0),
        json_constraint_sla_latency(12.0),
        json_constraint_sla_availability(2, True, 50.0),
        json_constraint_custom('diversity', {'end-to-end-diverse': 'all-other-accesses'}),
    ]

    for device_uuid, endpoint_uuid, region, priority in raw_endpoints:
        device_id = json_device_id(device_uuid)
        endpoint_id = json_endpoint_id(device_id, endpoint_uuid)
        endpoint_ids.append(endpoint_id)
        constraints.extend([
            json_constraint_endpoint_location_region(endpoint_id, region),
            json_constraint_endpoint_priority(endpoint_id, priority),
        ])

    service = json_service_l3nm_planned(service_uuid, endpoint_ids=endpoint_ids, constraints=constraints)
    request_services = [service]

    pathcomp_request = PathCompRequest(services=request_services)
    pathcomp_request.k_disjoint_path.num_disjoint = 2   #pylint: disable=no-member

    pathcomp_reply = pathcomp_client.Compute(pathcomp_request)

    pathcomp_reply = grpc_message_to_json(pathcomp_reply)
    reply_services = pathcomp_reply['services']
    reply_connections = pathcomp_reply['connections']
    assert len(request_services) <= len(reply_services)
    request_service_ids = {
        '{:s}/{:s}'.format(
            svc['service_id']['context_id']['context_uuid']['uuid'],
            svc['service_id']['service_uuid']['uuid']
        )
        for svc in request_services
    }
    reply_service_ids = {
        '{:s}/{:s}'.format(
            svc['service_id']['context_id']['context_uuid']['uuid'],
            svc['service_id']['service_uuid']['uuid']
        )
        for svc in reply_services
    }
    # Assert all requested services have a reply
    # It permits having other services not requested (i.e., sub-services)
    assert len(request_service_ids.difference(reply_service_ids)) == 0

    reply_connection_service_ids = {
        '{:s}/{:s}'.format(
            conn['service_id']['context_id']['context_uuid']['uuid'],
            conn['service_id']['service_uuid']['uuid']
        )
        for conn in reply_connections
    }
    # Assert all requested services have a connection associated
    # It permits having other connections not requested (i.e., connections for sub-services)
    assert len(request_service_ids.difference(reply_connection_service_ids)) == 0

    # TODO: implement other checks. examples:
    # - request service and reply service endpoints match
    # - request service and reply connection endpoints match
    # - reply sub-service and reply sub-connection endpoints match
    # - others?
    #for json_service,json_connection in zip(json_services, json_connections):


def test_cleanup_environment(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
) -> None:
    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(descriptors=DESCRIPTORS, context_client=context_client)
    descriptor_loader.validate()
    descriptor_loader.unload()
    validate_empty_scenario(context_client)
