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


class RuleMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: rule
    """
    from .rule_type import RuleType

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: rule
        """

        def __init__(self):
            super().__init__(Rule)

        def __get__(self, instance, owner=None) -> (
                'RuleMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['Rule']:
            pass

        def __iter__(self, key) -> Iterator['Rule']:
            return super().__iter__()

        def __getitem__(self, key) -> 'Rule':
            return super()[key]

        def __enter__(self) -> (
                'RuleMeta.yang_list_descriptor'):
            pass


class Rule(
        YANGListItem,
        metaclass=RuleMeta):
    """
    YANG list item handler.

    YANG name: rule
    """

    _yang_name: Final[str] = 'rule'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-netconf-acm'
    _yang_module_name: Final[str] = 'ietf-netconf-acm'

    _yang_list_key_names: Final[Tuple[str]] = (
        'name',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'action': (
            action := YANGLeafMember(
                'action',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'access-operations': (
            access_operations := YANGLeafMember(
                'access-operations',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'comment': (
            comment := YANGLeafMember(
                'comment',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'name': (
            name := YANGLeafMember(
                'name',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),

        'module-name': (
            module_name := YANGLeafMember(
                'module-name',
                'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',
                'ietf-netconf-acm')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Rule':
        instance = super().__new__(cls)
        instance._yang_choices = {

            'rule-type':
                RuleMeta.RuleType(
                    instance),
        }
        return instance

    @property
    def rule_type(self) -> (
            RuleMeta.RuleType):
        return self._yang_choices['rule-type']
