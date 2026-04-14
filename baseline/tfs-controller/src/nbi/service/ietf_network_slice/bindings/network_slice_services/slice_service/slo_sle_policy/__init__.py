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


class SloSlePolicyMeta(type):
    """
    Metaclass for YANG choice handler.

    YANG name: slo-sle-policy
    """

    from .standard import Standard
    from .custom import Custom

    class standard_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: standard
        """

        def __init__(self):
            super().__init__(
                SloSlePolicyMeta.Standard)

        def __get__(self, instance, owner=None) -> (
                'SloSlePolicyMeta.standard_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'SloSlePolicyMeta.Standard'):
            pass

        def __enter__(self) -> (
                'SloSlePolicyMeta.Standard'):
            pass

    class custom_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: custom
        """

        def __init__(self):
            super().__init__(
                SloSlePolicyMeta.Custom)

        def __get__(self, instance, owner=None) -> (
                'SloSlePolicyMeta.custom_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'SloSlePolicyMeta.Custom'):
            pass

        def __enter__(self) -> (
                'SloSlePolicyMeta.Custom'):
            pass


class SloSlePolicy(YANGChoice, metaclass=SloSlePolicyMeta):
    """
    YANG choice handler.

    YANG name: slo-sle-policy
    """

    _yang_name: Final[str] = 'slo-sle-policy'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_cases: Final[Dict[str, YANGChoiceCase]] = {

        'standard': (
            standard := (  # YANGChoiceCase(
                SloSlePolicyMeta.
                standard_case_descriptor())),

        'custom': (
            custom := (  # YANGChoiceCase(
                SloSlePolicyMeta.
                custom_case_descriptor())),
    }
