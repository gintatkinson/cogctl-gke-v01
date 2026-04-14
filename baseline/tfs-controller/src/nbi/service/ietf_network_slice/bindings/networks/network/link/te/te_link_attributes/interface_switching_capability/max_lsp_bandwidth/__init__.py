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


class MaxLspBandwidthMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: max-lsp-bandwidth
    """
    from .te_bandwidth import TeBandwidth

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: max-lsp-bandwidth
        """

        def __init__(self):
            super().__init__(MaxLspBandwidth)

        def __get__(self, instance, owner=None) -> (
                'MaxLspBandwidthMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['MaxLspBandwidth']:
            pass

        def __iter__(self, key) -> Iterator['MaxLspBandwidth']:
            return super().__iter__()

        def __getitem__(self, key) -> 'MaxLspBandwidth':
            return super()[key]

        def __enter__(self) -> (
                'MaxLspBandwidthMeta.yang_list_descriptor'):
            pass


class MaxLspBandwidth(
        YANGListItem,
        metaclass=MaxLspBandwidthMeta):
    """
    YANG list item handler.

    YANG name: max-lsp-bandwidth
    """

    _yang_name: Final[str] = 'max-lsp-bandwidth'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'priority',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'priority': (
            priority := YANGLeafMember(
                'priority',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'te-bandwidth': (
            te_bandwidth := (  # YANGContainerMember(
                MaxLspBandwidthMeta.
                TeBandwidth.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'MaxLspBandwidth':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
