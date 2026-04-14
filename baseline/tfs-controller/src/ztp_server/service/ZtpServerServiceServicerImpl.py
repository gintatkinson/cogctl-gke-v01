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

import grpc, logging, json, os
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.ztp_server_pb2 import ProvisioningScriptName, ProvisioningScript, ZtpFileName, ZtpFile
from common.proto.ztp_server_pb2_grpc import ZtpServerServiceServicer

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('ZTP_SERVER', 'RPC')


class ZtpServerServiceServicerImpl(ZtpServerServiceServicer):
    def __init__(self):
        LOGGER.info('Creating Servicer...')
        LOGGER.info('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetProvisioningScript(self, request : ProvisioningScriptName, context : grpc.ServicerContext) -> ProvisioningScript:
        try:
            provisioningPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', request.scriptname)
            with open(provisioningPath, 'r') as provisioning_file:
                provisioning_content = provisioning_file.read()
            return ProvisioningScript(script=provisioning_content)
        except FileNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('File not found')
            return ProvisioningScript()
