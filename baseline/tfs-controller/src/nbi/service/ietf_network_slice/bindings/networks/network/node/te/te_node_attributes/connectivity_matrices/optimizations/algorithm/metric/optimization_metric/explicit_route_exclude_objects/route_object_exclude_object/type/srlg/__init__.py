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


class SrlgMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: srlg
    """
    from .srlg import Srlg

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: srlg
        """

        def __init__(self):
            super().__init__(Srlg)

        def __get__(self, instance, owner=None) -> (
                'SrlgMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'Srlg':
            pass

        def __enter__(self) -> 'Srlg':
            pass


class Srlg(
        YANGContainer,
        metaclass=SrlgMeta):
    """
    YANG container handler.

    YANG name: srlg
    """

    _yang_name: Final[str] = 'srlg'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'srlg': (
            srlg := (  # YANGContainerMember(
                SrlgMeta.
                Srlg.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'Srlg':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
