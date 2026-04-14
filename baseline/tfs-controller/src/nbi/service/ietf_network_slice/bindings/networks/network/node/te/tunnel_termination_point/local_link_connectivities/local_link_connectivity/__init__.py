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


class LocalLinkConnectivityMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: local-link-connectivity
    """
    from .underlay import Underlay
    from .optimizations import Optimizations
    from .label_restrictions import LabelRestrictions
    from .path_properties import PathProperties
    from .path_constraints import PathConstraints

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: local-link-connectivity
        """

        def __init__(self):
            super().__init__(LocalLinkConnectivity)

        def __get__(self, instance, owner=None) -> (
                'LocalLinkConnectivityMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['LocalLinkConnectivity']:
            pass

        def __iter__(self, key) -> Iterator['LocalLinkConnectivity']:
            return super().__iter__()

        def __getitem__(self, key) -> 'LocalLinkConnectivity':
            return super()[key]

        def __enter__(self) -> (
                'LocalLinkConnectivityMeta.yang_list_descriptor'):
            pass


class LocalLinkConnectivity(
        YANGListItem,
        metaclass=LocalLinkConnectivityMeta):
    """
    YANG list item handler.

    YANG name: local-link-connectivity
    """

    _yang_name: Final[str] = 'local-link-connectivity'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'link-tp-ref',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'link-tp-ref': (
            link_tp_ref := YANGLeafMember(
                'link-tp-ref',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'is-allowed': (
            is_allowed := YANGLeafMember(
                'is-allowed',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'underlay': (
            underlay := (  # YANGContainerMember(
                LocalLinkConnectivityMeta.
                Underlay.
                yang_container_descriptor())),

        'optimizations': (
            optimizations := (  # YANGContainerMember(
                LocalLinkConnectivityMeta.
                Optimizations.
                yang_container_descriptor())),

        'label-restrictions': (
            label_restrictions := (  # YANGContainerMember(
                LocalLinkConnectivityMeta.
                LabelRestrictions.
                yang_container_descriptor())),

        'path-properties': (
            path_properties := (  # YANGContainerMember(
                LocalLinkConnectivityMeta.
                PathProperties.
                yang_container_descriptor())),

        'path-constraints': (
            path_constraints := (  # YANGContainerMember(
                LocalLinkConnectivityMeta.
                PathConstraints.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'LocalLinkConnectivity':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
