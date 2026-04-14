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
from typing import Any, Dict, Iterable, List, Set, Tuple
from ._Collector import _Collector
from .Exceptions import (
    UnsatisfiedFilterException, UnsupportedDriverClassException, UnsupportedFilterFieldException,
    UnsupportedFilterFieldValueException)
from .FilterFields import FILTER_FIELD_ALLOWED_VALUES, FilterFieldEnum

LOGGER = logging.getLogger(__name__)

class DriverFactory:
    def __init__(self, drivers : List[Tuple[type, List[Dict[FilterFieldEnum, Any]]]]) -> None:
        self.__indices : Dict[str, Dict[str, Set[_Collector]]] = {} # Dict{field_name => Dict{field_value => Set{Driver}}}

        for driver_class,filter_field_sets in drivers:
            for filter_fields in filter_field_sets:
                filter_fields = {k.value:v for k,v in filter_fields.items()}
                self.register_driver_class(driver_class, **filter_fields)

    def register_driver_class(self, driver_class, **filter_fields):
        if not issubclass(driver_class, _Collector): raise UnsupportedDriverClassException(str(driver_class))

        driver_name = driver_class.__name__
        supported_filter_fields = set(FILTER_FIELD_ALLOWED_VALUES.keys())
        unsupported_filter_fields = set(filter_fields.keys()).difference(supported_filter_fields)
        if len(unsupported_filter_fields) > 0:
            raise UnsupportedFilterFieldException(unsupported_filter_fields, driver_class_name=driver_name)

        for field_name, field_values in filter_fields.items():
            field_indice = self.__indices.setdefault(field_name, dict())
            field_enum_values = FILTER_FIELD_ALLOWED_VALUES.get(field_name)
            if not isinstance(field_values, Iterable) or isinstance(field_values, str):
                field_values = [field_values]
            for field_value in field_values:
                if isinstance(field_value, Enum): field_value = field_value.value
                if field_enum_values is not None and field_value not in field_enum_values:
                    raise UnsupportedFilterFieldValueException(
                        field_name, field_value, field_enum_values, driver_class_name=driver_name)
                field_indice_drivers = field_indice.setdefault(field_value, set())
                field_indice_drivers.add(driver_class)

    def get_driver_class(self, **filter_fields) -> _Collector:
        supported_filter_fields = set(FILTER_FIELD_ALLOWED_VALUES.keys())
        unsupported_filter_fields = set(filter_fields.keys()).difference(supported_filter_fields)
        if len(unsupported_filter_fields) > 0: raise UnsupportedFilterFieldException(unsupported_filter_fields)

        candidate_driver_classes : Dict[_Collector, int] = None # number of filter hits per driver
        for field_name, field_values in filter_fields.items():
            field_indice = self.__indices.get(field_name)
            if field_indice is None: continue
            field_enum_values = FILTER_FIELD_ALLOWED_VALUES.get(field_name)
            if not isinstance(field_values, Iterable) or isinstance(field_values, str):
                field_values = [field_values]

            field_candidate_driver_classes = set()
            for field_value in field_values:
                if field_enum_values is not None and field_value not in field_enum_values:
                    raise UnsupportedFilterFieldValueException(field_name, field_value, field_enum_values)
                field_indice_drivers = field_indice.get(field_value)
                if field_indice_drivers is None: continue
                field_candidate_driver_classes = field_candidate_driver_classes.union(field_indice_drivers)

            if candidate_driver_classes is None:
                if len(field_candidate_driver_classes) == 0: continue
                candidate_driver_classes = {k:1 for k in field_candidate_driver_classes}
            else:
                for candidate_driver_class in candidate_driver_classes:
                    if candidate_driver_class not in field_candidate_driver_classes: continue
                    candidate_driver_classes[candidate_driver_class] += 1

        if len(candidate_driver_classes) == 0: raise UnsatisfiedFilterException(filter_fields)
        candidate_driver_classes = sorted(candidate_driver_classes.items(), key=operator.itemgetter(1), reverse=True)
        return candidate_driver_classes[0][0]
