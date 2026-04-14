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


class PathPropertiesMeta(type):
    """
    Metaclass for YANG container handler.

    YANG name: path-properties
    """
    from .path_affinities_values import PathAffinitiesValues
    from .path_route_objects import PathRouteObjects
    from .path_srlgs_lists import PathSrlgsLists
    from .path_affinity_names import PathAffinityNames
    from .path_srlgs_names import PathSrlgsNames
    from .path_metric import PathMetric

    class yang_container_descriptor(
            YANGContainerMember):
        """
        YANG container descriptor class.

        YANG name: path-properties
        """

        def __init__(self):
            super().__init__(PathProperties)

        def __get__(self, instance, owner=None) -> (
                'PathPropertiesMeta.yang_container_descriptor'):
            return super().__get__(instance, owner)

        def __call__(self) -> 'PathProperties':
            pass

        def __enter__(self) -> 'PathProperties':
            pass


class PathProperties(
        YANGContainer,
        metaclass=PathPropertiesMeta):
    """
    YANG container handler.

    YANG name: path-properties
    """

    _yang_name: Final[str] = 'path-properties'
    _yang_namespace: Final[str] = 'urn:ietf:params:xml:ns:yang:ietf-te-topology'
    _yang_module_name: Final[str] = 'ietf-te-topology'

    _yang_leaf_members: Final[Dict[str, YANGLeafMember]] = {
    }

    _yang_container_members: Final[Dict[str, YANGContainerMember]] = {

        'path-affinities-values': (
            path_affinities_values := (  # YANGContainerMember(
                PathPropertiesMeta.
                PathAffinitiesValues.
                yang_container_descriptor())),

        'path-route-objects': (
            path_route_objects := (  # YANGContainerMember(
                PathPropertiesMeta.
                PathRouteObjects.
                yang_container_descriptor())),

        'path-srlgs-lists': (
            path_srlgs_lists := (  # YANGContainerMember(
                PathPropertiesMeta.
                PathSrlgsLists.
                yang_container_descriptor())),

        'path-affinity-names': (
            path_affinity_names := (  # YANGContainerMember(
                PathPropertiesMeta.
                PathAffinityNames.
                yang_container_descriptor())),

        'path-srlgs-names': (
            path_srlgs_names := (  # YANGContainerMember(
                PathPropertiesMeta.
                PathSrlgsNames.
                yang_container_descriptor())),
    }

    _yang_list_members: Final[Dict[str, YANGListMember]] = {

        'path-metric': (
            path_metric := (  # YANGListMember(
                PathPropertiesMeta.
                PathMetric.
                yang_list_descriptor())),
    }

    _yang_choices: Final[Dict[str, YANGChoice]] = None

    def __new__(cls, *args, **kwargs) -> 'PathProperties':
        instance = super().__new__(cls)
        instance._yang_choices = {
        }
        return instance
