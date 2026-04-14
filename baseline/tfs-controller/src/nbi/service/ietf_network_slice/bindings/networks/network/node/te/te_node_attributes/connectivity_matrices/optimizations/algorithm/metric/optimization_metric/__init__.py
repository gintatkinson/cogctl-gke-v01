# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, Final, Iterator, List, Tuple

from .. import (
    YANGChoice, YANGChoiceCase, YANGContainer, YANGContainerMember,
    YANGLeafMember, YANGListItem, YANGListMember)


class OptimizationMetricMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: optimization-metric
    """
    from .explicit_route_exclude_objects import ExplicitRouteExcludeObjects
    from .explicit_route_include_objects import ExplicitRouteIncludeObjects

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: optimization-metric
        """

        def __init__(self):
            super().__init__(OptimizationMetric)

        def __get__(self, instance, owner=None) -> (
                'OptimizationMetricMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['OptimizationMetric']:
            pass

        def __iter__(self, key) -> Iterator['OptimizationMetric']:
            return super().__iter__()

        def __getitem__(self, key) -> 'OptimizationMetric':
            return super()[key]

        def __enter__(self) -> (
                'OptimizationMetricMeta.yang_list_descriptor'):
            pass


class OptimizationMetric(
        YANGListItem,
        metaclass=OptimizationMetricMeta):
    """
    YANG list item handler.

    YANG name: optimization-metric
    """

    _yang_name: Final[str] = 'optimization-metric'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'metric-type',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'weight': (
            weight := YANGLeafMember(
                'weight',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'metric-type': (
            metric_type := YANGLeafMember(
                'metric-type',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'explicit-route-exclude-objects': (
            explicit_route_exclude_objects := (  # YANGContainerMember(
                OptimizationMetricMeta.
                ExplicitRouteExcludeObjects.
                yang_container_descriptor())),

        'explicit-route-include-objects': (
            explicit_route_include_objects := (  # YANGContainerMember(
                OptimizationMetricMeta.
                ExplicitRouteIncludeObjects.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'OptimizationMetric':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
