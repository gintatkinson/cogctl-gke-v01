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


class UnderlayMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: underlay
    """
    from .tunnels import Tunnels
    from .primary_path import PrimaryPath
    from .tunnel_termination_points import TunnelTerminationPoints
    from .backup_path import BackupPath

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: underlay
        """

        def __init__(self):
            super().__init__(Underlay)

        def __get__(self, instance, owner=None) -> (
                'UnderlayMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'Underlay':
            pass

        def __enter__(self) -> 'Underlay':
            pass


class Underlay(
        YANGContainer,
        metaclass=UnderlayMeta):
    """
    YANG container handler.

    YANG name: underlay
    """

    _yang_name: Final[str] = 'underlay'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'protection-type': (
            protection_type := YANGLeafMember(
                'protection-type',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'enabled': (
            enabled := YANGLeafMember(
                'enabled',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'tunnels': (
            tunnels := (  # YANGContainerMember(
                UnderlayMeta.
                Tunnels.
                yang_container_descriptor())),

        'primary-path': (
            primary_path := (  # YANGContainerMember(
                UnderlayMeta.
                PrimaryPath.
                yang_container_descriptor())),

        'tunnel-termination-points': (
            tunnel_termination_points := (  # YANGContainerMember(
                UnderlayMeta.
                TunnelTerminationPoints.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'backup-path': (
            backup_path := (  # YANGListMember(
                UnderlayMeta.
                BackupPath.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Underlay':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
