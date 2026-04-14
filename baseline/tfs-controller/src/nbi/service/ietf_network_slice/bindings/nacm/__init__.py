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


class NacmMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: nacm
    """
    from .groups import Groups
    from .rule_list import RuleList

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: nacm
        """

        def __init__(self):
            super().__init__(Nacm)

        def __get__(self, instance, owner=None) -> (
                'NacmMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'Nacm':
            pass

        def __enter__(self) -> 'Nacm':
            pass


class Nacm(
        YANGContainer,
        metaclass=NacmMeta):
    """
    YANG container handler.

    YANG name: nacm
    """

    _yang_name: Final[str] = 'nacm'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    _yang_module_name: Final[str] = 'ietf-netconf-acm'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'denied-data-writes': (
            denied_data_writes := YANGLeafMember(
                'denied-data-writes',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'exec-default': (
            exec_default := YANGLeafMember(
                'exec-default',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'denied-notifications': (
            denied_notifications := YANGLeafMember(
                'denied-notifications',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'enable-external-groups': (
            enable_external_groups := YANGLeafMember(
                'enable-external-groups',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'enable-nacm': (
            enable_nacm := YANGLeafMember(
                'enable-nacm',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'read-default': (
            read_default := YANGLeafMember(
                'read-default',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'denied-operations': (
            denied_operations := YANGLeafMember(
                'denied-operations',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'write-default': (
            write_default := YANGLeafMember(
                'write-default',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'groups': (
            groups := (  # YANGContainerMember(
                NacmMeta.
                Groups.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'rule-list': (
            rule_list := (  # YANGListMember(
                NacmMeta.
                RuleList.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Nacm':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
