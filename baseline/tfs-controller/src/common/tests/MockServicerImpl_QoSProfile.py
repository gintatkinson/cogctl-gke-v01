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

import grpc, logging
from typing import Iterator
from common.proto.context_pb2 import Constraint, Empty, QoSProfileId
from common.proto.qos_profile_pb2 import ConstraintList, QoDConstraintsRequest, QoSProfile, QoSProfileList
from common.proto.qos_profile_pb2_grpc import QoSProfileServiceServicer
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Constraint import json_constraint_qos_profile, json_constraint_schedule
from .InMemoryObjectDatabase import InMemoryObjectDatabase

LOGGER = logging.getLogger(__name__)

class MockServicerImpl_QoSProfile(QoSProfileServiceServicer):
    def __init__(self):
        LOGGER.debug('[__init__] Creating Servicer...')
        self.obj_db = InMemoryObjectDatabase()
        LOGGER.debug('[__init__] Servicer Created')

    def GetQoSProfiles(self, request : Empty, context : grpc.ServicerContext) -> QoSProfileList:
        LOGGER.debug('[GetQoSProfiles] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = QoSProfileList(qos_profiles=self.obj_db.get_entries('qos_profile'))
        LOGGER.debug('[GetQoSProfiles] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetQoSProfile(self, request : QoSProfileId, context : grpc.ServicerContext) -> QoSProfile:
        LOGGER.debug('[GetQoSProfile] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.get_entry('qos_profile', request.qos_profile_id.uuid, context)
        LOGGER.debug('[GetQoSProfile] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def CreateQoSProfile(self, request : QoSProfile, context : grpc.ServicerContext) -> QoSProfile:
        LOGGER.debug('[CreateQoSProfile] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.set_entry('qos_profile', request.qos_profile_id.qos_profile_id.uuid, request)
        LOGGER.debug('[CreateQoSProfile] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def UpdateQoSProfile(self, request : QoSProfile, context : grpc.ServicerContext) -> QoSProfile:
        LOGGER.debug('[UpdateQoSProfile] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.set_entry('qos_profile', request.qos_profile_id.qos_profile_id.uuid, request)
        LOGGER.debug('[UpdateQoSProfile] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def DeleteQoSProfile(self, request : QoSProfileId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[DeleteQoSProfile] request={:s}'.format(grpc_message_to_json_string(request)))
        self.obj_db.del_entry('qos_profile', request.qos_profile_id.uuid, context)
        reply = Empty()
        LOGGER.debug('[DeleteQoSProfile] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetConstraintsFromQoSProfile(
        self, request: QoDConstraintsRequest, context: grpc.ServicerContext
    ) -> ConstraintList:
        LOGGER.debug('[GetConstraintsFromQoSProfile] request={:s}'.format(grpc_message_to_json_string(request)))
        qos_profile = self.obj_db.get_entry(
            'qos_profile', request.qos_profile_id.qos_profile_id.uuid, context
        )
        reply = ConstraintList(constraints=[
            Constraint(**json_constraint_qos_profile(qos_profile.qos_profile_id, qos_profile.name)),
            Constraint(**json_constraint_schedule(request.start_timestamp, request.duration / 86400)),
        ])
        LOGGER.debug('[GetConstraintsFromQoSProfile] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply
