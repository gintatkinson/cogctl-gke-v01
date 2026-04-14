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


class SdpMonitoringMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: sdp-monitoring
    """

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: sdp-monitoring
        """

        def __init__(self):
            super().__init__(SdpMonitoring)

        def __get__(self, instance, owner=None) -> (
                'SdpMonitoringMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'SdpMonitoring':
            pass

        def __enter__(self) -> 'SdpMonitoring':
            pass


class SdpMonitoring(
        YANGContainer,
        metaclass=SdpMonitoringMeta):
    """
    YANG container handler.

    YANG name: sdp-monitoring
    """

    _yang_name: Final[str] = 'sdp-monitoring'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'incoming-utilized-bandwidth': (
            incoming_utilized_bandwidth := YANGLeafMember(
                'incoming-utilized-bandwidth',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'incoming-bw-utilization': (
            incoming_bw_utilization := YANGLeafMember(
                'incoming-bw-utilization',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'outgoing-bw-utilization': (
            outgoing_bw_utilization := YANGLeafMember(
                'outgoing-bw-utilization',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'outgoing-utilized-bandwidth': (
            outgoing_utilized_bandwidth := YANGLeafMember(
                'outgoing-utilized-bandwidth',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'SdpMonitoring':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
