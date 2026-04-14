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

import logging, os, re, time
from typing import Dict, List
from common.Constants import (
    DEFAULT_GRPC_BIND_ADDRESS, DEFAULT_GRPC_GRACE_PERIOD,
    DEFAULT_GRPC_MAX_WORKERS, DEFAULT_HTTP_BIND_ADDRESS,
    DEFAULT_LOG_LEVEL, DEFAULT_METRICS_PORT, DEFAULT_SERVICE_GRPC_PORTS,
    DEFAULT_SERVICE_HTTP_BASEURLS, DEFAULT_SERVICE_HTTP_PORTS,
    ServiceNameEnum
)

LOGGER = logging.getLogger(__name__)

DEFAULT_RESTART_DELAY = 5.0 # seconds

ENVVAR_KUBERNETES_PORT            = 'KUBERNETES_PORT'
ENVVAR_GRPC_BIND_ADDRESS          = 'GRPC_BIND_ADDRESS'
ENVVAR_GRPC_MAX_WORKERS           = 'GRPC_MAX_WORKERS'
ENVVAR_GRPC_GRACE_PERIOD          = 'GRPC_GRACE_PERIOD'
ENVVAR_HTTP_BIND_ADDRESS          = 'HTTP_BIND_ADDRESS'
ENVVAR_LOG_LEVEL                  = 'LOG_LEVEL'
ENVVAR_METRICS_PORT               = 'METRICS_PORT'

ENVVAR_SUFIX_SERVICE_BASEURL_HTTP = 'SERVICE_BASEURL_HTTP'
ENVVAR_SUFIX_SERVICE_HOST         = 'SERVICE_HOST'
ENVVAR_SUFIX_SERVICE_PORT_GRPC    = 'SERVICE_PORT_GRPC'
ENVVAR_SUFIX_SERVICE_PORT_HTTP    = 'SERVICE_PORT_HTTP'

def find_environment_variables(
    environment_variable_names : List[str] = []
) -> Dict[str, str]:
    environment_variable : Dict[str, str] = dict()
    for name in environment_variable_names:
        if name not in os.environ: continue
        environment_variable[name] = os.environ[name]
    return environment_variable

def wait_for_environment_variables(
    required_environment_variables : List[str] = [], wait_delay_seconds : float = DEFAULT_RESTART_DELAY
) -> None:
    if ENVVAR_KUBERNETES_PORT not in os.environ: return # Not running in Kubernetes
    found = find_environment_variables(required_environment_variables)
    missing = set(required_environment_variables).difference(set(found.keys()))
    if len(missing) == 0: return # We have all environment variables defined
    MSG = 'Variables({:s}) are missing in Environment({:s}), restarting in {:f} seconds...'
    LOGGER.error(MSG.format(str(missing), str(os.environ), wait_delay_seconds))
    time.sleep(wait_delay_seconds)
    raise Exception('Restarting...') # pylint: disable=broad-exception-raised

def get_setting(name, **kwargs):
    value = os.environ.get(name)
    if 'settings' in kwargs:
        value = kwargs['settings'].pop(name, value)
    if value is not None: return value
    if 'default' in kwargs: return kwargs['default']
    # pylint: disable=broad-exception-raised
    raise Exception('Setting({:s}) not specified in environment or configuration'.format(str(name)))

def get_env_var_name(service_name : ServiceNameEnum, env_var_group):
    service_name = re.sub(r'[^a-zA-Z0-9]', '_', service_name.value)
    return ('{:s}SERVICE_{:s}'.format(service_name, env_var_group)).upper()

def get_service_host(service_name : ServiceNameEnum):
    envvar_name = get_env_var_name(service_name, ENVVAR_SUFIX_SERVICE_HOST)
    default_value = ('{:s}service'.format(service_name.value))
    return get_setting(envvar_name, default=default_value)

def get_service_port_grpc(service_name : ServiceNameEnum):
    envvar_name = get_env_var_name(service_name, ENVVAR_SUFIX_SERVICE_PORT_GRPC)
    default_value = DEFAULT_SERVICE_GRPC_PORTS.get(service_name.value)
    return int(get_setting(envvar_name, default=default_value))

def get_service_port_http(service_name : ServiceNameEnum):
    envvar_name = get_env_var_name(service_name, ENVVAR_SUFIX_SERVICE_PORT_HTTP)
    default_value = DEFAULT_SERVICE_HTTP_PORTS.get(service_name.value)
    return int(get_setting(envvar_name, default=default_value))

def get_service_baseurl_http(service_name : ServiceNameEnum):
    envvar_name = get_env_var_name(service_name, ENVVAR_SUFIX_SERVICE_BASEURL_HTTP)
    default_value = DEFAULT_SERVICE_HTTP_BASEURLS.get(service_name.value)
    return get_setting(envvar_name, default=default_value)

def get_log_level():
    return get_setting(ENVVAR_LOG_LEVEL, default=DEFAULT_LOG_LEVEL)

def get_metrics_port():
    return int(get_setting(ENVVAR_METRICS_PORT, default=DEFAULT_METRICS_PORT))

def get_grpc_bind_address():
    return get_setting(ENVVAR_GRPC_BIND_ADDRESS, default=DEFAULT_GRPC_BIND_ADDRESS)

def get_grpc_max_workers():
    return int(get_setting(ENVVAR_GRPC_MAX_WORKERS, default=DEFAULT_GRPC_MAX_WORKERS))

def get_grpc_grace_period():
    return int(get_setting(ENVVAR_GRPC_GRACE_PERIOD, default=DEFAULT_GRPC_GRACE_PERIOD))

def get_http_bind_address():
    return get_setting(ENVVAR_HTTP_BIND_ADDRESS, default=DEFAULT_HTTP_BIND_ADDRESS)


##### ----- Detect deployed microservices ----- #####

def is_microservice_deployed(service_name : ServiceNameEnum) -> bool:
    host_env_var_name = get_env_var_name(service_name, ENVVAR_SUFIX_SERVICE_HOST     )
    port_env_var_name = get_env_var_name(service_name, ENVVAR_SUFIX_SERVICE_PORT_GRPC)
    return (host_env_var_name in os.environ) and (port_env_var_name in os.environ)

def is_deployed_bgpls     () -> bool: return is_microservice_deployed(ServiceNameEnum.BGPLS            )
def is_deployed_e2e_orch  () -> bool: return is_microservice_deployed(ServiceNameEnum.E2EORCHESTRATOR  )
def is_deployed_forecaster() -> bool: return is_microservice_deployed(ServiceNameEnum.FORECASTER       )
def is_deployed_load_gen  () -> bool: return is_microservice_deployed(ServiceNameEnum.LOAD_GENERATOR   )
def is_deployed_optical   () -> bool: return is_microservice_deployed(ServiceNameEnum.OPTICALCONTROLLER)
def is_deployed_policy    () -> bool: return is_microservice_deployed(ServiceNameEnum.POLICY           )
def is_deployed_qkd_app   () -> bool: return is_microservice_deployed(ServiceNameEnum.QKD_APP          )
def is_deployed_slice     () -> bool: return is_microservice_deployed(ServiceNameEnum.SLICE            )
def is_deployed_te        () -> bool: return is_microservice_deployed(ServiceNameEnum.TE               )
