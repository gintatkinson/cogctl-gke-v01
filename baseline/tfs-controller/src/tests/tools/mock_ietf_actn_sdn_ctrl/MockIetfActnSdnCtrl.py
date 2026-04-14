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

# Mock IETF ACTN SDN controller
# -----------------------------
# REST server implementing minimal support for:
# - IETF YANG Data Model for Transport Network Client Signals
#       Ref: https://www.ietf.org/archive/id/draft-ietf-ccamp-client-signal-yang-10.html
# - IETF YANG Data Model for Traffic Engineering Tunnels, Label Switched Paths and Interfaces
#       Ref: https://www.ietf.org/archive/id/draft-ietf-teas-yang-te-34.html


import functools, logging, sys, time
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from ResourceEthServices import EthService, EthServices
from ResourceOsuTunnels import OsuTunnel, OsuTunnels

BIND_ADDRESS = '0.0.0.0'
BIND_PORT    = 8443
BASE_URL     = '/restconf/v2/data'
STR_ENDPOINT = 'https://{:s}:{:s}{:s}'.format(str(BIND_ADDRESS), str(BIND_PORT), str(BASE_URL))
LOG_LEVEL    = logging.DEBUG

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

def main():
    LOGGER.info('Starting...')
    
    app = Flask(__name__)
    app.after_request(functools.partial(log_request, LOGGER))

    api = Api(app, prefix=BASE_URL)
    api.add_resource(
        Health, '/'
    )
    api.add_resource(
        OsuTunnels, '/ietf-te:te/tunnels'
    )
    api.add_resource(
        OsuTunnel, '/ietf-te:te/tunnels/tunnel="<string:osu_tunnel_name>"'
    )
    api.add_resource(
        EthServices, '/ietf-eth-tran-service:etht-svc'
    )
    api.add_resource(
        EthService, '/ietf-eth-tran-service:etht-svc/etht-svc-instances="<string:etht_service_name>"'
    )

    LOGGER.info('Listening on {:s}...'.format(str(STR_ENDPOINT)))
    app.run(debug=True, host=BIND_ADDRESS, port=BIND_PORT, ssl_context='adhoc')

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
