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

# Mock IPM controller (implements minimal support)

import functools, json, logging, sys, time, uuid
from typing import Any, Dict, Optional, Tuple
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource

BIND_ADDRESS = '0.0.0.0'
BIND_PORT    = 8444
IPM_USERNAME = 'xr-user-1'
IPM_PASSWORD = 'xr-user-1'
STR_ENDPOINT = 'https://{:s}:{:s}'.format(str(BIND_ADDRESS), str(BIND_PORT))
LOG_LEVEL    = logging.DEBUG

CONSTELLATION = {
    'id': 'ofc-constellation',
    'hubModule': {'state': {
        'module': {'moduleName': 'OFC HUB 1', 'trafficMode': 'L1Mode', 'capacity': 100},
        'endpoints': [{'moduleIf': {'clientIfAid': 'XR-T1'}}, {'moduleIf': {'clientIfAid': 'XR-T4'}}]
    }},
    'leafModules': [
        {'state': {
            'module': {'moduleName': 'OFC LEAF 1', 'trafficMode': 'L1Mode', 'capacity': 100},
            'endpoints': [{'moduleIf': {'clientIfAid': 'XR-T1'}}]
        }},
        {'state': {
            'module': {'moduleName': 'OFC LEAF 2', 'trafficMode': 'L1Mode', 'capacity': 100},
            'endpoints': [{'moduleIf': {'clientIfAid': 'XR-T1'}}]
        }}
    ]
}

CONNECTIONS : Dict[str, Any] = dict()
STATE_NAME_TO_CONNECTION : Dict[str, str] = dict()

def select_module_state(module_name : str) -> Optional[Dict]:
    hub_module_state = CONSTELLATION.get('hubModule', {}).get('state', {})
    if module_name == hub_module_state.get('module', {}).get('moduleName'): return hub_module_state
    for leaf_module in CONSTELLATION.get('leafModules', []):
        leaf_module_state = leaf_module.get('state', {})
        if module_name == leaf_module_state.get('module', {}).get('moduleName'): return leaf_module_state
    return None

def select_endpoint(module_state : Dict, module_if : str) -> Optional[Dict]:
    for endpoint in module_state.get('endpoints', []):
        if module_if == endpoint.get('moduleIf', {}).get('clientIfAid'): return endpoint
    return None

def select_module_endpoint(selector : Dict) -> Optional[Tuple[Dict, Dict]]:
    selected_module_name = selector['moduleIfSelectorByModuleName']['moduleName']
    selected_module_if = selector['moduleIfSelectorByModuleName']['moduleClientIfAid']
    module_state = select_module_state(selected_module_name)
    if module_state is None: return None
    return module_state, select_endpoint(module_state, selected_module_if)

def compose_endpoint(endpoint_selector : Dict) -> Dict:
   module, endpoint = select_module_endpoint(endpoint_selector['selector'])
   return {
       'href': '/' + str(uuid.uuid4()),
       'state': {
            'moduleIf': {
                'moduleName': module['module']['moduleName'],
                'clientIfAid': endpoint['moduleIf']['clientIfAid'],
            },
            'capacity': module['module']['capacity'],
        }
    }

logging.basicConfig(level=LOG_LEVEL, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
LOGGER = logging.getLogger(__name__)

logging.getLogger('werkzeug').setLevel(logging.WARNING)

def log_request(logger : logging.Logger, response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    logger.info('%s %s %s %s %s', timestamp, request.remote_addr, request.method, request.full_path, response.status)
    return response

class OpenIdConnect(Resource):
    ACCESS_TOKENS = {}

    def post(self):
        if request.content_type != 'application/x-www-form-urlencoded': return make_response('bad content type', 400)
        if request.content_length == 0: return make_response('bad content length', 400)
        request_form = request.form
        if request_form.get('client_id') != 'xr-web-client': return make_response('bad client_id', 403)
        if request_form.get('client_secret') != 'xr-web-client': return make_response('bad client_secret', 403)
        if request_form.get('grant_type') != 'password': return make_response('bad grant_type', 403)
        if request_form.get('username') != IPM_USERNAME: return make_response('bad username', 403)
        if request_form.get('password') != IPM_PASSWORD: return make_response('bad password', 403)
        access_token = OpenIdConnect.ACCESS_TOKENS.setdefault(IPM_USERNAME, uuid.uuid4())
        reply = {'access_token': access_token, 'expires_in': 86400}
        return make_response(jsonify(reply), 200)

class XrNetworks(Resource):
    def get(self):
        query = json.loads(request.args.get('q'))
        hub_module_name = query.get('hubModule.state.module.moduleName')
        if hub_module_name != 'OFC HUB 1': return make_response('unexpected hub module', 404)
        return make_response(jsonify([CONSTELLATION]), 200)

class XrNetworkConnections(Resource):
    def get(self):
        query = json.loads(request.args.get('q'))
        state_name = query.get('state.name')
        if state_name is None:
            connections = [connection for connection in CONNECTIONS.values()]
        else:
            connection_uuid = STATE_NAME_TO_CONNECTION.get(state_name)
            if connection_uuid is None: return make_response('state name not found', 404)
            connection = CONNECTIONS.get(connection_uuid)
            if connection is None: return make_response('connection for state name not found', 404)
            connections = [connection]
        return make_response(jsonify(connections), 200)

    def post(self):
        if request.content_type != 'application/json': return make_response('bad content type', 400)
        if request.content_length == 0: return make_response('bad content length', 400)
        request_json = request.json
        if not isinstance(request_json, list): return make_response('content is not list', 400)
        reply = []
        for connection in request_json:
            connection_uuid = str(uuid.uuid4())
            state_name = connection['name']

            if state_name is not None: STATE_NAME_TO_CONNECTION[state_name] = connection_uuid
            CONNECTIONS[connection_uuid] = {
                'href': '/network-connections/{:s}'.format(str(connection_uuid)),
                'config': {
                    'implicitTransportCapacity': connection['implicitTransportCapacity']
                    # 'mc': ??
                },
                'state': {
                    'name': state_name,
                    'serviceMode': connection['serviceMode']
                    # 'outerVID' : ??
                },
                'endpoints': [
                    compose_endpoint(endpoint)
                    for endpoint in connection['endpoints']
                ]
            }
            reply.append(CONNECTIONS[connection_uuid])
        return make_response(jsonify(reply), 202)

class XrNetworkConnection(Resource):
    def get(self, connection_uuid : str):
        connection = CONNECTIONS.get(connection_uuid)
        if connection is None: return make_response('unexpected connection id', 404)
        return make_response(jsonify(connection), 200)

    def delete(self, connection_uuid : str):
        connection = CONNECTIONS.pop(connection_uuid, None)
        if connection is None: return make_response('unexpected connection id', 404)
        state_name = connection['state']['name']
        STATE_NAME_TO_CONNECTION.pop(state_name, None)
        return make_response(jsonify({}), 202)

def main():
    LOGGER.info('Starting...')
    
    app = Flask(__name__)
    app.after_request(functools.partial(log_request, LOGGER))

    api = Api(app)
    api.add_resource(OpenIdConnect,        '/realms/xr-cm/protocol/openid-connect/token')
    api.add_resource(XrNetworks,           '/api/v1/xr-networks')
    api.add_resource(XrNetworkConnections, '/api/v1/network-connections')
    api.add_resource(XrNetworkConnection,  '/api/v1/network-connections/<string:connection_uuid>')

    LOGGER.info('Listening on {:s}...'.format(str(STR_ENDPOINT)))
    app.run(debug=True, host=BIND_ADDRESS, port=BIND_PORT, ssl_context='adhoc')

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
