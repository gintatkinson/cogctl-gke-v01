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

from typing import Dict, Final

from .. import (
    YANGChoice, YANGChoiceCase, YANGContainer, YANGContainerMember,
    YANGLeafMember, YANGListItem, YANGListMember)


class PathMetricBoundsMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: path-metric-bounds
    """
    from .path_metric_bound import PathMetricBound

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: path-metric-bounds
        """

        def __init__(self):
            super().__init__(PathMetricBounds)

        def __get__(self, instance, owner=None) -> (
                'PathMetricBoundsMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'PathMetricBounds':
            pass

        def __enter__(self) -> 'PathMetricBounds':
            pass


class PathMetricBounds(
        YANGContainer,
        metaclass=PathMetricBoundsMeta):
    """
    YANG container handler.

    YANG name: path-metric-bounds
    """

    _yang_name: Final[str] = 'path-metric-bounds'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'path-metric-bound': (
            path_metric_bound := (  # YANGListMember(
                PathMetricBoundsMeta.
                PathMetricBound.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'PathMetricBounds':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
