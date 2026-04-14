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


class MaxLinkBandwidthMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: max-link-bandwidth
    """
    from .te_bandwidth import TeBandwidth

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: max-link-bandwidth
        """

        def __init__(self):
            super().__init__(MaxLinkBandwidth)

        def __get__(self, instance, owner=None) -> (
                'MaxLinkBandwidthMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'MaxLinkBandwidth':
            pass

        def __enter__(self) -> 'MaxLinkBandwidth':
            pass


class MaxLinkBandwidth(
        YANGContainer,
        metaclass=MaxLinkBandwidthMeta):
    """
    YANG container handler.

    YANG name: max-link-bandwidth
    """

    _yang_name: Final[str] = 'max-link-bandwidth'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'te-bandwidth': (
            te_bandwidth := (  # YANGContainerMember(
                MaxLinkBandwidthMeta.
                TeBandwidth.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'MaxLinkBandwidth':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
