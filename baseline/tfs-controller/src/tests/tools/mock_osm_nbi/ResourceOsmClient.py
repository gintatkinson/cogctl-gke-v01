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

import json, logging, uuid
from typing import Dict
from flask import jsonify, make_response, request
from flask_restful import Resource
from hashlib import sha1


LOGGER = logging.getLogger(__name__)


def generate_uuid(raw_string : str) -> str:
    ''' Generate a str(UUID) from the SHA-1 hash of a string. '''
    _hash = sha1(raw_string.encode('utf-8')).digest()
    return str(uuid.UUID(bytes=_hash[:16]))

OSM_VIM : Dict[str, Dict] = {
    generate_uuid('account1') : {
        '_id'      : generate_uuid('account1'),
        'name'     : 'account1',
        'vim_type' : 'account1',
        'tenant'   : 'account1',
        'vim_url'  : 'http://account1.local',
    }
}

OSM_NST : Dict[str, Dict] = {
    generate_uuid('nst1') :             {
        '_id'        : generate_uuid('nst1'),
        'name'       : 'nst1',
        'description': 'Nst_Mock',
        'vendor'     : 'ExampleVendor',
        'version'    : '1.0',
    },
    generate_uuid('nst2') : {
        '_id'        : generate_uuid('nst2'),
        'name'       : 'nst2',
        'description': 'Nst_Mock',
        'vendor'     : 'AnotherVendor',
        'version'    : '2.1',
    },
}

OSM_NSI : Dict[str, Dict] = dict()


class OsmNST(Resource):
    def get(self):
        LOGGER.info('Get NST request received')
        return make_response(jsonify(list(OSM_NST.values())), 200)

class OsmNBI(Resource):
    def get(self):
        LOGGER.info('Get NBI request received')
        return make_response(jsonify(list(OSM_NSI.values())), 200)

    def post(self):
        LOGGER.info('Post request received')
        LOGGER.info('request: {:s}'.format(str(request)))
        LOGGER.info('request.headers: {:s}'.format(str(request.headers)))
        LOGGER.info('request.data: {:s}'.format(str(request.data)))

        try:
            payload = json.loads(request.data)
            LOGGER.info('payload: {:s}'.format(str(payload)))
        except Exception as e:
            MSG = 'Unable to parse payload({:s}) : {:s}'
            error = {'error': MSG.format(str(request.data), str(e))}
            return make_response(jsonify(error), 400)

        nst_id  = payload.get('nstId'         )
        name    = payload.get('nsiName'       )
        desc    = payload.get('nsiDescription') or ''

        new_nsi_id = str(generate_uuid(name))
        new_nsi = {
            'id'               : new_nsi_id,
            'name'             : name,
            'nstId'            : nst_id,
            'description'      : desc,
            'operationalStatus': 'CREATED'
        }
        OSM_NSI[new_nsi_id] = new_nsi
        return make_response(jsonify(new_nsi), 201)


class VimAccounts(Resource):
    '''
    Mock -> /osm/admin/v1/vim_accounts
    Support:
      • GET    → get all VIM Account
      • POST   → Create a VIM Account
    '''
    def get(self):
        return make_response(jsonify(list(OSM_VIM.values())), 200)

    def post(self):
        payload = request.get_json(silent=True) or {}
        name      = payload.get('name')
        vim_type  = payload.get('vim_type')

        if not name or not vim_type:
            error = {'error': 'name and vim_type are required'}
            return make_response(jsonify(error), 400)

        new_vim_id = str(generate_uuid(name))
        new_vim = {
            '_id'     : new_vim_id,
            'name'    : name,
            'vim_type': vim_type,
            'tenant'  : payload.get('tenant', 'admin'),
            'vim_url' : payload.get('vim_url', 'http://mock.local')
        }

        OSM_VIM[new_vim_id] = new_vim
        return make_response(jsonify(new_vim), 201)


class VimAccountItem(Resource):
    '''
    Mock -> /osm/admin/v1/vim_accounts/<account_id>
    Support:
      • GET    → get VIM Account
      • PUT    → Upadate fields
      • DELETE → Delete VIM Account
    '''

    # ------------------------
    # GET /vim_accounts/<id>
    # ------------------------
    def get(self, account_id : str):
        vim_account = OSM_VIM.get(account_id)
        if not vim_account:
            error = {'error': 'not found'}
            return make_response(jsonify(error), 404)
        return make_response(jsonify(vim_account), 200)

    # ------------------------
    # PUT /vim_accounts/<id>
    # ------------------------
    def put(self, account_id : str):
        vim_account = OSM_VIM.get(account_id)
        if not vim_account:
            error = {'error': 'not found'}
            return make_response(jsonify(error), 404)

        payload = request.get_json(silent=True) or {}
        for field in ('name', 'vim_type', 'tenant', 'vim_url'):
            if field in payload:
                vim_account[field] = payload[field]

        return jsonify(vim_account)

    # ------------------------
    # DELETE /vim_accounts/<id>
    # ------------------------
    def delete(self, account_id : str):
        vim_account = OSM_VIM.get(account_id)
        if not vim_account:
            error = {'error': 'not found'}
            return make_response(jsonify(error), 404)

        del OSM_VIM[account_id]
        return make_response(jsonify({}), 204)
