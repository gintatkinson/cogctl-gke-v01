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


class MatchCriterionMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: match-criterion
    """

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: match-criterion
        """

        def __init__(self):
            super().__init__(MatchCriterion)

        def __get__(self, instance, owner=None) -> (
                'MatchCriterionMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['MatchCriterion']:
            pass

        def __iter__(self, key) -> Iterator['MatchCriterion']:
            return super().__iter__()

        def __getitem__(self, key) -> 'MatchCriterion':
            return super()[key]

        def __enter__(self) -> (
                'MatchCriterionMeta.yang_list_descriptor'):
            pass


class MatchCriterion(
        YANGListItem,
        metaclass=MatchCriterionMeta):
    """
    YANG list item handler.

    YANG name: match-criterion
    """

    _yang_name: Final[str] = 'match-criterion'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'index',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'index': (
            index := YANGLeafMember(
                'index',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'connection-group-sdp-role': (
            connection_group_sdp_role := YANGLeafMember(
                'connection-group-sdp-role',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'target-connection-group-id': (
            target_connection_group_id := YANGLeafMember(
                'target-connection-group-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'target-connectivity-construct-id': (
            target_connectivity_construct_id := YANGLeafMember(
                'target-connectivity-construct-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'match-type': (
            match_type := YANGLeafMember(
                'match-type',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'MatchCriterion':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
