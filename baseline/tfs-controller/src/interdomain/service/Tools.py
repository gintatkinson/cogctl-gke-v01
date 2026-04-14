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

import json, logging
from typing import List, Optional, Set
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import (
    ConfigRule, Constraint, ContextId, Empty, EndPointId, Slice, SliceStatusEnum)
from common.tools.context_queries.CheckType import device_type_is_network, endpoint_type_is_border
from common.tools.context_queries.InterDomain import get_local_device_uuids
from common.tools.grpc.ConfigRules import copy_config_rules
from common.tools.grpc.Constraints import copy_constraints
from common.tools.grpc.Tools import grpc_message_to_json, grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

def compute_slice_owner(
    context_client : ContextClient, traversed_domain_uuids : Set[str]
) -> Optional[str]:
    existing_topologies = context_client.ListTopologies(ContextId(**json_context_id(DEFAULT_CONTEXT_NAME)))
    domain_uuids_names = set()
    DISCARD_TOPOLOGY_NAMES = {DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME}
    for topology in existing_topologies.topologies:
        topology_uuid = topology.topology_id.topology_uuid.uuid
        if topology_uuid in DISCARD_TOPOLOGY_NAMES: continue
        topology_name = topology.name
        if topology_name in DISCARD_TOPOLOGY_NAMES: continue
        domain_uuids_names.add(topology_uuid)
        domain_uuids_names.add(topology_name)

    for topology in existing_topologies.topologies:
        topology_details = context_client.GetTopologyDetails(topology.topology_id)
        for device in topology_details.devices:
            if device.device_type != DeviceTypeEnum.NETWORK.value: continue
            domain_uuids_names.discard(device.device_id.device_uuid.uuid)
            domain_uuids_names.discard(device.name)

    candidate_owner_uuids = traversed_domain_uuids.intersection(domain_uuids_names)
    if len(candidate_owner_uuids) != 1:
        data = {
            'traversed_domain_uuids': [td_uuid for td_uuid in traversed_domain_uuids],
            'domain_uuids_names'    : [et_uuid for et_uuid in domain_uuids_names    ],
            'candidate_owner_uuids' : [co_uuid for co_uuid in candidate_owner_uuids ],
        }
        LOGGER.warning('Unable to identify slice owner: {:s}'.format(json.dumps(data)))
        return None

    return candidate_owner_uuids.pop()

def compose_slice(
    context_uuid : str, slice_uuid : str, endpoint_ids : List[EndPointId], slice_name : Optional[str] = None,
    constraints : List[Constraint] = [], config_rules : List[ConfigRule] = [], owner_uuid : Optional[str] = None,
    owner_string : Optional[str] = None
) -> Slice:
    slice_ = Slice()
    slice_.slice_id.context_id.context_uuid.uuid = context_uuid             # pylint: disable=no-member
    slice_.slice_id.slice_uuid.uuid = slice_uuid                            # pylint: disable=no-member
    slice_.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_PLANNED  # pylint: disable=no-member

    if slice_name is not None:
        slice_.name = slice_name

    if owner_uuid is not None:
        slice_.slice_owner.owner_uuid.uuid = owner_uuid                     # pylint: disable=no-member

    if owner_string is not None:
        slice_.slice_owner.owner_string = owner_string                      # pylint: disable=no-member

    if len(endpoint_ids) >= 2:
        slice_.slice_endpoint_ids.add().CopyFrom(endpoint_ids[0])           # pylint: disable=no-member
        slice_.slice_endpoint_ids.add().CopyFrom(endpoint_ids[-1])          # pylint: disable=no-member

    if len(constraints) > 0:
        copy_constraints(constraints, slice_.slice_constraints)             # pylint: disable=no-member

    if len(config_rules) > 0:
        copy_config_rules(config_rules, slice_.slice_config.config_rules)   # pylint: disable=no-member

    return slice_

def map_abstract_endpoints_to_real(
    context_client : ContextClient, local_domain_uuid : str, abstract_endpoint_ids : List[EndPointId]
) -> List[EndPointId]:

    local_device_uuids = get_local_device_uuids(context_client)
    all_devices = context_client.ListDevices(Empty())

    map_endpoints_to_devices = dict()
    for device in all_devices.devices:
        LOGGER.info('[map_abstract_endpoints_to_real] Checking device {:s}'.format(
            grpc_message_to_json_string(device)))

        if device_type_is_network(device.device_type):
            LOGGER.info('[map_abstract_endpoints_to_real]   Ignoring network device')
            continue
        device_uuid = device.device_id.device_uuid.uuid
        if device_uuid not in local_device_uuids:
            LOGGER.info('[map_abstract_endpoints_to_real]   Ignoring non-local device')
            continue

        for endpoint in device.device_endpoints:
            LOGGER.info('[map_abstract_endpoints_to_real]   Checking endpoint {:s}'.format(
                grpc_message_to_json_string(endpoint)))
            endpoint_id = endpoint.endpoint_id
            device_uuid = endpoint_id.device_id.device_uuid.uuid
            endpoint_uuid = endpoint_id.endpoint_uuid.uuid
            map_endpoints_to_devices[(device_uuid, endpoint_uuid)] = endpoint_id
            if endpoint_type_is_border(endpoint.endpoint_type):
                map_endpoints_to_devices[(local_domain_uuid, endpoint_uuid)] = endpoint_id

    LOGGER.info('[map_abstract_endpoints_to_real] map_endpoints_to_devices={:s}'.format(
        str({
            endpoint_tuple:grpc_message_to_json(endpoint_id)
            for endpoint_tuple,endpoint_id in map_endpoints_to_devices.items()
        })))

    # map abstract device/endpoints to real device/endpoints
    real_endpoint_ids = []
    for endpoint_id in abstract_endpoint_ids:
        LOGGER.info('[map_abstract_endpoints_to_real] Mapping endpoint_id {:s} ...'.format(
                grpc_message_to_json_string(endpoint_id)))
        device_uuid = endpoint_id.device_id.device_uuid.uuid
        endpoint_uuid = endpoint_id.endpoint_uuid.uuid
        _endpoint_id = map_endpoints_to_devices.get((device_uuid, endpoint_uuid))
        if _endpoint_id is None:
            LOGGER.warning('map_endpoints_to_devices={:s}'.format(str(map_endpoints_to_devices)))
            MSG = 'Unable to map abstract EndPoint({:s}) to real one.'
            raise Exception(MSG.format(grpc_message_to_json_string(endpoint_id)))
        
        LOGGER.info('[map_abstract_endpoints_to_real] ... to endpoint_id {:s}'.format(
                grpc_message_to_json_string(_endpoint_id)))
        real_endpoint_ids.append(_endpoint_id)

    return real_endpoint_ids
