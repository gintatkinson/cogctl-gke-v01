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


class ConnectivityConstructTypeMeta(type):
    """
    Metaclass for YANG choice handler.

    YANG name: connectivity-construct-type
    """

    from .p2mp import P2mp
    from .a2a import A2a
    from .p2p import P2p

    class p2mp_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: p2mp
        """

        def __init__(self):
            super().__init__(
                ConnectivityConstructTypeMeta.P2mp)

        def __get__(self, instance, owner=None) -> (
                'ConnectivityConstructTypeMeta.p2mp_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'ConnectivityConstructTypeMeta.P2mp'):
            pass

        def __enter__(self) -> (
                'ConnectivityConstructTypeMeta.P2mp'):
            pass

    class a2a_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: a2a
        """

        def __init__(self):
            super().__init__(
                ConnectivityConstructTypeMeta.A2a)

        def __get__(self, instance, owner=None) -> (
                'ConnectivityConstructTypeMeta.a2a_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'ConnectivityConstructTypeMeta.A2a'):
            pass

        def __enter__(self) -> (
                'ConnectivityConstructTypeMeta.A2a'):
            pass

    class p2p_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: p2p
        """

        def __init__(self):
            super().__init__(
                ConnectivityConstructTypeMeta.P2p)

        def __get__(self, instance, owner=None) -> (
                'ConnectivityConstructTypeMeta.p2p_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'ConnectivityConstructTypeMeta.P2p'):
            pass

        def __enter__(self) -> (
                'ConnectivityConstructTypeMeta.P2p'):
            pass


class ConnectivityConstructType(YANGChoice, metaclass=ConnectivityConstructTypeMeta):
    """
    YANG choice handler.

    YANG name: connectivity-construct-type
    """

    _yang_name: Final[str] = 'connectivity-construct-type'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_cases: Final[Dict[str, YANGChoiceCase]] = {

        'p2mp': (
            p2mp := (  # YANGChoiceCase(
                ConnectivityConstructTypeMeta.
                p2mp_case_descriptor())),

        'a2a': (
            a2a := (  # YANGChoiceCase(
                ConnectivityConstructTypeMeta.
                a2a_case_descriptor())),

        'p2p': (
            p2p := (  # YANGChoiceCase(
                ConnectivityConstructTypeMeta.
                p2p_case_descriptor())),
    }
