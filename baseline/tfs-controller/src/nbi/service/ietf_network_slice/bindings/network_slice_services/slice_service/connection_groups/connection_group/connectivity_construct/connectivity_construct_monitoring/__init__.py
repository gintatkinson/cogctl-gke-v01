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


class ConnectivityConstructMonitoringMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: connectivity-construct-monitoring
    """

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: connectivity-construct-monitoring
        """

        def __init__(self):
            super().__init__(ConnectivityConstructMonitoring)

        def __get__(self, instance, owner=None) -> (
                'ConnectivityConstructMonitoringMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'ConnectivityConstructMonitoring':
            pass

        def __enter__(self) -> 'ConnectivityConstructMonitoring':
            pass


class ConnectivityConstructMonitoring(
        YANGContainer,
        metaclass=ConnectivityConstructMonitoringMeta):
    """
    YANG container handler.

    YANG name: connectivity-construct-monitoring
    """

    _yang_name: Final[str] = 'connectivity-construct-monitoring'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'one-way-delay-variation': (
            one_way_delay_variation := YANGLeafMember(
                'one-way-delay-variation',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'two-way-max-delay': (
            two_way_max_delay := YANGLeafMember(
                'two-way-max-delay',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'two-way-packet-loss': (
            two_way_packet_loss := YANGLeafMember(
                'two-way-packet-loss',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'one-way-packet-loss': (
            one_way_packet_loss := YANGLeafMember(
                'one-way-packet-loss',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'one-way-max-delay': (
            one_way_max_delay := YANGLeafMember(
                'one-way-max-delay',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'two-way-delay-variation': (
            two_way_delay_variation := YANGLeafMember(
                'two-way-delay-variation',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'two-way-min-delay': (
            two_way_min_delay := YANGLeafMember(
                'two-way-min-delay',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'one-way-min-delay': (
            one_way_min_delay := YANGLeafMember(
                'one-way-min-delay',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'ConnectivityConstructMonitoring':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
