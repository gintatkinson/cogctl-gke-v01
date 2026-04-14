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

from typing import Dict, Final

from .. import (
    YANGChoice, YANGChoiceCase, YANGContainer, YANGContainerMember,
    YANGLeafMember, YANGListItem, YANGListMember)


class TeLinkAttributesMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: te-link-attributes
    """
    from .max_resv_link_bandwidth import MaxResvLinkBandwidth
    from .max_link_bandwidth import MaxLinkBandwidth
    from .underlay import Underlay
    from .te_srlgs import TeSrlgs
    from .label_restrictions import LabelRestrictions
    from .external_domain import ExternalDomain
    from .te_nsrlgs import TeNsrlgs
    from .unreserved_bandwidth import UnreservedBandwidth
    from .interface_switching_capability import InterfaceSwitchingCapability

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: te-link-attributes
        """

        def __init__(self):
            super().__init__(TeLinkAttributes)

        def __get__(self, instance, owner=None) -> (
                'TeLinkAttributesMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'TeLinkAttributes':
            pass

        def __enter__(self) -> 'TeLinkAttributes':
            pass


class TeLinkAttributes(
        YANGContainer,
        metaclass=TeLinkAttributesMeta):
    """
    YANG container handler.

    YANG name: te-link-attributes
    """

    _yang_name: Final[str] = 'te-link-attributes'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'is-abstract': (
            is_abstract := YANGLeafMember(
                'is-abstract',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'link-index': (
            link_index := YANGLeafMember(
                'link-index',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'te-default-metric': (
            te_default_metric := YANGLeafMember(
                'te-default-metric',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'link-protection-type': (
            link_protection_type := YANGLeafMember(
                'link-protection-type',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'name': (
            name := YANGLeafMember(
                'name',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'admin-status': (
            admin_status := YANGLeafMember(
                'admin-status',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'te-igp-metric': (
            te_igp_metric := YANGLeafMember(
                'te-igp-metric',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'access-type': (
            access_type := YANGLeafMember(
                'access-type',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'te-delay-metric': (
            te_delay_metric := YANGLeafMember(
                'te-delay-metric',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'administrative-group': (
            administrative_group := YANGLeafMember(
                'administrative-group',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'max-resv-link-bandwidth': (
            max_resv_link_bandwidth := (  # YANGContainerMember(
                TeLinkAttributesMeta.
                MaxResvLinkBandwidth.
                yang_container_descriptor())),

        'max-link-bandwidth': (
            max_link_bandwidth := (  # YANGContainerMember(
                TeLinkAttributesMeta.
                MaxLinkBandwidth.
                yang_container_descriptor())),

        'underlay': (
            underlay := (  # YANGContainerMember(
                TeLinkAttributesMeta.
                Underlay.
                yang_container_descriptor())),

        'te-srlgs': (
            te_srlgs := (  # YANGContainerMember(
                TeLinkAttributesMeta.
                TeSrlgs.
                yang_container_descriptor())),

        'label-restrictions': (
            label_restrictions := (  # YANGContainerMember(
                TeLinkAttributesMeta.
                LabelRestrictions.
                yang_container_descriptor())),

        'external-domain': (
            external_domain := (  # YANGContainerMember(
                TeLinkAttributesMeta.
                ExternalDomain.
                yang_container_descriptor())),

        'te-nsrlgs': (
            te_nsrlgs := (  # YANGContainerMember(
                TeLinkAttributesMeta.
                TeNsrlgs.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'unreserved-bandwidth': (
            unreserved_bandwidth := (  # YANGListMember(
                TeLinkAttributesMeta.
                UnreservedBandwidth.
                yang_list_descriptor())),

        'interface-switching-capability': (
            interface_switching_capability := (  # YANGListMember(
                TeLinkAttributesMeta.
                InterfaceSwitchingCapability.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'TeLinkAttributes':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
