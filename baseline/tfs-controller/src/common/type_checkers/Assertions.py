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
from typing import Callable, Dict


LOGGER = logging.getLogger(__name__)

# ----- Enumerations ---------------------------------------------------------------------------------------------------
def validate_config_action_enum(message):
    assert isinstance(message, str)
    assert message in [
        'CONFIGACTION_UNDEFINED',
        'CONFIGACTION_SET',
        'CONFIGACTION_DELETE',
    ]

def validate_constraint_action_enum(message):
    assert isinstance(message, str)
    assert message in [
        'CONSTRAINTACTION_UNDEFINED',
        'CONSTRAINTACTION_SET',
        'CONSTRAINTACTION_DELETE',
    ]

def validate_device_driver_enum(message):
    assert isinstance(message, str)
    assert message in [
        'DEVICEDRIVER_UNDEFINED',
        'DEVICEDRIVER_OPENCONFIG',
        'DEVICEDRIVER_TRANSPORT_API',
        'DEVICEDRIVER_P4',
        'DEVICEDRIVER_IETF_NETWORK_TOPOLOGY',
        'DEVICEDRIVER_ONF_TR_532',
        'DEVICEDRIVER_XR',
        'DEVICEDRIVER_IETF_L2VPN',
        'DEVICEDRIVER_GNMI_OPENCONFIG',
        'DEVICEDRIVER_OPTICAL_TFS',
        'DEVICEDRIVER_IETF_ACTN',
        'DEVICEDRIVER_OC',
        'DEVICEDRIVER_QKD',
        'DEVICEDRIVER_IETF_L3VPN',
        'DEVICEDRIVER_IETF_SLICE',
        'DEVICEDRIVER_NCE',
        'DEVICEDRIVER_SMARTNIC',
        'DEVICEDRIVER_MORPHEUS',
        'DEVICEDRIVER_RYU',
        'DEVICEDRIVER_GNMI_NOKIA_SRLINUX',
        'DEVICEDRIVER_OPENROADM',
        'DEVICEDRIVER_GNMI_OPENCONFIG',
    ]

def validate_device_operational_status_enum(message):
    assert isinstance(message, str)
    assert message in [
        'DEVICEOPERATIONALSTATUS_UNDEFINED',
        'DEVICEOPERATIONALSTATUS_DISABLED',
        'DEVICEOPERATIONALSTATUS_ENABLED',
    ]

def validate_isolation_level_enum(message):
    assert isinstance(message, str)
    assert message in [
        'NO_ISOLATION',
        'PHYSICAL_ISOLATION',
        'LOGICAL_ISOLATION',
        'PROCESS_ISOLATION',
        'PHYSICAL_MEMORY_ISOLATION',
        'PHYSICAL_NETWORK_ISOLATION',
        'VIRTUAL_RESOURCE_ISOLATION',
        'NETWORK_FUNCTIONS_ISOLATION',
        'SERVICE_ISOLATION',
    ]

def validate_kpi_sample_types_enum(message):
    assert isinstance(message, str)
    assert message in [
        'KPISAMPLETYPE_UNKNOWN',
        'KPISAMPLETYPE_PACKETS_TRANSMITTED',
        'KPISAMPLETYPE_PACKETS_RECEIVED',
        'KPISAMPLETYPE_BYTES_TRANSMITTED',
        'KPISAMPLETYPE_BYTES_RECEIVED',
        'KPISAMPLETYPE_LINK_TOTAL_CAPACITY_GBPS',
        'KPISAMPLETYPE_LINK_USED_CAPACITY_GBPS',
    ]

def validate_link_type_enum(message):
    assert isinstance(message, str)
    assert message in [
        'LINKTYPE_UNKNOWN',
        'LINKTYPE_COPPER',
        'LINKTYPE_VIRTUAL_COPPER',
        'LINKTYPE_OPTICAL',
        'LINKTYPE_VIRTUAL_OPTICAL',
    ]

def validate_service_type_enum(message):
    assert isinstance(message, str)
    assert message in [
        'SERVICETYPE_UNKNOWN',
        'SERVICETYPE_L3NM',
        'SERVICETYPE_L2NM',
        'SERVICETYPE_TAPI_CONNECTIVITY_SERVICE',
        'SERVICETYPE_TE',
        'SERVICETYPE_E2E',
        'SERVICETYPE_IP_LINK'
        'SERVICETYPE_OPTICAL_CONNECTIVITY',
        'SERVICETYPE_QKD',
        'SERVICETYPE_IPOWDM',
        'SERVICETYPE_TAPI_LSP',
    ]

def validate_service_state_enum(message):
    assert isinstance(message, str)
    assert message in [
        'SERVICESTATUS_UNDEFINED',
        'SERVICESTATUS_PLANNED',
        'SERVICESTATUS_ACTIVE',
        'SERVICESTATUS_UPDATING',
        'SERVICESTATUS_PENDING_REMOVAL',
        'SERVICESTATUS_SLA_VIOLATED',
    ]

def validate_slice_status_enum(message):
    assert isinstance(message, str)
    assert message in [
        'SLICESTATUS_UNDEFINED',
        'SLICESTATUS_PLANNED',
        'SLICESTATUS_INIT',
        'SLICESTATUS_ACTIVE',
        'SLICESTATUS_DEINIT',
        'SLICESTATUS_SLA_VIOLATED',
    ]


# ----- Common ---------------------------------------------------------------------------------------------------------
def validate_uuid(message, allow_empty=False):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'uuid' in message
    assert isinstance(message['uuid'], str)
    if allow_empty: return
    assert len(message['uuid']) > 1

CONFIG_RULE_TYPES = {
    'custom',
    'acl',
    'ip_link',
    'ipowdm',
    'tapi_lsp'
}
def validate_config_rule(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 2
    assert 'action' in message
    validate_config_action_enum(message['action'])
    other_keys = set(list(message.keys()))
    other_keys.discard('action')
    config_rule_type = other_keys.pop()
    assert config_rule_type in CONFIG_RULE_TYPES
    assert config_rule_type == 'custom', 'ConfigRule Type Validator for {:s} not implemented'.format(config_rule_type)
    custom : Dict = message['custom']
    assert len(custom.keys()) == 2
    assert 'resource_key' in custom
    assert isinstance(custom['resource_key'], str)
    assert 'resource_value' in custom
    assert isinstance(custom['resource_value'], str)

def validate_config_rules(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'config_rules' in message
    for config_rule in message['config_rules']: validate_config_rule(config_rule)

def validate_constraint_custom(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 2
    assert 'constraint_type' in message
    assert isinstance(message['constraint_type'], str)
    assert 'constraint_value' in message
    assert isinstance(message['constraint_value'], str)

def validate_constraint_schedule(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 2
    assert 'start_timestamp' in message
    assert isinstance(message['start_timestamp'], (int, float))
    assert 'duration_days' in message
    assert isinstance(message['duration_days'], (int, float))

def validate_constraint_endpoint_priority(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 2
    assert 'endpoint_id' in message
    validate_endpoint_id(message['endpoint_id'])
    assert 'priority' in message
    assert isinstance(message['priority'], int)

def validate_constraint_sla_capacity(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'capacity_gbps' in message
    assert isinstance(message['capacity_gbps'], (int, float))

def validate_constraint_sla_latency(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'e2e_latency_ms' in message
    assert isinstance(message['e2e_latency_ms'], (int, float))

def validate_constraint_sla_availability(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 3
    assert 'num_disjoint_paths' in message
    assert isinstance(message['num_disjoint_paths'], int)
    assert message['num_disjoint_paths'] >= 0
    assert 'all_active' in message
    assert isinstance(message['all_active'], bool)
    assert 'availability' in message
    assert isinstance(message['availability'], (int, float))
    assert message['availability'] >= 0 and message['availability'] <= 100

def validate_constraint_sla_isolation(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'isolation_level' in message
    assert isinstance(message['isolation_level'], list)
    for isolation_level in message['isolation_level']:
        validate_isolation_level_enum(isolation_level)

CONSTRAINT_TYPE_TO_VALIDATOR = {
    'custom'            : validate_constraint_custom,
    'schedule'          : validate_constraint_schedule,
    #'endpoint_location' : validate_constraint_endpoint_location,
    'endpoint_priority' : validate_constraint_endpoint_priority,
    'sla_capacity'      : validate_constraint_sla_capacity,
    'sla_latency'       : validate_constraint_sla_latency,
    'sla_availability'  : validate_constraint_sla_availability,
    'sla_isolation'     : validate_constraint_sla_isolation,
    #'exclusions'        : validate_constraint_exclusions,
    #'qos_profile'       : validate_constraint_qos_profile,
}

def validate_constraint(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 2
    assert 'action' in message
    validate_constraint_action_enum(message['action'])
    other_keys = set(list(message.keys()))
    other_keys.discard('action')
    constraint_type = other_keys.pop()
    validator : Callable = CONSTRAINT_TYPE_TO_VALIDATOR.get(constraint_type)
    assert validator is not None, 'Constraint Type Validator for {:s} not implemented'.format(constraint_type)
    validator(message[constraint_type])


# ----- Identifiers ----------------------------------------------------------------------------------------------------

def validate_context_id(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'context_uuid' in message
    validate_uuid(message['context_uuid'])

def validate_service_id(message, context_uuid=None):
    assert isinstance(message, dict)
    assert len(message.keys()) == 2
    assert 'context_id' in message
    validate_context_id(message['context_id'])
    if context_uuid is not None: assert message['context_id']['context_uuid']['uuid'] == context_uuid
    assert 'service_uuid' in message
    validate_uuid(message['service_uuid'])

def validate_topology_id(message, context_uuid=None):
    assert isinstance(message, dict)
    assert len(message.keys()) == 2
    assert 'context_id' in message
    validate_context_id(message['context_id'])
    if context_uuid is not None: assert message['context_id']['context_uuid']['uuid'] == context_uuid
    assert 'topology_uuid' in message
    validate_uuid(message['topology_uuid'])

def validate_device_id(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'device_uuid' in message
    validate_uuid(message['device_uuid'])

def validate_link_id(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'link_uuid' in message
    validate_uuid(message['link_uuid'])

def validate_endpoint_id(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 3
    assert 'topology_id' in message
    validate_topology_id(message['topology_id'])
    assert 'device_id' in message
    validate_device_id(message['device_id'])
    assert 'endpoint_uuid' in message
    validate_uuid(message['endpoint_uuid'])

def validate_connection_id(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'connection_uuid' in message
    validate_uuid(message['connection_uuid'])

def validate_slice_id(message, context_uuid = None):
    assert isinstance(message, dict)
    assert len(message.keys()) == 2
    assert 'context_id' in message
    validate_context_id(message['context_id'])
    if context_uuid is not None: assert message['context_id']['context_uuid']['uuid'] == context_uuid
    assert 'slice_uuid' in message
    validate_uuid(message['slice_uuid'])


# ----- Lists of Identifiers -------------------------------------------------------------------------------------------

def validate_context_ids(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'context_ids' in message
    assert isinstance(message['context_ids'], list)
    for context_id in message['context_ids']: validate_context_id(context_id)

def validate_service_ids(message, context_uuid=None):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'service_ids' in message
    assert isinstance(message['service_ids'], list)
    for service_id in message['service_ids']: validate_service_id(service_id, context_uuid=context_uuid)

def validate_slice_ids(message, context_uuid=None):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'slice_ids' in message
    assert isinstance(message['slice_ids'], list)
    for slice_id in message['slice_ids']: validate_slice_id(slice_id, context_uuid=context_uuid)

def validate_topology_ids(message, context_uuid=None):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'topology_ids' in message
    assert isinstance(message['topology_ids'], list)
    for topology_id in message['topology_ids']: validate_topology_id(topology_id, context_uuid=context_uuid)

def validate_device_ids(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'device_ids' in message
    assert isinstance(message['device_ids'], list)
    for device_id in message['device_ids']: validate_device_id(device_id)

def validate_link_ids(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'link_ids' in message
    assert isinstance(message['link_ids'], list)
    for link_id in message['link_ids']: validate_link_id(link_id)

def validate_connection_ids(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'connection_ids' in message
    assert isinstance(message['connection_ids'], list)
    for connection_id in message['connection_ids']: validate_connection_id(connection_id)


# ----- Objects --------------------------------------------------------------------------------------------------------

def validate_context(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 5
    assert 'context_id' in message
    validate_context_id(message['context_id'])
    context_uuid = message['context_id']['context_uuid']['uuid']
    assert 'name' in message
    assert isinstance(message['name'], str)
    assert 'topology_ids' in message
    assert isinstance(message['topology_ids'], list)
    for topology_id in message['topology_ids']: validate_topology_id(topology_id, context_uuid=context_uuid)
    assert 'service_ids' in message
    assert isinstance(message['service_ids'], list)
    for service_id in message['service_ids']: validate_service_id(service_id, context_uuid=context_uuid)
    assert 'slice_ids' in message
    assert isinstance(message['slice_ids'], list)
    for slice_id in message['slice_ids']: validate_slice_id(slice_id, context_uuid=context_uuid)

def validate_service_state(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'service_status' in message
    validate_service_state_enum(message['service_status'])

def validate_slice_status(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'slice_status' in message
    validate_slice_status_enum(message['slice_status'])

def validate_service(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 7
    assert 'service_id' in message
    validate_service_id(message['service_id'])
    assert 'name' in message
    assert isinstance(message['name'], str)
    assert 'service_type' in message
    validate_service_type_enum(message['service_type'])
    assert 'service_endpoint_ids' in message
    assert isinstance(message['service_endpoint_ids'], list)
    for endpoint_id in message['service_endpoint_ids']: validate_endpoint_id(endpoint_id)
    assert 'service_constraints' in message
    assert isinstance(message['service_constraints'], list)
    for constraint in message['service_constraints']: validate_constraint(constraint)
    assert 'service_status' in message
    validate_service_state(message['service_status'])
    assert 'service_config' in message
    validate_config_rules(message['service_config'])

def validate_slice(message):
    assert isinstance(message, dict)
    assert len(message.keys()) in {8, 9}
    assert 'slice_id' in message
    validate_slice_id(message['slice_id'])
    assert 'name' in message
    assert isinstance(message['name'], str)
    assert 'slice_endpoint_ids' in message
    assert isinstance(message['slice_endpoint_ids'], list)
    for endpoint_id in message['slice_endpoint_ids']: validate_endpoint_id(endpoint_id)
    assert 'slice_constraints' in message
    assert isinstance(message['slice_constraints'], list)
    for constraint in message['slice_constraints']: validate_constraint(constraint)
    assert 'slice_service_ids' in message
    assert isinstance(message['slice_service_ids'], list)
    for service_id in message['slice_service_ids']: validate_service_id(service_id)
    assert 'slice_subslice_ids' in message
    assert isinstance(message['slice_subslice_ids'], list)
    for slice_id in message['slice_subslice_ids']: validate_slice_id(slice_id)
    assert 'slice_status' in message
    validate_slice_status(message['slice_status'])
    assert 'slice_config' in message
    validate_config_rules(message['slice_config'])
    if len(message.keys()) == 9:
        assert 'slice_owner' in message
        assert isinstance(message['slice_owner'], dict)
        assert 'owner_uuid' in message['slice_owner']
        validate_uuid(message['slice_owner']['owner_uuid'])
        assert 'owner_string' in message['slice_owner']
        assert isinstance(message['slice_owner']['owner_string'], str)

def validate_topology(message, num_devices=None, num_links=None):
    assert isinstance(message, dict)
    assert len(message.keys()) == 5
    assert 'topology_id' in message
    validate_topology_id(message['topology_id'])
    assert 'name' in message
    assert isinstance(message['name'], str)
    assert 'device_ids' in message
    assert isinstance(message['device_ids'], list)
    if num_devices is not None: assert len(message['device_ids']) == num_devices
    for device_id in message['device_ids']: validate_device_id(device_id)
    assert 'link_ids' in message
    assert isinstance(message['link_ids'], list)
    if num_links is not None: assert len(message['link_ids']) == num_links
    for link_id in message['link_ids']: validate_link_id(link_id)
    assert 'optical_link_ids' in message
    assert isinstance(message['optical_link_ids'], list)
    #if num_links is not None: assert len(message['optical_link_ids']) == num_links
    for link_id in message['optical_link_ids']: validate_link_id(link_id)

def validate_endpoint(message):
    assert isinstance(message, dict)
    assert len(message.keys()) in {5, 6}, 'Wrong number of attributes: {:s}'.format(str(message))
    assert 'endpoint_id' in message
    validate_endpoint_id(message['endpoint_id'])
    assert 'name' in message
    assert isinstance(message['name'], str)
    assert 'endpoint_type' in message
    assert isinstance(message['endpoint_type'], str)
    assert 'kpi_sample_types' in message
    assert isinstance(message['kpi_sample_types'], list)
    for kpi_sample_type in message['kpi_sample_types']: validate_kpi_sample_types_enum(kpi_sample_type)
    if 'endpoint_location' in message:
        #assert 'endpoint_location' in message
        # TODO: validate "endpoint_location"
        pass
    if 'capabilities' in message:
        #assert 'capabilities' in message
        # TODO: validate "capabilities"
        pass

def validate_component(component):
    assert isinstance(component, dict)
    assert len(component.keys()) == 5
    assert 'component_uuid' in component
    validate_uuid(component['component_uuid'])
    assert 'name' in component
    assert isinstance(component['name'], str)
    assert 'type' in component
    assert isinstance(component['type'], str)
    assert 'attributes' in component
    assert isinstance(component['attributes'], dict)
    for k,v in component['attributes'].items():
        assert isinstance(k, str)
        assert isinstance(v, str)
    assert 'parent' in component
    assert isinstance(component['parent'], str)

def validate_link_attributes(link_attributes):
    assert isinstance(link_attributes, dict)
    assert len(link_attributes.keys()) == 3
    assert 'is_bidirectional' in link_attributes
    assert isinstance(link_attributes['is_bidirectional'], bool)
    assert 'total_capacity_gbps' in link_attributes
    assert isinstance(link_attributes['total_capacity_gbps'], (int, float))
    assert 'used_capacity_gbps' in link_attributes
    assert isinstance(link_attributes['used_capacity_gbps'], (int, float))

def validate_device(message):
    assert isinstance(message, dict)
    assert len(message.keys()) in {8, 9}
    assert 'device_id' in message
    validate_device_id(message['device_id'])
    assert 'name' in message
    assert isinstance(message['name'], str)
    assert 'device_type' in message
    assert isinstance(message['device_type'], str)
    assert 'device_config' in message
    validate_config_rules(message['device_config'])
    assert 'device_operational_status' in message
    validate_device_operational_status_enum(message['device_operational_status'])
    assert 'device_drivers' in message
    assert isinstance(message['device_drivers'], list)
    for driver in message['device_drivers']: validate_device_driver_enum(driver)
    assert 'device_endpoints' in message
    assert isinstance(message['device_endpoints'], list)
    for endpoint in message['device_endpoints']: validate_endpoint(endpoint)
    assert 'components' in message
    assert isinstance(message['components'], list)
    for component in message['components']: validate_component(component)
    if len(message.keys()) == 9:
        assert 'controller_id' in message
        if len(message['controller_id']) > 0:
            validate_device_id(message['controller_id'])

def validate_link(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 5
    assert 'link_id' in message
    validate_link_id(message['link_id'])
    assert 'name' in message
    assert isinstance(message['name'], str)
    assert 'link_endpoint_ids' in message
    assert isinstance(message['link_endpoint_ids'], list)
    for endpoint_id in message['link_endpoint_ids']: validate_endpoint_id(endpoint_id)
    assert 'attributes' in message
    validate_link_attributes(message['attributes'])
    assert 'link_type' in message
    validate_link_type_enum(message['link_type'])

def validate_connection(message):
    assert isinstance(message, dict)
    assert len(message.keys()) in {4, 5}
    assert 'connection_id' in message
    validate_connection_id(message['connection_id'])
    assert 'service_id' in message
    validate_service_id(message['service_id'])
    assert 'path_hops_endpoint_ids' in message
    assert isinstance(message['path_hops_endpoint_ids'], list)
    for endpoint_id in message['path_hops_endpoint_ids']: validate_endpoint_id(endpoint_id)
    assert 'sub_service_ids' in message
    assert isinstance(message['sub_service_ids'], list)
    for sub_service_id in message['sub_service_ids']: validate_service_id(sub_service_id)
    if len(message.keys()) == 5:
        assert 'settings' in message
        assert isinstance(message['settings'], dict)
        # TODO: improve validation of data types, especially for uint values, IP/MAC addresses, TCP/UDP ports, etc.
        if 'l0' in message['settings']:
            assert isinstance(message['settings']['l0'], dict)
            if 'lsp_symbolic_name' in message['settings']['l0']:
                assert isinstance(message['settings']['l0']['lsp_symbolic_name'], str)
        if 'l2' in message['settings']:
            assert isinstance(message['settings']['l2'], dict)
            if 'src_mac_address' in message['settings']['l2']:
                assert isinstance(message['settings']['l2']['src_mac_address'], str)
            if 'dst_mac_address' in message['settings']['l2']:
                assert isinstance(message['settings']['l2']['dst_mac_address'], str)
            if 'ether_type' in message['settings']['l2']:
                assert isinstance(message['settings']['l2']['ether_type'], int)
            if 'vlan_id' in message['settings']['l2']:
                assert isinstance(message['settings']['l2']['vlan_id'], int)
            if 'mpls_label' in message['settings']['l2']:
                assert isinstance(message['settings']['l2']['mpls_label'], int)
            if 'mpls_traffic_class' in message['settings']['l2']:
                assert isinstance(message['settings']['l2']['mpls_traffic_class'], int)
        if 'l3' in message['settings']:
            assert isinstance(message['settings']['l3'], dict)
            if 'src_ip_address' in message['settings']['l3']:
                assert isinstance(message['settings']['l3']['src_ip_address'], str)
            if 'dst_ip_address' in message['settings']['l3']:
                assert isinstance(message['settings']['l3']['dst_ip_address'], str)
            if 'dscp' in message['settings']['l3']:
                assert isinstance(message['settings']['l3']['dscp'], int)
            if 'protocol' in message['settings']['l3']:
                assert isinstance(message['settings']['l3']['protocol'], int)
            if 'ttl' in message['settings']['l3']:
                assert isinstance(message['settings']['l3']['ttl'], int)
        if 'l4' in message['settings']:
            assert isinstance(message['settings']['l4'], dict)
            if 'src_port' in message['settings']['l4']:
                assert isinstance(message['settings']['l4']['src_port'], int)
            if 'dst_port' in message['settings']['l4']:
                assert isinstance(message['settings']['l4']['dst_port'], int)
            if 'tcp_flags' in message['settings']['l4']:
                assert isinstance(message['settings']['l4']['tcp_flags'], int)
            if 'ttl' in message['settings']['l4']:
                assert isinstance(message['settings']['l4']['ttl'], int)


# ----- Lists of Objects -----------------------------------------------------------------------------------------------

def validate_contexts(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'contexts' in message
    assert isinstance(message['contexts'], list)
    for context in message['contexts']: validate_context(context)

def validate_services(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'services' in message
    assert isinstance(message['services'], list)
    for service in message['services']: validate_service(service)

def validate_slices(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'slices' in message
    assert isinstance(message['slices'], list)
    for slice_ in message['slices']: validate_slice(slice_)

def validate_topologies(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'topologies' in message
    assert isinstance(message['topologies'], list)
    for topology in message['topologies']: validate_topology(topology)

def validate_devices(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'devices' in message
    assert isinstance(message['devices'], list)
    for device in message['devices']: validate_device(device)

def validate_links(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'links' in message
    assert isinstance(message['links'], list)
    for link in message['links']: validate_link(link)

def validate_connections(message):
    assert isinstance(message, dict)
    assert len(message.keys()) == 1
    assert 'connections' in message
    assert isinstance(message['connections'], list)
    for connection in message['connections']: validate_connection(connection)
