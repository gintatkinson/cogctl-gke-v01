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

import logging, pytest
from typing import Dict, List, Tuple
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import EndPointId
from common.proto.pathcomp_pb2 import PathCompRequest
from common.tools.context_queries.Device import get_device
from common.tools.context_queries.InterDomain import get_device_to_domain_map, get_local_device_uuids
from common.tools.grpc.Tools import grpc_message_list_to_json, grpc_message_list_to_json_string, grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from pathcomp.frontend.client.PathCompClient import PathCompClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture(scope='session')
def context_client():
    _client = ContextClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def pathcomp_client():
    _client = PathCompClient()
    yield _client
    _client.close()

def test_interdomain_topology_abstractor(
    context_client  : ContextClient,    # pylint: disable=redefined-outer-name
    pathcomp_client : PathCompClient,   # pylint: disable=redefined-outer-name
) -> None:

    pathcomp_req = PathCompRequest(**{
        "services": [
            {"name": "", "service_constraints": [{"sla_capacity": {"capacity_gbps": 10.0}}, {"sla_latency": {"e2e_latency_ms": 100.0}}], "service_endpoint_ids": [
                {"device_id": {"device_uuid": {"uuid": "cda90d2f-e7b0-5837-8f2e-2fb29dd9b367"}}, "endpoint_uuid": {"uuid": "37ab67ef-0064-54e3-ae9b-d40100953834"}, "topology_id": {"context_id": {"context_uuid": {"uuid": "43813baf-195e-5da6-af20-b3d0922e71a7"}}, "topology_uuid": {"uuid": "c76135e3-24a8-5e92-9bed-c3c9139359c8"}}},
                {"device_id": {"device_uuid": {"uuid": "800d5bd4-a7a3-5a66-82ab-d399767ca3d8"}}, "endpoint_uuid": {"uuid": "97f57787-cfec-5315-9718-7e850905f11a"}, "topology_id": {"context_id": {"context_uuid": {"uuid": "43813baf-195e-5da6-af20-b3d0922e71a7"}}, "topology_uuid": {"uuid": "c76135e3-24a8-5e92-9bed-c3c9139359c8"}}}
            ], "service_id": {"context_id": {"context_uuid": {"uuid": "43813baf-195e-5da6-af20-b3d0922e71a7"}}, "service_uuid": {"uuid": "77277b43-f9cd-5e01-a3e7-6c5fa4577137"}}, "service_type": "SERVICETYPE_L2NM"}
        ],
        "shortest_path": {}
    })
    pathcomp_req_svc = pathcomp_req.services[0]

    pathcomp_rep = pathcomp_client.Compute(pathcomp_req)
    LOGGER.warning('pathcomp_rep = {:s}'.format(grpc_message_to_json_string(pathcomp_rep)))

    num_services = len(pathcomp_rep.services)
    if num_services == 0:
        raise Exception('No services received : {:s}'.format(grpc_message_to_json_string(pathcomp_rep)))

    num_connections = len(pathcomp_rep.connections)
    if num_connections == 0:
        raise Exception('No connections received : {:s}'.format(grpc_message_to_json_string(pathcomp_rep)))

    local_device_uuids = get_local_device_uuids(context_client)
    LOGGER.warning('local_device_uuids={:s}'.format(str(local_device_uuids)))

    device_to_domain_map = get_device_to_domain_map(context_client)
    LOGGER.warning('device_to_domain_map={:s}'.format(str(device_to_domain_map)))

    local_slices  : List[List[EndPointId]] = list()
    remote_slices : List[List[EndPointId]] = list()
    req_service_uuid = pathcomp_req_svc.service_id.service_uuid.uuid
    for service in pathcomp_rep.services:
        service_uuid = service.service_id.service_uuid.uuid
        if service_uuid == req_service_uuid: continue # main synthetic service; we don't care
        device_uuids = {
            endpoint_id.device_id.device_uuid.uuid
            for endpoint_id in service.service_endpoint_ids
        }
        local_domain_uuids = set()
        remote_domain_uuids = set()
        for device_uuid in device_uuids:
            if device_uuid in local_device_uuids:
                domain_uuid = device_to_domain_map.get(device_uuid)
                if domain_uuid is None:
                    raise Exception('Unable to map device({:s}) to a domain'.format(str(device_uuid)))
                local_domain_uuids.add(domain_uuid)
            else:
                device = get_device(
                    context_client, device_uuid, include_endpoints=True, include_config_rules=False,
                    include_components=False)
                if device is None: raise Exception('Device({:s}) not found'.format(str(device_uuid)))
                device_type = DeviceTypeEnum._value2member_map_.get(device.device_type)
                is_remote = device_type == DeviceTypeEnum.NETWORK
                if not is_remote:
                    MSG = 'Weird device({:s}) is not local and not network'
                    raise Exception(MSG.format(grpc_message_to_json_string(device)))
                remote_domain_uuids.add(device_uuid)
        is_local = len(local_domain_uuids) > 0
        is_remote = len(remote_domain_uuids) > 0
        if is_local == is_remote:
            MSG = 'Weird service combines local and remote devices: {:s}'
            raise Exception(MSG.format(grpc_message_to_json_string(service)))
        elif is_local:
            local_slices.append(service.service_endpoint_ids)
        else:
            remote_slices.append(service.service_endpoint_ids)

    str_local_slices = [grpc_message_list_to_json(endpoint_ids) for endpoint_ids in local_slices]
    LOGGER.warning('local_slices={:s}'.format(str(str_local_slices)))

    str_remote_slices = [grpc_message_list_to_json(endpoint_ids) for endpoint_ids in remote_slices]
    LOGGER.warning('remote_slices={:s}'.format(str(str_remote_slices)))

    raise Exception()
