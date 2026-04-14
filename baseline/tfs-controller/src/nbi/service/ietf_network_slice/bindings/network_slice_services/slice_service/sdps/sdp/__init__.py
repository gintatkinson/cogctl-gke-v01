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


class SdpMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: sdp
    """
    from .sdp_monitoring import SdpMonitoring
    from .outgoing_qos_policy import OutgoingQosPolicy
    from .service_match_criteria import ServiceMatchCriteria
    from .sdp_peering import SdpPeering
    from .status import Status
    from .attachment_circuits import AttachmentCircuits
    from .location import Location
    from .incoming_qos_policy import IncomingQosPolicy

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: sdp
        """

        def __init__(self):
            super().__init__(Sdp)

        def __get__(self, instance, owner=None) -> (
                'SdpMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['Sdp']:
            pass

        def __iter__(self, key) -> Iterator['Sdp']:
            return super().__iter__()

        def __getitem__(self, key) -> 'Sdp':
            return super()[key]

        def __enter__(self) -> (
                'SdpMeta.yang_list_descriptor'):
            pass


class Sdp(
        YANGListItem,
        metaclass=SdpMeta):
    """
    YANG list item handler.

    YANG name: sdp
    """

    _yang_name: Final[str] = 'sdp'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'sdp-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'sdp-id': (
            sdp_id := YANGLeafMember(
                'sdp-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'peer-sap-id': (
            peer_sap_id := YANGLeafMember(
                'peer-sap-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'sdp-description': (
            sdp_description := YANGLeafMember(
                'sdp-description',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'node-id': (
            node_id := YANGLeafMember(
                'node-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'sdp-ip': (
            sdp_ip := YANGLeafMember(
                'sdp-ip',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'ltp': (
            ltp := YANGLeafMember(
                'ltp',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'sdp-monitoring': (
            sdp_monitoring := (  # YANGContainerMember(
                SdpMeta.
                SdpMonitoring.
                yang_container_descriptor())),

        'outgoing-qos-policy': (
            outgoing_qos_policy := (  # YANGContainerMember(
                SdpMeta.
                OutgoingQosPolicy.
                yang_container_descriptor())),

        'service-match-criteria': (
            service_match_criteria := (  # YANGContainerMember(
                SdpMeta.
                ServiceMatchCriteria.
                yang_container_descriptor())),

        'sdp-peering': (
            sdp_peering := (  # YANGContainerMember(
                SdpMeta.
                SdpPeering.
                yang_container_descriptor())),

        'status': (
            status := (  # YANGContainerMember(
                SdpMeta.
                Status.
                yang_container_descriptor())),

        'attachment-circuits': (
            attachment_circuits := (  # YANGContainerMember(
                SdpMeta.
                AttachmentCircuits.
                yang_container_descriptor())),

        'location': (
            location := (  # YANGContainerMember(
                SdpMeta.
                Location.
                yang_container_descriptor())),

        'incoming-qos-policy': (
            incoming_qos_policy := (  # YANGContainerMember(
                SdpMeta.
                IncomingQosPolicy.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Sdp':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
