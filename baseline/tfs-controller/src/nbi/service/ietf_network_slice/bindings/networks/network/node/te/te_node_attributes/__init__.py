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


class TeNodeAttributesMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: te-node-attributes
    """
    from .connectivity_matrices import ConnectivityMatrices
    from .underlay_topology import UnderlayTopology

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: te-node-attributes
        """

        def __init__(self):
            super().__init__(TeNodeAttributes)

        def __get__(self, instance, owner=None) -> (
                'TeNodeAttributesMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'TeNodeAttributes':
            pass

        def __enter__(self) -> 'TeNodeAttributes':
            pass


class TeNodeAttributes(
        YANGContainer,
        metaclass=TeNodeAttributesMeta):
    """
    YANG container handler.

    YANG name: te-node-attributes
    """

    _yang_name: Final[str] = 'te-node-attributes'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'domain-id': (
            domain_id := YANGLeafMember(
                'domain-id',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'is-abstract': (
            is_abstract := YANGLeafMember(
                'is-abstract',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'admin-status': (
            admin_status := YANGLeafMember(
                'admin-status',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'name': (
            name := YANGLeafMember(
                'name',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'connectivity-matrices': (
            connectivity_matrices := (  # YANGContainerMember(
                TeNodeAttributesMeta.
                ConnectivityMatrices.
                yang_container_descriptor())),

        'underlay-topology': (
            underlay_topology := (  # YANGContainerMember(
                TeNodeAttributesMeta.
                UnderlayTopology.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'TeNodeAttributes':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
