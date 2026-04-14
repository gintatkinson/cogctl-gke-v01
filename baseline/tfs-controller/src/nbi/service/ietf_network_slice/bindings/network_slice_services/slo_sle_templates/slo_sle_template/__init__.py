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


class SloSleTemplateMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: slo-sle-template
    """
    from .service_slo_sle_policy import ServiceSloSlePolicy

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: slo-sle-template
        """

        def __init__(self):
            super().__init__(SloSleTemplate)

        def __get__(self, instance, owner=None) -> (
                'SloSleTemplateMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['SloSleTemplate']:
            pass

        def __iter__(self, key) -> Iterator['SloSleTemplate']:
            return super().__iter__()

        def __getitem__(self, key) -> 'SloSleTemplate':
            return super()[key]

        def __enter__(self) -> (
                'SloSleTemplateMeta.yang_list_descriptor'):
            pass


class SloSleTemplate(
        YANGListItem,
        metaclass=SloSleTemplateMeta):
    """
    YANG list item handler.

    YANG name: slo-sle-template
    """

    _yang_name: Final[str] = 'slo-sle-template'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'id': (
            id := YANGLeafMember(
                'id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'template-ref': (
            template_ref := YANGLeafMember(
                'template-ref',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'template-description': (
            template_description := YANGLeafMember(
                'template-description',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'service-slo-sle-policy': (
            service_slo_sle_policy := (  # YANGContainerMember(
                SloSleTemplateMeta.
                ServiceSloSlePolicy.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'SloSleTemplate':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
