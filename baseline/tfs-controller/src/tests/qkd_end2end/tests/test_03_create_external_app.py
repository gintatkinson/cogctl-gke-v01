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


import json, logging, os
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId
from common.proto.qkd_app_pb2 import QKDAppStatusEnum, QKDAppTypesEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from qkd_app.client.QKDAppClient import QKDAppClient
from .Fixtures import context_client, qkd_app_client    # pylint: disable=unused-import
from .Tools import do_rest_post_request


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))


def compose_path(file_name : str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', file_name)


# pylint: disable=redefined-outer-name
def test_check_qkd_apps_before(
    context_client : ContextClient,
    qkd_app_client : QKDAppClient,
):
    # Check there are no services
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 3

    response = qkd_app_client.ListApps(ADMIN_CONTEXT_ID)
    LOGGER.warning('QKDApps[{:d}] = {:s}'.format(
        len(response.apps), grpc_message_to_json_string(response)
    ))
    assert len(response.apps) == 2
    for app in response.apps:
        assert app.app_status == QKDAppStatusEnum.QKDAPPSTATUS_ON
        assert app.app_type == QKDAppTypesEnum.QKDAPPTYPES_INTERNAL


# pylint: disable=redefined-outer-name
def test_create_external_app_qkd1_to_qkd3(
    qkd_app_client : QKDAppClient,
):
    request_file = compose_path('tfs-05-app-1-qkd1-qkd3.json')

    # Issue external QKD App creation request (QKD1-QKD3)
    with open(request_file, 'r', encoding='UTF-8') as f:
        req_data = json.load(f)

    URL = '/qkd_app/create_qkd_app'
    do_rest_post_request(URL, body=req_data, logger=LOGGER, expected_status_codes={200})

    # Verify QKD app was created
    response = qkd_app_client.ListApps(ADMIN_CONTEXT_ID)
    LOGGER.warning('QKDApps[{:d}] = {:s}'.format(
        len(response.apps), grpc_message_to_json_string(response)
    ))
    assert len(response.apps) == 3

    num_internal = 0
    num_external = 0
    for app in response.apps:
        if app.app_type == QKDAppTypesEnum.QKDAPPTYPES_INTERNAL:
            assert app.app_status == QKDAppStatusEnum.QKDAPPSTATUS_ON
            num_internal += 1
        elif app.app_type == QKDAppTypesEnum.QKDAPPTYPES_CLIENT:
            assert app.app_status == QKDAppStatusEnum.QKDAPPSTATUS_ON
            num_external += 1
    assert num_internal == 2
    assert num_external == 1


# pylint: disable=redefined-outer-name
def test_create_external_app_qkd3_to_qkd1(
    qkd_app_client : QKDAppClient,
):
    request_file = compose_path('tfs-06-app-1-qkd3-qkd1.json')

    # Issue external QKD App creation request (QKD3-QKD1)
    with open(request_file, 'r', encoding='UTF-8') as f:
        req_data = json.load(f)

    URL = '/qkd_app/create_qkd_app'
    do_rest_post_request(URL, body=req_data, logger=LOGGER, expected_status_codes={200})

    # Verify no new QKD app was created
    response = qkd_app_client.ListApps(ADMIN_CONTEXT_ID)
    LOGGER.warning('QKDApps[{:d}] = {:s}'.format(
        len(response.apps), grpc_message_to_json_string(response)
    ))
    assert len(response.apps) == 3

    num_internal = 0
    num_external = 0
    for app in response.apps:
        if app.app_type == QKDAppTypesEnum.QKDAPPTYPES_INTERNAL:
            assert app.app_status == QKDAppStatusEnum.QKDAPPSTATUS_ON
            num_internal += 1
        elif app.app_type == QKDAppTypesEnum.QKDAPPTYPES_CLIENT:
            assert app.app_status == QKDAppStatusEnum.QKDAPPSTATUS_ON
            num_external += 1
    assert num_internal == 2
    assert num_external == 1
