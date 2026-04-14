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


class TerminationPointMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: termination-point
    """
    from .te import Te
    from .supporting_termination_point import SupportingTerminationPoint

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: termination-point
        """

        def __init__(self):
            super().__init__(TerminationPoint)

        def __get__(self, instance, owner=None) -> (
                'TerminationPointMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['TerminationPoint']:
            pass

        def __iter__(self, key) -> Iterator['TerminationPoint']:
            return super().__iter__()

        def __getitem__(self, key) -> 'TerminationPoint':
            return super()[key]

        def __enter__(self) -> (
                'TerminationPointMeta.yang_list_descriptor'):
            pass


class TerminationPoint(
        YANGListItem,
        metaclass=TerminationPointMeta):
    """
    YANG list item handler.

    YANG name: termination-point
    """

    _yang_name: Final[str] = 'termination-point'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-topology'
    _yang_module_name: Final[str] = 'ietf-network-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'tp-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'te-tp-id': (
            te_tp_id := YANGLeafMember(
                'te-tp-id',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'tp-id': (
            tp_id := YANGLeafMember(
                'tp-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-topology',
                'ietf-network-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'te': (
            te := (  # YANGContainerMember(
                TerminationPointMeta.
                Te.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'supporting-termination-point': (
            supporting_termination_point := (  # YANGListMember(
                TerminationPointMeta.
                SupportingTerminationPoint.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'TerminationPoint':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
