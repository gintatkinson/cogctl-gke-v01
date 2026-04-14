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


class InformationSourceEntryMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: information-source-entry
    """
    from .max_link_bandwidth import MaxLinkBandwidth
    from .label_restrictions import LabelRestrictions
    from .information_source_state import InformationSourceState
    from .max_resv_link_bandwidth import MaxResvLinkBandwidth
    from .te_srlgs import TeSrlgs
    from .te_nsrlgs import TeNsrlgs
    from .interface_switching_capability import InterfaceSwitchingCapability
    from .unreserved_bandwidth import UnreservedBandwidth

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: information-source-entry
        """

        def __init__(self):
            super().__init__(InformationSourceEntry)

        def __get__(self, instance, owner=None) -> (
                'InformationSourceEntryMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['InformationSourceEntry']:
            pass

        def __iter__(self, key) -> Iterator['InformationSourceEntry']:
            return super().__iter__()

        def __getitem__(self, key) -> 'InformationSourceEntry':
            return super()[key]

        def __enter__(self) -> (
                'InformationSourceEntryMeta.yang_list_descriptor'):
            pass


class InformationSourceEntry(
        YANGListItem,
        metaclass=InformationSourceEntryMeta):
    """
    YANG list item handler.

    YANG name: information-source-entry
    """

    _yang_name: Final[str] = 'information-source-entry'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'information-source',
        'information-source-instance',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'information-source-instance': (
            information_source_instance := YANGLeafMember(
                'information-source-instance',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'te-igp-metric': (
            te_igp_metric := YANGLeafMember(
                'te-igp-metric',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'te-default-metric': (
            te_default_metric := YANGLeafMember(
                'te-default-metric',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'te-delay-metric': (
            te_delay_metric := YANGLeafMember(
                'te-delay-metric',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'link-index': (
            link_index := YANGLeafMember(
                'link-index',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'link-protection-type': (
            link_protection_type := YANGLeafMember(
                'link-protection-type',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'administrative-group': (
            administrative_group := YANGLeafMember(
                'administrative-group',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'information-source': (
            information_source := YANGLeafMember(
                'information-source',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'max-link-bandwidth': (
            max_link_bandwidth := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                MaxLinkBandwidth.
                yang_container_descriptor())),

        'label-restrictions': (
            label_restrictions := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                LabelRestrictions.
                yang_container_descriptor())),

        'information-source-state': (
            information_source_state := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                InformationSourceState.
                yang_container_descriptor())),

        'max-resv-link-bandwidth': (
            max_resv_link_bandwidth := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                MaxResvLinkBandwidth.
                yang_container_descriptor())),

        'te-srlgs': (
            te_srlgs := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                TeSrlgs.
                yang_container_descriptor())),

        'te-nsrlgs': (
            te_nsrlgs := (  # YANGContainerMember(
                InformationSourceEntryMeta.
                TeNsrlgs.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'interface-switching-capability': (
            interface_switching_capability := (  # YANGListMember(
                InformationSourceEntryMeta.
                InterfaceSwitchingCapability.
                yang_list_descriptor())),

        'unreserved-bandwidth': (
            unreserved_bandwidth := (  # YANGListMember(
                InformationSourceEntryMeta.
                UnreservedBandwidth.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'InformationSourceEntry':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
