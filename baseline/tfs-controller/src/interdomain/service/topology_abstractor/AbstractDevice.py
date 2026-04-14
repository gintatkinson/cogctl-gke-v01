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

import copy, logging
from typing import Dict, Optional
from common.Constants import DEFAULT_CONTEXT_NAME, INTERDOMAIN_TOPOLOGY_NAME
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import (
    ContextId, Device, DeviceDriverEnum, DeviceId, DeviceOperationalStatusEnum, EndPoint)
from common.tools.context_queries.CheckType import (
    device_type_is_datacenter, device_type_is_network, endpoint_type_is_border)
from common.tools.context_queries.Device import add_device_to_topology, get_existing_device_uuids
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device, json_device_id
from context.client.ContextClient import ContextClient
from context.service.database.uuids.EndPoint import endpoint_get_uuid

LOGGER = logging.getLogger(__name__)

class AbstractDevice:
    def __init__(self, device_uuid : str, device_name : str, device_type : DeviceTypeEnum):
        self.__context_client = ContextClient()
        self.__device_uuid : str = device_uuid
        self.__device_name : str = device_name
        self.__device_type : DeviceTypeEnum = device_type
        self.__device : Optional[Device] = None
        self.__device_id : Optional[DeviceId] = None

        # Dict[device_uuid, Dict[endpoint_uuid, abstract EndPoint]]
        self.__device_endpoint_to_abstract : Dict[str, Dict[str, EndPoint]] = dict()

        # Dict[endpoint_uuid, device_uuid]
        self.__abstract_endpoint_to_device : Dict[str, str] = dict()

    def to_json(self) -> Dict:
        return {
            'device_uuid' : self.__device_uuid,
            'device_name' : self.__device_name,
            'device_type' : self.__device_type,
            'device' : self.__device,
            'device_id' : self.__device_id,
            'device_endpoint_to_abstract' : self.__device_endpoint_to_abstract,
            'abstract_endpoint_to_device' : self.__abstract_endpoint_to_device,
        }

    @property
    def uuid(self) -> str: return self.__device_uuid

    @property
    def name(self) -> str: return self.__device_name

    @property
    def device_id(self) -> Optional[DeviceId]: return self.__device_id

    @property
    def device(self) -> Optional[Device]: return self.__device

    def get_endpoint(self, device_uuid : str, endpoint_uuid : str) -> Optional[EndPoint]:
        return self.__device_endpoint_to_abstract.get(device_uuid, {}).get(endpoint_uuid)

    def initialize(self) -> bool:
        if self.__device is not None: return False

        existing_device_uuids = get_existing_device_uuids(self.__context_client)
        create_abstract_device = self.__device_uuid not in existing_device_uuids

        if create_abstract_device:
            self._create_empty()
        else:
            self._load_existing()

        is_datacenter = device_type_is_datacenter(self.__device_type)
        is_network = device_type_is_network(self.__device_type)
        if is_datacenter or is_network:
            # Add abstract device to topologies [INTERDOMAIN_TOPOLOGY_NAME]
            context_id = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))
            topology_uuids = [INTERDOMAIN_TOPOLOGY_NAME]
            for topology_uuid in topology_uuids:
                add_device_to_topology(self.__context_client, context_id, topology_uuid, self.__device_uuid)

        # seems not needed; to be removed in future releases
        #if is_datacenter and create_abstract_device:
        #    dc_device = self.__context_client.GetDevice(DeviceId(**json_device_id(self.__device_uuid)))
        #    if device_type_is_datacenter(dc_device.device_type):
        #        self.update_endpoints(dc_device)
        #elif is_network:
        #    devices_in_admin_topology = get_devices_in_topology(
        #        self.__context_client, context_id, DEFAULT_TOPOLOGY_NAME)
        #    for device in devices_in_admin_topology:
        #        if device_type_is_datacenter(device.device_type): continue
        #        self.update_endpoints(device)

        return True

    def _create_empty(self) -> None:
        device_uuid = self.__device_uuid

        device = Device(**json_device(
            device_uuid, self.__device_type.value, DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED,
            name=self.__device_name, endpoints=[], config_rules=[], drivers=[DeviceDriverEnum.DEVICEDRIVER_UNDEFINED]
        ))
        self.__context_client.SetDevice(device)
        self.__device = device
        self.__device_id = self.__device.device_id

    def _load_existing(self) -> None:
        self.__device_endpoint_to_abstract = dict()
        self.__abstract_endpoint_to_device = dict()

        self.__device_id = DeviceId(**json_device_id(self.__device_uuid))
        self.__device = self.__context_client.GetDevice(self.__device_id)
        self.__device_type = self.__device.device_type
        device_uuid = self.__device_id.device_uuid.uuid

        device_type = self.__device_type
        is_datacenter = device_type_is_datacenter(device_type)
        is_network = device_type_is_network(device_type)
        if not is_datacenter and not is_network:
            LOGGER.warning('Unsupported InterDomain Device Type: {:s}'.format(str(device_type)))
            return

        # for each endpoint in abstract device, populate internal data structures and mappings
        for interdomain_endpoint in self.__device.device_endpoints:
            endpoint_uuid : str = interdomain_endpoint.endpoint_id.endpoint_uuid.uuid

            if is_network:
                endpoint_uuid,device_uuid = endpoint_uuid.split('@', maxsplit=1)

            self.__device_endpoint_to_abstract\
                .setdefault(device_uuid, {}).setdefault(endpoint_uuid, interdomain_endpoint)
            self.__abstract_endpoint_to_device\
                .setdefault(endpoint_uuid, device_uuid)

    def _update_endpoint_name(self, device_uuid : str, endpoint_uuid : str, endpoint_name : str) -> bool:
        device_endpoint_to_abstract = self.__device_endpoint_to_abstract.get(device_uuid, {})
        interdomain_endpoint = device_endpoint_to_abstract.get(endpoint_uuid)
        interdomain_endpoint_name = interdomain_endpoint.name
        if endpoint_name == interdomain_endpoint_name: return False
        interdomain_endpoint.name = endpoint_name
        return True

    def _update_endpoint_type(self, device_uuid : str, endpoint_uuid : str, endpoint_type : str) -> bool:
        device_endpoint_to_abstract = self.__device_endpoint_to_abstract.get(device_uuid, {})
        interdomain_endpoint = device_endpoint_to_abstract.get(endpoint_uuid)
        interdomain_endpoint_type = interdomain_endpoint.endpoint_type
        if endpoint_type == interdomain_endpoint_type: return False
        interdomain_endpoint.endpoint_type = endpoint_type
        return True

    def _add_endpoint(
        self, device_uuid : str, endpoint_uuid : str, endpoint_name : str, endpoint_type : str
    ) -> EndPoint:
        interdomain_endpoint = self.__device.device_endpoints.add()
        interdomain_endpoint.endpoint_id.topology_id.topology_uuid.uuid = INTERDOMAIN_TOPOLOGY_NAME
        interdomain_endpoint.endpoint_id.topology_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
        interdomain_endpoint.endpoint_id.device_id.CopyFrom(self.__device_id)
        interdomain_endpoint.endpoint_id.endpoint_uuid.uuid = endpoint_name
        interdomain_endpoint.name = endpoint_name
        interdomain_endpoint.endpoint_type = endpoint_type

        uuids = endpoint_get_uuid(interdomain_endpoint.endpoint_id, endpoint_name=endpoint_name, allow_random=False)
        _, _, interdomain_endpoint_uuid = uuids

        self.__device_endpoint_to_abstract\
            .setdefault(device_uuid, {}).setdefault(endpoint_uuid, interdomain_endpoint)
        self.__abstract_endpoint_to_device\
            .setdefault(interdomain_endpoint_uuid, device_uuid)

        return interdomain_endpoint

    def _remove_endpoint(
        self, device_uuid : str, endpoint_uuid : str, interdomain_endpoint : EndPoint
    ) -> None:
        self.__abstract_endpoint_to_device.pop(endpoint_uuid, None)
        device_endpoint_to_abstract = self.__device_endpoint_to_abstract.get(device_uuid, {})
        device_endpoint_to_abstract.pop(endpoint_uuid, None)
        self.__device.device_endpoints.remove(interdomain_endpoint)

    def update_endpoints(self, device : Device) -> bool:
        if device_type_is_datacenter(self.__device.device_type): return False

        device_uuid = device.device_id.device_uuid.uuid
        device_border_endpoint_uuids = {
            endpoint.endpoint_id.endpoint_uuid.uuid : (endpoint.name, endpoint.endpoint_type)
            for endpoint in device.device_endpoints
            if endpoint_type_is_border(endpoint.endpoint_type)
        }

        updated = False

        # for each border endpoint in abstract device that is not in device; remove from abstract device
        device_endpoint_to_abstract = self.__device_endpoint_to_abstract.get(device_uuid, {})
        _device_endpoint_to_abstract = copy.deepcopy(device_endpoint_to_abstract)
        for endpoint_uuid, interdomain_endpoint in _device_endpoint_to_abstract.items():
            if endpoint_uuid in device_border_endpoint_uuids: continue
            # remove interdomain endpoint that is not in device
            self._remove_endpoint(device_uuid, endpoint_uuid, interdomain_endpoint)
            updated = True

        # for each border endpoint in device that is not in abstract device; add to abstract device
        for endpoint_uuid,(endpoint_name, endpoint_type) in device_border_endpoint_uuids.items():
            # if already added; just check endpoint name and type are not modified
            if endpoint_uuid in self.__abstract_endpoint_to_device:
                updated = updated or self._update_endpoint_name(device_uuid, endpoint_uuid, endpoint_name)
                updated = updated or self._update_endpoint_type(device_uuid, endpoint_uuid, endpoint_type)
                continue

            # otherwise, add it to the abstract device
            self._add_endpoint(device_uuid, endpoint_uuid, endpoint_name, endpoint_type)
            updated = True

        return updated
