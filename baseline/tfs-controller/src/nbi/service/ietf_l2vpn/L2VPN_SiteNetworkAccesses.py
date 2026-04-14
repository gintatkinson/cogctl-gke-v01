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
from typing import Dict, Optional
from flask import request
from flask.json import jsonify
from flask.wrappers import Response
from flask_restful import Resource
from werkzeug.exceptions import UnsupportedMediaType
from common.proto.context_pb2 import Slice
from common.tools.context_queries.Slice import get_slice_by_uuid
from common.tools.grpc.ConfigRules import update_config_rule_custom
from common.tools.grpc.Constraints import (
    update_constraint_custom_dict, update_constraint_endpoint_location, update_constraint_endpoint_priority,
    update_constraint_sla_availability)
from common.tools.grpc.EndPointIds import update_endpoint_ids
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from slice.client.SliceClient import SliceClient
from nbi.service._tools.Authentication import HTTP_AUTH
from nbi.service._tools.HttpStatusCodes import HTTP_NOCONTENT, HTTP_SERVERERROR
from nbi.service._tools.Validator import validate_message
from .schemas.site_network_access import SCHEMA_SITE_NETWORK_ACCESS
from .Constants import BEARER_MAPPINGS, DEFAULT_ADDRESS_FAMILIES, DEFAULT_BGP_AS, DEFAULT_BGP_ROUTE_TARGET, DEFAULT_MTU

LOGGER = logging.getLogger(__name__)

def process_site_network_access(context_client : ContextClient, site_id : str, site_network_access : Dict) -> Slice:
    vpn_id = site_network_access['vpn-attachment']['vpn-id']
    encapsulation_type = site_network_access['connection']['encapsulation-type']
    cvlan_id = site_network_access['connection']['tagged-interface'][encapsulation_type]['cvlan-id']

    bearer_reference = site_network_access['bearer']['bearer-reference']

    access_priority : Optional[int] = site_network_access.get('availability', {}).get('access-priority')
    single_active   : bool = len(site_network_access.get('availability', {}).get('single-active', [])) > 0
    all_active      : bool = len(site_network_access.get('availability', {}).get('all-active', [])) > 0

    diversity_constraints = site_network_access.get('access-diversity', {}).get('constraints', {}).get('constraint', [])
    raise_if_differs = True
    diversity_constraints = {
        constraint['constraint-type']:([
            target[0]
            for target in constraint['target'].items()
            if len(target[1]) == 1
        ][0], raise_if_differs)
        for constraint in diversity_constraints
    }

    mapping = BEARER_MAPPINGS.get(bearer_reference)
    if mapping is None:
        msg = 'Specified Bearer({:s}) is not configured.'
        raise Exception(msg.format(str(bearer_reference)))
    (
        device_uuid, endpoint_uuid, router_id, route_dist, sub_if_index,
        address_ip, address_prefix, remote_router, circuit_id
    ) = mapping

    target = get_slice_by_uuid(context_client, vpn_id, rw_copy=True)
    if target is None: raise Exception('VPN({:s}) not found in database'.format(str(vpn_id)))

    endpoint_ids = target.slice_endpoint_ids        # pylint: disable=no-member
    config_rules = target.slice_config.config_rules # pylint: disable=no-member
    constraints  = target.slice_constraints         # pylint: disable=no-member

    endpoint_id = update_endpoint_ids(endpoint_ids, device_uuid, endpoint_uuid)

    service_settings_key = '/settings'
    update_config_rule_custom(config_rules, service_settings_key, {
        'mtu'             : (DEFAULT_MTU,              True),
        'address_families': (DEFAULT_ADDRESS_FAMILIES, True),
        'bgp_as'          : (DEFAULT_BGP_AS,           True),
        'bgp_route_target': (DEFAULT_BGP_ROUTE_TARGET, True),
    })

    endpoint_settings_key = '/device[{:s}]/endpoint[{:s}]/settings'.format(device_uuid, endpoint_uuid)
    field_updates = {}
    if router_id      is not None: field_updates['router_id'          ] = (router_id,      True)
    if route_dist     is not None: field_updates['route_distinguisher'] = (route_dist,     True)
    if sub_if_index   is not None: field_updates['sub_interface_index'] = (sub_if_index,   True)
    if cvlan_id       is not None: field_updates['vlan_id'            ] = (cvlan_id,       True)
    if address_ip     is not None: field_updates['address_ip'         ] = (address_ip,     True)
    if address_prefix is not None: field_updates['address_prefix'     ] = (address_prefix, True)
    if remote_router  is not None: field_updates['remote_router'      ] = (remote_router,  True)
    if circuit_id     is not None: field_updates['circuit_id'         ] = (circuit_id,     True)
    update_config_rule_custom(config_rules, endpoint_settings_key, field_updates)

    if len(diversity_constraints) > 0:
        update_constraint_custom_dict(constraints, 'diversity', diversity_constraints)

    update_constraint_endpoint_location(constraints, endpoint_id, region=site_id)
    if access_priority is not None: update_constraint_endpoint_priority(constraints, endpoint_id, access_priority)
    if single_active or all_active:
        # assume 1 disjoint path per endpoint/location included in service/slice
        location_endpoints = {}
        for constraint in constraints:
            if constraint.WhichOneof('constraint') != 'endpoint_location': continue
            str_endpoint_id = grpc_message_to_json_string(constraint.endpoint_location.endpoint_id)
            str_location_id = grpc_message_to_json_string(constraint.endpoint_location.location)
            location_endpoints.setdefault(str_location_id, set()).add(str_endpoint_id)
        num_endpoints_per_location = {len(endpoints) for endpoints in location_endpoints.values()}
        num_disjoint_paths = max(num_endpoints_per_location)
        update_constraint_sla_availability(constraints, num_disjoint_paths, all_active, 0.0)

    return target

def process_list_site_network_access(
        context_client : ContextClient, slice_client : SliceClient, site_id : str, request_data : Dict
    ) -> Response:

    LOGGER.debug('Request: {:s}'.format(str(request_data)))
    validate_message(SCHEMA_SITE_NETWORK_ACCESS, request_data)

    errors = []
    for site_network_access in request_data['ietf-l2vpn-svc:site-network-access']:
        sna_request = process_site_network_access(context_client, site_id, site_network_access)
        LOGGER.debug('sna_request = {:s}'.format(grpc_message_to_json_string(sna_request)))
        try:
            slice_client.UpdateSlice(sna_request)
        except Exception as e: # pylint: disable=broad-except
            msg = 'Something went wrong Updating VPN {:s}'
            LOGGER.exception(msg.format(grpc_message_to_json_string(sna_request)))
            errors.append({'error': str(e)})

    response = jsonify(errors)
    response.status_code = HTTP_NOCONTENT if len(errors) == 0 else HTTP_SERVERERROR
    return response

class L2VPN_SiteNetworkAccesses(Resource):
    @HTTP_AUTH.login_required
    def post(self, site_id : str):
        if not request.is_json: raise UnsupportedMediaType('JSON payload is required')
        LOGGER.debug('Site_Id: {:s}'.format(str(site_id)))
        context_client = ContextClient()
        slice_client = SliceClient()
        return process_list_site_network_access(context_client, slice_client, site_id, request.json)

    @HTTP_AUTH.login_required
    def put(self, site_id : str):
        if not request.is_json: raise UnsupportedMediaType('JSON payload is required')
        LOGGER.debug('Site_Id: {:s}'.format(str(site_id)))
        context_client = ContextClient()
        slice_client = SliceClient()
        return process_list_site_network_access(context_client, slice_client, site_id, request.json)
