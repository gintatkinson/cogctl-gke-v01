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

import logging, netaddr
from typing import Dict, List, Optional, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import Service, ServiceStatusEnum, ServiceTypeEnum
from common.tools.context_queries.Service import get_service_by_uuid
from common.tools.grpc.ConfigRules import update_config_rule_custom
from common.tools.grpc.Constraints import (
    update_constraint_endpoint_location, update_constraint_sla_availability, update_constraint_sla_capacity,
    update_constraint_sla_latency
)
from common.tools.grpc.EndPointIds import update_endpoint_ids
from context.client.ContextClient import ContextClient
from service.client.ServiceClient import ServiceClient

LOGGER = logging.getLogger(__name__)

def create_service(
    service_uuid : str, context_uuid : Optional[str] = DEFAULT_CONTEXT_NAME
) -> Optional[Exception]:
    # pylint: disable=no-member
    service_request = Service()
    service_request.service_id.context_id.context_uuid.uuid = context_uuid
    service_request.service_id.service_uuid.uuid = service_uuid
    service_request.service_type = ServiceTypeEnum.SERVICETYPE_L3NM
    service_request.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED

    try:
        service_client = ServiceClient()
        service_client.CreateService(service_request)
        return None
    except Exception as e: # pylint: disable=broad-except
        LOGGER.exception('Unhandled exception creating Service')
        return e

def process_vpn_service(
    vpn_service : Dict, errors : List[Dict]
) -> None:
    vpn_id = vpn_service['vpn-id']
    exc = create_service(vpn_id)
    if exc is not None: errors.append({'error': str(exc)})

def update_service_endpoint(
    service_uuid : str, site_id : str, device_uuid : str, endpoint_uuid : str,
    vlan_tag : int, ipv4_address : str, neighbor_ipv4_address : str, ipv4_prefix_length : int,
    capacity_gbps : Optional[float] = None, e2e_latency_ms : Optional[float] = None,
    availability : Optional[float] = None, mtu : Optional[int] = None,
    static_routing : Optional[Dict[Tuple[str, int, int], str]] = None,
    context_uuid : Optional[str] = DEFAULT_CONTEXT_NAME, 
) -> Optional[Exception]:
    context_client = ContextClient()
    service = get_service_by_uuid(context_client, service_uuid, context_uuid=context_uuid, rw_copy=True)
    if service is None: raise Exception('VPN({:s}) not found in database'.format(str(service_uuid)))

    endpoint_ids = service.service_endpoint_ids
    endpoint_id =  update_endpoint_ids(endpoint_ids, device_uuid, endpoint_uuid)

    constraints  = service.service_constraints
    update_constraint_endpoint_location(constraints, endpoint_id, region=site_id)
    if capacity_gbps  is not None: update_constraint_sla_capacity    (constraints, capacity_gbps)
    if e2e_latency_ms is not None: update_constraint_sla_latency     (constraints, e2e_latency_ms)
    if availability   is not None: update_constraint_sla_availability(constraints, 1, True, availability)

    config_rules = service.service_config.config_rules

    service_settings_key = '/settings'
    service_settings = {'address_families': (['IPV4'], True)}
    if mtu is not None: service_settings['mtu'] = (mtu, True)
    update_config_rule_custom(config_rules, service_settings_key, service_settings)

    if static_routing is not None:
        service_static_routing_key = '/static_routing'
        update_config_rule_custom(config_rules, service_static_routing_key, {
            '{:d}-{:s}/{:d}'.format(lan_tag, ip_range, ip_prefix_len): (
                {'vlan-id': lan_tag, 'ip-network': '{:s}/{:d}'.format(ip_range, ip_prefix_len), 'next-hop': next_hop},
                True
            )
            for (ip_range, ip_prefix_len, lan_tag), next_hop in static_routing.items()
        })

    #ENDPOINT_SETTINGS_KEY = '/device[{:s}]/endpoint[{:s}]/vlan[{:d}]/settings'
    #endpoint_settings_key = ENDPOINT_SETTINGS_KEY.format(device_uuid, endpoint_uuid, vlan_tag)
    ENDPOINT_SETTINGS_KEY = '/device[{:s}]/endpoint[{:s}]/settings'
    endpoint_settings_key = ENDPOINT_SETTINGS_KEY.format(device_uuid, endpoint_uuid)
    field_updates = {}
    if vlan_tag              is not None: field_updates['vlan_tag'        ] = (vlan_tag,              True)
    if ipv4_address          is not None: field_updates['ip_address'      ] = (ipv4_address,          True)
    if neighbor_ipv4_address is not None: field_updates['neighbor_address'] = (neighbor_ipv4_address, True)
    if ipv4_prefix_length    is not None: field_updates['prefix_length'   ] = (ipv4_prefix_length,    True)
    update_config_rule_custom(config_rules, endpoint_settings_key, field_updates)

    try:
        service_client = ServiceClient()
        service_client.UpdateService(service)
        return None
    except Exception as e: # pylint: disable=broad-except
        LOGGER.exception('Unhandled exception updating Service')
        return e

def process_site_network_access(
    site_id : str, network_access : Dict, site_static_routing : Dict[Tuple[str, int, int], str], errors : List[Dict]
) -> None:
    endpoint_uuid = network_access['site-network-access-id']

    if 'ietf-l3vpn-svc' in network_access['site-network-access-type']:
        # replace 'ietf-l3vpn-svc:multipoint' with 'multipoint' for backward compatibility
        network_access['site-network-access-type'] = network_access['site-network-access-type'].replace('ietf-l3vpn-svc:', '')
    if network_access['site-network-access-type'] != 'multipoint':
        MSG = 'Site Network Access Type: {:s}'
        raise NotImplementedError(MSG.format(str(network_access['site-network-access-type'])))

    device_uuid  = network_access['device-reference']
    service_uuid = network_access['vpn-attachment']['vpn-id']

    access_role : str = network_access['vpn-attachment']['site-role']
    access_role = access_role.replace('ietf-l3vpn-svc:', '').replace('-role', '') # hub/spoke
    if access_role not in {'hub', 'spoke'}:
        MSG = 'Site VPN Attackment Role: {:s}'
        raise NotImplementedError(MSG.format(str(network_access['site-network-access-type'])))

    ipv4_allocation = network_access['ip-connection']['ipv4']
    if 'ietf-l3vpn-svc' in ipv4_allocation['address-allocation-type']:
        # replace 'ietf-l3vpn-svc:static-address' with 'static-address' for backward compatibility
        ipv4_allocation['address-allocation-type'] = ipv4_allocation['address-allocation-type'].replace('ietf-l3vpn-svc:', '')
    if ipv4_allocation['address-allocation-type'] != 'static-address':
        MSG = 'Site Network Access IPv4 Allocation Type: {:s}'
        raise NotImplementedError(MSG.format(str(ipv4_allocation['address-allocation-type'])))
    ipv4_allocation_addresses = ipv4_allocation['addresses']
    ipv4_provider_address = ipv4_allocation_addresses.get('provider-address')
    ipv4_customer_address = ipv4_allocation_addresses['customer-address']
    ipv4_prefix_length    = ipv4_allocation_addresses['prefix-length'   ]

    vlan_tag = None
    ipv4_provider_range = netaddr.IPNetwork('{:s}/{:d}'.format(ipv4_provider_address, ipv4_prefix_length))
    for (_, _, lan_tag), next_hop in site_static_routing.items():
        ip_next_hop = netaddr.IPAddress(next_hop)
        if ip_next_hop not in ipv4_provider_range: continue
        vlan_tag = lan_tag
        break

    ## network_access_static_routing: (lan-range, lan-prefix-len, lan-tag) => next-hop
    #network_access_static_routing : Dict[Tuple[str, str], str] = {}
    #for rt_proto in network_access['routing-protocols']['routing-protocol']:
    #    if rt_proto['type'] != 'ietf-l3vpn-svc:static':
    #        MSG = 'Site Network Access Routing Protocol Type: {:s}'
    #        raise NotImplementedError(MSG.format(str(rt_proto['type'])))
    #    for ipv4_rt in rt_proto['static']['cascaded-lan-prefixes']['ipv4-lan-prefixes']:
    #        lan_range, lan_prefix = ipv4_rt['lan'].split('/')
    #        lan_prefix = int(lan_prefix)
    #        lan_tag   = int(ipv4_rt['lan-tag'].replace('vlan', ''))
    #        next_hop  = ipv4_rt['next-hop']
    #        network_access_static_routing[(lan_range, lan_prefix, lan_tag)] = next_hop

    service_mtu              = network_access['service']['svc-mtu']
    service_input_bandwidth  = network_access['service']['svc-input-bandwidth']
    service_output_bandwidth = network_access['service']['svc-output-bandwidth']
    service_bandwidth_bps    = max(service_input_bandwidth, service_output_bandwidth)
    service_bandwidth_gbps   = service_bandwidth_bps / 1.e9

    max_e2e_latency_ms = None
    availability       = None
    for qos_profile_class in network_access['service']['qos']['qos-profile']['classes']['class']:
        if qos_profile_class['class-id'] != 'qos-realtime':
            MSG = 'Site Network Access QoS Class Id: {:s}'
            raise NotImplementedError(MSG.format(str(qos_profile_class['class-id'])))

        if 'ietf-l3vpn-svc' in qos_profile_class['direction']:
            # replace 'ietf-l3vpn-svc:both' with 'both' for backward compatibility
            qos_profile_class['direction'] = qos_profile_class['direction'].replace('ietf-l3vpn-svc:', '')
        if qos_profile_class['direction'] != 'both':
            MSG = 'Site Network Access QoS Class Direction: {:s}'
            raise NotImplementedError(MSG.format(str(qos_profile_class['direction'])))

        max_e2e_latency_ms = qos_profile_class['latency']['latency-boundary']
        availability       = qos_profile_class['bandwidth']['guaranteed-bw-percent']

    exc = update_service_endpoint(
        service_uuid, site_id, device_uuid, endpoint_uuid,
        vlan_tag, ipv4_customer_address, ipv4_provider_address, ipv4_prefix_length,
        capacity_gbps=service_bandwidth_gbps, e2e_latency_ms=max_e2e_latency_ms, availability=availability,
        mtu=service_mtu, static_routing=site_static_routing
    )
    if exc is not None: errors.append({'error': str(exc)})

def process_site(site : Dict, errors : List[Dict]) -> None:
    site_id = site['site-id']

    # this change is made for ECOC2025 demo purposes
    if site['management']['type'] != 'ietf-l3vpn-svc:provider-managed':
    # if site['management']['type'] == 'customer-managed':
        MSG = 'Site Management Type: {:s}'
        raise NotImplementedError(MSG.format(str(site['management']['type'])))

    # site_static_routing: (lan-range, lan-prefix-len, lan-tag) => next-hop
    site_static_routing : Dict[Tuple[str, int, int], str] = {}
    site_routing_protocols : Dict = site.get('routing-protocols', dict())
    site_routing_protocol : List = site_routing_protocols.get('routing-protocol', list())
    for rt_proto in site_routing_protocol:
        if 'ietf-l3vpn-svc' in rt_proto['type']:
            # replace 'ietf-l3vpn-svc:static' with 'static' for backward compatibility
            rt_proto['type'] = rt_proto['type'].replace('ietf-l3vpn-svc:', '')
        if rt_proto['type'] != 'static':
            MSG = 'Site Routing Protocol Type: {:s}'
            raise NotImplementedError(MSG.format(str(rt_proto['type'])))

        rt_proto_static : Dict = rt_proto.get('static', dict())
        rt_proto_static_clps : Dict = rt_proto_static.get('cascaded-lan-prefixes', dict())
        rt_proto_static_clps_v4 = rt_proto_static_clps.get('ipv4-lan-prefixes', list())
        for ipv4_rt in rt_proto_static_clps_v4:
            lan_range, lan_prefix = ipv4_rt['lan'].split('/')
            lan_prefix = int(lan_prefix)
            lan_tag   = int(ipv4_rt['lan-tag'].replace('vlan', ''))
            next_hop  = ipv4_rt['next-hop']
            site_static_routing[(lan_range, lan_prefix, lan_tag)] = next_hop

    network_accesses : List[Dict] = site['site-network-accesses']['site-network-access']
    for network_access in network_accesses:
        process_site_network_access(site_id, network_access, site_static_routing, errors)

def update_vpn(site : Dict, errors : List[Dict]) -> None:

    if site['management']['type'] != 'ietf-l3vpn-svc:provider-managed':
        MSG = 'Site Management Type: {:s}'
        raise NotImplementedError(MSG.format(str(site['management']['type'])))

    network_accesses : List[Dict] = site['site-network-accesses']['site-network-access']
    for network_access in network_accesses:
        update_site_network_access(network_access, errors)

def update_site_network_access(
    network_access : Dict, errors : List[Dict]
) -> None:

    if network_access['site-network-access-type'] != 'ietf-l3vpn-svc:multipoint':
        MSG = 'Site Network Access Type: {:s}'
        raise NotImplementedError(MSG.format(str(network_access['site-network-access-type'])))

    service_uuid = network_access['vpn-attachment']['vpn-id']

    service_input_bandwidth  = network_access['service']['svc-input-bandwidth']
    service_output_bandwidth = network_access['service']['svc-output-bandwidth']
    service_bandwidth_bps    = max(service_input_bandwidth, service_output_bandwidth)
    service_bandwidth_gbps   = service_bandwidth_bps / 1.e9

    max_e2e_latency_ms = None
    availability       = None

    exc = update_site_endpoint(
        service_uuid, capacity_gbps=service_bandwidth_gbps,
        e2e_latency_ms=max_e2e_latency_ms, availability=availability,
    )
    if exc is not None: errors.append({'error': str(exc)})

def update_site_endpoint(
    service_uuid : str, capacity_gbps : Optional[float] = None,
    e2e_latency_ms : Optional[float] = None, availability : Optional[float] = None,
    context_uuid : Optional[str] = DEFAULT_CONTEXT_NAME
) -> Optional[Exception]:
    context_client = ContextClient()
    service = get_service_by_uuid(context_client, service_uuid, context_uuid=context_uuid, rw_copy=True)
    if service is None: raise Exception('VPN({:s}) not found in database'.format(str(service_uuid)))

    constraints  = service.service_constraints
    if capacity_gbps  is not None: update_constraint_sla_capacity    (constraints, capacity_gbps)
    if e2e_latency_ms is not None: update_constraint_sla_latency     (constraints, e2e_latency_ms)
    if availability   is not None: update_constraint_sla_availability(constraints, 1, True, availability)

    try:
        service_client = ServiceClient()
        service_client.UpdateService(service)
        return None
    except Exception as e: # pylint: disable=broad-except
        LOGGER.exception('Unhandled exception updating Service')
        return e
