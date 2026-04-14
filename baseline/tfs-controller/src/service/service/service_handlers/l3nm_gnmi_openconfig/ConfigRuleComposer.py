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

import json, logging, netaddr, re
from typing import Dict, List, Optional, Set, Tuple
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import ConfigActionEnum, Device, EndPoint, Service
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from service.service.service_handler_api.AnyTreeTools import TreeNode

LOGGER = logging.getLogger(__name__)

#NETWORK_INSTANCE = 'teraflowsdn' # TODO: investigate; sometimes it does not create/delete static rules properly
NETWORK_INSTANCE = 'default'
DEFAULT_NETWORK_INSTANCE = 'default'

RE_IF    = re.compile(r'^\/interface\[([^\]]+)\]$')
RE_SUBIF = re.compile(r'^\/interface\[([^\]]+)\]\/subinterface\[([^\]]+)\]$')
RE_SR    = re.compile(r'^\/network_instance\[([^\]]+)\]\/protocols\[STATIC\]/route\[([^\:]+)\:([^\]]+)\]$')

def _interface(
    interface : str, if_type : Optional[str] = 'l3ipvlan', index : int = 0, vlan_id : Optional[int] = None,
    address_ip : Optional[str] = None, address_prefix : Optional[int] = None, mtu : Optional[int] = None,
    enabled : bool = True
) -> Tuple[str, Dict]:
    path = '/interface[{:s}]/subinterface[{:d}]'.format(interface, index)
    data = {'name': interface, 'type': if_type, 'index': index, 'enabled': enabled}
    if if_type is not None: data['type'] = if_type
    if vlan_id is not None: data['vlan_id'] = vlan_id
    if address_ip is not None: data['address_ip'] = address_ip
    if address_prefix is not None: data['address_prefix'] = address_prefix
    if mtu is not None: data['mtu'] = mtu
    return path, data

def _network_instance(ni_name : str, ni_type : str) -> Tuple[str, Dict]:
    path = '/network_instance[{:s}]'.format(ni_name)
    data = {'name': ni_name, 'type': ni_type}
    return path, data

def _network_instance_protocol(ni_name : str, protocol : str) -> Tuple[str, Dict]:
    path = '/network_instance[{:s}]/protocols[{:s}]'.format(ni_name, protocol)
    data = {'name': ni_name, 'identifier': protocol, 'protocol_name': protocol}
    return path, data

def _network_instance_protocol_static(ni_name : str) -> Tuple[str, Dict]:
    return _network_instance_protocol(ni_name, 'STATIC')

def _network_instance_protocol_static_route(
    ni_name : str, prefix : str, next_hop : str, metric : int
) -> Tuple[str, Dict]:
    protocol = 'STATIC'
    path = '/network_instance[{:s}]/protocols[{:s}]/static_route[{:s}:{:d}]'.format(ni_name, protocol, prefix, metric)
    index = 'AUTO_{:d}_{:s}'.format(metric, next_hop.replace('.', '-'))
    data = {
        'name': ni_name, 'identifier': protocol, 'protocol_name': protocol,
        'prefix': prefix, 'index': index, 'next_hop': next_hop, 'metric': metric
    }
    return path, data

def _network_instance_interface(ni_name : str, interface : str, sub_interface_index : int) -> Tuple[str, Dict]:
    sub_interface_name = '{:s}.{:d}'.format(interface, sub_interface_index)
    path = '/network_instance[{:s}]/interface[{:s}]'.format(ni_name, sub_interface_name)
    data = {'name': ni_name, 'id': sub_interface_name, 'interface': interface, 'subinterface': sub_interface_index}
    return path, data

class EndpointComposer:
    def __init__(self, endpoint_uuid : str) -> None:
        self.uuid = endpoint_uuid
        self.objekt : Optional[EndPoint] = None
        self.sub_interface_index = 0
        self.ipv4_address = None
        self.ipv4_prefix_len = None

    def configure(self, endpoint_obj : Optional[EndPoint], settings : Optional[TreeNode]) -> None:
        if endpoint_obj is not None:
            self.objekt = endpoint_obj
        if settings is None: return
        json_settings : Dict = settings.value

        if 'address_ip' in json_settings:
            self.ipv4_address = json_settings['address_ip']
        elif 'ip_address' in json_settings:
            self.ipv4_address = json_settings['ip_address']
        else:
            MSG = 'IP Address not found. Tried: address_ip and ip_address. endpoint_obj={:s} settings={:s}'
            LOGGER.warning(MSG.format(str(endpoint_obj), str(settings)))

        if 'address_prefix' in json_settings:
            self.ipv4_prefix_len = json_settings['address_prefix']
        elif 'prefix_length' in json_settings:
            self.ipv4_prefix_len = json_settings['prefix_length']
        else:
            MSG = 'IP Address Prefix not found. Tried: address_prefix and prefix_length. endpoint_obj={:s} settings={:s}'
            LOGGER.warning(MSG.format(str(endpoint_obj), str(settings)))

        self.sub_interface_index = json_settings.get('index', 0)

    def get_config_rules(self, network_instance_name : str, delete : bool = False) -> List[Dict]:
        if self.ipv4_address is None: return []
        if self.ipv4_prefix_len is None: return []
        json_config_rule = json_config_rule_delete if delete else json_config_rule_set

        config_rules : List[Dict] = list()
        if network_instance_name != DEFAULT_NETWORK_INSTANCE:
            config_rules.append(json_config_rule(*_network_instance_interface(
                network_instance_name, self.objekt.name, self.sub_interface_index
            )))

        if delete:
            config_rules.extend([
                json_config_rule(*_interface(
                    self.objekt.name, index=self.sub_interface_index, address_ip=None,
                    address_prefix=None, enabled=False
                )),
            ])
        else:
            config_rules.extend([
                json_config_rule(*_interface(
                    self.objekt.name, index=self.sub_interface_index, address_ip=self.ipv4_address,
                    address_prefix=self.ipv4_prefix_len, enabled=True
                )),
            ])
        return config_rules

    def dump(self) -> Dict:
        return {
            'index'         : self.sub_interface_index,
            'address_ip'    : self.ipv4_address,
            'address_prefix': self.ipv4_prefix_len,
        }
    
    def __str__(self):
        data = {'uuid': self.uuid}
        if self.objekt is not None: data['name'] = self.objekt.name
        data.update(self.dump())
        return json.dumps(data)

class DeviceComposer:
    def __init__(self, device_uuid : str) -> None:
        self.uuid = device_uuid
        self.objekt : Optional[Device] = None
        self.aliases : Dict[str, str] = dict() # endpoint_name => endpoint_uuid
        self.endpoints : Dict[str, EndpointComposer] = dict() # endpoint_uuid => EndpointComposer
        self.connected : Set[str] = set()
        self.static_routes : Dict[str, Dict[int, str]] = dict() # {prefix => {metric => next_hop}}

    def set_endpoint_alias(self, endpoint_name : str, endpoint_uuid : str) -> None:
        self.aliases[endpoint_name] = endpoint_uuid

    def get_endpoint(self, endpoint_uuid : str) -> EndpointComposer:
        endpoint_uuid = self.aliases.get(endpoint_uuid, endpoint_uuid)
        if endpoint_uuid not in self.endpoints:
            self.endpoints[endpoint_uuid] = EndpointComposer(endpoint_uuid)
        return self.endpoints[endpoint_uuid]

    def configure(self, device_obj : Device, settings : Optional[TreeNode]) -> None:
        self.objekt = device_obj
        for endpoint_obj in device_obj.device_endpoints:
            endpoint_uuid = endpoint_obj.endpoint_id.endpoint_uuid.uuid
            self.set_endpoint_alias(endpoint_obj.name, endpoint_uuid)
            self.get_endpoint(endpoint_obj.name).configure(endpoint_obj, None)

        # Find management interfaces
        mgmt_ifaces = set()
        for config_rule in device_obj.device_config.config_rules:
            if config_rule.action != ConfigActionEnum.CONFIGACTION_SET: continue
            if config_rule.WhichOneof('config_rule') != 'custom': continue
            config_rule_custom = config_rule.custom
            match = RE_IF.match(config_rule_custom.resource_key)
            if match is None: continue
            if_name = match.groups()[0]
            resource_value = json.loads(config_rule_custom.resource_value)
            management = resource_value.get('management', False)
            if management: mgmt_ifaces.add(if_name)

        # Find data plane interfaces
        for config_rule in device_obj.device_config.config_rules:
            if config_rule.action != ConfigActionEnum.CONFIGACTION_SET: continue
            if config_rule.WhichOneof('config_rule') != 'custom': continue
            config_rule_custom = config_rule.custom

            match = RE_SUBIF.match(config_rule_custom.resource_key)
            if match is not None:
                if_name, subif_index = match.groups()
                if if_name in mgmt_ifaces: continue
                resource_value = json.loads(config_rule_custom.resource_value)
                if 'address_ip' not in resource_value: continue
                if 'address_prefix' not in resource_value: continue
                ipv4_network    = str(resource_value['address_ip'])
                ipv4_prefix_len = int(resource_value['address_prefix'])
                endpoint = self.get_endpoint(if_name)
                endpoint.ipv4_address = ipv4_network
                endpoint.ipv4_prefix_len = ipv4_prefix_len
                endpoint.sub_interface_index = int(subif_index)
                endpoint_ip_network = netaddr.IPNetwork('{:s}/{:d}'.format(ipv4_network, ipv4_prefix_len))
                if '0.0.0.0/' not in str(endpoint_ip_network.cidr):
                    self.connected.add(str(endpoint_ip_network.cidr))

            match = RE_SR.match(config_rule_custom.resource_key)
            if match is not None:
                ni_name, prefix, metric = match.groups()
                if ni_name != NETWORK_INSTANCE: continue
                resource_value : Dict = json.loads(config_rule_custom.resource_value)
                next_hop = resource_value['next_hop']
                self.static_routes.setdefault(prefix, dict())[metric] = next_hop

        if settings is None: return
        json_settings : Dict = settings.value
        static_routes : List[Dict] = json_settings.get('static_routes', [])
        for static_route in static_routes:
            prefix   = static_route['prefix']
            next_hop = static_route['next_hop']
            metric   = static_route.get('metric', 0)
            self.static_routes.setdefault(prefix, dict())[metric] = next_hop

    def get_config_rules(self, network_instance_name : str, delete : bool = False) -> List[Dict]:
        SELECTED_DEVICES = {
            DeviceTypeEnum.PACKET_POP.value,
            DeviceTypeEnum.PACKET_ROUTER.value,
            DeviceTypeEnum.EMULATED_PACKET_ROUTER.value
        }
        if self.objekt.device_type not in SELECTED_DEVICES: return []

        json_config_rule = json_config_rule_delete if delete else json_config_rule_set
        config_rules : List[Dict] = list()
        if network_instance_name != DEFAULT_NETWORK_INSTANCE:
            json_config_rule(*_network_instance(network_instance_name, 'L3VRF'))
        for endpoint in self.endpoints.values():
            config_rules.extend(endpoint.get_config_rules(network_instance_name, delete=delete))
        if len(self.static_routes) > 0:
            config_rules.append(
                json_config_rule(*_network_instance_protocol_static(network_instance_name))
            )
        for prefix, metric_next_hop in self.static_routes.items():
            for metric, next_hop in metric_next_hop.items():
                config_rules.append(
                    json_config_rule(*_network_instance_protocol_static_route(
                        network_instance_name, prefix, next_hop, metric
                    ))
                )
        if delete: config_rules = list(reversed(config_rules))
        return config_rules

    def dump(self) -> Dict:
        return {
            'endpoints' : {
                endpoint_uuid : endpoint.dump()
                for endpoint_uuid, endpoint in self.endpoints.items()
            },
            'connected' : list(self.connected),
            'static_routes' : self.static_routes,
        }

    def __str__(self):
        data = {'uuid': self.uuid}
        if self.objekt is not None: data['name'] = self.objekt.name
        data.update(self.dump())
        return json.dumps(data)

class ConfigRuleComposer:
    def __init__(self) -> None:
        self.objekt : Optional[Service] = None
        self.aliases : Dict[str, str] = dict() # device_name => device_uuid
        self.devices : Dict[str, DeviceComposer] = dict() # device_uuid => DeviceComposer

    def set_device_alias(self, device_name : str, device_uuid : str) -> None:
        self.aliases[device_name] = device_uuid

    def get_device(self, device_uuid : str) -> DeviceComposer:
        device_uuid = self.aliases.get(device_uuid, device_uuid)
        if device_uuid not in self.devices:
            self.devices[device_uuid] = DeviceComposer(device_uuid)
        return self.devices[device_uuid]

    def configure(self, service_obj : Service, settings : Optional[TreeNode]) -> None:
        self.objekt = service_obj
        if settings is None: return
        #json_settings : Dict = settings.value
        # For future use

    def get_config_rules(
        self, network_instance_name : str = NETWORK_INSTANCE, delete : bool = False
    ) -> Dict[str, List[Dict]]:
        return {
            device_uuid : device.get_config_rules(network_instance_name, delete=delete)
            for device_uuid, device in self.devices.items()
        }

    def dump(self) -> Dict:
        return {
            'devices' : {
                device_uuid : device.dump()
                for device_uuid, device in self.devices.items()
            }
        }
