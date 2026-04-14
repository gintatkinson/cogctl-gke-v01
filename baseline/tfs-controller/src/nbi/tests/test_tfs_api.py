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


# Enable eventlet for async networking
# NOTE: monkey_patch needs to be executed before importing any other module.
import eventlet
eventlet.monkey_patch()

#pylint: disable=wrong-import-position
import logging, urllib
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import ContextId
from common.tools.descriptor.Loader import (
    DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
)
from common.tools.object_factory.Context import json_context_id
from common.type_checkers.Assertions import (
    validate_connection, validate_connection_ids, validate_connections,
    validate_context, validate_context_ids, validate_contexts,
    validate_device, validate_device_ids, validate_devices,
    validate_link, validate_link_ids, validate_links,
    validate_service, validate_service_ids, validate_services,
    validate_slice, validate_slice_ids, validate_slices,
    validate_topologies, validate_topology, validate_topology_ids
)
from context.client.ContextClient import ContextClient
from nbi.service.NbiApplication import NbiApplication
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    nbi_application, context_client,
    do_rest_get_request
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = 'nbi/tests/data/tfs_api_dummy.json'

JSON_ADMIN_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
ADMIN_CONTEXT_ID = ContextId(**JSON_ADMIN_CONTEXT_ID)


# ----- Prepare Environment --------------------------------------------------------------------------------------------

def test_prepare_environment(context_client : ContextClient) -> None: # pylint: disable=redefined-outer-name
    validate_empty_scenario(context_client)
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    descriptor_loader.validate()

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.topology_ids) == 1
    assert len(response.service_ids ) == 3
    assert len(response.slice_ids   ) == 1


# ----- Context --------------------------------------------------------------------------------------------------------

def test_rest_get_context_ids(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    reply = do_rest_get_request('/tfs-api/context_ids')
    validate_context_ids(reply)

def test_rest_get_contexts(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    reply = do_rest_get_request('/tfs-api/contexts')
    validate_contexts(reply)

def test_rest_get_context(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request('/tfs-api/context/{:s}'.format(context_uuid))
    validate_context(reply)


# ----- Topology -------------------------------------------------------------------------------------------------------

def test_rest_get_topology_ids(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request('/tfs-api/context/{:s}/topology_ids'.format(context_uuid))
    validate_topology_ids(reply)

def test_rest_get_topologies(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request('/tfs-api/context/{:s}/topologies'.format(context_uuid))
    validate_topologies(reply)

def test_rest_get_topology(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    topology_uuid = urllib.parse.quote(DEFAULT_TOPOLOGY_NAME)
    reply = do_rest_get_request('/tfs-api/context/{:s}/topology/{:s}'.format(context_uuid, topology_uuid))
    validate_topology(reply, num_devices=3, num_links=6)


# ----- Device ---------------------------------------------------------------------------------------------------------

def test_rest_get_device_ids(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    reply = do_rest_get_request('/tfs-api/device_ids')
    validate_device_ids(reply)

def test_rest_get_devices(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    reply = do_rest_get_request('/tfs-api/devices')
    validate_devices(reply)

def test_rest_get_device(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    device_uuid = urllib.parse.quote('R1', safe='')
    reply = do_rest_get_request('/tfs-api/device/{:s}'.format(device_uuid))
    validate_device(reply)


# ----- Link -----------------------------------------------------------------------------------------------------------

def test_rest_get_link_ids(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    reply = do_rest_get_request('/tfs-api/link_ids')
    validate_link_ids(reply)

def test_rest_get_links(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    reply = do_rest_get_request('/tfs-api/links')
    validate_links(reply)

def test_rest_get_link(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    link_uuid = urllib.parse.quote('R1/502==R2/501', safe='')
    reply = do_rest_get_request('/tfs-api/link/{:s}'.format(link_uuid))
    validate_link(reply)


# ----- Service --------------------------------------------------------------------------------------------------------

def test_rest_get_service_ids(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request('/tfs-api/context/{:s}/service_ids'.format(context_uuid))
    validate_service_ids(reply)

def test_rest_get_services(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request('/tfs-api/context/{:s}/services'.format(context_uuid))
    validate_services(reply)

def test_rest_get_service(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    service_uuid = urllib.parse.quote('SVC:R1/200==R2/200', safe='')
    reply = do_rest_get_request('/tfs-api/context/{:s}/service/{:s}'.format(context_uuid, service_uuid))
    validate_service(reply)


# ----- Slice ----------------------------------------------------------------------------------------------------------

def test_rest_get_slice_ids(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request('/tfs-api/context/{:s}/slice_ids'.format(context_uuid))
    validate_slice_ids(reply)

def test_rest_get_slices(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    reply = do_rest_get_request('/tfs-api/context/{:s}/slices'.format(context_uuid))
    validate_slices(reply)

def test_rest_get_slice(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    slice_uuid = urllib.parse.quote('SLC:R1-R2-R3', safe='')
    reply = do_rest_get_request('/tfs-api/context/{:s}/slice/{:s}'.format(context_uuid, slice_uuid))
    validate_slice(reply)


# ----- Connection -----------------------------------------------------------------------------------------------------

def test_rest_get_connection_ids(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    service_uuid = urllib.parse.quote('SVC:R1/200==R2/200', safe='')
    reply = do_rest_get_request('/tfs-api/context/{:s}/service/{:s}/connection_ids'.format(context_uuid, service_uuid))
    validate_connection_ids(reply)

def test_rest_get_connections(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    context_uuid = urllib.parse.quote(DEFAULT_CONTEXT_NAME)
    service_uuid = urllib.parse.quote('SVC:R1/200==R2/200', safe='')
    reply = do_rest_get_request('/tfs-api/context/{:s}/service/{:s}/connections'.format(context_uuid, service_uuid))
    validate_connections(reply)

def test_rest_get_connection(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    connection_uuid = urllib.parse.quote('CON:R1/200==R2/200:1', safe='')
    reply = do_rest_get_request('/tfs-api/connection/{:s}'.format(connection_uuid))
    validate_connection(reply)

# ----- Policy ---------------------------------------------------------------------------------------------------------

#def test_rest_get_policyrule_ids(
#    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
#) -> None:
#    reply = do_rest_get_request('/tfs-api/policyrule_ids')
#    validate_policyrule_ids(reply)

#def test_rest_get_policyrules(
#    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
#) -> None:
#    reply = do_rest_get_request('/tfs-api/policyrules')
#    validate_policyrules(reply)

#def test_rest_get_policyrule(
#    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
#) -> None:
#    policyrule_uuid_quoted = urllib.parse.quote(policyrule_uuid, safe='')
#    reply = do_rest_get_request('/tfs-api/policyrule/{:s}'.format(policyrule_uuid_quoted))
#    validate_policyrule(reply)


# ----- Cleanup Environment --------------------------------------------------------------------------------------------

def test_cleanup_environment(context_client : ContextClient) -> None: # pylint: disable=redefined-outer-name
    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.topology_ids) == 1
    assert len(response.service_ids ) == 3
    assert len(response.slice_ids   ) == 1

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    descriptor_loader.validate()
    descriptor_loader.unload()
    validate_empty_scenario(context_client)
