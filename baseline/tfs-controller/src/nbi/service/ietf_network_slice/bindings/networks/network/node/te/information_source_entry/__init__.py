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


class InformationSourceEntryMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: information-source-entry
    """
    from .information_source_state import InformationSourceState
    from .underlay_topology import UnderlayTopology
    from .connectivity_matrices import ConnectivityMatrices

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: information-source-entry
        """

        def __init__(self):
            super().__init__(InformationSourceEntry)

        def __get__(self, instance, owner=None) -> (
                'InformationSourceEntryMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['InformationSourceEntry']:
            pass

        def __iter__(self, key) -> Iterator['InformationSourceEntry']:
            return super().__iter__()

        def __getitem__(self, key) -> 'InformationSourceEntry':
            return super()[key]

        def __enter__(self) -> (
                'InformationSourceEntryMeta.yang_list_descriptor'):
            pass


class InformationSourceEntry(
        YANGListItem,
        metaclass=InformationSourceEntryMeta):
    """
    YANG list item handler.

    YANG name: information-source-entry
    """

    _yang_name: Final[str] = 'information-source-entry'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'information-source',
        'information-source-instance',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'information-source': (
            information_source := YANGLeafMember(
                'information-source',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'name': (
            name := YANGLeafMember(
                'name',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'domain-id': (
            domain_id := YANGLeafMember(
                'domain-id',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'is-abstract': (
            is_abstract := YANGLeafMember(
                'is-abstract',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'information-source-instance': (
            information_source_instance := YANGLeafMember(
                'information-source-instance',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'information-source-state': (
            information_source_state := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                InformationSourceState.
                yang_container_descriptor())),

        'underlay-topology': (
            underlay_topology := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                UnderlayTopology.
                yang_container_descriptor())),

        'connectivity-matrices': (
            connectivity_matrices := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                ConnectivityMatrices.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'InformationSourceEntry':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
