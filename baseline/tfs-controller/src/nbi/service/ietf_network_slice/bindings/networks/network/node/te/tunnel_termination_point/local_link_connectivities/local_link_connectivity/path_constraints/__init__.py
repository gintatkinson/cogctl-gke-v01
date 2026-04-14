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


class PathConstraintsMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: path-constraints
    """
    from .path_srlgs_names import PathSrlgsNames
    from .path_affinities_values import PathAffinitiesValues
    from .path_srlgs_lists import PathSrlgsLists
    from .path_metric_bounds import PathMetricBounds
    from .te_bandwidth import TeBandwidth
    from .path_affinity_names import PathAffinityNames

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: path-constraints
        """

        def __init__(self):
            super().__init__(PathConstraints)

        def __get__(self, instance, owner=None) -> (
                'PathConstraintsMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'PathConstraints':
            pass

        def __enter__(self) -> 'PathConstraints':
            pass


class PathConstraints(
        YANGContainer,
        metaclass=PathConstraintsMeta):
    """
    YANG container handler.

    YANG name: path-constraints
    """

    _yang_name: Final[str] = 'path-constraints'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {

        'setup-priority': (
            setup_priority := YANGLeafMember(
                'setup-priority',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'link-protection': (
            link_protection := YANGLeafMember(
                'link-protection',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'disjointness': (
            disjointness := YANGLeafMember(
                'disjointness',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'signaling-type': (
            signaling_type := YANGLeafMember(
                'signaling-type',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),

        'hold-priority': (
            hold_priority := YANGLeafMember(
                'hold-priority',
                'urn:ietf:params:xml:ns:yang:ietf-te-topology',
                'ietf-te-topology')),
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'path-srlgs-names': (
            path_srlgs_names := (  # YANGContainerMember(
                PathConstraintsMeta.
                PathSrlgsNames.
                yang_container_descriptor())),

        'path-affinities-values': (
            path_affinities_values := (  # YANGContainerMember(
                PathConstraintsMeta.
                PathAffinitiesValues.
                yang_container_descriptor())),

        'path-srlgs-lists': (
            path_srlgs_lists := (  # YANGContainerMember(
                PathConstraintsMeta.
                PathSrlgsLists.
                yang_container_descriptor())),

        'path-metric-bounds': (
            path_metric_bounds := (  # YANGContainerMember(
                PathConstraintsMeta.
                PathMetricBounds.
                yang_container_descriptor())),

        'te-bandwidth': (
            te_bandwidth := (  # YANGContainerMember(
                PathConstraintsMeta.
                TeBandwidth.
                yang_container_descriptor())),

        'path-affinity-names': (
            path_affinity_names := (  # YANGContainerMember(
                PathConstraintsMeta.
                PathAffinityNames.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'PathConstraints':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
