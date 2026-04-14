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


class TunnelTerminationPointMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: tunnel-termination-point
    """
    from .client_layer_adaptation import ClientLayerAdaptation
    from .statistics import Statistics
    from .local_link_connectivities import LocalLinkConnectivities
    from .geolocation import Geolocation
    from .supporting_tunnel_termination_point import SupportingTunnelTerminationPoint

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: tunnel-termination-point
        """

        def __init__(self):
            super().__init__(TunnelTerminationPoint)

        def __get__(self, instance, owner=None) -> (
                'TunnelTerminationPointMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['TunnelTerminationPoint']:
            pass

        def __iter__(self, key) -> Iterator['TunnelTerminationPoint']:
            return super().__iter__()

        def __getitem__(self, key) -> 'TunnelTerminationPoint':
            return super()[key]

        def __enter__(self) -> (
                'TunnelTerminationPointMeta.yang_list_descriptor'):
            pass


class TunnelTerminationPoint(
        YANGListItem,
        metaclass=TunnelTerminationPointMeta):
    """
    YANG list item handler.

    YANG name: tunnel-termination-point
    """

    _yang_name: Final[str] = 'tunnel-termination-point'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_list_key_names: Final[Tuple[str]] = (
        'tunnel-tp-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'protection-type': (
            protection_type := YANGLeafMember(
                'protection-type',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'admin-status': (
            admin_status := YANGLeafMember(
                'admin-status',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'tunnel-tp-id': (
            tunnel_tp_id := YANGLeafMember(
                'tunnel-tp-id',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'encoding': (
            encoding := YANGLeafMember(
                'encoding',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'name': (
            name := YANGLeafMember(
                'name',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'switching-capability': (
            switching_capability := YANGLeafMember(
                'switching-capability',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'oper-status': (
            oper_status := YANGLeafMember(
                'oper-status',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'client-layer-adaptation': (
            client_layer_adaptation := (  # YANGContainerMember(
                TunnelTerminationPointMeta.
                ClientLayerAdaptation.
                yang_container_descriptor())),

        'statistics': (
            statistics := (  # YANGContainerMember(
                TunnelTerminationPointMeta.
                Statistics.
                yang_container_descriptor())),

        'local-link-connectivities': (
            local_link_connectivities := (  # YANGContainerMember(
                TunnelTerminationPointMeta.
                LocalLinkConnectivities.
                yang_container_descriptor())),

        'geolocation': (
            geolocation := (  # YANGContainerMember(
                TunnelTerminationPointMeta.
                Geolocation.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'supporting-tunnel-termination-point': (
            supporting_tunnel_termination_point := (  # YANGListMember(
                TunnelTerminationPointMeta.
                SupportingTunnelTerminationPoint.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'TunnelTerminationPoint':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
