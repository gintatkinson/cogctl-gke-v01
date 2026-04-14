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


import copy, grpc, grpc._channel, logging
from typing import Dict
from uuid import uuid4
from flask_restful import Resource, request
from common.proto.context_pb2 import Empty, QoSProfileId, Uuid
from common.Constants import DEFAULT_CONTEXT_NAME
from common.tools.context_queries.Service import get_service_by_uuid
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from qos_profile.client.QoSProfileClient import QoSProfileClient
from service.client.ServiceClient import ServiceClient
from .Tools import (
    create_qos_profile_from_json, grpc_context_id, grpc_service_id,
    grpc_message_to_qos_table_data, QOD_2_service, service_2_qod
)
from nbi.service._tools.HttpStatusCodes import (
    HTTP_ACCEPTED, HTTP_BADREQUEST, HTTP_CREATED, HTTP_NOCONTENT, HTTP_NOTFOUND,
    HTTP_OK, HTTP_SERVERERROR, HTTP_UNSUPMEDIATYPE
)

LOGGER = logging.getLogger(__name__)

class _Resource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.context_client     = ContextClient()
        self.qos_profile_client = QoSProfileClient()
        self.service_client     = ServiceClient()

def compose_error(msg_error, http_status_code):
    LOGGER.exception(msg_error)
    return {"error": msg_error}, http_status_code

def compose_internal_server_error(msg_error):
    return compose_error(msg_error, HTTP_SERVERERROR)

def compose_bad_request_error(msg_error):
    return compose_error(msg_error, HTTP_BADREQUEST)

def compose_not_found_error(msg_error):
    return compose_error(msg_error, HTTP_NOTFOUND)

def compose_unsupported_media_type_error():
    msg_error = "JSON payload is required to proceed"
    return compose_error(msg_error, HTTP_UNSUPMEDIATYPE)



##### PROFILES #########################################################################################################

class ProfileList(_Resource):
    def post(self):
        if not request.is_json: return compose_unsupported_media_type_error()

        request_data : Dict = request.get_json()
        request_data_with_id = copy.deepcopy(request_data)
        request_data_with_id["qos_profile_id"] = str(uuid4())

        try:
            qos_profile = create_qos_profile_from_json(request_data_with_id)
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error parsing QoSProfile({:s})".format(str(request_data))
            )

        try:
            qos_profile_created = self.qos_profile_client.CreateQoSProfile(qos_profile) 
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error creating QoSProfile({:s}) QoSProfileWithUuid({:s})".format(
                    str(request_data), str(request_data_with_id)
                )
            )

        return grpc_message_to_qos_table_data(qos_profile_created), HTTP_CREATED

    def get(self):
        list_qos_profiles = self.qos_profile_client.GetQoSProfiles(Empty())
        list_qos_profiles = [
            grpc_message_to_qos_table_data(qos_profile)
            for qos_profile in list_qos_profiles
        ]
        return list_qos_profiles, HTTP_OK

class ProfileDetail(_Resource):
    def get(self, qos_profile_id : str):
        _qos_profile_id = QoSProfileId(qos_profile_id=Uuid(uuid=qos_profile_id))

        try:
            qos_profile = self.qos_profile_client.GetQoSProfile(_qos_profile_id)
            return grpc_message_to_qos_table_data(qos_profile), HTTP_OK
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return compose_not_found_error(
                    "QoSProfileId({:s}) not found".format(str(qos_profile_id))
                )
            else:
                return compose_internal_server_error(
                    "gRPC error fetching QoSProfileId({:s})".format(str(qos_profile_id))
                )
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error fetching QoSProfileId({:s})".format(str(qos_profile_id))
            )

    def put(self, qos_profile_id : str):
        if not request.is_json: return compose_unsupported_media_type_error()

        request_data : Dict = request.get_json()
        request_data_orig = copy.deepcopy(request_data)

        if "qos_profile_id" in request_data:
            if request_data["qos_profile_id"] != qos_profile_id:
                return compose_bad_request_error(
                    "qos_profile_id({:s}) in JSON payload mismatches qos_profile_id({:s}) in URL".format(
                        str(request_data["qos_profile_id"]), str(qos_profile_id)
                    )
                )
        else:
            request_data["qos_profile_id"] = qos_profile_id

        try:
            qos_profile = create_qos_profile_from_json(request_data)
            qos_profile_updated = self.qos_profile_client.UpdateQoSProfile(qos_profile)
            return grpc_message_to_qos_table_data(qos_profile_updated), HTTP_ACCEPTED
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return compose_not_found_error(
                    "QoSProfileId({:s}) not found".format(str(qos_profile_id))
                )
            else:
                return compose_internal_server_error(
                    "gRPC error updating QoSProfileId({:s}) with content QosProfile({:s})".format(
                        str(qos_profile_id), str(request_data_orig)
                    )
                )
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error updating QoSProfileId({:s}) with content QosProfile({:s})".format(
                    str(qos_profile_id), str(request_data_orig)
                )
            )

    def delete(self, qos_profile_id : str):
        _qos_profile_id = QoSProfileId(qos_profile_id=Uuid(uuid=qos_profile_id))

        try:
            self.qos_profile_client.DeleteQoSProfile(_qos_profile_id)
            return {}, HTTP_NOCONTENT
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return compose_not_found_error(
                    "QoSProfileId({:s}) not found".format(str(qos_profile_id))
                )
            else:
                return compose_internal_server_error(
                    "gRPC error deleting QoSProfileId({:s})".format(str(qos_profile_id))
                )
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error deleting QoSProfileId({:s})".format(str(qos_profile_id))
            )


##### SESSIONS #########################################################################################################

class QodInfo(_Resource):
    def post(self):
        if not request.is_json: return compose_unsupported_media_type_error()

        request_data : Dict = request.get_json()
        request_data_orig = copy.deepcopy(request_data)

        session_id = request_data.get("session_id")
        if session_id is not None:
            return compose_bad_request_error("session_id is not allowed in creation")

        qos_profile_id = request_data.get("qos_profile_id")
        if qos_profile_id is None:
            return compose_bad_request_error("qos_profile_id is required")

        try:
            service = QOD_2_service(self.context_client, self.qos_profile_client, request_data)
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error parsing QoDSession({:s})".format(str(request_data_orig))
            )

        stripped_service = copy.deepcopy(service)
        stripped_service.ClearField("service_endpoint_ids")
        stripped_service.ClearField("service_constraints")
        stripped_service.ClearField("service_config")
        try:
            self.service_client.CreateService(stripped_service)
            self.service_client.UpdateService(service)

            service_uuid = service.service_id.service_uuid.uuid
            updated_service = get_service_by_uuid(self.context_client, service_uuid, rw_copy=False)
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error creating Service({:s}) for QoDSession({:s})".format(
                    grpc_message_to_json_string(service), str(request_data_orig)
                )
            )

        return service_2_qod(updated_service), HTTP_CREATED

    def get(self):
        list_services = self.context_client.ListServices(grpc_context_id(DEFAULT_CONTEXT_NAME))
        list_services = [service_2_qod(service) for service in list_services.services]
        return list_services, HTTP_OK


class QodInfoID(_Resource):
    def get(self, session_id: str):
        try:
            service = get_service_by_uuid(self.context_client, session_id, rw_copy=True)
            return service_2_qod(service), HTTP_OK
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return compose_not_found_error(
                    "QoDSessionId({:s}) not found".format(str(session_id))
                )
            else:
                return compose_internal_server_error(
                    "gRPC error fetching QoDSessionId({:s})".format(str(session_id))
                )
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error fetching QoDSessionId({:s})".format(str(session_id))
            )

    def put(self, session_id : str):
        if not request.is_json: return compose_unsupported_media_type_error()

        request_data : Dict = request.get_json()
        request_data_orig = copy.deepcopy(request_data)

        if "session_id" in request_data:
            if request_data["session_id"] != session_id:
                return compose_bad_request_error(
                    "session_id({:s}) in JSON payload mismatches session_id({:s}) in URL".format(
                        str(request_data["session_id"]), str(session_id)
                    )
                )
        else:
            request_data["session_id"] = session_id

        qos_profile_id = request_data.get("qos_profile_id")
        if qos_profile_id is None:
            return compose_bad_request_error("qos_profile_id is required")

        duration = request_data.get("duration")
        if duration is None:
            return compose_bad_request_error("duration is required")

        try:
            service = get_service_by_uuid(self.context_client, session_id, rw_copy=True)
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return compose_not_found_error(
                    "QoDSessionId({:s}) not found".format(str(session_id))
                )
            else:
                return compose_internal_server_error(
                    "gRPC error fetching QoDSessionId({:s})".format(str(session_id))
                )
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error fetching QoDSessionId({:s})".format(str(session_id))
            )

        for constraint in service.service_constraints:
            if constraint.WhichOneof("constraint") == "schedule":
                constraint.schedule.duration_days = duration

        try:
            self.service_client.UpdateService(service)

            service_uuid = service.service_id.service_uuid.uuid
            updated_service = get_service_by_uuid(self.context_client, service_uuid, rw_copy=False)
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error updating Service({:s}) for QoDSession({:s})".format(
                    grpc_message_to_json_string(service), str(request_data_orig)
                )
            )

        return service_2_qod(updated_service), HTTP_ACCEPTED

    def delete(self, session_id: str):
        try:
            self.service_client.DeleteService(grpc_service_id(DEFAULT_CONTEXT_NAME, session_id))
            return {}, HTTP_NOCONTENT
        except grpc._channel._InactiveRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return compose_not_found_error(
                    "QoDSessionId({:s}) not found".format(str(session_id))
                )
            else:
                return compose_internal_server_error(
                    "gRPC error deleting QoDSessionId({:s})".format(str(session_id))
                )
        except: # pylint: disable=bare-except
            return compose_internal_server_error(
                "Error deleting QoDSessionId({:s})".format(str(session_id))
            )
