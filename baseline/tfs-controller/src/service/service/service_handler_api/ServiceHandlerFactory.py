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

import logging, operator
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Set, Tuple
from common.proto.context_pb2 import Device, DeviceDriverEnum, Service
from common.tools.grpc.Tools import grpc_message_to_json_string
from .Exceptions import (
    UnsatisfiedFilterException, UnsupportedServiceHandlerClassException, UnsupportedFilterFieldException,
    UnsupportedFilterFieldValueException)
from .FilterFields import FILTER_FIELD_ALLOWED_VALUES, FilterFieldEnum

if TYPE_CHECKING:
    from service.service.service_handler_api._ServiceHandler import _ServiceHandler

LOGGER = logging.getLogger(__name__)

class ServiceHandlerFactory:
    def __init__(self, service_handlers : List[Tuple[type, List[Dict[FilterFieldEnum, Any]]]]) -> None:
        # Dict{field_name => Dict{field_value => Set{ServiceHandler}}}
        self.__indices : Dict[str, Dict[str, Set['_ServiceHandler']]] = {}

        for service_handler_class,filter_field_sets in service_handlers:
            for filter_fields in filter_field_sets:
                filter_fields = {k.value:v for k,v in filter_fields.items()}
                self.register_service_handler_class(service_handler_class, **filter_fields)

    def register_service_handler_class(self, service_handler_class, **filter_fields):
        from service.service.service_handler_api._ServiceHandler import _ServiceHandler
        if not issubclass(service_handler_class, _ServiceHandler):
            raise UnsupportedServiceHandlerClassException(str(service_handler_class))

        service_handler_name = service_handler_class.__name__
        supported_filter_fields = set(FILTER_FIELD_ALLOWED_VALUES.keys())
        unsupported_filter_fields = set(filter_fields.keys()).difference(supported_filter_fields)
        if len(unsupported_filter_fields) > 0:
            raise UnsupportedFilterFieldException(
                unsupported_filter_fields, service_handler_class_name=service_handler_name)

        for field_name, field_values in filter_fields.items():
            field_indice = self.__indices.setdefault(field_name, dict())
            field_enum_values = FILTER_FIELD_ALLOWED_VALUES.get(field_name)
            if not isinstance(field_values, Iterable) or isinstance(field_values, str):
                field_values = [field_values]
            for field_value in field_values:
                if isinstance(field_value, Enum): field_value = field_value.value
                if field_enum_values is not None and field_value not in field_enum_values:
                    raise UnsupportedFilterFieldValueException(
                        field_name, field_value, field_enum_values, service_handler_class_name=service_handler_name)
                field_indice_service_handlers = field_indice.setdefault(field_value, set())
                field_indice_service_handlers.add(service_handler_class)

    def get_service_handler_class(self, **filter_fields) -> '_ServiceHandler':
        supported_filter_fields = set(FILTER_FIELD_ALLOWED_VALUES.keys())
        unsupported_filter_fields = set(filter_fields.keys()).difference(supported_filter_fields)
        if len(unsupported_filter_fields) > 0: raise UnsupportedFilterFieldException(unsupported_filter_fields)

        candidate_service_handler_classes : Dict['_ServiceHandler', int] = None # num. filter hits per service_handler
        for field_name, field_values in filter_fields.items():
            field_indice = self.__indices.get(field_name)
            if field_indice is None: continue
            if not isinstance(field_values, Iterable) or isinstance(field_values, str):
                field_values = [field_values]
            if len(field_values) == 0:
                # do not allow empty fields; might cause wrong selection
                raise UnsatisfiedFilterException(filter_fields)

            field_enum_values = FILTER_FIELD_ALLOWED_VALUES.get(field_name)

            field_candidate_service_handler_classes = set()
            for field_value in field_values:
                if field_enum_values is not None and field_value not in field_enum_values:
                    raise UnsupportedFilterFieldValueException(field_name, field_value, field_enum_values)
                field_indice_service_handlers = field_indice.get(field_value)
                if field_indice_service_handlers is None: continue
                field_candidate_service_handler_classes = field_candidate_service_handler_classes.union(
                    field_indice_service_handlers)

            if candidate_service_handler_classes is None:
                candidate_service_handler_classes = {k:1 for k in field_candidate_service_handler_classes}
            else:
                for candidate_service_handler_class in candidate_service_handler_classes:
                    if candidate_service_handler_class not in field_candidate_service_handler_classes: continue
                    candidate_service_handler_classes[candidate_service_handler_class] += 1

        if len(candidate_service_handler_classes) == 0: raise UnsatisfiedFilterException(filter_fields)
        candidate_service_handler_classes = sorted(
            candidate_service_handler_classes.items(), key=operator.itemgetter(1), reverse=True)
        return candidate_service_handler_classes[0][0]

def get_common_device_drivers(drivers_per_device : List[Set[int]]) -> Set[int]:
    common_device_drivers = None
    for device_drivers in drivers_per_device:
        if common_device_drivers is None:
            common_device_drivers = set(device_drivers)
        else:
            common_device_drivers.intersection_update(device_drivers)
    if common_device_drivers is None: common_device_drivers = set()
    return common_device_drivers

def get_service_handler_class(
    service_handler_factory : ServiceHandlerFactory, service : Service,
    device_and_drivers: Dict[str, Tuple[Device, Set[int]]]
) -> Optional['_ServiceHandler']:
    str_service_key = grpc_message_to_json_string(service.service_id)
    # Checks if the service is of type ipowdm
    if 'ipowdm' in str(service.service_config.config_rules):
        common_device_drivers = [DeviceDriverEnum.DEVICEDRIVER_IETF_L3VPN]
    # Checks if the service is of type tapi_lsp
    elif 'tapi_lsp' in str(service.service_config.config_rules):
        common_device_drivers = [DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API]
    else:
        common_device_drivers = get_common_device_drivers([
            device_drivers
            for _,device_drivers in device_and_drivers.values()
        ])
    LOGGER.debug('common_device_drivers={:s}'.format(str(common_device_drivers)))

    filter_fields = {
        FilterFieldEnum.SERVICE_TYPE.value  : service.service_type,     # must be supported
        FilterFieldEnum.DEVICE_DRIVER.value : common_device_drivers,    # at least one must be supported
    }

    MSG = 'Selecting service handler for service({:s}) with filter_fields({:s})...'
    LOGGER.info(MSG.format(str(str_service_key), str(filter_fields)))
    service_handler_class = service_handler_factory.get_service_handler_class(**filter_fields)
    MSG = 'ServiceHandler({:s}) selected for service({:s}) with filter_fields({:s})...'
    LOGGER.info(MSG.format(str(service_handler_class.__name__), str(str_service_key), str(filter_fields)))
    return service_handler_class
