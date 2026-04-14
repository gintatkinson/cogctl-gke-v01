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


class NodeMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: node
    """
    from .te import Te
    from .termination_point import TerminationPoint
    from .supporting_node import SupportingNode

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: node
        """

        def __init__(self):
            super().__init__(Node)

        def __get__(self, instance, owner=None) -> (
                'NodeMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['Node']:
            pass

        def __iter__(self, key) -> Iterator['Node']:
            return super().__iter__()

        def __getitem__(self, key) -> 'Node':
            return super()[key]

        def __enter__(self) -> (
                'NodeMeta.yang_list_descriptor'):
            pass


class Node(
        YANGListItem,
        metaclass=NodeMeta):
    """
    YANG list item handler.

    YANG name: node
    """

    _yang_name: Final[str] = 'node'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network'
    _yang_module_name: Final[str] = 'ietf-network'

    _yang_list_key_names: Final[Tuple[str]] = (
        'node-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'te-node-id': (
            te_node_id := YANGLeafMember(
                'te-node-id',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'node-id': (
            node_id := YANGLeafMember(
                'node-id',
                'urn:ietf:params:xml:ns:yang:ietf-network',
                'ietf-network')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'te': (
            te := (  # YANGContainerMember(
                NodeMeta.
                Te.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'termination-point': (
            termination_point := (  # YANGListMember(
                NodeMeta.
                TerminationPoint.
                yang_list_descriptor())),

        'supporting-node': (
            supporting_node := (  # YANGListMember(
                NodeMeta.
                SupportingNode.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Node':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
