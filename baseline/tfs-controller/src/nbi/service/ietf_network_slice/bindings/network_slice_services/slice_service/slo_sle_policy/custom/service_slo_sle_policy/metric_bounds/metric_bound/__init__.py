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


class MetricBoundMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: metric-bound
    """

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: metric-bound
        """

        def __init__(self):
            super().__init__(MetricBound)

        def __get__(self, instance, owner=None) -> (
                'MetricBoundMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['MetricBound']:
            pass

        def __iter__(self, key) -> Iterator['MetricBound']:
            return super().__iter__()

        def __getitem__(self, key) -> 'MetricBound':
            return super()[key]

        def __enter__(self) -> (
                'MetricBoundMeta.yang_list_descriptor'):
            pass


class MetricBound(
        YANGListItem,
        metaclass=MetricBoundMeta):
    """
    YANG list item handler.

    YANG name: metric-bound
    """

    _yang_name: Final[str] = 'metric-bound'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'metric-type',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'value-description': (
            value_description := YANGLeafMember(
                'value-description',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'bound': (
            bound := YANGLeafMember(
                'bound',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'metric-unit': (
            metric_unit := YANGLeafMember(
                'metric-unit',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'metric-type': (
            metric_type := YANGLeafMember(
                'metric-type',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'MetricBound':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
