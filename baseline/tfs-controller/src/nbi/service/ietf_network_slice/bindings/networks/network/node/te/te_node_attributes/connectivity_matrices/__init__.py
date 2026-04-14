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


class ConnectivityMatricesMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: connectivity-matrices
    """
    from .label_restrictions import LabelRestrictions
    from .optimizations import Optimizations
    from .underlay import Underlay
    from .path_properties import PathProperties
    from .path_constraints import PathConstraints
    from .connectivity_matrix import ConnectivityMatrix

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: connectivity-matrices
        """

        def __init__(self):
            super().__init__(ConnectivityMatrices)

        def __get__(self, instance, owner=None) -> (
                'ConnectivityMatricesMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'ConnectivityMatrices':
            pass

        def __enter__(self) -> 'ConnectivityMatrices':
            pass


class ConnectivityMatrices(
        YANGContainer,
        metaclass=ConnectivityMatricesMeta):
    """
    YANG container handler.

    YANG name: connectivity-matrices
    """

    _yang_name: Final[str] = 'connectivity-matrices'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'number-of-entries': (
            number_of_entries := YANGLeafMember(
                'number-of-entries',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'is-allowed': (
            is_allowed := YANGLeafMember(
                'is-allowed',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'label-restrictions': (
            label_restrictions := (  # YANGContainerMember(
                ConnectivityMatricesMeta.
                LabelRestrictions.
                yang_container_descriptor())),

        'optimizations': (
            optimizations := (  # YANGContainerMember(
                ConnectivityMatricesMeta.
                Optimizations.
                yang_container_descriptor())),

        'underlay': (
            underlay := (  # YANGContainerMember(
                ConnectivityMatricesMeta.
                Underlay.
                yang_container_descriptor())),

        'path-properties': (
            path_properties := (  # YANGContainerMember(
                ConnectivityMatricesMeta.
                PathProperties.
                yang_container_descriptor())),

        'path-constraints': (
            path_constraints := (  # YANGContainerMember(
                ConnectivityMatricesMeta.
                PathConstraints.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'connectivity-matrix': (
            connectivity_matrix := (  # YANGListMember(
                ConnectivityMatricesMeta.
                ConnectivityMatrix.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'ConnectivityMatrices':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
