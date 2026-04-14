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


class PathAffinityNameMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: path-affinity-name
    """
    from .affinity_name import AffinityName

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: path-affinity-name
        """

        def __init__(self):
            super().__init__(PathAffinityName)

        def __get__(self, instance, owner=None) -> (
                'PathAffinityNameMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['PathAffinityName']:
            pass

        def __iter__(self, key) -> Iterator['PathAffinityName']:
            return super().__iter__()

        def __getitem__(self, key) -> 'PathAffinityName':
            return super()[key]

        def __enter__(self) -> (
                'PathAffinityNameMeta.yang_list_descriptor'):
            pass


class PathAffinityName(
        YANGListItem,
        metaclass=PathAffinityNameMeta):
    """
    YANG list item handler.

    YANG name: path-affinity-name
    """

    _yang_name: Final[str] = 'path-affinity-name'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'usage',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'usage': (
            usage := YANGLeafMember(
                'usage',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'affinity-name': (
            affinity_name := (  # YANGListMember(
                PathAffinityNameMeta.
                AffinityName.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'PathAffinityName':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
