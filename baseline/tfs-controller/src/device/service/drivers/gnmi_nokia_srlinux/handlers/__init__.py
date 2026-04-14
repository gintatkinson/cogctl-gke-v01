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
from typing import Dict, List, Optional, Tuple, Union
from device.service.driver_api._Driver import (
    RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES,
    RESOURCE_NETWORK_INSTANCE_VXLAN, RESOURCE_ROUTING_POLICY, RESOURCE_TUNNEL_INTERFACE
)
from ._Handler import _Handler
from .Component import ComponentHandler
from .Interface import InterfaceHandler
from .InterfaceCounter import InterfaceCounterHandler
from .NetworkInstance import NetworkInstanceHandler
from .NetworkInstanceInterface import NetworkInstanceInterfaceHandler
from .NetworkInstanceVxlanInterface import NetworkInstanceVxlanInterfacehandler
from .RoutingPolicy import RoutingPolicyHandler
from .TunnelInterface import TunnelInterfaceHandler
from .Tools import get_schema


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

comph  = ComponentHandler()
ifaceh = InterfaceHandler()
ifctrh = InterfaceCounterHandler()
nih    = NetworkInstanceHandler()
niifh  = NetworkInstanceInterfaceHandler()
nivi   = NetworkInstanceVxlanInterfacehandler()
rp     = RoutingPolicyHandler()
ti     = TunnelInterfaceHandler()


ALL_RESOURCE_KEYS = [
    RESOURCE_ENDPOINTS,
    RESOURCE_INTERFACES,
    RESOURCE_NETWORK_INSTANCES,
    RESOURCE_NETWORK_INSTANCE_VXLAN,
    RESOURCE_ROUTING_POLICY,
    RESOURCE_TUNNEL_INTERFACE,
]

RESOURCE_KEY_MAPPER = {
    RESOURCE_ENDPOINTS              : comph.get_resource_key(),
    RESOURCE_INTERFACES             : ifaceh.get_resource_key(),
    RESOURCE_NETWORK_INSTANCES      : nih.get_resource_key(),
    RESOURCE_NETWORK_INSTANCE_VXLAN : nivi.get_resource_key(),
    RESOURCE_ROUTING_POLICY         : rp.get_resource_key(),
    RESOURCE_TUNNEL_INTERFACE       : ti.get_resource_key(),
}

PATH_MAPPER = {
    '/components'                 : comph.get_path(),
    '/interface'                  : ifaceh.get_path(),
    '/network-instance'           : nih.get_path(),
    '/network-instance/interface' : nivi.get_path(),
    '/routing-policy'             : rp.get_path(),
    '/tunnel-interface'           : ti.get_path(),

}

RESOURCE_KEY_TO_HANDLER = {
    comph.get_resource_key()  : comph,
    ifaceh.get_resource_key() : ifaceh,
    ifctrh.get_resource_key() : ifctrh,
    nih.get_resource_key()    : nih,
    niifh.get_resource_key()  : niifh,
    nivi.get_resource_key()   : nivi,
    rp.get_resource_key()     : rp,
    ti.get_resource_key()     :ti,

}

PATH_TO_HANDLER = {
    comph.get_path()  : comph,
    ifaceh.get_path() : ifaceh,
    ifctrh.get_path() : ifctrh,
    nih.get_path()    : nih,
    niifh.get_path()  : niifh,
    nivi.get_path()   : nivi,
    rp.get_path()     :rp,
    ti.get_path()     :ti,
}

def get_handler(
    resource_key: Optional[str] = None, path: Optional[str] = None, raise_if_not_found=True
) -> Optional[_Handler]:
    if (resource_key is None) == (path is None):
        MSG = 'Exactly one of resource_key({:s}) or path({:s}) must be specified'
        raise Exception(MSG.format(str(resource_key), str(path)))  # pylint: disable=broad-exception-raised
    if resource_key is not None:
        resource_key_schema = get_schema(resource_key)
        resource_key_schema = RESOURCE_KEY_MAPPER.get(resource_key_schema, resource_key_schema)
        handler = RESOURCE_KEY_TO_HANDLER.get(resource_key_schema)
        if handler is None and raise_if_not_found:
            MSG = 'Handler not found: resource_key={:s} resource_key_schema={:s}'
            raise Exception(MSG.format(str(resource_key), str(resource_key_schema)))
    elif path is not None:
        path_schema = get_schema(path)
        path_schema = PATH_MAPPER.get(path_schema, path_schema)
        #LOGGER.debug("Original path: %s, Schema path: %s", path, path_schema)
        handler = PATH_TO_HANDLER.get(path_schema)
        LOGGER.debug("Mapped path schema: %s", path_schema)
        if handler is None and raise_if_not_found:
            MSG = 'Handler not found: path={:s} path_schema={:s}'
            LOGGER.error(MSG.format(str(path), str(path_schema)))
            raise Exception(MSG.format(str(path), str(path_schema)))
        LOGGER.debug("Handler found for path: %s", handler.get_path())  
    return handler



def get_path(resource_key: str) -> str:
    handler = get_handler(resource_key=resource_key)
    path = handler.get_path()
    #LOGGER.debug("get_path: resource_key=%s, path=%s", resource_key, path)
    return path

def parse(resource_key: str, str_path: str, value: Union[Dict, List]):
    #if str_path == '/': str_path = '/{:s}'.format(list(value.keys())[0])
    handler = get_handler(resource_key=resource_key)
    #LOGGER.debug("parse: str_path=%s, value=%s", str_path, value)
    return handler.parse(value)

def compose(resource_key: str, resource_value: Union[Dict, List], delete: bool = False) -> Tuple[str, str]:
    handler = get_handler(resource_key=resource_key)
    #LOGGER.debug("compose: resource_key=%s, resource_value=%s, delete=%s", resource_key, resource_value, delete)
    return handler.compose(resource_key, resource_value, delete=delete)

#def get_path(resource_key : str) -> str:
#    return get_handler(resource_key=resource_key).get_path()
#
#def parse(str_path : str, value : Union[Dict, List]):
#    return get_handler(path=str_path).parse(value)
#
#def compose(resource_key : str, resource_value : Union[Dict, List], delete : bool = False) -> Tuple[str, str]:
#    return get_handler(resource_key=resource_key).compose(resource_key, resource_value, delete=delete)
