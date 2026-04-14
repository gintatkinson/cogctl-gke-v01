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

import functools, logging, sys, time
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from uuid import uuid4

from .ResourceOsmClient import OsmNBI, OsmNST, VimAccounts, VimAccountItem


BIND_ADDRESS = '0.0.0.0'
BIND_PORT    = 443
BASE_URL     = '/osm'
STR_ENDPOINT = 'https://{:s}:{:s}{:s}'.format(str(BIND_ADDRESS), str(BIND_PORT), str(BASE_URL))
LOG_LEVEL    = logging.DEBUG

logging.basicConfig(level=LOG_LEVEL, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
logging.getLogger('werkzeug').setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


def log_request(logger : logging.Logger, response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    logger.info('%s %s %s %s %s', timestamp, request.remote_addr, request.method, request.full_path, response.status)
    return response

class Health(Resource):
    def get(self):
        LOGGER.info('health request received')
        return make_response(jsonify({"hola"}), 200)
    
class OsmAdmin(Resource):
    def post(self):
        LOGGER.info('token request received')
        data = request.get_json(silent=True) or {}

        token = str(uuid4())

        return jsonify({"id": token})

def main():
    LOGGER.info('Starting...')
    
    app = Flask(__name__)
    app.after_request(functools.partial(log_request, LOGGER))

    api = Api(app, prefix=BASE_URL)

    api.add_resource(
        Health, '/'
    )
    api.add_resource(
        OsmNBI, '/nsilcm/v1/netslice_instances_content'
    )
    api.add_resource(
        OsmAdmin, '/admin/v1/tokens'
    )
    api.add_resource(
        OsmNST, '/nst/v1/netslice_templates'
    )
    api.add_resource(
        VimAccounts, '/admin/v1/vim_accounts'
    )

    api.add_resource(
        VimAccountItem, '/admin/v1/vim_accounts/<string:account_id>'
    )

    LOGGER.info('Listening on {:s}...'.format(str(STR_ENDPOINT)))
    app.run(debug=True, host=BIND_ADDRESS, port=BIND_PORT, ssl_context='adhoc')

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
