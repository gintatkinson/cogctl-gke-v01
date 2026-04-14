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

import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from device.service.driver_api._Driver import RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES, RESOURCE_ACL
from ._Handler import _Handler
from .Component import ComponentHandler
from .Interface import InterfaceHandler
from .InterfaceCounter import InterfaceCounterHandler
from .NetworkInstance import NetworkInstanceHandler
from .NetworkInstanceInterface import NetworkInstanceInterfaceHandler
from .NetworkInstanceProtocol import NetworkInstanceProtocolHandler
from .NetworkInstanceStaticRoute import NetworkInstanceStaticRouteHandler
from .Acl import AclHandler
from .Tools import get_schema
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

comph  = ComponentHandler()
ifaceh = InterfaceHandler()
ifctrh = InterfaceCounterHandler()
nih    = NetworkInstanceHandler()
niifh  = NetworkInstanceInterfaceHandler()
niph   = NetworkInstanceProtocolHandler()
nisrh  = NetworkInstanceStaticRouteHandler()
aclh   = AclHandler()

ALL_RESOURCE_KEYS = [
    RESOURCE_ENDPOINTS,
    RESOURCE_INTERFACES,
    RESOURCE_NETWORK_INSTANCES,
    RESOURCE_ACL,
]

RESOURCE_KEY_MAPPER = {
    RESOURCE_ENDPOINTS         : comph.get_resource_key(),
    RESOURCE_INTERFACES        : ifaceh.get_resource_key(),
    RESOURCE_NETWORK_INSTANCES : nih.get_resource_key(),
    RESOURCE_ACL               : aclh.get_resource_key(),
}

PATH_MAPPER = {
    '/components'           : comph.get_path(),
    '/components/component' : comph.get_path(),
    '/interfaces'           : ifaceh.get_path(),
    '/network-instances'    : nih.get_path(),
    '/acl'                  : aclh.get_path(),
}

RESOURCE_KEY_TO_HANDLER = {
    comph.get_resource_key()  : comph,
    ifaceh.get_resource_key() : ifaceh,
    ifctrh.get_resource_key() : ifctrh,
    nih.get_resource_key()    : nih,
    niifh.get_resource_key()  : niifh,
    niph.get_resource_key()   : niph,
    nisrh.get_resource_key()  : nisrh,
    aclh.get_resource_key()   : aclh,
}

PATH_TO_HANDLER = {
    comph.get_path()  : comph,
    ifaceh.get_path() : ifaceh,
    ifctrh.get_path() : ifctrh,
    nih.get_path()    : nih,
    niifh.get_path()  : niifh,
    niph.get_path()   : niph,
    nisrh.get_path()  : nisrh,
    aclh.get_path()   : aclh,
}

def get_handler(
    resource_key : Optional[str] = None, path : Optional[str] = None,
    raise_if_not_found=True
) -> Optional[_Handler]:
    if (resource_key is None) == (path is None):
        MSG = 'Exactly one of resource_key({:s}) or path({:s}) must be specified'
        raise Exception(MSG.format(str(resource_key), str(path))) # pylint: disable=broad-exception-raised
    if resource_key is not None:
        resource_key_schema = get_schema(resource_key)
        resource_key_schema = RESOURCE_KEY_MAPPER.get(resource_key_schema, resource_key_schema)
        handler = RESOURCE_KEY_TO_HANDLER.get(resource_key_schema)
        if handler is None and raise_if_not_found:
            MSG = 'Handler not found: resource_key={:s} resource_key_schema={:s}'
            # pylint: disable=broad-exception-raised
            raise Exception(MSG.format(str(resource_key), str(resource_key_schema)))
    elif path is not None:
        path_schema = get_schema(path)
        path_schema = PATH_MAPPER.get(path_schema, path_schema)
        handler = PATH_TO_HANDLER.get(path_schema)
        if handler is None and raise_if_not_found:
            MSG = 'Handler not found: path={:s} path_schema={:s}'
            # pylint: disable=broad-exception-raised
            raise Exception(MSG.format(str(path), str(path_schema)))
    return handler

def get_path(resource_key : str) -> str:
    handler = get_handler(resource_key=resource_key)
    return handler.get_path()

def parse(
    str_path : str, value : Union[Dict, List], yang_handler : YangHandler
) -> List[Tuple[str, Dict[str, Any]]]:
    handler = get_handler(path=str_path)
    return handler.parse(value, yang_handler)

def compose(
    resource_key : str, resource_value : Union[Dict, List],
    yang_handler : YangHandler, delete : bool = False
) -> Tuple[str, str]:
    handler = get_handler(resource_key=resource_key)
    return handler.compose(resource_key, resource_value, yang_handler, delete=delete)
