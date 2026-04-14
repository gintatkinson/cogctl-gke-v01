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


class SliceServiceMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: slice-service
    """
    from .connection_groups import ConnectionGroups
    from .te_topology_identifier import TeTopologyIdentifier
    from .status import Status
    from .sdps import Sdps
    from .service_tags import ServiceTags
    from .slo_sle_policy import SloSlePolicy

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: slice-service
        """

        def __init__(self):
            super().__init__(SliceService)

        def __get__(self, instance, owner=None) -> (
                'SliceServiceMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['SliceService']:
            pass

        def __iter__(self, key) -> Iterator['SliceService']:
            return super().__iter__()

        def __getitem__(self, key) -> 'SliceService':
            return super()[key]

        def __enter__(self) -> (
                'SliceServiceMeta.yang_list_descriptor'):
            pass


class SliceService(
        YANGListItem,
        metaclass=SliceServiceMeta):
    """
    YANG list item handler.

    YANG name: slice-service
    """

    _yang_name: Final[str] = 'slice-service'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'service-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'service-id': (
            service_id := YANGLeafMember(
                'service-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'service-description': (
            service_description := YANGLeafMember(
                'service-description',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'connection-groups': (
            connection_groups := (  # YANGContainerMember(
                SliceServiceMeta.
                ConnectionGroups.
                yang_container_descriptor())),

        'te-topology-identifier': (
            te_topology_identifier := (  # YANGContainerMember(
                SliceServiceMeta.
                TeTopologyIdentifier.
                yang_container_descriptor())),

        'status': (
            status := (  # YANGContainerMember(
                SliceServiceMeta.
                Status.
                yang_container_descriptor())),

        'sdps': (
            sdps := (  # YANGContainerMember(
                SliceServiceMeta.
                Sdps.
                yang_container_descriptor())),

        'service-tags': (
            service_tags := (  # YANGContainerMember(
                SliceServiceMeta.
                ServiceTags.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'SliceService':
        instance = super().__new__(cls)
        instance._yang_choices = {

            'slo-sle-policy':
                SliceServiceMeta.SloSlePolicy(
                    instance),
        }
        return instance

    @property
    def slo_sle_policy(self) -> (
            SliceServiceMeta.SloSlePolicy):
        return self._yang_choices['slo-sle-policy']
