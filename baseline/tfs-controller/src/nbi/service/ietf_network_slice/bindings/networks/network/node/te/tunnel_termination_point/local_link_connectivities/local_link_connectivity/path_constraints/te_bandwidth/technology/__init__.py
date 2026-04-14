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


class TechnologyMeta(type):
    """
    Metaclass for YANG choice handler.

    YANG name: technology
    """

    from .generic import Generic

    class generic_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: generic
        """

        def __init__(self):
            super().__init__(
                TechnologyMeta.Generic)

        def __get__(self, instance, owner=None) -> (
                'TechnologyMeta.generic_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'TechnologyMeta.Generic'):
            pass

        def __enter__(self) -> (
                'TechnologyMeta.Generic'):
            pass


class Technology(YANGChoice, metaclass=TechnologyMeta):
    """
    YANG choice handler.

    YANG name: technology
    """

    _yang_name: Final[str] = 'technology'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_cases: Final[Dict[str, YANGChoiceCase]] = {

        'generic': (
            generic := (  # YANGChoiceCase(
                TechnologyMeta.
                generic_case_descriptor())),
    }
