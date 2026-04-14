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


class ServiceSloSlePolicyMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: service-slo-sle-policy
    """
    from .steering_constraints import SteeringConstraints
    from .metric_bounds import MetricBounds

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: service-slo-sle-policy
        """

        def __init__(self):
            super().__init__(ServiceSloSlePolicy)

        def __get__(self, instance, owner=None) -> (
                'ServiceSloSlePolicyMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'ServiceSloSlePolicy':
            pass

        def __enter__(self) -> 'ServiceSloSlePolicy':
            pass


class ServiceSloSlePolicy(
        YANGContainer,
        metaclass=ServiceSloSlePolicyMeta):
    """
    YANG container handler.

    YANG name: service-slo-sle-policy
    """

    _yang_name: Final[str] = 'service-slo-sle-policy'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-network-slice-service'
    _yang_module_name: Final[str] = 'ietf-network-slice-service'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'isolation': (
            isolation := YANGLeafMember(
                'isolation',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'mtu': (
            mtu := YANGLeafMember(
                'mtu',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'max-occupancy-level': (
            max_occupancy_level := YANGLeafMember(
                'max-occupancy-level',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),

        'policy-description': (
            policy_description := YANGLeafMember(
                'policy-description',
                'urn:ietf:params:xml:ns:yang:ietf-network-slice-service',
                'ietf-network-slice-service')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'steering-constraints': (
            steering_constraints := (  # YANGContainerMember(
                ServiceSloSlePolicyMeta.
                SteeringConstraints.
                yang_container_descriptor())),

        'metric-bounds': (
            metric_bounds := (  # YANGContainerMember(
                ServiceSloSlePolicyMeta.
                MetricBounds.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'ServiceSloSlePolicy':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
