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


class BundleStackLevelMeta(type):
    """
    Metaclass for YANG choice handler.

    YANG name: bundle-stack-level
    """

    from .component import Component
    from .bundle import Bundle

    class component_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: component
        """

        def __init__(self):
            super().__init__(
                BundleStackLevelMeta.Component)

        def __get__(self, instance, owner=None) -> (
                'BundleStackLevelMeta.component_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'BundleStackLevelMeta.Component'):
            pass

        def __enter__(self) -> (
                'BundleStackLevelMeta.Component'):
            pass

    class bundle_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: bundle
        """

        def __init__(self):
            super().__init__(
                BundleStackLevelMeta.Bundle)

        def __get__(self, instance, owner=None) -> (
                'BundleStackLevelMeta.bundle_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'BundleStackLevelMeta.Bundle'):
            pass

        def __enter__(self) -> (
                'BundleStackLevelMeta.Bundle'):
            pass


class BundleStackLevel(YANGChoice, metaclass=BundleStackLevelMeta):
    """
    YANG choice handler.

    YANG name: bundle-stack-level
    """

    _yang_name: Final[str] = 'bundle-stack-level'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_cases: Final[Dict[str, YANGChoiceCase]] = {

        'component': (
            component := (  # YANGChoiceCase(
                BundleStackLevelMeta.
                component_case_descriptor())),

        'bundle': (
            bundle := (  # YANGChoiceCase(
                BundleStackLevelMeta.
                bundle_case_descriptor())),
    }
