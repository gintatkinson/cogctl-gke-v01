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


class LinkMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: link
    """
    from .source import Source
    from .destination import Destination
    from .te import Te
    from .supporting_link import SupportingLink

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: link
        """

        def __init__(self):
            super().__init__(Link)

        def __get__(self, instance, owner=None) -> (
                'LinkMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['Link']:
            pass

        def __iter__(self, key) -> Iterator['Link']:
            return super().__iter__()

        def __getitem__(self, key) -> 'Link':
            return super()[key]

        def __enter__(self) -> (
                'LinkMeta.yang_list_descriptor'):
            pass


class Link(
        YANGListItem,
        metaclass=LinkMeta):
    """
    YANG list item handler.

    YANG name: link
    """

    _yang_name: Final[str] = 'link'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-topology'
    _yang_module_name: Final[str] = 'ietf-network-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'link-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'link-id': (
            link_id := YANGLeafMember(
                'link-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-topology',
                'ietf-network-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'source': (
            source := (  # YANGContainerMember(
                LinkMeta.
                Source.
                yang_container_descriptor())),

        'destination': (
            destination := (  # YANGContainerMember(
                LinkMeta.
                Destination.
                yang_container_descriptor())),

        'te': (
            te := (  # YANGContainerMember(
                LinkMeta.
                Te.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'supporting-link': (
            supporting_link := (  # YANGListMember(
                LinkMeta.
                SupportingLink.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Link':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
