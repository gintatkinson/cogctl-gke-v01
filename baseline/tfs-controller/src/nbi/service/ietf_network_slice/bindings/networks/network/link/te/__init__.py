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


class TeMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: te
    """
    from .statistics import Statistics
    from .te_link_attributes import TeLinkAttributes
    from .underlay import Underlay
    from .recovery import Recovery
    from .information_source_state import InformationSourceState
    from .information_source_entry import InformationSourceEntry
    from .bundle_stack_level import BundleStackLevel

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: te
        """

        def __init__(self):
            super().__init__(Te)

        def __get__(self, instance, owner=None) -> (
                'TeMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'Te':
            pass

        def __enter__(self) -> 'Te':
            pass


class Te(
        YANGContainer,
        metaclass=TeMeta):
    """
    YANG container handler.

    YANG name: te
    """

    _yang_name: Final[str] = 'te'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'is-transitional': (
            is_transitional := YANGLeafMember(
                'is-transitional',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'information-source-instance': (
            information_source_instance := YANGLeafMember(
                'information-source-instance',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'oper-status': (
            oper_status := YANGLeafMember(
                'oper-status',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'information-source': (
            information_source := YANGLeafMember(
                'information-source',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'statistics': (
            statistics := (  # YANGContainerMember(
                TeMeta.
                Statistics.
                yang_container_descriptor())),

        'te-link-attributes': (
            te_link_attributes := (  # YANGContainerMember(
                TeMeta.
                TeLinkAttributes.
                yang_container_descriptor())),

        'underlay': (
            underlay := (  # YANGContainerMember(
                TeMeta.
                Underlay.
                yang_container_descriptor())),

        'recovery': (
            recovery := (  # YANGContainerMember(
                TeMeta.
                Recovery.
                yang_container_descriptor())),

        'information-source-state': (
            information_source_state := (  # YANGContainerMember(
                TeMeta.
                InformationSourceState.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'information-source-entry': (
            information_source_entry := (  # YANGListMember(
                TeMeta.
                InformationSourceEntry.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Te':
        instance = super().__new__(cls)
        instance._yang_choices = {

            'bundle-stack-level':
                TeMeta.BundleStackLevel(
                    instance),
        }
        return instance

    @property
    def bundle_stack_level(self) -> (
            TeMeta.BundleStackLevel):
        return self._yang_choices['bundle-stack-level']
