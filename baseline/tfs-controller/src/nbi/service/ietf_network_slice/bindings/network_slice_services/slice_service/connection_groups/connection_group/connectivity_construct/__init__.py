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


class ConnectivityConstructMeta(type):
    """
    Metaclass for YANG list item handler.

    YANG name: connectivity-construct
    """
    from .connectivity_construct_monitoring import ConnectivityConstructMonitoring
    from .slo_sle_policy import SloSlePolicy
    from .connectivity_construct_type import ConnectivityConstructType

    class yang_list_descriptor(
            YANGListMember):
        """
        YANG list descriptor class.

        YANG name: connectivity-construct
        """

        def __init__(self):
            super().__init__(ConnectivityConstruct)

        def __get__(self, instance, owner=None) -> (
                'ConnectivityConstructMeta.yang_list_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> List['ConnectivityConstruct']:
            pass

        def __iter__(self, key) -> Iterator['ConnectivityConstruct']:
            return super().__iter__()

        def __getitem__(self, key) -> 'ConnectivityConstruct':
            return super()[key]

        def __enter__(self) -> (
                'ConnectivityConstructMeta.yang_list_descriptor'):
            pass


class ConnectivityConstruct(
        YANGListItem,
        metaclass=ConnectivityConstructMeta):
    """
    YANG list item handler.

    YANG name: connectivity-construct
    """

    _yang_name: Final[str] = 'connectivity-construct'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_list_key_names: Final[Tuple[str]] = (
        'cc-id',
    )

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'service-slo-sle-policy-override': (
            service_slo_sle_policy_override := YANGLeafMember(
                'service-slo-sle-policy-override',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'cc-id': (
            cc_id := YANGLeafMember(
                'cc-id',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'connectivity-construct-monitoring': (
            connectivity_construct_monitoring := (  # YANGContainerMember(
                ConnectivityConstructMeta.
                ConnectivityConstructMonitoring.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'ConnectivityConstruct':
        instance = super().__new__(cls)
        instance._yang_choices = {

            'slo-sle-policy':
                ConnectivityConstructMeta.SloSlePolicy(
                    instance),

            'connectivity-construct-type':
                ConnectivityConstructMeta.ConnectivityConstructType(
                    instance),
        }
        return instance

    @property
    def slo_sle_policy(self) -> (
            ConnectivityConstructMeta.SloSlePolicy):
        return self._yang_choices['slo-sle-policy']

    @property
    def connectivity_construct_type(self) -> (
            ConnectivityConstructMeta.ConnectivityConstructType):
        return self._yang_choices['connectivity-construct-type']
