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


class LocalLinkConnectivitiesMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: local-link-connectivities
    """
    from .underlay import Underlay
    from .path_constraints import PathConstraints
    from .path_properties import PathProperties
    from .label_restrictions import LabelRestrictions
    from .optimizations import Optimizations
    from .local_link_connectivity import LocalLinkConnectivity

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: local-link-connectivities
        """

        def __init__(self):
            super().__init__(LocalLinkConnectivities)

        def __get__(self, instance, owner=None) -> (
                'LocalLinkConnectivitiesMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'LocalLinkConnectivities':
            pass

        def __enter__(self) -> 'LocalLinkConnectivities':
            pass


class LocalLinkConnectivities(
        YANGContainer,
        metaclass=LocalLinkConnectivitiesMeta):
    """
    YANG container handler.

    YANG name: local-link-connectivities
    """

    _yang_name: Final[str] = 'local-link-connectivities'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'is-allowed': (
            is_allowed := YANGLeafMember(
                'is-allowed',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'number-of-entries': (
            number_of_entries := YANGLeafMember(
                'number-of-entries',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'underlay': (
            underlay := (  # YANGContainerMember(
                LocalLinkConnectivitiesMeta.
                Underlay.
                yang_container_descriptor())),

        'path-constraints': (
            path_constraints := (  # YANGContainerMember(
                LocalLinkConnectivitiesMeta.
                PathConstraints.
                yang_container_descriptor())),

        'path-properties': (
            path_properties := (  # YANGContainerMember(
                LocalLinkConnectivitiesMeta.
                PathProperties.
                yang_container_descriptor())),

        'label-restrictions': (
            label_restrictions := (  # YANGContainerMember(
                LocalLinkConnectivitiesMeta.
                LabelRestrictions.
                yang_container_descriptor())),

        'optimizations': (
            optimizations := (  # YANGContainerMember(
                LocalLinkConnectivitiesMeta.
                Optimizations.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'local-link-connectivity': (
            local_link_connectivity := (  # YANGListMember(
                LocalLinkConnectivitiesMeta.
                LocalLinkConnectivity.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'LocalLinkConnectivities':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
