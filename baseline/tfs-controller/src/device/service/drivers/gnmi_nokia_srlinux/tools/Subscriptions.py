# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Collection of samples through NetConf is very slow and each request collects all the data.
# Populate a cache periodically (when first interface is interrogated).
# Evict data after some seconds, when data is considered as outdated

import anytree
from typing import Any, List
from device.service.driver_api.AnyTreeTools import TreeNode, get_subnode, set_subnode_value

class Subscriptions:
    def __init__(self) -> None:
        self.__resolver = anytree.Resolver(pathattr='name')
        self.__subscriptions = TreeNode('.')
    
    def add(
        self, resource_path : List[str], sampling_duration : float, sampling_interval : float, value : Any
    ) -> None:
        subscription_path = resource_path + ['{:.3f}:{:.3f}'.format(sampling_duration, sampling_interval)]
        set_subnode_value(self.__resolver, self.__subscriptions, subscription_path, value)

    def get(
        self, resource_path : List[str], sampling_duration : float, sampling_interval : float
    ) -> TreeNode:
        subscription_path = resource_path + ['{:.3f}:{:.3f}'.format(sampling_duration, sampling_interval)]
        value = get_subnode(self.__resolver, self.__subscriptions, subscription_path)
        return value

    def delete(
        self, reference : TreeNode
    ) -> None:
        parent : TreeNode = reference.parent
        children = list(parent.children)
        children.remove(reference)
        parent.children = tuple(children)
