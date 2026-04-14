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
from data import ADDLIGHTPATH_REPLY

BIND_ADDRESS = '0.0.0.0'
BIND_PORT    = 8443
BASE_URL     = '/OpticalTFS'
STR_ENDPOINT = 'https://{:s}:{:s}{:s}'.format(str(BIND_ADDRESS), str(BIND_PORT), str(BASE_URL))
LOG_LEVEL    = logging.DEBUG


logging.basicConfig(level=LOG_LEVEL, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
LOGGER = logging.getLogger(__name__)
logging.getLogger('werkzeug').setLevel(logging.WARNING)

def log_request(logger : logging.Logger, response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    logger.info('%s %s %s %s %s', timestamp, request.remote_addr, request.method, request.full_path, response.status)
    return response

class AddLightpath(Resource):
    def put(self, src_node: str, dst_node: str, bitrate: int):
        return make_response(jsonify(ADDLIGHTPATH_REPLY), 200)

class DelLightpath(Resource):
    def delete(self, flow_id: str, src_node: str, dst_node: str, bitrate: int):
        return make_response(jsonify({}), 200)

class GetLightpaths(Resource):
    def get(self):
        return make_response(jsonify({}), 200)

class GetLinks(Resource):
    def get(self):
        return make_response(jsonify({}), 200)


def main():
    LOGGER.info('Starting...')
    
    app = Flask(__name__)
    app.after_request(functools.partial(log_request, LOGGER))

    api = Api(app, prefix=BASE_URL)
    api.add_resource(AddLightpath,  '/AddLightpath/<string:src_node>/<string:dst_node>/<string:bitrate>')
    api.add_resource(DelLightpath,  '/DelLightpath/<string:flow_id>/<string:src_node>/<string:dst_node>/<string:bitrate>')
    api.add_resource(GetLightpaths, '/GetLightpaths')
    api.add_resource(GetLinks,      '/GetLinks')

    LOGGER.info('Listening on {:s}...'.format(str(STR_ENDPOINT)))
    app.run(debug=True, host=BIND_ADDRESS, port=BIND_PORT)

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
