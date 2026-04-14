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

import logging, operator, random
from typing import Dict, Tuple
from common.proto.context_pb2 import Device, Link, Service, Slice
from dlt.connector.client.DltGatewayClient import DltGatewayClient
from .Enums import ActionEnum, RecordTypeEnum
from .Dlt import (
    DLT_OPERATION_CREATE, DLT_OPERATION_DELETE, DLT_OPERATION_UPDATE,
    DLT_RECORD_TYPE_DEVICE, DLT_RECORD_TYPE_LINK, DLT_RECORD_TYPE_SERVICE, DLT_RECORD_TYPE_SLICE,
    dlt_record_get, dlt_record_set)
from .PerfData import PerfData
from .Random import random_device, random_link, random_service, random_slice

LOGGER = logging.getLogger(__name__)

class PlayGround:
    def __init__(self, dltgateway_client : DltGatewayClient, domain_uuid : str) -> None:
        self._dltgateway_client = dltgateway_client
        self._domain_uuid = domain_uuid
        self._perf_data = PerfData()
        self._devices  : Dict[str, Device ] = dict()
        self._links    : Dict[str, Link   ] = dict()
        self._services : Dict[str, Service] = dict()
        self._slices   : Dict[str, Slice  ] = dict()

    @property
    def perf_data(self): return self._perf_data

    def _choose_operation(self) -> Tuple[ActionEnum, RecordTypeEnum]:
        operations = self._perf_data.operation_counters
        if len(operations) == 0:
            action = random.choice(list(ActionEnum.__members__.values()))
            record_type = random.choice(list(RecordTypeEnum.__members__.values()))
            return action, record_type

        operations = sorted(operations.items(), key=operator.itemgetter(1))
        min_executions = operations[0][1]
        max_executions = operations[-1][1]
        bound = (max_executions + min_executions) / 2 # enable randomness, but try to keep some level of balance
        operations = list(filter(lambda t: t[1] <= bound, operations))
        if len(operations) == 0:
            action = random.choice(list(ActionEnum.__members__.values()))
            record_type = random.choice(list(RecordTypeEnum.__members__.values()))
            return action, record_type

        (action, record_type),_ = random.choice(operations)
        return action, record_type

    def run_random_operation(self) -> bool:
        method = None
        while method is None:
            action, record_type = self._choose_operation()
            method_name = '{:s}_{:s}'.format(action.value, record_type.value)
            method = getattr(self, method_name, None)
        return method()

    def create_device(self) -> bool:
        device = random_device()
        if device is None: return False
        device_uuid = device.device_id.device_uuid.uuid # pylint: disable=no-member
        self._devices[device_uuid] = device
        perf_point = self._perf_data.add_point(ActionEnum.CREATE, RecordTypeEnum.DEVICE, device_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_CREATE, self._domain_uuid, device)
        return True

    def get_device(self) -> bool:
        if len(self._devices) == 0: return False
        device_uuid = random.choice(list(self._devices.keys()))
        perf_point = self._perf_data.add_point(ActionEnum.GET, RecordTypeEnum.DEVICE, device_uuid)
        data = dlt_record_get(
            self._dltgateway_client, perf_point, self._domain_uuid, DLT_RECORD_TYPE_DEVICE, device_uuid)
        self._devices[device_uuid] = Device(**data)
        return True

    def update_device(self) -> bool:
        if len(self._devices) == 0: return False
        device_uuid = random.choice(list(self._devices.keys()))
        device = random_device(device_uuid=device_uuid)
        if device is None: return False
        perf_point = self._perf_data.add_point(ActionEnum.UPDATE, RecordTypeEnum.DEVICE, device_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_UPDATE, self._domain_uuid, device)
        self._devices[device_uuid] = device
        return True

    def delete_device(self) -> bool:
        if len(self._devices) == 0: return False
        device_uuid = random.choice(list(self._devices.keys()))
        device = self._devices.pop(device_uuid, None)
        if device is None: return False
        perf_point = self._perf_data.add_point(ActionEnum.DELETE, RecordTypeEnum.DEVICE, device_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_DELETE, self._domain_uuid, device)
        return True

    def create_link(self) -> bool:
        link = random_link(self._devices)
        if link is None: return False
        link_uuid = link.link_id.link_uuid.uuid # pylint: disable=no-member
        perf_point = self._perf_data.add_point(ActionEnum.CREATE, RecordTypeEnum.LINK, link_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_CREATE, self._domain_uuid, link)
        self._links[link_uuid] = link
        return True

    def get_link(self) -> bool:
        if len(self._links) == 0: return False
        link_uuid = random.choice(list(self._links.keys()))
        perf_point = self._perf_data.add_point(ActionEnum.GET, RecordTypeEnum.LINK, link_uuid)
        data = dlt_record_get(
            self._dltgateway_client, perf_point, self._domain_uuid, DLT_RECORD_TYPE_LINK, link_uuid)
        self._links[link_uuid] = Link(**data)
        return True

    def update_link(self) -> bool:
        if len(self._links) == 0: return False
        link_uuid = random.choice(list(self._links.keys()))
        link = random_link(self._devices, link_uuid=link_uuid)
        if link is None: return False
        perf_point = self._perf_data.add_point(ActionEnum.UPDATE, RecordTypeEnum.LINK, link_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_UPDATE, self._domain_uuid, link)
        self._links[link_uuid] = link
        return True

    def delete_link(self) -> bool:
        if len(self._links) == 0: return False
        link_uuid = random.choice(list(self._links.keys()))
        link = self._links.pop(link_uuid, None)
        if link is None: return False
        perf_point = self._perf_data.add_point(ActionEnum.DELETE, RecordTypeEnum.LINK, link_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_DELETE, self._domain_uuid, link)
        return True

    def create_service(self) -> bool:
        service = random_service(self._devices)
        if service is None: return False
        service_uuid = service.service_id.service_uuid.uuid # pylint: disable=no-member
        perf_point = self._perf_data.add_point(ActionEnum.CREATE, RecordTypeEnum.SERVICE, service_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_CREATE, self._domain_uuid, service)
        self._services[service_uuid] = service
        return True

    def get_service(self) -> bool:
        if len(self._services) == 0: return False
        service_uuid = random.choice(list(self._services.keys()))
        perf_point = self._perf_data.add_point(ActionEnum.GET, RecordTypeEnum.SERVICE, service_uuid)
        data = dlt_record_get(
            self._dltgateway_client, perf_point, self._domain_uuid, DLT_RECORD_TYPE_SERVICE, service_uuid)
        self._services[service_uuid] = Service(**data)
        return True

    def update_service(self) -> bool:
        if len(self._services) == 0: return False
        service_uuid = random.choice(list(self._services.keys()))
        service = random_service(self._devices, service_uuid=service_uuid)
        if service is None: return False
        perf_point = self._perf_data.add_point(ActionEnum.UPDATE, RecordTypeEnum.SERVICE, service_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_UPDATE, self._domain_uuid, service)
        self._services[service_uuid] = service
        return True

    def delete_service(self) -> bool:
        if len(self._services) == 0: return False
        service_uuid = random.choice(list(self._services.keys()))
        service = self._services.pop(service_uuid, None)
        if service is None: return False
        perf_point = self._perf_data.add_point(ActionEnum.DELETE, RecordTypeEnum.SERVICE, service_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_DELETE, self._domain_uuid, service)
        return True

    def create_slice(self) -> bool:
        slice_ = random_slice(self._devices, self._services, self._slices)
        if slice_ is None: return False
        slice_uuid = slice_.slice_id.slice_uuid.uuid # pylint: disable=no-member
        perf_point = self._perf_data.add_point(ActionEnum.CREATE, RecordTypeEnum.SLICE, slice_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_CREATE, self._domain_uuid, slice_)
        self._slices[slice_uuid] = slice_
        return True

    def get_slice(self) -> bool:
        if len(self._slices) == 0: return False
        slice_uuid = random.choice(list(self._slices.keys()))
        perf_point = self._perf_data.add_point(ActionEnum.GET, RecordTypeEnum.SLICE, slice_uuid)
        data = dlt_record_get(
            self._dltgateway_client, perf_point, self._domain_uuid, DLT_RECORD_TYPE_SLICE, slice_uuid)
        self._slices[slice_uuid] = Slice(**data)
        return True

    def update_slice(self) -> bool:
        if len(self._slices) == 0: return False
        slice_uuid = random.choice(list(self._slices.keys()))
        slice_ = random_slice(self._devices, self._services, self._slices, slice_uuid=slice_uuid)
        if slice_ is None: return False
        perf_point = self._perf_data.add_point(ActionEnum.UPDATE, RecordTypeEnum.SLICE, slice_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_UPDATE, self._domain_uuid, slice_)
        self._slices[slice_uuid] = slice_
        return True

    def delete_slice(self) -> bool:
        if len(self._slices) == 0: return False
        slice_uuid = random.choice(list(self._slices.keys()))
        slice_ = self._slices.pop(slice_uuid, None)
        if slice_ is None: return False
        perf_point = self._perf_data.add_point(ActionEnum.DELETE, RecordTypeEnum.SLICE, slice_uuid)
        dlt_record_set(self._dltgateway_client, perf_point, DLT_OPERATION_DELETE, self._domain_uuid, slice_)
        return True
