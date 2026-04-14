#!/usr/bin/env python3
# Copyright 2022-2024 ETSI OSG/SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import connexion
import json
import sys

from flask import current_app
from tapi_server import encoder
from tapi_server.models.tapi_common_context import TapiCommonContext
from tapi_server import database


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml',
        arguments={'title': 'tapi-notification,tapi-connectivity,tapi-topology,tapi-common,tapi-path-computation API'},
        base_path='/restconf',
        pythonic_params=True)
    with app.app.app_context():
        with current_app.open_resource(sys.argv[2], 'r') as f:
            data = json.load(f)
            database.context = TapiCommonContext.from_dict(data)
    app.run(port=sys.argv[1])

if __name__ == '__main__':
    main()
