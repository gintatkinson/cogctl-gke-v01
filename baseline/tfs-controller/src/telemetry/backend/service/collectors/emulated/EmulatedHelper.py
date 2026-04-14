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

from anytree import Node
import json
from typing import Any, List


class EmulatedCollectorHelper:
    """
    Helper class for the emulated collector.
    """
    def __init__(self):
        pass

    def validate_resource_key(self, key: str) -> str:
        """
        Splits the input string into two parts: 
        - The first part is '_connect/settings/endpoints/'.
        - The second part is the remaining string after the first part, with '/' replaced by '_'.
        
        Args:
            key (str): The input string to process.
            
        Returns:
            str: A single string with the processed result.
        """
        prefix = '_connect/settings/endpoints/'
        if not key.startswith(prefix):
            raise ValueError(f"The input path '{key}' does not start with the expected prefix: {prefix}")
        second_part = key[len(prefix):]
        second_part_processed = second_part.replace('/', '_')
        validated_key = prefix + second_part_processed
        return validated_key

#--------------------------------------------------------------------------------------
# ------- Below function is kept for debugging purposes (test-cases) only -------------
#--------------------------------------------------------------------------------------

#  This below methods can be commented but are called by the SetConfig method in EmulatedCollector.py

    def _find_or_create_node(self, name: str, parent: Node) -> Node:
        """
        Finds or creates a node with the given name under the specified parent.

        Args:
            name (str): The name of the node to find or create.
            parent (Node): The parent node.

        Returns:
            Node: The found or created node.
        """
        node = next((child for child in parent.children if child.name == name), None)
        if not node:
            node = Node(name, parent=parent)
        return node


    def _create_or_update_node(self, name: str, parent: Node, value: Any):
        """
        Creates or updates a node with the given name and value under the specified parent.

        Args:
            name (str): The name of the node.
            parent (Node): The parent node.
            value (Any): The value to set on the node.
        """
        node = next((child for child in parent.children if child.name == name), None)
        if node:
            node.value = json.dumps(value)
        else:
            Node(name, parent=parent, value=json.dumps(value))


    def _parse_resource_key(self, resource_key: str) -> List[str]:
        """
        Parses the resource key into parts, correctly handling brackets.

        Args:
            resource_key (str): The resource key to parse.

        Returns:
            List[str]: A list of parts from the resource key.
        """
        resource_path = []
        current_part = ""
        in_brackets = False

        if not resource_key.startswith('/interface'):
            for char in resource_key.strip('/'):
                if char == '[':
                    in_brackets = True
                    current_part += char
                elif char == ']':
                    in_brackets = False
                    current_part += char
                elif char == '/' and not in_brackets:
                    resource_path.append(current_part)
                    current_part = ""
                else:
                    current_part += char
            if current_part:
                resource_path.append(current_part)
            return resource_path
        else:
            resource_path = resource_key.strip('/').split('/', 1)
            if resource_path[1] == 'settings':
                return resource_path
            else:
                resource_path = [resource_key.strip('/').split('[')[0].strip('/'), resource_key.strip('/').split('[')[1].split(']')[0].replace('/', '_')]
                return resource_path


#-----------------------------------
# ------- EXTRA Methods ------------
#-----------------------------------

    # def _generate_subtree(self, node: Node) -> dict:
    #     """
    #     Generates a subtree of the configuration tree starting from the specified node.

    #     Args:
    #         node (Node): The node from which to generate the subtree.

    #     Returns:
    #         dict: The subtree as a dictionary.
    #     """
    #     subtree = {}
    #     for child in node.children:
    #         if child.children:
    #             subtree[child.name] = self._generate_subtree(child)
    #         else:
    #             value = getattr(child, "value", None)
    #             subtree[child.name] = json.loads(value) if value else None
    #     return subtree


    # def _find_or_raise_node(self, name: str, parent: Node) -> Node:
    #     """
    #     Finds a node with the given name under the specified parent or raises an exception if not found.

    #     Args:
    #         name (str): The name of the node to find.
    #         parent (Node): The parent node.

    #     Returns:
    #         Node: The found node.

    #     Raises:
    #         ValueError: If the node is not found.
    #     """
    #     node = next((child for child in parent.children if child.name == name), None)
    #     if not node:
    #         raise ValueError(f"Node '{name}' not found under parent '{parent.name}'.")
    #     return node
