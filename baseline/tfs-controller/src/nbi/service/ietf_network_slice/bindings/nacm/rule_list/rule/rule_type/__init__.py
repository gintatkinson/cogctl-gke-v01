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


class RuleTypeMeta(type):
    """
    Metaclass for YANG choice handler.

    YANG name: rule-type
    """

    from .notification import Notification
    from .protocol_operation import ProtocolOperation
    from .data_node import DataNode

    class notification_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: notification
        """

        def __init__(self):
            super().__init__(
                RuleTypeMeta.Notification)

        def __get__(self, instance, owner=None) -> (
                'RuleTypeMeta.notification_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'RuleTypeMeta.Notification'):
            pass

        def __enter__(self) -> (
                'RuleTypeMeta.Notification'):
            pass

    class protocol_operation_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: protocol-operation
        """

        def __init__(self):
            super().__init__(
                RuleTypeMeta.ProtocolOperation)

        def __get__(self, instance, owner=None) -> (
                'RuleTypeMeta.protocol_operation_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'RuleTypeMeta.ProtocolOperation'):
            pass

        def __enter__(self) -> (
                'RuleTypeMeta.ProtocolOperation'):
            pass

    class data_node_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: data-node
        """

        def __init__(self):
            super().__init__(
                RuleTypeMeta.DataNode)

        def __get__(self, instance, owner=None) -> (
                'RuleTypeMeta.data_node_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'RuleTypeMeta.DataNode'):
            pass

        def __enter__(self) -> (
                'RuleTypeMeta.DataNode'):
            pass


class RuleType(YANGChoice, metaclass=RuleTypeMeta):
    """
    YANG choice handler.

    YANG name: rule-type
    """

    _yang_name: Final[str] = 'rule-type'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    _yang_module_name: Final[str] = 'ietf-netconf-acm'

    _yang_cases: Final[Dict[str, YANGChoiceCase]] = {

        'notification': (
            notification := (  # YANGChoiceCase(
                RuleTypeMeta.
                notification_case_descriptor())),

        'protocol-operation': (
            protocol_operation := (  # YANGChoiceCase(
                RuleTypeMeta.
                protocol_operation_case_descriptor())),

        'data-node': (
            data_node := (  # YANGChoiceCase(
                RuleTypeMeta.
                data_node_case_descriptor())),
    }
