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

import anytree
from typing import Any, List, Optional, Union
from apscheduler.job import Job

class TreeNode(anytree.node.Node):
    def __init__(self, name, parent=None, children=None, **kwargs) -> None:
        super().__init__(name, parent=parent, children=children, **kwargs)
        self.value : Optional[Any] = None

    def get_full_path(self):
        return self.separator.join([''] + [str(node.name) for node in self.path])

class RawStyle(anytree.render.AbstractStyle):
    def __init__(self):
        """
        Raw style.

        >>> from anytree import Node, RenderTree
        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)
        >>> print(RenderTree(root, style=RawStyle()))
        Node('/root')
        Node('/root/sub0')
        Node('/root/sub0/sub0B')
        Node('/root/sub0/sub0A')
        Node('/root/sub1')
        """
        super(RawStyle, self).__init__('', '', '')

def get_subnode(
    resolver : anytree.Resolver, root : TreeNode, key_or_path : Union[str, List[str]], default : Optional[Any] = None):

    if isinstance(key_or_path, str): key_or_path = key_or_path.split('/')
    node = root
    for path_item in key_or_path:
        try:
            node = resolver.get(node, path_item)
        except anytree.ChildResolverError:
            return default
    return node

def set_subnode_value(resolver : anytree.Resolver, root : TreeNode, key_or_path : Union[str, List[str]], value : Any):
    if isinstance(key_or_path, str): key_or_path = key_or_path.split('/')
    node = root
    for path_item in key_or_path:
        try:
            node = resolver.get(node, path_item)
        except anytree.ChildResolverError:
            node = TreeNode(path_item, parent=node)
    if isinstance(node.value, dict) and isinstance(value, dict):
        node.value.update(value)
    else:
        node.value = value

def dump_subtree(root : TreeNode):
    if not isinstance(root, TreeNode): raise Exception('root must be a TreeNode')
    results = []
    for row in anytree.RenderTree(root, style=RawStyle()):
        node : TreeNode = row.node
        path = node.get_full_path()[2:] # get full path except the heading root placeholder "/."
        if len(path) == 0: continue
        value = node.value
        if value is None: continue
        if isinstance(value, Job): value = str(value)
        results.append((path, value))
    return results
