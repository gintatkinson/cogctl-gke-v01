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


class NetworkMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: network
    """
    from .te import Te
    from .te_topology_identifier import TeTopologyIdentifier
    from .network_types import NetworkTypes
    from .node import Node
    from .supporting_network import SupportingNetwork
    from .link import Link

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: network
        """

        def __init__(self):
            super().__init__(Network)

        def __get__(self, instance, owner=None) -> (
                'NetworkMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['Network']:
            pass

        def __iter__(self, key) -> Iterator['Network']:
            return super().__iter__()

        def __getitem__(self, key) -> 'Network':
            return super()[key]

        def __enter__(self) -> (
                'NetworkMeta.yang_list_descriptor'):
            pass


class Network(
        YANGListItem,
        metaclass=NetworkMeta):
    """
    YANG list item handler.

    YANG name: network
    """

    _yang_name: Final[str] = 'network'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network'
    _yang_module_name: Final[str] = 'ietf-network'

    _yang_list_key_names: Final[Tuple[str]] = (
        'network-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'network-id': (
            network_id := YANGLeafMember(
                'network-id',
                'urn:ietf:params:xml:ns:yang:ietf-network',
                'ietf-network')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'te': (
            te := (  # YANGContainerMember(
                NetworkMeta.
                Te.
                yang_container_descriptor())),

        'te-topology-identifier': (
            te_topology_identifier := (  # YANGContainerMember(
                NetworkMeta.
                TeTopologyIdentifier.
                yang_container_descriptor())),

        'network-types': (
            network_types := (  # YANGContainerMember(
                NetworkMeta.
                NetworkTypes.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'node': (
            node := (  # YANGListMember(
                NetworkMeta.
                Node.
                yang_list_descriptor())),

        'supporting-network': (
            supporting_network := (  # YANGListMember(
                NetworkMeta.
                SupportingNetwork.
                yang_list_descriptor())),

        'link': (
            link := (  # YANGListMember(
                NetworkMeta.
                Link.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Network':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
