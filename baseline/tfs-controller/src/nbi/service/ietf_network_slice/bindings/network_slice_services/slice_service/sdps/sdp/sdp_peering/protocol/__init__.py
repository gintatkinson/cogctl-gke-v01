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


class ProtocolMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: protocol
    """
    from .attribute import Attribute

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: protocol
        """

        def __init__(self):
            super().__init__(Protocol)

        def __get__(self, instance, owner=None) -> (
                'ProtocolMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['Protocol']:
            pass

        def __iter__(self, key) -> Iterator['Protocol']:
            return super().__iter__()

        def __getitem__(self, key) -> 'Protocol':
            return super()[key]

        def __enter__(self) -> (
                'ProtocolMeta.yang_list_descriptor'):
            pass


class Protocol(
        YANGListItem,
        metaclass=ProtocolMeta):
    """
    YANG list item handler.

    YANG name: protocol
    """

    _yang_name: Final[str] = 'protocol'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'protocol-type',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'protocol-type': (
            protocol_type := YANGLeafMember(
                'protocol-type',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'attribute': (
            attribute := (  # YANGListMember(
                ProtocolMeta.
                Attribute.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Protocol':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
