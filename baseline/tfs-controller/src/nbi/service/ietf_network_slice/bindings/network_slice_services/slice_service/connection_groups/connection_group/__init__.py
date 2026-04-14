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


class ConnectionGroupMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: connection-group
    """
    from .connection_group_monitoring import ConnectionGroupMonitoring
    from .connectivity_construct import ConnectivityConstruct
    from .slo_sle_policy import SloSlePolicy

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: connection-group
        """

        def __init__(self):
            super().__init__(ConnectionGroup)

        def __get__(self, instance, owner=None) -> (
                'ConnectionGroupMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['ConnectionGroup']:
            pass

        def __iter__(self, key) -> Iterator['ConnectionGroup']:
            return super().__iter__()

        def __getitem__(self, key) -> 'ConnectionGroup':
            return super()[key]

        def __enter__(self) -> (
                'ConnectionGroupMeta.yang_list_descriptor'):
            pass


class ConnectionGroup(
        YANGListItem,
        metaclass=ConnectionGroupMeta):
    """
    YANG list item handler.

    YANG name: connection-group
    """

    _yang_name: Final[str] = 'connection-group'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'connection-group-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'connectivity-type': (
            connectivity_type := YANGLeafMember(
                'connectivity-type',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'connection-group-id': (
            connection_group_id := YANGLeafMember(
                'connection-group-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'service-slo-sle-policy-override': (
            service_slo_sle_policy_override := YANGLeafMember(
                'service-slo-sle-policy-override',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'connection-group-monitoring': (
            connection_group_monitoring := (  # YANGContainerMember(
                ConnectionGroupMeta.
                ConnectionGroupMonitoring.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'connectivity-construct': (
            connectivity_construct := (  # YANGListMember(
                ConnectionGroupMeta.
                ConnectivityConstruct.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'ConnectionGroup':
        instance = super().__new__(cls)
        instance._yang_choices = {

            'slo-sle-policy':
                ConnectionGroupMeta.SloSlePolicy(
                    instance),
        }
        return instance

    @property
    def slo_sle_policy(self) -> (
            ConnectionGroupMeta.SloSlePolicy):
        return self._yang_choices['slo-sle-policy']
