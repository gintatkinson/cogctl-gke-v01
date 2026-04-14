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


class StatisticsMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: statistics
    """

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: statistics
        """

        def __init__(self):
            super().__init__(Statistics)

        def __get__(self, instance, owner=None) -> (
                'StatisticsMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'Statistics':
            pass

        def __enter__(self) -> 'Statistics':
            pass


class Statistics(
        YANGContainer,
        metaclass=StatisticsMeta):
    """
    YANG container handler.

    YANG name: statistics
    """

    _yang_name: Final[str] = 'statistics'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'enables': (
            enables := YANGLeafMember(
                'enables',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'modifies': (
            modifies := YANGLeafMember(
                'modifies',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'fault-detects': (
            fault_detects := YANGLeafMember(
                'fault-detects',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'restoration-failures': (
            restoration_failures := YANGLeafMember(
                'restoration-failures',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'protection-switches': (
            protection_switches := YANGLeafMember(
                'protection-switches',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'downs': (
            downs := YANGLeafMember(
                'downs',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'restoration-successes': (
            restoration_successes := YANGLeafMember(
                'restoration-successes',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'restoration-reversion-starts': (
            restoration_reversion_starts := YANGLeafMember(
                'restoration-reversion-starts',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'maintenance-clears': (
            maintenance_clears := YANGLeafMember(
                'maintenance-clears',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'protection-reverts': (
            protection_reverts := YANGLeafMember(
                'protection-reverts',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'restoration-reversion-successes': (
            restoration_reversion_successes := YANGLeafMember(
                'restoration-reversion-successes',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'ups': (
            ups := YANGLeafMember(
                'ups',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'restoration-starts': (
            restoration_starts := YANGLeafMember(
                'restoration-starts',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'discontinuity-time': (
            discontinuity_time := YANGLeafMember(
                'discontinuity-time',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'disables': (
            disables := YANGLeafMember(
                'disables',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'fault-clears': (
            fault_clears := YANGLeafMember(
                'fault-clears',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'maintenance-sets': (
            maintenance_sets := YANGLeafMember(
                'maintenance-sets',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'restoration-reversion-failures': (
            restoration_reversion_failures := YANGLeafMember(
                'restoration-reversion-failures',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Statistics':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
