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
from common.proto.context_pb2 import ContextId, ServiceId
from common.proto.qkd_app_pb2 import AppId, QKDAppStatusEnum, QKDAppTypesEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from qkd_app.client.QKDAppClient import QKDAppClient
from service.client.ServiceClient import ServiceClient
from .Fixtures import (
    # pylint: disable=unused-import
    context_client, qkd_app_client, service_client
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))


# pylint: disable=redefined-outer-name
def test_check_qkd_apps_before(
    context_client : ContextClient,
    qkd_app_client : QKDAppClient,
):
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
            assert app.app_status == QKDAppStatusEnum.QKDAPPSTATUS_ON
            num_external += 1
    assert num_internal == 2
    assert num_external == 0


# pylint: disable=redefined-outer-name
def test_delete_internal_apps(
    context_client : ContextClient,
    qkd_app_client : QKDAppClient,
):
    response = qkd_app_client.ListApps(ADMIN_CONTEXT_ID)
    LOGGER.warning('QKDApps[{:d}] = {:s}'.format(
        len(response.apps), grpc_message_to_json_string(response)
    ))
    assert len(response.apps) == 2

    # Identify internal QKD apps to delete
    internal_app_uuids : Set[str] = set()
    for app in response.apps:
        if app.app_type != QKDAppTypesEnum.QKDAPPTYPES_INTERNAL: continue
        internal_app_uuids.add(app.app_id.app_uuid.uuid)

    assert len(internal_app_uuids) == 2
    for app_uuid in internal_app_uuids:
        app_id = AppId()
        app_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
        app_id.app_uuid.uuid = app_uuid
        response = qkd_app_client.DeleteApp(app_id)

    response = qkd_app_client.ListApps(ADMIN_CONTEXT_ID)
    LOGGER.warning('QKDApps[{:d}] = {:s}'.format(
        len(response.apps), grpc_message_to_json_string(response)
    ))
    assert len(response.apps) == 0


# pylint: disable=redefined-outer-name
def test_delete_services_associated_qkd_apps(
    context_client : ContextClient,
    service_client : ServiceClient,
):
    # Check there are 3 services
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 3

    # Identify services for QKD links to delete
    virtual_link_service_uuids : Set[str] = set()
    direct_link_service_uuids  : Set[str] = set()
    for service in response.services:
        if 'virtual' in str(service.name).lower():
            virtual_link_service_uuids.add(service.service_id.service_uuid.uuid)
        if 'direct' in str(service.name).lower():
            direct_link_service_uuids.add(service.service_id.service_uuid.uuid)

    assert len(virtual_link_service_uuids) == 1
    assert len(direct_link_service_uuids ) == 2

    # Delete the services for virtual links
    for svc_uuid in virtual_link_service_uuids:
        svc_id = ServiceId()
        svc_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
        svc_id.service_uuid.uuid = svc_uuid
        response = service_client.DeleteService(svc_id)

    # Delete the services for direct links
    for svc_uuid in direct_link_service_uuids:
        svc_id = ServiceId()
        svc_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
        svc_id.service_uuid.uuid = svc_uuid
        response = service_client.DeleteService(svc_id)

    # Check there are no services
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 0
