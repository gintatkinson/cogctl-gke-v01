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


class LocationMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: location
    """

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: location
        """

        def __init__(self):
            super().__init__(Location)

        def __get__(self, instance, owner=None) -> (
                'LocationMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'Location':
            pass

        def __enter__(self) -> 'Location':
            pass


class Location(
        YANGContainer,
        metaclass=LocationMeta):
    """
    YANG container handler.

    YANG name: location
    """

    _yang_name: Final[str] = 'location'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'altitude': (
            altitude := YANGLeafMember(
                'altitude',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'latitude': (
            latitude := YANGLeafMember(
                'latitude',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'longitude': (
            longitude := YANGLeafMember(
                'longitude',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Location':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
