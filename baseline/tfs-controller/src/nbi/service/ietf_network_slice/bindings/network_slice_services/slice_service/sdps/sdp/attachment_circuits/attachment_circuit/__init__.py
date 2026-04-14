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


class AttachmentCircuitMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: attachment-circuit
    """
    from .ac_tags import AcTags
    from .outgoing_qos_policy import OutgoingQosPolicy
    from .incoming_qos_policy import IncomingQosPolicy
    from .sdp_peering import SdpPeering

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: attachment-circuit
        """

        def __init__(self):
            super().__init__(AttachmentCircuit)

        def __get__(self, instance, owner=None) -> (
                'AttachmentCircuitMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['AttachmentCircuit']:
            pass

        def __iter__(self, key) -> Iterator['AttachmentCircuit']:
            return super().__iter__()

        def __getitem__(self, key) -> 'AttachmentCircuit':
            return super()[key]

        def __enter__(self) -> (
                'AttachmentCircuitMeta.yang_list_descriptor'):
            pass


class AttachmentCircuit(
        YANGListItem,
        metaclass=AttachmentCircuitMeta):
    """
    YANG list item handler.

    YANG name: attachment-circuit
    """

    _yang_name: Final[str] = 'attachment-circuit'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'ac-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'ac-node-id': (
            ac_node_id := YANGLeafMember(
                'ac-node-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'ac-tp-id': (
            ac_tp_id := YANGLeafMember(
                'ac-tp-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'ac-ip-prefix-length': (
            ac_ip_prefix_length := YANGLeafMember(
                'ac-ip-prefix-length',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'ac-ip-address': (
            ac_ip_address := YANGLeafMember(
                'ac-ip-address',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'mtu': (
            mtu := YANGLeafMember(
                'mtu',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'ac-description': (
            ac_description := YANGLeafMember(
                'ac-description',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'ac-id': (
            ac_id := YANGLeafMember(
                'ac-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'peer-sap-id': (
            peer_sap_id := YANGLeafMember(
                'peer-sap-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'ac-tags': (
            ac_tags := (  # YANGContainerMember(
                AttachmentCircuitMeta.
                AcTags.
                yang_container_descriptor())),

        'outgoing-qos-policy': (
            outgoing_qos_policy := (  # YANGContainerMember(
                AttachmentCircuitMeta.
                OutgoingQosPolicy.
                yang_container_descriptor())),

        'incoming-qos-policy': (
            incoming_qos_policy := (  # YANGContainerMember(
                AttachmentCircuitMeta.
                IncomingQosPolicy.
                yang_container_descriptor())),

        'sdp-peering': (
            sdp_peering := (  # YANGContainerMember(
                AttachmentCircuitMeta.
                SdpPeering.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'AttachmentCircuit':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
