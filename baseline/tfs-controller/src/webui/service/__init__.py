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

import json
from typing import List, Tuple, Union
from flask import Flask, session
from flask_healthz import healthz, HealthError
from common.tools.grpc.Tools import grpc_message_to_json
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from common.Settings import (
    is_deployed_bgpls, is_deployed_load_gen, is_deployed_optical,
    is_deployed_policy, is_deployed_qkd_app, is_deployed_slice
)

def get_working_context() -> str:
    return session['context_uuid'] if 'context_uuid' in session else '---'

def get_working_topology() -> str:
    return session['topology_uuid'] if 'topology_uuid' in session else '---'

def liveness():
    pass

def readiness():
    try:  # this component is ready when it is able to connect with the other components it depends on
        context_client = ContextClient()
        context_client.connect()
        context_client.close()
        device_client = DeviceClient()
        device_client.connect()
        device_client.close()
    except Exception as e:
        raise HealthError("Can't connect with the service: {:s}".format(str(e))) from e

def json_to_list(json_str : str) -> List[Union[str, Tuple[str, str]]]:
    try:
        data = json.loads(json_str)
    except: # pylint: disable=bare-except
        return [('item', str(json_str))]

    if isinstance(data, dict):
        return [('kv', (key, value)) for key, value in data.items()]
    elif isinstance(data, list):
        if len(data) == 1 and isinstance(data[0], dict):
            return [('kv', (key, value)) for key, value in data[0].items()]
        else:
            return [('item', ', '.join([str(d) for d in data]))]
    else:
        return [('item', str(data))]

class SetSubAppMiddleware():
    def __init__(self, app, web_app_root):
        self.app = app
        self.web_app_root = web_app_root

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.web_app_root
        environ['APPLICATION_ROOT'] = self.web_app_root
        return self.app(environ, start_response)

def create_app(use_config=None, web_app_root=None):
    app = Flask(__name__)
    if use_config:
        app.config.from_mapping(**use_config)

    app.config.update(HEALTHZ={
        'live': liveness,
        'ready': readiness
    })

    app.register_blueprint(healthz, url_prefix='/healthz')

    from webui.service.js.routes import js                          # pylint: disable=import-outside-toplevel
    app.register_blueprint(js)

    from webui.service.main.routes import main                      # pylint: disable=import-outside-toplevel
    app.register_blueprint(main)

    from webui.service.load_gen.routes import load_gen              # pylint: disable=import-outside-toplevel
    app.register_blueprint(load_gen)

    from webui.service.base_optical.route import base_optical       # pylint: disable=import-outside-toplevel
    app.register_blueprint(base_optical)

    from webui.service.opticalconfig.routes import opticalconfig    # pylint: disable=import-outside-toplevel
    app.register_blueprint(opticalconfig)

    from webui.service.optical_link.routes import optical_link      # pylint: disable=import-outside-toplevel
    app.register_blueprint(optical_link)

    from webui.service.service.routes import service                # pylint: disable=import-outside-toplevel
    app.register_blueprint(service)

    from webui.service.slice.routes import slice                    # pylint: disable=import-outside-toplevel,redefined-builtin
    app.register_blueprint(slice)

    from webui.service.device.routes import device                  # pylint: disable=import-outside-toplevel
    app.register_blueprint(device)
    
    from webui.service.bgpls.routes import bgpls                    # pylint: disable=import-outside-toplevel
    app.register_blueprint(bgpls)

    from webui.service.link.routes import link                      # pylint: disable=import-outside-toplevel
    app.register_blueprint(link)

    from webui.service.qkd_app.routes import qkd_app                # pylint: disable=import-outside-toplevel
    app.register_blueprint(qkd_app)

    from webui.service.policy_rule.routes import policy_rule        # pylint: disable=import-outside-toplevel
    app.register_blueprint(policy_rule)

    app.jinja_env.globals.update({              # pylint: disable=no-member
        'enumerate'           : enumerate,
        'grpc_message_to_json': grpc_message_to_json,
        'json_to_list'        : json_to_list,
        'round'               : round,
        'get_working_context' : get_working_context,
        'get_working_topology': get_working_topology,

        'is_deployed_bgpls'   : is_deployed_bgpls,
        'is_deployed_load_gen': is_deployed_load_gen,
        'is_deployed_optical' : is_deployed_optical,
        'is_deployed_policy'  : is_deployed_policy,
        'is_deployed_qkd_app' : is_deployed_qkd_app,
        'is_deployed_slice'   : is_deployed_slice,
    })

    if web_app_root is not None and len(web_app_root) > 0:
        app.wsgi_app = SetSubAppMiddleware(app.wsgi_app, web_app_root)
    return app
