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


class AlgorithmMeta(type):
    """
    Metaclass for YANG choice handler.

    YANG name: algorithm
    """

    from .metric import Metric
    from .objective_function import ObjectiveFunction

    class metric_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: metric
        """

        def __init__(self):
            super().__init__(
                AlgorithmMeta.Metric)

        def __get__(self, instance, owner=None) -> (
                'AlgorithmMeta.metric_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'AlgorithmMeta.Metric'):
            pass

        def __enter__(self) -> (
                'AlgorithmMeta.Metric'):
            pass

    class objective_function_case_descriptor(YANGChoiceCase):
        """
        YANG choice case descriptor class.

        YANG name: objective-function
        """

        def __init__(self):
            super().__init__(
                AlgorithmMeta.ObjectiveFunction)

        def __get__(self, instance, owner=None) -> (
                'AlgorithmMeta.objective_function_case_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> (
                'AlgorithmMeta.ObjectiveFunction'):
            pass

        def __enter__(self) -> (
                'AlgorithmMeta.ObjectiveFunction'):
            pass


class Algorithm(YANGChoice, metaclass=AlgorithmMeta):
    """
    YANG choice handler.

    YANG name: algorithm
    """

    _yang_name: Final[str] = 'algorithm'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_cases: Final[Dict[str, YANGChoiceCase]] = {

        'metric': (
            metric := (  # YANGChoiceCase(
                AlgorithmMeta.
                metric_case_descriptor())),

        'objective-function': (
            objective_function := (  # YANGChoiceCase(
                AlgorithmMeta.
                objective_function_case_descriptor())),
    }
