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


class TypeMeta(type):
    """
    Metaclass for YANG choice handler.

    YANG name: type
    """

    from .as_number import AsNumber
    from .numbered_node_hop import NumberedNodeHop
    from .numbered_link_hop import NumberedLinkHop
    from .unnumbered_link_hop import UnnumberedLinkHop
    from .label import Label
    from .srlg import Srlg

    class as_number_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: as-number
        """

        def __init__(self):
            super().__init__(
                TypeMeta.AsNumber)

        def __get__(self, instance, owner=None) -> (
                'TypeMeta.as_number_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'TypeMeta.AsNumber'):
            pass

        def __enter__(self) -> (
                'TypeMeta.AsNumber'):
            pass

    class numbered_node_hop_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: numbered-node-hop
        """

        def __init__(self):
            super().__init__(
                TypeMeta.NumberedNodeHop)

        def __get__(self, instance, owner=None) -> (
                'TypeMeta.numbered_node_hop_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'TypeMeta.NumberedNodeHop'):
            pass

        def __enter__(self) -> (
                'TypeMeta.NumberedNodeHop'):
            pass

    class numbered_link_hop_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: numbered-link-hop
        """

        def __init__(self):
            super().__init__(
                TypeMeta.NumberedLinkHop)

        def __get__(self, instance, owner=None) -> (
                'TypeMeta.numbered_link_hop_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'TypeMeta.NumberedLinkHop'):
            pass

        def __enter__(self) -> (
                'TypeMeta.NumberedLinkHop'):
            pass

    class unnumbered_link_hop_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: unnumbered-link-hop
        """

        def __init__(self):
            super().__init__(
                TypeMeta.UnnumberedLinkHop)

        def __get__(self, instance, owner=None) -> (
                'TypeMeta.unnumbered_link_hop_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'TypeMeta.UnnumberedLinkHop'):
            pass

        def __enter__(self) -> (
                'TypeMeta.UnnumberedLinkHop'):
            pass

    class label_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: label
        """

        def __init__(self):
            super().__init__(
                TypeMeta.Label)

        def __get__(self, instance, owner=None) -> (
                'TypeMeta.label_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'TypeMeta.Label'):
            pass

        def __enter__(self) -> (
                'TypeMeta.Label'):
            pass

    class srlg_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: srlg
        """

        def __init__(self):
            super().__init__(
                TypeMeta.Srlg)

        def __get__(self, instance, owner=None) -> (
                'TypeMeta.srlg_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'TypeMeta.Srlg'):
            pass

        def __enter__(self) -> (
                'TypeMeta.Srlg'):
            pass


class Type(YANGChoice, metaclass=TypeMeta):
    """
    YANG choice handler.

    YANG name: type
    """

    _yang_name: Final[str] = 'type'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_cases: Final[Dict[str, YANGChoiceCase]] = {

        'as-number': (
            as_number := (  # YANGChoiceCase(
                TypeMeta.
                as_number_case_descriptor())),

        'numbered-node-hop': (
            numbered_node_hop := (  # YANGChoiceCase(
                TypeMeta.
                numbered_node_hop_case_descriptor())),

        'numbered-link-hop': (
            numbered_link_hop := (  # YANGChoiceCase(
                TypeMeta.
                numbered_link_hop_case_descriptor())),

        'unnumbered-link-hop': (
            unnumbered_link_hop := (  # YANGChoiceCase(
                TypeMeta.
                unnumbered_link_hop_case_descriptor())),

        'label': (
            label := (  # YANGChoiceCase(
                TypeMeta.
                label_case_descriptor())),

        'srlg': (
            srlg := (  # YANGChoiceCase(
                TypeMeta.
                srlg_case_descriptor())),
    }
