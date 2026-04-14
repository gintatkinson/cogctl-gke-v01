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

import enum, json, logging
import pyangbind.lib.pybindJSON as pybindJSON
from flask import request
from flask.json import jsonify
from flask_restful import Resource
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.Settings import get_setting
from common.proto.context_pb2 import ContextId, Empty
from common.tools.context_queries.Topology import get_topology_details
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from nbi.service._tools.Authentication import HTTP_AUTH
from nbi.service._tools.HttpStatusCodes import HTTP_OK, HTTP_SERVERERROR
from .bindings import ietf_network
from .ComposeNetwork import compose_network
from .ManualFixes import manual_fixes
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

TE_TOPOLOGY_NAMES = [
    'providerId-10-clientId-0-topologyId-1',
    'providerId-10-clientId-0-topologyId-2'
]

class Renderer(enum.Enum):
    LIBYANG   = 'LIBYANG'
    PYANGBIND = 'PYANGBIND'

DEFAULT_RENDERER = Renderer.LIBYANG
USE_RENDERER = get_setting('IETF_NETWORK_RENDERER', default=DEFAULT_RENDERER.value)


class Networks(Resource):
    @HTTP_AUTH.login_required
    def get(self):
        LOGGER.info('Request: {:s}'.format(str(request)))
        topology_id = ''
        try:
            context_client = ContextClient()

            if USE_RENDERER == Renderer.PYANGBIND.value:
                #target = get_slice_by_uuid(context_client, vpn_id, rw_copy=True)
                #if target is None:
                #    raise Exception('VPN({:s}) not found in database'.format(str(vpn_id)))

                ietf_nets = ietf_network()

                topology_details = get_topology_details(
                    context_client, DEFAULT_TOPOLOGY_NAME, context_uuid=DEFAULT_CONTEXT_NAME,
                    #rw_copy=True
                )
                if topology_details is None:
                    MSG = 'Topology({:s}/{:s}) not found'
                    raise Exception(MSG.format(DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME))

                for te_topology_name in TE_TOPOLOGY_NAMES:
                    ietf_net = ietf_nets.networks.network.add(te_topology_name)
                    compose_network(ietf_net, te_topology_name, topology_details)

                # TODO: improve these workarounds to enhance performance
                json_response = json.loads(pybindJSON.dumps(ietf_nets, mode='ietf'))

                # Workaround; pyangbind does not allow to set otn_topology / eth-tran-topology
                manual_fixes(json_response)
            elif USE_RENDERER == Renderer.LIBYANG.value:
                yang_handler = YangHandler()
                json_response = []

                contexts = context_client.ListContexts(Empty()).contexts
                context_names = [context.name for context in contexts]
                LOGGER.info(f'Contexts detected: {context_names}')

                for context_name in context_names:
                    topologies = context_client.ListTopologies(ContextId(**json_context_id(context_name))).topologies
                    topology_names = [topology.name for topology in topologies]
                    LOGGER.info(f'Topologies detected for context {context_name}: {topology_names}')

                    for topology_name in topology_names:
                        topology_details = get_topology_details(context_client, topology_name, context_name)
                        if topology_details is None:
                            raise Exception(f'Topology({context_name}/{topology_name}) not found')

                        network_reply = yang_handler.compose_network(topology_name, topology_details)
                        json_response.append(network_reply)

                yang_handler.destroy()
            else:
                raise Exception('Unsupported Renderer: {:s}'.format(str(USE_RENDERER)))

            response = jsonify(json_response)
            response.status_code = HTTP_OK

        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Something went wrong Retrieving Topology({:s})'.format(str(topology_id)))
            response = jsonify({'error': str(e)})
            response.status_code = HTTP_SERVERERROR
        return response
