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

import logging
from typing import Set
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId
from common.proto.qkd_app_pb2 import AppId, QKDAppStatusEnum, QKDAppTypesEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from qkd_app.client.QKDAppClient import QKDAppClient
from .Fixtures import context_client, qkd_app_client    # pylint: disable=unused-import


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))


# pylint: disable=redefined-outer-name
def test_check_qkd_apps_before(
    context_client : ContextClient,
    qkd_app_client : QKDAppClient,
):
    # Check there are 3 services
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 3

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
def test_delete_external_app(
    context_client : ContextClient,
    qkd_app_client : QKDAppClient,
):
    response = qkd_app_client.ListApps(ADMIN_CONTEXT_ID)
    LOGGER.warning('QKDApps[{:d}] = {:s}'.format(
        len(response.apps), grpc_message_to_json_string(response)
    ))
    assert len(response.apps) == 3

    external_app_uuids : Set[str] = set()
    for app in response.apps:
        if app.app_type != QKDAppTypesEnum.QKDAPPTYPES_CLIENT: continue
        external_app_uuids.add(app.app_id.app_uuid.uuid)

    # Identify QKD ext app to delete
    assert len(external_app_uuids) == 1
    external_app_uuid = set(external_app_uuids).pop()

    app_id = AppId()
    app_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
    app_id.app_uuid.uuid = external_app_uuid

    response = qkd_app_client.DeleteApp(app_id)


# pylint: disable=redefined-outer-name
def test_check_qkd_apps_after(
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

    num_internal = 0
    num_external = 0
    for app in response.apps:
        if app.app_type == QKDAppTypesEnum.QKDAPPTYPES_INTERNAL:
            assert app.app_status == QKDAppStatusEnum.QKDAPPSTATUS_ON
            num_internal += 1
        elif app.app_type == QKDAppTypesEnum.QKDAPPTYPES_CLIENT:
            num_external += 1
    assert num_internal == 2
    assert num_external == 0
