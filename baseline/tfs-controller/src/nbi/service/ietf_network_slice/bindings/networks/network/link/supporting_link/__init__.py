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


class SupportingLinkMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: supporting-link
    """

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: supporting-link
        """

        def __init__(self):
            super().__init__(SupportingLink)

        def __get__(self, instance, owner=None) -> (
                'SupportingLinkMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['SupportingLink']:
            pass

        def __iter__(self, key) -> Iterator['SupportingLink']:
            return super().__iter__()

        def __getitem__(self, key) -> 'SupportingLink':
            return super()[key]

        def __enter__(self) -> (
                'SupportingLinkMeta.yang_list_descriptor'):
            pass


class SupportingLink(
        YANGListItem,
        metaclass=SupportingLinkMeta):
    """
    YANG list item handler.

    YANG name: supporting-link
    """

    _yang_name: Final[str] = 'supporting-link'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-topology'
    _yang_module_name: Final[str] = 'ietf-network-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'network-ref',
        'link-ref',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'link-ref': (
            link_ref := YANGLeafMember(
                'link-ref',
                'urn:ietf:params:xml:ns:yang:ietf-network-topology',
                'ietf-network-topology')),

        'network-ref': (
            network_ref := YANGLeafMember(
                'network-ref',
                'urn:ietf:params:xml:ns:yang:ietf-network-topology',
                'ietf-network-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'SupportingLink':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
