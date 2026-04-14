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

# Mock MicroWave SDN controller
# -----------------------------
# REST server implementing minimal support for:
# - IETF YANG data model for Network Topology
#       Ref: https://www.rfc-editor.org/rfc/rfc8345.html
# - IETF YANG data model for Transport Network Client Signals
#       Ref: https://www.ietf.org/archive/id/draft-ietf-ccamp-client-signal-yang-07.html


# Ref: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
# Ref: https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful

import functools, logging, sys, time
from flask import Flask, abort, jsonify, make_response, request
from flask_restful import Api, Resource

BIND_ADDRESS = '0.0.0.0'
BIND_PORT    = 8443
BASE_URL     = '/nmswebs/restconf/data'
STR_ENDPOINT = 'https://{:s}:{:s}{:s}'.format(str(BIND_ADDRESS), str(BIND_PORT), str(BASE_URL))
LOG_LEVEL    = logging.DEBUG

NETWORK_NODES = [
    {'node-id': '192.168.27.139', 'ietf-network-topology:termination-point': [
        {'tp-id': '1', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '2', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '3', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '4', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '5', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '6', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '10', 'ietf-te-topology:te': {'name': 'antena' }},
    ]},
    {'node-id': '192.168.27.140', 'ietf-network-topology:termination-point': [
        {'tp-id': '1', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '2', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '3', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '4', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '5', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '6', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '10', 'ietf-te-topology:te': {'name': 'antena' }},
    ]},
    {'node-id': '192.168.27.141', 'ietf-network-topology:termination-point': [
        {'tp-id': '1', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '2', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '3', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '4', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '5', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '6', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '10', 'ietf-te-topology:te': {'name': 'antena' }},
    ]},
    {'node-id': '192.168.27.142', 'ietf-network-topology:termination-point': [
        {'tp-id': '1', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '2', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '3', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '4', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '5', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '6', 'ietf-te-topology:te': {'name': 'ethernet'}},
        {'tp-id': '10', 'ietf-te-topology:te': {'name': 'antena' }},
    ]}
]
NETWORK_LINKS = [
    {   'link-id'    : '192.168.27.139:10--192.168.27.140:10',
        'source'     : {'source-node': '192.168.27.139', 'source-tp': '10'},
        'destination': {'dest-node'  : '192.168.27.140', 'dest-tp'  : '10'},
    },
    {   'link-id'    : '192.168.27.141:10--192.168.27.142:10',
        'source'     : {'source-node': '192.168.27.141', 'source-tp': '10'},
        'destination': {'dest-node'  : '192.168.27.142', 'dest-tp'  : '10'},
    }
]
NETWORK_SERVICES = {}


logging.basicConfig(level=LOG_LEVEL, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
LOGGER = logging.getLogger(__name__)

logging.getLogger('werkzeug').setLevel(logging.WARNING)

def log_request(logger : logging.Logger, response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    logger.info('%s %s %s %s %s', timestamp, request.remote_addr, request.method, request.full_path, response.status)
    return response

class Health(Resource):
    def get(self):
        return make_response(jsonify({}), 200)

class Network(Resource):
    def get(self, network_uuid : str):
        if network_uuid != 'SIAE-ETH-TOPOLOGY': abort(400)
        network = {'node': NETWORK_NODES, 'ietf-network-topology:link': NETWORK_LINKS}
        return make_response(jsonify({'ietf-network:network': network}), 200)

class Services(Resource):
    def get(self):
        services = [service for service in NETWORK_SERVICES.values()]
        return make_response(jsonify({'ietf-eth-tran-service:etht-svc': {'etht-svc-instances': services}}), 200)

    def post(self):
        json_request = request.get_json()
        if not json_request: abort(400)
        if not isinstance(json_request, dict): abort(400)
        if 'etht-svc-instances' not in json_request: abort(400)
        json_services = json_request['etht-svc-instances']
        if not isinstance(json_services, list): abort(400)
        if len(json_services) != 1: abort(400)
        svc_data = json_services[0]
        etht_svc_name = svc_data['etht-svc-name']
        NETWORK_SERVICES[etht_svc_name] = svc_data
        return make_response(jsonify({}), 201)

class DelServices(Resource):
    def delete(self, service_uuid : str):
        NETWORK_SERVICES.pop(service_uuid, None)
        return make_response(jsonify({}), 204)

def main():
    LOGGER.info('Starting...')
    
    app = Flask(__name__)
    app.after_request(functools.partial(log_request, LOGGER))

    api = Api(app, prefix=BASE_URL)
    api.add_resource(Health,      '/ietf-network:networks')
    api.add_resource(Network,     '/ietf-network:networks/network=<string:network_uuid>')
    api.add_resource(Services,    '/ietf-eth-tran-service:etht-svc')
    api.add_resource(DelServices, '/ietf-eth-tran-service:etht-svc/etht-svc-instances=<string:service_uuid>')

    LOGGER.info('Listening on {:s}...'.format(str(STR_ENDPOINT)))
    app.run(debug=True, host=BIND_ADDRESS, port=BIND_PORT, ssl_context='adhoc')

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
