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

import hashlib, sys, logging
from prometheus_client import start_http_server
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name,
    get_log_level, get_metrics_port, get_service_baseurl_http, get_service_port_http,
    get_setting, wait_for_environment_variables
)
from webui.service import create_app
from webui.Config import MAX_CONTENT_LENGTH, HOST, SECRET_KEY, DEBUG

def create_unique_session_cookie_name() -> str:
    hostname = get_setting('HOSTNAME')
    if hostname is None: return 'session'
    hasher = hashlib.blake2b(digest_size=8)
    hasher.update(hostname.encode('UTF-8'))
    return 'session:{:s}'.format(str(hasher.hexdigest()))

def main():
    log_level = get_log_level()
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)

    wait_for_environment_variables([
        get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
        get_env_var_name(ServiceNameEnum.DEVICE,  ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.DEVICE,  ENVVAR_SUFIX_SERVICE_PORT_GRPC),
        get_env_var_name(ServiceNameEnum.SERVICE, ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.SERVICE, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
    ])

    logger.info('Starting...')

    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    host = get_setting('HOST', default=HOST)
    service_port = get_service_port_http(ServiceNameEnum.WEBUI)
    web_app_root = get_service_baseurl_http(ServiceNameEnum.WEBUI)
    debug = get_setting('DEBUG', default=DEBUG)
    if isinstance(debug, str): debug = (debug.upper() in {'T', '1', 'TRUE'})

    app = create_app(use_config={
        'SECRET_KEY'          : SECRET_KEY,
        'MAX_CONTENT_LENGTH'  : MAX_CONTENT_LENGTH,
        'SESSION_COOKIE_NAME' : create_unique_session_cookie_name(),
        'WTF_CSRF_ENABLED'    : False,
    }, web_app_root=web_app_root)

    app.run(host=host, port=service_port, debug=debug)

    logger.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
