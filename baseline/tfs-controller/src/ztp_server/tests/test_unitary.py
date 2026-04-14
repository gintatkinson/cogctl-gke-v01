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

import grpc, pytest, logging, json
from ztp_server.client.ZtpClient import ZtpClient
from common.proto.ztp_server_pb2 import ProvisioningScriptName, ProvisioningScript, ZtpFileName, ZtpFile

from common.tools.grpc.Tools import grpc_message_to_json_string

from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    ztp_client
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def test_GetProvisioningScript(
    ztp_client : ZtpClient,
):  # pylint: disable=redefined-outer-name

    ztp_provisioning_file_request = ProvisioningScriptName()
    ztp_provisioning_file_request.scriptname = "provisioning_script_sonic.sh" # pylint: disable=no-member
    ztp_reply = ztp_client.GetProvisioningScript(ztp_provisioning_file_request)

    LOGGER.debug('retrieved_data={:s}'.format(grpc_message_to_json_string(ztp_reply)))
    assert ztp_reply.script.startswith("#!/bin/bash")
