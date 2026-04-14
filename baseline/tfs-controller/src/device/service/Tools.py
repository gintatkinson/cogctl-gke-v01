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

import json, logging, re
from graphlib import TopologicalSorter, CycleError
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.DeviceTypes import DeviceTypeEnum
from common.method_wrappers.ServiceExceptions import InvalidArgumentException, NotFoundException
from common.proto.context_pb2 import (
    ConfigActionEnum, ConfigRule, ConfigRule_ACL, Device, DeviceConfig, EndPoint, Link, Location, OpticalConfig
)
from common.proto.device_pb2 import MonitoringSettings
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.grpc.ConfigRules import update_config_rule_custom
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.type_checkers.Checkers import chk_length, chk_type
from .driver_api._Driver import _Driver, RESOURCE_ENDPOINTS
from .monitoring.MonitoringLoops import MonitoringLoops
from .ErrorMessages import (
    ERROR_BAD_RESOURCE, ERROR_DELETE, ERROR_GET, ERROR_GET_INIT,
    ERROR_MISSING_KPI, ERROR_SAMPLETYPE, ERROR_SET,
    ERROR_SUBSCRIBE, ERROR_UNSUBSCRIBE, ERROR_UNSUP_RESOURCE
)

LOGGER = logging.getLogger(__name__)

def get_endpoint_matching(device : Device, endpoint_uuid_or_name : str) -> EndPoint:
    for endpoint in device.device_endpoints:
        choices = {endpoint.endpoint_id.endpoint_uuid.uuid, endpoint.name}
        if endpoint_uuid_or_name in choices: return endpoint

    device_uuid = device.device_id.device_uuid.uuid
    extra_details = 'Device({:s})'.format(str(device_uuid))
    raise NotFoundException('Endpoint', endpoint_uuid_or_name, extra_details=extra_details)

def get_device_endpoint_uuids(endpoint : Tuple[str, str, Optional[str]]) -> Tuple[str, str]:
    chk_type('endpoint', endpoint, (tuple, list))
    chk_length('endpoint', endpoint, min_length=2, max_length=3)
    device_uuid, endpoint_uuid = endpoint[0:2] # ignore topology_uuid by now
    return device_uuid, endpoint_uuid

def check_connect_rules(device_config : DeviceConfig) -> Dict[str, Any]:
    connection_config_rules = dict()
    unexpected_config_rules = list()
    for config_rule in device_config.config_rules:
        is_action_set = (config_rule.action == ConfigActionEnum.CONFIGACTION_SET)
        is_custom_rule = (config_rule.WhichOneof('config_rule') == 'custom')
        if is_action_set and is_custom_rule and (config_rule.custom.resource_key.startswith('_connect/')):
            connect_attribute = config_rule.custom.resource_key.replace('_connect/', '')
            connection_config_rules[connect_attribute] = config_rule.custom.resource_value
        else:
            unexpected_config_rules.append(config_rule)

    if len(unexpected_config_rules) > 0:
        unexpected_config_rules = grpc_message_to_json(device_config)
        unexpected_config_rules = unexpected_config_rules['config_rules']
        unexpected_config_rules = list(filter(
            lambda cr: cr.get('custom', {})['resource_key'].replace('_connect/', '') not in connection_config_rules,
            unexpected_config_rules))
        str_unexpected_config_rules = json.dumps(unexpected_config_rules, sort_keys=True)
        raise InvalidArgumentException(
            'device.device_config.config_rules', str_unexpected_config_rules,
            extra_details='RPC method AddDevice only accepts connection Config Rules that should start '\
                            'with "_connect/" tag. Others should be configured after adding the device.')

    return connection_config_rules

def get_connect_rules(device_config : DeviceConfig) -> Dict[str, Any]:
    connect_rules = dict()
    for config_rule in device_config.config_rules:
        if config_rule.action != ConfigActionEnum.CONFIGACTION_SET: continue
        if config_rule.WhichOneof('config_rule') != 'custom': continue
        if not config_rule.custom.resource_key.startswith('_connect/'): continue
        connect_attribute = config_rule.custom.resource_key.replace('_connect/', '')
        connect_rules[connect_attribute] = config_rule.custom.resource_value
    return connect_rules

def check_no_endpoints(device_endpoints) -> None:
    if len(device_endpoints) == 0: return
    unexpected_endpoints = []
    for device_endpoint in device_endpoints:
        unexpected_endpoints.append(grpc_message_to_json(device_endpoint))
    str_unexpected_endpoints = json.dumps(unexpected_endpoints, sort_keys=True)
    raise InvalidArgumentException(
        'device.device_endpoints', str_unexpected_endpoints,
        extra_details='RPC method AddDevice does not accept Endpoints. Endpoints are discovered through '\
                        'interrogation of the physical device.')

def get_device_controller_uuid(device : Device) -> Optional[str]:
    controller_uuid = device.controller_id.device_uuid.uuid
    if len(controller_uuid) > 0: return controller_uuid
    return None

def populate_endpoints(
    device : Device, driver : _Driver, monitoring_loops : MonitoringLoops,
    new_sub_devices : Dict[str, Device], sorted_sub_device_uuids : List[str],
    new_sub_links : Dict[str, Link], new_optical_configs : Dict[str, OpticalConfig]
) -> List[str]:
    device_uuid = device.device_id.device_uuid.uuid
    device_name = device.name

    resources_to_get = [RESOURCE_ENDPOINTS]
    results_getconfig = driver.GetConfig(resources_to_get)
    LOGGER.debug('results_getconfig = {:s}'.format(str(results_getconfig)))

    # first quick pass to identify need of mgmt endpoints and links
    add_mgmt_port = False
    for resource_data in results_getconfig:
        if len(resource_data) != 2: continue
        resource_key, _ = resource_data
        if resource_key.startswith('/devices/device'):
            add_mgmt_port = True
            break

    devices_with_mgmt_endpoints : Set[str] = set()
    mgmt_links : Set[Tuple[str, str]] = set()

    if add_mgmt_port:
        # add mgmt port to main device
        device_mgmt_endpoint = device.device_endpoints.add()
        device_mgmt_endpoint.endpoint_id.topology_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
        device_mgmt_endpoint.endpoint_id.topology_id.topology_uuid.uuid = DEFAULT_TOPOLOGY_NAME
        device_mgmt_endpoint.endpoint_id.device_id.device_uuid.uuid = device_uuid
        device_mgmt_endpoint.endpoint_id.endpoint_uuid.uuid = 'mgmt'
        device_mgmt_endpoint.name = 'mgmt'
        device_mgmt_endpoint.endpoint_type = 'mgmt'

        devices_with_mgmt_endpoints.add(device_uuid)
        devices_with_mgmt_endpoints.add(device_name)

    errors : List[str] = list()
    for resource_data in results_getconfig:
        if len(resource_data) != 2:
            errors.append(ERROR_BAD_RESOURCE.format(device_uuid=device_uuid, resource_data=str(resource_data)))
            continue

        resource_key, resource_value = resource_data
        if isinstance(resource_value, Exception):
            errors.append(ERROR_GET.format(
                device_uuid=device_uuid, resource_key=str(resource_key), error=str(resource_value)))
            continue
        if resource_value is None:
            continue

        if resource_key.startswith('/devices/device'):
            # create sub-device
            _sub_device_uuid = resource_value['uuid']
            _sub_device_name = resource_value['name']
            _sub_device_ctrl = resource_value.get('ctrl_uuid')
            _sub_device = Device()
            _sub_device.device_id.device_uuid.uuid = _sub_device_uuid           # pylint: disable=no-member
            _sub_device.name = _sub_device_name
            _sub_device.device_type = resource_value['type']
            _sub_device.device_operational_status = resource_value['status']

            # Sub-devices might not have a driver assigned.
            if 'drivers' in resource_value:
                drivers = resource_value['drivers']
                if isinstance(drivers, (list, set)):
                    _sub_device.device_drivers.extend(drivers)  # pylint: disable=no-member
                elif isinstance(drivers, (int, str)):
                    _sub_device.device_drivers.append(drivers)  # pylint: disable=no-member
                else:
                    MSG = 'Unsupported drivers definition in sub-device({:s}, {:s})'
                    raise Exception(MSG.format(str(resource_key), str(resource_value)))

            if _sub_device_ctrl is not None:
                # Sub-device is managed by an underlying controller
                _sub_device.controller_id.device_uuid.uuid = _sub_device_ctrl
            else:
                # Sub-devices should always have a controller associated.
                _sub_device.controller_id.device_uuid.uuid = device_uuid

            new_sub_devices[_sub_device_uuid] = _sub_device

            # add mgmt port to sub-device
            if (
                _sub_device_uuid not in devices_with_mgmt_endpoints and
                _sub_device_name not in devices_with_mgmt_endpoints
            ):
                _sub_device_mgmt_endpoint = _sub_device.device_endpoints.add()      # pylint: disable=no-member
                _sub_device_mgmt_endpoint.endpoint_id.topology_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
                _sub_device_mgmt_endpoint.endpoint_id.topology_id.topology_uuid.uuid = DEFAULT_TOPOLOGY_NAME
                _sub_device_mgmt_endpoint.endpoint_id.device_id.device_uuid.uuid = _sub_device_uuid
                _sub_device_mgmt_endpoint.endpoint_id.endpoint_uuid.uuid = 'mgmt'
                _sub_device_mgmt_endpoint.name = 'mgmt'
                _sub_device_mgmt_endpoint.endpoint_type = 'mgmt'

                devices_with_mgmt_endpoints.add(_sub_device_uuid)
                devices_with_mgmt_endpoints.add(_sub_device_name)

            # add mgmt link
            if (
                _sub_device_ctrl is None and
                (device_name, _sub_device_name) not in mgmt_links
            ):
                _mgmt_link_uuid = '{:s}/{:s}=={:s}/{:s}'.format(device_name, 'mgmt', _sub_device_name, 'mgmt')
                _mgmt_link = Link()
                _mgmt_link.link_id.link_uuid.uuid = _mgmt_link_uuid                         # pylint: disable=no-member
                _mgmt_link.name = _mgmt_link_uuid
                _mgmt_link.link_endpoint_ids.append(device_mgmt_endpoint.endpoint_id)       # pylint: disable=no-member
                _mgmt_link.link_endpoint_ids.append(_sub_device_mgmt_endpoint.endpoint_id)  # pylint: disable=no-member
                new_sub_links[_mgmt_link_uuid] = _mgmt_link

                mgmt_links.add((device_name, _sub_device_name))

        elif resource_key.startswith('/endpoints/endpoint'):
            endpoint_uuid = resource_value['uuid']
            _device_uuid = resource_value.get('device_uuid')
            endpoint_name = resource_value.get('name')

            if endpoint_uuid == 'mgmt' or endpoint_name == 'mgmt':
                if _device_uuid is None:
                    if device_uuid in devices_with_mgmt_endpoints:
                        continue
                else:
                    if _device_uuid in devices_with_mgmt_endpoints:
                        continue

            if _device_uuid is None:
                # add endpoint to current device
                device_endpoint = device.device_endpoints.add()
                device_endpoint.endpoint_id.device_id.device_uuid.uuid = device_uuid
                device_config_rules = device.device_config.config_rules
            else:
                # add endpoint to specified device
                device_endpoint = new_sub_devices[_device_uuid].device_endpoints.add()
                device_endpoint.endpoint_id.device_id.device_uuid.uuid = _device_uuid
                device_config_rules = new_sub_devices[_device_uuid].device_config.config_rules

            device_endpoint.endpoint_id.endpoint_uuid.uuid = endpoint_uuid

            endpoint_context_uuid = resource_value.get('context_uuid', DEFAULT_CONTEXT_NAME)
            device_endpoint.endpoint_id.topology_id.context_id.context_uuid.uuid = endpoint_context_uuid

            endpoint_topology_uuid = resource_value.get('topology_uuid', DEFAULT_TOPOLOGY_NAME)
            device_endpoint.endpoint_id.topology_id.topology_uuid.uuid = endpoint_topology_uuid

            endpoint_name = resource_value.get('name')
            if endpoint_name is not None: device_endpoint.name = endpoint_name

            device_endpoint.endpoint_type = resource_value.get('type', '-')

            sample_types : Dict[int, str] = resource_value.get('sample_types', {})
            for kpi_sample_type, monitor_resource_key in sample_types.items():
                device_endpoint.kpi_sample_types.append(kpi_sample_type)
                monitoring_loops.add_resource_key(device_uuid, endpoint_uuid, kpi_sample_type, monitor_resource_key)

            location = resource_value.get('location', None)
            if location is not None:
                device_endpoint.endpoint_location.MergeFrom(Location(**location))

            settings = resource_value.get('settings', None)
            if settings is not None:
                device_config_rules.append(ConfigRule(**json_config_rule_set(
                    '/endpoints/endpoint[{:s}]'.format(str(endpoint_name)), settings
                )))

            if endpoint_uuid == 'mgmt' or endpoint_name == 'mgmt':
                if _device_uuid is None:
                    devices_with_mgmt_endpoints.add(device_uuid)
                    devices_with_mgmt_endpoints.add(device_name)
                else:
                    devices_with_mgmt_endpoints.add(_device_uuid)
                    devices_with_mgmt_endpoints.add(new_sub_devices[_device_uuid].name)

        elif resource_key.startswith('/links/link'):
            link_name = resource_value['name']
            mgmt_match = re.match(r'^([^\/]+)\/mgmt\=\=([^\/]+)\/mgmt$', link_name)
            if mgmt_match is not None:
                # is management link
                src_dev_name, dst_dev_name = mgmt_match.groups()
                if (src_dev_name, dst_dev_name) in mgmt_links: continue

            # create sub-link
            _sub_link_uuid = resource_value['uuid']
            _sub_link = Link()
            _sub_link.link_id.link_uuid.uuid = _sub_link_uuid           # pylint: disable=no-member
            _sub_link.name = resource_value['name']
            new_sub_links[_sub_link_uuid] = _sub_link

            for _device_uuid,_endpoint_uuid in resource_value['endpoints']:
                _sub_link_endpoint_id = _sub_link.link_endpoint_ids.add()      # pylint: disable=no-member
                _sub_link_endpoint_id.topology_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
                _sub_link_endpoint_id.topology_id.topology_uuid.uuid = DEFAULT_TOPOLOGY_NAME
                _sub_link_endpoint_id.device_id.device_uuid.uuid = _device_uuid
                _sub_link_endpoint_id.endpoint_uuid.uuid = _endpoint_uuid

            if mgmt_match is not None:
                mgmt_links.add((src_dev_name, dst_dev_name))

        # ----------Experimental --------------
        elif resource_key.startswith('/opticalconfigs/opticalconfig/'):
            new_optical_configs["new_optical_config"]=resource_value
        else:
            errors.append(ERROR_UNSUP_RESOURCE.format(device_uuid=device_uuid, resource_data=str(resource_data)))
            continue

    # Topologically sort new_sub_devices so that controllers (those referenced by other
    # devices via their controller_id) come before the devices that depend on them.

    graph : Dict[str, Set[str]] = dict()
    for dev_uuid, sub_device in new_sub_devices.items():
        ctrl_uuid = get_device_controller_uuid(sub_device)
        if ctrl_uuid is None: continue # sub_device has no controller
        predecesors = graph.setdefault(dev_uuid, set())
        predecesors.add(ctrl_uuid)

    try:
        ts = TopologicalSorter(graph)
        sorted_sub_device_uuids.extend(list(ts.static_order()))
        if device_uuid in sorted_sub_device_uuids:
            sorted_sub_device_uuids.remove(device_uuid)
    except CycleError:
        MSG = 'Topological sort failed due to cycle among sub-devices({:s}), graph({:s})'
        msg = MSG.format(str(new_sub_devices), str(graph))
        LOGGER.exception(msg)
        errors.append(msg)

    return errors

def populate_endpoint_monitoring_resources(device_with_uuids : Device, monitoring_loops : MonitoringLoops) -> None:
    device_uuid = device_with_uuids.device_id.device_uuid.uuid

    for endpoint in device_with_uuids.device_endpoints:
        endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
        endpoint_name = endpoint.name
        kpi_sample_types = endpoint.kpi_sample_types
        for kpi_sample_type in kpi_sample_types:
            monitor_resource_key = monitoring_loops.get_resource_key(device_uuid, endpoint_uuid, kpi_sample_type)
            if monitor_resource_key is not None: continue

            monitor_resource_key = monitoring_loops.get_resource_key(device_uuid, endpoint_name, kpi_sample_type)
            if monitor_resource_key is None: continue
            monitoring_loops.add_resource_key(device_uuid, endpoint_uuid, kpi_sample_type, monitor_resource_key)

def _raw_config_rules_to_grpc(
    device_uuid : str, device_config : DeviceConfig, error_template : str, config_action : ConfigActionEnum,
    raw_config_rules : List[Tuple[str, Union[Any, Exception, None]]]
) -> List[str]:
    errors : List[str] = list()

    for resource_key, resource_value in raw_config_rules:
        if isinstance(resource_value, Exception):
            errors.append(error_template.format(
                device_uuid=device_uuid, resource_key=str(resource_key), resource_value=str(resource_value),
                error=str(resource_value)))
            continue

        if resource_value is None: continue
        resource_value = json.loads(resource_value) if isinstance(resource_value, str) else resource_value
        if isinstance(resource_value, ConfigRule_ACL): resource_value = grpc_message_to_json(resource_value)
        resource_value = {field_name : (field_value, False) for field_name,field_value in resource_value.items()}
        update_config_rule_custom(device_config.config_rules, resource_key, resource_value, new_action=config_action)

    return errors

def populate_config_rules(device : Device, driver : _Driver) -> List[str]:
    device_uuid = device.device_id.device_uuid.uuid
    results_getconfig = driver.GetConfig()
    return _raw_config_rules_to_grpc(
        device_uuid, device.device_config, ERROR_GET, ConfigActionEnum.CONFIGACTION_SET, results_getconfig)

def populate_initial_config_rules(device_uuid : str, device_config : DeviceConfig, driver : _Driver) -> List[str]:
    results_getinitconfig = driver.GetInitialConfig()
    return _raw_config_rules_to_grpc(
        device_uuid, device_config, ERROR_GET_INIT, ConfigActionEnum.CONFIGACTION_SET, results_getinitconfig)

def compute_rules_to_add_delete(
    device : Device, request : Device
) -> Tuple[List[Tuple[str, Any]], List[Tuple[str, Any]]]:
    # convert config rules from context into a dictionary
    context_config_rules = {}
    for config_rule in device.device_config.config_rules:
        config_rule_kind = config_rule.WhichOneof('config_rule')
        if config_rule_kind == 'custom':    # process "custom" rules
            context_config_rules[config_rule.custom.resource_key] = config_rule.custom.resource_value # get the resource value of the rule resource
        elif config_rule_kind == 'acl':     # process "custom" rules
            device_uuid = config_rule.acl.endpoint_id.device_id.device_uuid.uuid # get the device name
            endpoint_uuid = config_rule.acl.endpoint_id.endpoint_uuid.uuid       # get the endpoint name
            acl_ruleset_name = config_rule.acl.rule_set.name                     # get the acl name
            ACL_KEY_TEMPLATE = '/device[{:s}]/endpoint[{:s}]/acl_ruleset[{:s}]'
            key_or_path = ACL_KEY_TEMPLATE.format(device_uuid, endpoint_uuid, acl_ruleset_name)
            context_config_rules[key_or_path] = grpc_message_to_json(config_rule.acl)    # get the resource value of the acl
        elif config_rule_kind == 'ip_link':
            device_uuid = config_rule.ip_link.endpoint_id.device_id.device_uuid.uuid # get the device name
            endpoint_uuid = config_rule.ip_link.endpoint_id.endpoint_uuid.uuid       # get the endpoint name    request_config_rules = []
            ip_link_ruleset_name = config_rule.ip_link.rule_set.name                     # get the ip_link name
            IP_LINK_KEY_TEMPLATE = '/device[{:s}]/endpoint[{:s}]/ip_link_ruleset[{:s}]'
            key_or_path = IP_LINK_KEY_TEMPLATE.format(device_uuid, endpoint_uuid, ip_link_ruleset_name)
            context_config_rules[key_or_path] = grpc_message_to_json(config_rule.ip_link)    # get the resource value of the ip_link
        elif config_rule_kind == 'ipowdm':
            device_uuid = config_rule.ipowdm.endpoint_id.device_id.device_uuid.uuid
            endpoint_uuid = config_rule.ipowdm.endpoint_id.endpoint_uuid.uuid
            ipowdm_ruleset_name = config_rule.ipowdm.rule_set.uuid
            IPOWDM_KEY_TEMPLATE = '/device[{:s}]/endpoint[{:s}]/ipowdm_ruleset[{:s}]'
            key_or_path = IPOWDM_KEY_TEMPLATE.format(device_uuid, endpoint_uuid, ipowdm_ruleset_name)
            context_config_rules[key_or_path] = grpc_message_to_json(config_rule.ipowdm)
            LOGGER.debug('context_config_rules [%s] = %s', key_or_path, context_config_rules[key_or_path])
        elif config_rule_kind == 'tapi_lsp':
            device_uuid = config_rule.tapi_lsp.endpoint_id.device_id.device_uuid.uuid # get the device name
            endpoint_uuid = config_rule.tapi_lsp.endpoint_id.endpoint_uuid.uuid       # get the endpoint name
            tapi_lsp_ruleset_name = config_rule.tapi_lsp.rule_set.name                # get the ip_link name
            TAPI_LSP_KEY_TEMPLATE = '/device[{:s}]/endpoint[{:s}]/tapi_lsp_ruleset[{:s}]'
            key_or_path = TAPI_LSP_KEY_TEMPLATE.format(device_uuid, endpoint_uuid, tapi_lsp_ruleset_name)
            context_config_rules[key_or_path] = grpc_message_to_json(config_rule.tapi_lsp)
            LOGGER.debug('context_config_rules [%s] = {context_config_rules[%s]}',key_or_path, key_or_path)

    request_config_rules = []
    for config_rule in request.device_config.config_rules:
        config_rule_kind = config_rule.WhichOneof('config_rule')
        if config_rule_kind == 'custom': # resource management of "custom" rule
            request_config_rules.append((
                config_rule.action, config_rule.custom.resource_key, config_rule.custom.resource_value
            ))
        elif config_rule_kind == 'acl':  # resource management of "acl" rule
            device_uuid = config_rule.acl.endpoint_id.device_id.device_uuid.uuid
            endpoint_uuid = config_rule.acl.endpoint_id.endpoint_uuid.uuid
            acl_ruleset_name = config_rule.acl.rule_set.name
            ACL_KEY_TEMPLATE = '/device[{:s}]/endpoint[{:s}]/acl_ruleset[{:s}]'
            key_or_path = ACL_KEY_TEMPLATE.format(device_uuid, endpoint_uuid, acl_ruleset_name)
            request_config_rules.append((
                config_rule.action, key_or_path, grpc_message_to_json(config_rule.acl)
            ))
        elif config_rule_kind == 'ip_link':  # resource management of "ip_link" rule
            device_uuid = config_rule.ip_link.endpoint_id.device_id.device_uuid.uuid
            endpoint_uuid = config_rule.ip_link.endpoint_id.endpoint_uuid.uuid
            IP_LINK_KEY_TEMPLATE = '/device[{:s}]/endpoint[{:s}]/ip_link_ruleset'
            key_or_path = IP_LINK_KEY_TEMPLATE.format(device_uuid, endpoint_uuid)
            request_config_rules.append((
                config_rule.action, key_or_path, grpc_message_to_json(config_rule.ip_link)
            ))
        elif config_rule_kind == 'ipowdm':  # resource management of "ipowdm" rule
            device_uuid = config_rule.ipowdm.endpoint_id.device_id.device_uuid.uuid
            endpoint_uuid = config_rule.ipowdm.endpoint_id.endpoint_uuid.uuid
            ipowdm_name = config_rule.ipowdm.rule_set.uuid
            IPOWDM_KEY_TEMPLATE = '/device[{:s}]/endpoint[{:s}]/ipowdm_ruleset[{:s}]'
            key_or_path = IPOWDM_KEY_TEMPLATE.format(device_uuid, endpoint_uuid,ipowdm_name)
            request_config_rules.append((
                config_rule.action, key_or_path, grpc_message_to_json(config_rule.ipowdm)
            ))
            LOGGER.debug('context_config_rules= %s', request_config_rules)
        elif config_rule_kind == 'tapi_lsp':  # resource management of "tapi_lsp" rule
            device_uuid = config_rule.tapi_lsp.endpoint_id.device_id.device_uuid.uuid
            endpoint_uuid = config_rule.tapi_lsp.endpoint_id.endpoint_uuid.uuid
            TAPI_LSP_KEY_TEMPLATE = '/device[{:s}]/endpoint[{:s}]/tapi_lsp_ruleset'
            key_or_path = TAPI_LSP_KEY_TEMPLATE.format(device_uuid, endpoint_uuid)
            request_config_rules.append((
                config_rule.action, key_or_path, grpc_message_to_json(config_rule.tapi_lsp)
            ))

    resources_to_set    : List[Tuple[str, Any]] = [] # key, value
    resources_to_delete : List[Tuple[str, Any]] = [] # key, value

    for action, key, value in request_config_rules:
        if action == ConfigActionEnum.CONFIGACTION_SET:
            if (key in context_config_rules) and (context_config_rules[key][0] == value): continue
            resources_to_set.append((key, value))
        elif action == ConfigActionEnum.CONFIGACTION_DELETE:
            if key not in context_config_rules: continue
            resources_to_delete.append((key, value))

    return resources_to_set, resources_to_delete

def configure_rules(device : Device, driver : _Driver, resources_to_set : List[Tuple[str, Any]]) -> List[str]:
    if len(resources_to_set) == 0: return []

    results_setconfig = driver.SetConfig(resources_to_set)
    results_setconfig = [
        (resource_key, result if isinstance(result, Exception) else resource_value)
        for (resource_key, resource_value), result in zip(resources_to_set, results_setconfig)
    ]

    device_uuid = device.device_id.device_uuid.uuid
    return _raw_config_rules_to_grpc(
        device_uuid, device.device_config, ERROR_SET, ConfigActionEnum.CONFIGACTION_SET, results_setconfig)

def deconfigure_rules(device : Device, driver : _Driver, resources_to_delete : List[Tuple[str, Any]]) -> List[str]:
    if len(resources_to_delete) == 0: return []

    results_deleteconfig = driver.DeleteConfig(resources_to_delete)
    results_deleteconfig = [
        (resource_key, result if isinstance(result, Exception) else resource_value)
        for (resource_key, resource_value), result in zip(resources_to_delete, results_deleteconfig)
    ]

    device_uuid = device.device_id.device_uuid.uuid
    return _raw_config_rules_to_grpc(
        device_uuid, device.device_config, ERROR_DELETE, ConfigActionEnum.CONFIGACTION_DELETE, results_deleteconfig)

def subscribe_kpi(request : MonitoringSettings, driver : _Driver, monitoring_loops : MonitoringLoops) -> List[str]:
    kpi_uuid = request.kpi_id.kpi_id.uuid
    device_uuid = request.kpi_descriptor.device_id.device_uuid.uuid
    endpoint_uuid = request.kpi_descriptor.endpoint_id.endpoint_uuid.uuid
    kpi_sample_type = request.kpi_descriptor.kpi_sample_type

    resource_key = monitoring_loops.get_resource_key(device_uuid, endpoint_uuid, kpi_sample_type)
    if resource_key is None:
        kpi_sample_type_name = KpiSampleType.Name(kpi_sample_type).upper().replace('KPISAMPLETYPE_', '')
        MSG = ERROR_SAMPLETYPE.format(
            device_uuid=str(device_uuid), endpoint_uuid=str(endpoint_uuid), sample_type_id=str(kpi_sample_type),
            sample_type_name=str(kpi_sample_type_name)
        )
        LOGGER.warning('{:s} Supported Device-Endpoint-KpiSampleType items: {:s}'.format(
            MSG, str(monitoring_loops.get_all_resource_keys())))
        return [MSG]

    sampling_duration = request.sampling_duration_s # seconds
    sampling_interval = request.sampling_interval_s # seconds

    resources_to_subscribe = [(resource_key, sampling_duration, sampling_interval)]
    results_subscribestate = driver.SubscribeState(resources_to_subscribe)

    errors : List[str] = list()
    for (resource_key, duration, interval), result in zip(resources_to_subscribe, results_subscribestate):
        if isinstance(result, Exception):
            errors.append(ERROR_SUBSCRIBE.format(
                device_uuid=str(device_uuid), subscr_key=str(resource_key), subscr_duration=str(duration),
                subscr_interval=str(interval), error=str(result)
            ))
            continue

    monitoring_loops.add_kpi(device_uuid, resource_key, kpi_uuid, sampling_duration, sampling_interval)
    monitoring_loops.add_device(device_uuid, driver)

    return errors

def unsubscribe_kpi(request : MonitoringSettings, driver : _Driver, monitoring_loops : MonitoringLoops) -> List[str]:
    kpi_uuid = request.kpi_id.kpi_id.uuid

    kpi_details = monitoring_loops.get_kpi_by_uuid(kpi_uuid)
    if kpi_details is None:
        return [ERROR_MISSING_KPI.format(kpi_uuid=str(kpi_uuid))]

    device_uuid, resource_key, sampling_duration, sampling_interval = kpi_details

    resources_to_unsubscribe = [(resource_key, sampling_duration, sampling_interval)]
    results_unsubscribestate = driver.UnsubscribeState(resources_to_unsubscribe)

    errors : List[str] = list()
    for (resource_key, duration, interval), result in zip(resources_to_unsubscribe, results_unsubscribestate):
        if isinstance(result, Exception):
            errors.append(ERROR_UNSUBSCRIBE.format(
                device_uuid=str(device_uuid), subscr_key=str(resource_key), subscr_duration=str(duration),
                subscr_interval=str(interval), error=str(result)
            ))
            continue

    monitoring_loops.remove_kpi(kpi_uuid)
    #monitoring_loops.remove_device(device_uuid) # Do not remove; one monitoring_loop/device used by multiple requests

    return errors

def update_endpoints(src_device : Device, dst_device : Device) -> None:
    for src_endpoint in src_device.device_endpoints:
        src_device_uuid   = src_endpoint.endpoint_id.device_id.device_uuid.uuid
        src_endpoint_uuid = src_endpoint.endpoint_id.endpoint_uuid.uuid
        src_context_uuid  = src_endpoint.endpoint_id.topology_id.context_id.context_uuid.uuid
        src_topology_uuid = src_endpoint.endpoint_id.topology_id.topology_uuid.uuid

        for dst_endpoint in dst_device.device_endpoints:
            dst_endpoint_id = dst_endpoint.endpoint_id
            if src_endpoint_uuid not in {dst_endpoint_id.endpoint_uuid.uuid, dst_endpoint.name}: continue
            if src_device_uuid != dst_endpoint_id.device_id.device_uuid.uuid: continue

            dst_topology_id = dst_endpoint_id.topology_id
            if len(src_topology_uuid) > 0 and src_topology_uuid != dst_topology_id.topology_uuid.uuid: continue
            if len(src_context_uuid) > 0 and src_context_uuid != dst_topology_id.context_id.context_uuid.uuid: continue
            break   # found, do nothing
        else:
            # not found, add it
            dst_endpoint = dst_device.device_endpoints.add()    # pylint: disable=no-member
            dst_endpoint_id = dst_endpoint.endpoint_id
            dst_endpoint_id.endpoint_uuid.uuid = src_endpoint_uuid
            dst_endpoint_id.device_id.device_uuid.uuid = src_device_uuid
            dst_topology_id = dst_endpoint_id.topology_id
            if len(src_topology_uuid) > 0: dst_topology_id.topology_uuid.uuid = src_topology_uuid
            if len(src_context_uuid) > 0: dst_topology_id.context_id.context_uuid.uuid = src_context_uuid

def get_edit_target(device : Device, is_opticalband : bool,has_flow_id:bool) -> str:
    if is_opticalband:return 'optical-band'
    if device.device_type == DeviceTypeEnum.OPTICAL_ROADM._value_: return 'media-channel'
    if device.device_type == DeviceTypeEnum.OPEN_ROADM._value_: return 'or'
    return 'optical-channel'

def is_key_existed(key : str, keys_dic = dict, key_name_to_use = None) -> dict:
    dic = {}
    dic['resource_key'] = key
    if key_name_to_use is not None:
        dic['resource_key'] = key_name_to_use
    if key in keys_dic:
        dic['value'] = keys_dic[key]
    else:
        dic['value'] = None
    return dic

def extract_resources(config : dict, device : Device) -> list[list[dict], dict]:
    conditions = {}
    resources : list[dict] = []
    is_opticalband = config.get('is_opticalband', False)
    flow_id=is_key_existed('flow_id', keys_dic=config['new_config'], key_name_to_use='index')
    conditions['edit_type'] = get_edit_target(device, is_opticalband,'value' in flow_id)

    if device.device_type == DeviceTypeEnum.OPEN_ROADM._value_ :
        ports_dic = is_key_existed('ports',keys_dic=config['new_config'])
        interfaces_list = []
        config_type = is_key_existed('config_type', keys_dic=config['new_config'])
        resources.append(config_type)
        resources.append(is_key_existed('administrative-state', keys_dic=config['new_config']))
        resources.append(is_key_existed('frequency', keys_dic=config['new_config']))
        resources.append(is_key_existed('width', keys_dic=config['new_config']))

        for port in ports_dic["value"]:
            circuit_pack_dic = is_key_existed('supporting-circuit-pack-name', keys_dic=port)
            interface_list = is_key_existed('supporting-interface-list', keys_dic=port)
            supporting_port = is_key_existed('supporting-port', keys_dic=port)
            interfaces_list.append([
                circuit_pack_dic,
                interface_list,
                supporting_port
            ])
        resources.append({'resource_key':'interfaces','value':interfaces_list})
    else :
        resources.append(is_key_existed('channel_namespace', config))
        resources.append(is_key_existed('add_transceiver', config))

        conditions['is_opticalband'] = is_opticalband
        if 'flow' in config:
            #for tuple_value in config['flow'][device.name]:
            source_vals = []
            dest_vals = []
            handled_flow = []
            for tuple_value in config['flow']:
                source_port = None
                destination_port = None
                source_port_uuid, destination_port_uuid = tuple_value
                if source_port_uuid != '0':
                    src_endpoint_obj = get_endpoint_matching(device, source_port_uuid)
                    source_port = src_endpoint_obj.name
                source_vals.append(source_port)
                if destination_port_uuid != '0':
                    dst_endpoint_obj = get_endpoint_matching(device, destination_port_uuid)
                    destination_port = dst_endpoint_obj.name
                dest_vals.append(destination_port)
                handled_flow.append((source_port, destination_port))
            resources.append({'resource_key': 'source_port',      'value': source_vals })
            resources.append({'resource_key': 'destination_port', 'value': dest_vals   })
            resources.append({'resource_key': 'handled_flow',     'value': handled_flow})
        if 'new_config' in config:
            lower_frequency = None
            upper_frequency = None
            resources.append(is_key_existed('target-output-power', keys_dic=config['new_config']))
            resources.append(is_key_existed('frequency',           keys_dic=config['new_config']))
            resources.append(is_key_existed('operational-mode',    keys_dic=config['new_config']))
            resources.append(is_key_existed('line-port',           keys_dic=config['new_config']))
            resources.append(is_key_existed('status',              keys_dic=config['new_config'], key_name_to_use="admin-state"))
            resources.append(is_key_existed('band_type',           keys_dic=config['new_config'], key_name_to_use='name'))
            resources.append(is_key_existed('ob_id',               keys_dic=config['new_config'], key_name_to_use='optical-band-parent'))
            resources.append(is_key_existed('bidir',               keys_dic=config['new_config']))
            #resources.append(is_key_existed('name',      keys_dic=config['new_config'], key_name_to_use='channel_name'))

        if device.device_type == DeviceTypeEnum.OPEN_ROADM._value_ :
                resources.append(is_key_existed('band', keys_dic=config['new_config'], key_name_to_use='band'))

                for t_port in handled_flow:
                    for i in  list(t_port):
                        if i :
                            t_circuit ={}
                            for c in config['interfaces'] :

                                ports_list = c["port"].split('/')

                                if i in ports_list  :
                                    # in case it has no type the targeted port has no configuration yet
                                    if c['type'] =='Null' :
                                        resources.append({'resource_key': 'interface_list'+'-'+i, 'value': c["interface_list"]   })
                                        resources.append({"resource_key":"supporting-circuit-pack-name"+'-'+i,"value":c["circuit_pack_name"]})
                                        resources.append({"resource_key":"administrative_state"+'-'+i,"value":c["administrative_state"]})
                                        resources.append({"resource_key":"frequency","value":c["frequency"]})
                                        resources.append({'resource_key': 'interface_type'+'-'+i, 'value': "Null"  })
                                    # in case it has nmc type , extract only the interface name which may be used later in cross connection
                                    elif c['type'] == 'nmc':
                                        resources.append({'resource_key': 'interface_name'+'-'+i+'-'+'nmc', 'value': c["name"]   })
                                        resources.append({'resource_key': 'interface_list'+'-'+i, 'value': c["interface_list"]   })
                                        resources.append({'resource_key': 'interface_type'+'-'+i+'-'+'nmc', 'value': "nmc"  })
                                    elif c['type'] == 'srg':
                                        resources.append({'resource_key': 'interface_name'+'-'+i+'-'+'srg', 'value': c["name"]   })
                                        resources.append({'resource_key': 'interface_list'+'-'+i, 'value': c["interface_list"]   })
                                        resources.append({'resource_key': 'interface_type'+'-'+i+'-'+'srg', 'value': "srg"  })


        if not is_opticalband:

            if 'frequency' in config['new_config'] and 'band' in config['new_config'] and conditions['edit_type'] == 'media-channel':
                if config['new_config']['frequency'] is not None and config['new_config']['band'] is not None:
                    lower_frequency = int(int(config['new_config']['frequency']) - (int(config['new_config']['band'])/2)+1)
                    upper_frequency = int(int(config['new_config']['frequency']) + (int(config['new_config']['band'])/2))
                resources.append(flow_id)
                #resources.append({'resource_key':'index','value':config['new_config']['flow_id'] if 'flow_id' in config['new_config'] else None})
        else:
            lower_frequency = config['new_config']['low-freq'] if 'low-freq' in config['new_config'] else None
            upper_frequency = config['new_config']['up-freq' ] if 'up-freq'  in config['new_config'] else None
            resources.append(is_key_existed('ob_id', keys_dic=config['new_config'], key_name_to_use='index'))
            #resources.append({'resource_key':'index','value':config['new_config']['ob_id'] if 'ob_id' in config['new_config'] else None})
        resources.append({'resource_key': 'lower-frequency', 'value': lower_frequency})
        resources.append({'resource_key': 'upper-frequency', 'value': upper_frequency})

    return [resources, conditions]
