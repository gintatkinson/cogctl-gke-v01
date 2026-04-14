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

import random, uuid
from typing import Dict, List, Optional, Set
from common.proto.context_pb2 import (
    Device, EndPoint, Link, Service, ServiceStatusEnum, ServiceTypeEnum, Slice, SliceStatusEnum
)
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.tools.object_factory.Constraint import json_constraint_custom
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import (
    DEVICE_DISABLED, DEVICE_EMU_DRIVERS, DEVICE_EMUPR_TYPE, json_device, json_device_id
)
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_id
from common.tools.object_factory.Link import json_link
from common.tools.object_factory.Service import json_service
from common.tools.object_factory.Slice import json_slice
from common.tools.object_factory.Topology import json_topology_id
from .Settings import (
    CONFIG_RULES_MIN_ENTRIES, CONFIG_RULES_MAX_ENTRIES, CONSTRAINTS_MIN_ENTRIES, CONSTRAINTS_MAX_ENTRIES,
    DEVICE_MAX_ENDPOINTS, DEVICE_MIN_ENDPOINTS, DICT_MAX_ENTRIES, DICT_MIN_ENTRIES, PATH_MAX_PARTS, PATH_MIN_PARTS,
    SLICE_MAX_SUBSERVICES, SLICE_MAX_SUBSLICES, SLICE_MIN_SUBSERVICES, SLICE_MIN_SUBSLICES,
    WORD_ALPHABET, WORD_MAX_LENGTH, WORD_MIN_LENGTH,
)

def random_word(length : Optional[int] = None, alphabet : Optional[str] = None) -> str:
    if alphabet is None: alphabet = WORD_ALPHABET
    if length is None: length = int(random.uniform(WORD_MIN_LENGTH, WORD_MAX_LENGTH))
    word = []
    remaining_length = length
    while remaining_length > 0:
        part_length = min(len(alphabet), remaining_length)
        word.extend(random.sample(alphabet, part_length))
        remaining_length = length - len(word)
    return ''.join(word)

def random_path(
    num_parts : Optional[int] = None, part_length : Optional[int] = None, alphabet : Optional[str] = None,
    separator : str = '/'
) -> str:
    if num_parts is None: num_parts = int(random.uniform(PATH_MIN_PARTS, PATH_MAX_PARTS))
    return separator.join([random_word(length=part_length, alphabet=alphabet) for _ in range(num_parts)])

def random_dict(
    num_entries : Optional[int] = None, key_length : Optional[str] = None, value_length : Optional[str] = None
) -> Dict:
    if num_entries is None: num_entries = int(random.uniform(DICT_MIN_ENTRIES, DICT_MAX_ENTRIES))
    return {random_word(length=key_length) : random_word(length=value_length) for _ in range(num_entries)}

def random_config_rule() -> Dict:
    resource_key = random_path()
    resource_value = random_dict()
    return json_config_rule_set(resource_key, resource_value)

def random_config_rules(count : Optional[int] = None) -> List:
    if count is None: count = int(random.uniform(CONFIG_RULES_MIN_ENTRIES, CONFIG_RULES_MAX_ENTRIES))
    return [random_config_rule() for _ in range(count)]

def random_constraint() -> Dict:
    constraint_type = random_path()
    constraint_value = random_dict()
    return json_constraint_custom(constraint_type, constraint_value)

def random_constraints(count : Optional[int] = None) -> List:
    if count is None: count = int(random.uniform(CONSTRAINTS_MIN_ENTRIES, CONSTRAINTS_MAX_ENTRIES))
    return [random_constraint() for _ in range(count)]

def random_endpoint(device_uuid : str) -> Dict:
    topology_id = json_topology_id(str(uuid.uuid4()), context_id=json_context_id(str(uuid.uuid4())))
    return json_endpoint(json_device_id(device_uuid), str(uuid.uuid4()), 'internal/copper', topology_id=topology_id)

def random_endpoints(device_uuid : str, count : Optional[int] = None) -> List:
    if count is None: count = int(random.uniform(DEVICE_MIN_ENDPOINTS, DEVICE_MAX_ENDPOINTS))
    return [random_endpoint(device_uuid) for _ in range(count)]

def random_endpoint_id(device_uuid : str) -> Dict:
    topology_id = json_topology_id(str(uuid.uuid4()), context_id=json_context_id(str(uuid.uuid4())))
    return json_endpoint_id(json_device_id(device_uuid), str(uuid.uuid4()), topology_id=topology_id)

def random_endpoint_ids(device_uuid : str, count : Optional[int] = None) -> List:
    if count is None: count = int(random.uniform(DEVICE_MIN_ENDPOINTS, DEVICE_MAX_ENDPOINTS))
    return [random_endpoint(device_uuid) for _ in range(count)]

def get_random_endpoint(
    devices : Dict[str, Device], excluded_device_uuids : Set[str] = set()
) -> EndPoint:
    device_uuids = set(devices.keys())
    device_uuids = list(device_uuids.difference(excluded_device_uuids))
    device_uuid = random.choice(device_uuids)
    device = devices[device_uuid]
    return random.choice(device.device_endpoints)

def get_random_endpoints(
    devices : Dict[str, Device], count : Optional[int] = None
) -> Optional[List[EndPoint]]:
    if len(devices) < count: return None # Too few devices
    endpoints = list()
    used_device_uuids = set()
    for _ in range(count):
        endpoint = get_random_endpoint(devices, used_device_uuids)
        used_device_uuids.add(endpoint.endpoint_id.device_id.device_uuid.uuid)
        endpoints.append(endpoint)
    return endpoints

def random_device(device_uuid : Optional[str] = None) -> Device:
    if device_uuid is None: device_uuid = str(uuid.uuid4())
    device_type = DEVICE_EMUPR_TYPE
    device_op_stat = DEVICE_DISABLED
    drivers = DEVICE_EMU_DRIVERS
    endpoints = random_endpoints(device_uuid)
    config_rules = random_config_rules()
    return Device(**json_device(
        device_uuid, device_type, device_op_stat, endpoints=endpoints, config_rules=config_rules, drivers=drivers
    ))

def random_link(
    devices : Dict[str, Device], link_uuid : Optional[str] = None
) -> Optional[Link]:
    if link_uuid is None: link_uuid = str(uuid.uuid4())
    endpoints = get_random_endpoints(devices, count=2)
    if endpoints is None: return None
    endpoint_ids = [grpc_message_to_json(endpoint.endpoint_id) for endpoint in endpoints]
    return Link(**json_link(link_uuid, endpoint_ids))

def random_service(
    devices : Dict[str, Device], service_uuid : Optional[str] = None
) -> Optional[Service]:
    if service_uuid is None: service_uuid = str(uuid.uuid4())
    context_id = json_context_id(str(uuid.uuid4()))
    service_type = ServiceTypeEnum.SERVICETYPE_L2NM
    service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED
    endpoints = get_random_endpoints(devices, count=2)
    if endpoints is None: return None
    endpoint_ids = [grpc_message_to_json(endpoint.endpoint_id) for endpoint in endpoints]
    constraints = random_constraints(count=3)
    config_rules = random_config_rules(count=5)
    return Service(**json_service(
        service_uuid, service_type, context_id=context_id, status=service_status,
        endpoint_ids=endpoint_ids, constraints=constraints, config_rules=config_rules))

def random_slice(
    devices : Dict[str, Device], services : Dict[str, Service], slices : Dict[str, Service],
    slice_uuid : Optional[str] = None
) -> Optional[Slice]:
    if slice_uuid is None: slice_uuid = str(uuid.uuid4())
    context_id = json_context_id(str(uuid.uuid4()))
    slice_status = SliceStatusEnum.SLICESTATUS_PLANNED
    endpoints = get_random_endpoints(devices, count=2)
    if endpoints is None: return None
    endpoint_ids = [grpc_message_to_json(endpoint.endpoint_id) for endpoint in endpoints]
    constraints = random_constraints(count=3)
    config_rules = random_config_rules(count=5)

    num_sub_services = int(random.uniform(SLICE_MIN_SUBSERVICES, SLICE_MAX_SUBSERVICES))
    num_sub_services = min(num_sub_services, len(services))
    sub_services = random.sample(list(services.values()), num_sub_services) if num_sub_services > 0 else []
    sub_service_ids = [grpc_message_to_json(sub_service.service_id) for sub_service in sub_services]

    num_sub_slices = int(random.uniform(SLICE_MIN_SUBSLICES, SLICE_MAX_SUBSLICES))
    num_sub_slices = min(num_sub_slices, len(slices))
    sub_slices = random.sample(list(slices.values()), num_sub_slices) if num_sub_slices > 0 else []
    sub_slice_ids = [grpc_message_to_json(sub_slice.slice_id) for sub_slice in sub_slices]

    owner = {'owner_uuid': {'uuid': str(uuid.uuid4())}, 'owner_string': random_word()}

    return Slice(**json_slice(
        slice_uuid, context_id=context_id, status=slice_status,
        endpoint_ids=endpoint_ids, constraints=constraints, config_rules=config_rules,
        service_ids=sub_service_ids, subslice_ids=sub_slice_ids, owner=owner))
