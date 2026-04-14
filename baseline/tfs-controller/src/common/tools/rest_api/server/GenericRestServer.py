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

import functools, logging, threading, time
from typing import Optional, Union
from flask import Flask, request
from flask_restful import Api, Resource
from werkzeug.serving import make_server
from common.Settings import get_http_bind_address

logging.getLogger('werkzeug').setLevel(logging.WARNING)


def log_request(logger, response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    logger.info('%s %s %s %s %s', timestamp, request.remote_addr, request.method, request.full_path, response.status)
    return response

class GenericRestServer(threading.Thread):
    def __init__(
        self, bind_port : Union[str, int], base_url : Optional[str] = None,
        bind_address : Optional[str] = None, cls_name : str = __name__
    ) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.logger = logging.getLogger(cls_name)
        self.bind_port = bind_port
        self.base_url = base_url
        self.bind_address = get_http_bind_address() if bind_address is None else bind_address
        self.endpoint = 'http://{:s}:{:s}'.format(str(self.bind_address), str(self.bind_port))
        if self.base_url is not None: self.endpoint += str(self.base_url)
        self.srv = None
        self.ctx = None
        self.app = Flask(__name__)
        self.app.after_request(functools.partial(log_request, self.logger))
        self.api = Api(self.app, prefix=self.base_url)

    def add_resource(self, resource : Resource, *urls, **kwargs):
        self.api.add_resource(resource, *urls, **kwargs)

    def run(self):
        self.srv = make_server(self.bind_address, self.bind_port, self.app, threaded=True)
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.logger.info('Listening on {:s}...'.format(str(self.endpoint)))
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
