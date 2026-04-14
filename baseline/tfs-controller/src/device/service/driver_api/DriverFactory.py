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

import logging
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Type
from ._Driver import _Driver
from .Exceptions import (
    AmbiguousFilterException, EmptyFilterFieldException,
    UnsatisfiedFilterException, UnsupportedDriverClassException,
    UnsupportedFilterFieldException, UnsupportedFilterFieldValueException
)
from .FilterFields import FILTER_FIELD_ALLOWED_VALUES, FilterFieldEnum


LOGGER = logging.getLogger(__name__)

SUPPORTED_FILTER_FIELDS = set(FILTER_FIELD_ALLOWED_VALUES.keys())


def sanitize_filter_fields(
    filter_fields : Dict[FilterFieldEnum, Any], driver_name : Optional[str] = None
) -> Dict[FilterFieldEnum, Any]:
    if len(filter_fields) == 0:
        raise EmptyFilterFieldException(
            filter_fields, driver_class_name=driver_name
        )

    unsupported_filter_fields = set(filter_fields.keys()).difference(SUPPORTED_FILTER_FIELDS)
    if len(unsupported_filter_fields) > 0:
        raise UnsupportedFilterFieldException(
            unsupported_filter_fields, driver_class_name=driver_name
        )

    sanitized_filter_fields : Dict[FilterFieldEnum, Set[Any]] = dict()
    for field_name, field_values in filter_fields.items():
        field_enum_values = FILTER_FIELD_ALLOWED_VALUES.get(field_name)
        if not isinstance(field_values, Iterable) or isinstance(field_values, str):
            field_values = [field_values]
        
        sanitized_field_values : Set[Any] = set()
        for field_value in field_values:
            if isinstance(field_value, Enum): field_value = field_value.value
            if field_enum_values is not None and field_value not in field_enum_values:
                raise UnsupportedFilterFieldValueException(
                    field_name, field_value, field_enum_values,
                    driver_class_name=driver_name
                )
            sanitized_field_values.add(field_value)
        
        if len(sanitized_field_values) == 0: continue # do not add empty filters
        sanitized_filter_fields[field_name] = sanitized_field_values
    
    return sanitized_filter_fields


class DriverFactory:
    def __init__(
        self, drivers : List[Tuple[Type[_Driver], List[Dict[FilterFieldEnum, Any]]]]
    ) -> None:
        self.__drivers : List[Tuple[Type[_Driver], Dict[FilterFieldEnum, Any]]] = list()

        for driver_class,filter_field_sets in drivers:
            #if not issubclass(driver_class, _Driver):
            #    raise UnsupportedDriverClassException(str(driver_class))
            driver_name = driver_class #.__name__

            for filter_fields in filter_field_sets:
                filter_fields = {k.value:v for k,v in filter_fields.items()}
                filter_fields = sanitize_filter_fields(
                    filter_fields, driver_name=driver_name
                )
                self.__drivers.append((driver_class, filter_fields))


    def is_driver_compatible(
        self, driver_filter_fields : Dict[FilterFieldEnum, Any],
        selection_filter_fields  : Dict[FilterFieldEnum, Any]
    ) -> bool:
        # by construction empty driver_filter_fields are not allowed
        # by construction empty selection_filter_fields are not allowed
        for filter_field in SUPPORTED_FILTER_FIELDS:
            driver_values = set(driver_filter_fields.get(filter_field, set()))
            if driver_values is None  : continue # means driver does not restrict
            if len(driver_values) == 0: continue # means driver does not restrict

            selection_values = set(selection_filter_fields.get(filter_field, set()))
            is_field_compatible = selection_values.issubset(driver_values)
            if not is_field_compatible: return False

        return True


    def get_driver_class(self, **selection_filter_fields) -> _Driver:
        sanitized_filter_fields = sanitize_filter_fields(selection_filter_fields)

        compatible_drivers : List[Tuple[Type[_Driver], Dict[FilterFieldEnum, Any]]] = [
            driver_class
            for driver_class,driver_filter_fields in self.__drivers
            if self.is_driver_compatible(driver_filter_fields, sanitized_filter_fields)
        ]

        MSG = '[get_driver_class] compatible_drivers={:s}'
        LOGGER.debug(MSG.format(str(compatible_drivers)))

        num_compatible = len(compatible_drivers)
        if num_compatible == 0: 
            raise UnsatisfiedFilterException(selection_filter_fields)
        if num_compatible > 1:
            raise AmbiguousFilterException(selection_filter_fields, compatible_drivers)
        return compatible_drivers[0]
