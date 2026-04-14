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


class A2aSdpMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: a2a-sdp
    """
    from .slo_sle_policy import SloSlePolicy

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: a2a-sdp
        """

        def __init__(self):
            super().__init__(A2aSdp)

        def __get__(self, instance, owner=None) -> (
                'A2aSdpMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['A2aSdp']:
            pass

        def __iter__(self, key) -> Iterator['A2aSdp']:
            return super().__iter__()

        def __getitem__(self, key) -> 'A2aSdp':
            return super()[key]

        def __enter__(self) -> (
                'A2aSdpMeta.yang_list_descriptor'):
            pass


class A2aSdp(
        YANGListItem,
        metaclass=A2aSdpMeta):
    """
    YANG list item handler.

    YANG name: a2a-sdp
    """

    _yang_name: Final[str] = 'a2a-sdp'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'sdp-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'sdp-id': (
            sdp_id := YANGLeafMember(
                'sdp-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'A2aSdp':
        instance = super().__new__(cls)
        instance._yang_choices = {

            'slo-sle-policy':
                A2aSdpMeta.SloSlePolicy(
                    instance),
        }
        return instance

    @property
    def slo_sle_policy(self) -> (
            A2aSdpMeta.SloSlePolicy):
        return self._yang_choices['slo-sle-policy']
