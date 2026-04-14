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

import logging, urllib
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import ContextId
from common.tools.descriptor.Loader import DescriptorLoader
from context.client.ContextClient import ContextClient
from nbi.service.rest_server.RestServer import RestServer
from common.tools.object_factory.Context import json_context_id
from device.tests.qkd.unit.PrepareScenario import mock_service, nbi_service_rest, do_rest_get_request 

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

JSON_ADMIN_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
ADMIN_CONTEXT_ID = ContextId(**JSON_ADMIN_CONTEXT_ID)


# ----- Context --------------------------------------------------------------------------------------------------------

def test_rest_get_context_ids(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    reply = do_rest_get_request('/tfs-api/context_ids')
    print("Context IDs:", reply)

def test_rest_get_contexts(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    reply = do_rest_get_request('/tfs-api/contexts')
    print("Contexts:", reply)

def test_rest_get_context(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request(f'/tfs-api/context/{context_uuid}')
    print("Context data:", reply)


# ----- Topology -------------------------------------------------------------------------------------------------------

def test_rest_get_topology_ids(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request(f'/tfs-api/context/{context_uuid}/topology_ids')
    print("Topology IDs:", reply)

def test_rest_get_topologies(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request(f'/tfs-api/context/{context_uuid}/topologies')
    print("Topologies:", reply)

def test_rest_get_topology(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    topology_uuid = urllib.parse.quote(DEFAULT_TOPOLOGY_NAME)
    reply = do_rest_get_request(f'/tfs-api/context/{context_uuid}/topology/{topology_uuid}')
    print("Topology data:", reply)


# ----- Device ---------------------------------------------------------------------------------------------------------

def test_rest_get_device_ids(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    reply = do_rest_get_request('/tfs-api/device_ids')
    print("Device IDs:", reply)

def test_rest_get_devices(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    reply = do_rest_get_request('/tfs-api/devices')
    print("Devices:", reply)


# ----- Link -----------------------------------------------------------------------------------------------------------

def test_rest_get_link_ids(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    reply = do_rest_get_request('/tfs-api/link_ids')
    print("Link IDs:", reply)

def test_rest_get_links(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    reply = do_rest_get_request('/tfs-api/links')
    print("Links:", reply)


# ----- Service --------------------------------------------------------------------------------------------------------

def test_rest_get_service_ids(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    reply = do_rest_get_request('/tfs-api/link_ids')
    print("Service IDs:", reply)

def test_rest_get_topologies(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request(f'/tfs-api/context/{context_uuid}/services')
    print("Services:", reply)

# ----- Apps -----------------------------------------------------------------------------------------------------------

def test_rest_get_apps(nbi_service_rest: RestServer):  # pylint: disable=redefined-outer-name, unused-argument
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)  # Context ID
    reply = do_rest_get_request(f'/tfs-api/context/{context_uuid}/apps')
    print("Apps:", reply)
