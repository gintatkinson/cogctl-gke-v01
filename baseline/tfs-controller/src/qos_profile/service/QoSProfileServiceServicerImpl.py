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

import grpc, logging, sqlalchemy
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import Constraint, Empty, QoSProfileId
from common.proto.qos_profile_pb2 import ConstraintList, QoSProfile, QoDConstraintsRequest, QoSProfileList
from common.proto.qos_profile_pb2_grpc import QoSProfileServiceServicer
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Constraint import json_constraint_qos_profile, json_constraint_schedule
from .database.QoSProfile import set_qos_profile, delete_qos_profile, get_qos_profile, get_qos_profiles


LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('QoSProfile', 'RPC')

class QoSProfileServiceServicerImpl(QoSProfileServiceServicer):
    def __init__(self, db_engine: sqlalchemy.engine.Engine) -> None:
        LOGGER.debug('Servicer Created')
        self.db_engine = db_engine

    def _get_metrics(self) -> MetricsPool: return METRICS_POOL

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def CreateQoSProfile(self, request: QoSProfile, context: grpc.ServicerContext) -> QoSProfile:
        qos_profile = get_qos_profile(self.db_engine, request.qos_profile_id.qos_profile_id.uuid)
        if qos_profile is not None:
            context.set_details(f'QoSProfile {request.qos_profile_id.qos_profile_id.uuid} already exists')
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return QoSProfile()
        return set_qos_profile(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def UpdateQoSProfile(self, request: QoSProfile, context: grpc.ServicerContext) -> QoSProfile:
        qos_profile = get_qos_profile(self.db_engine, request.qos_profile_id.qos_profile_id.uuid)
        if qos_profile is None:
            context.set_details(f'QoSProfile {request.qos_profile_id.qos_profile_id.uuid} not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return QoSProfile()
        return set_qos_profile(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteQoSProfile(self, request: QoSProfileId, context: grpc.ServicerContext) -> Empty:
        qos_profile = get_qos_profile(self.db_engine, request.qos_profile_id.uuid)
        if qos_profile is None:
            context.set_details(f'QoSProfile {request.qos_profile_id.uuid} not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return QoSProfile()
        return delete_qos_profile(self.db_engine, request.qos_profile_id.uuid)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetQoSProfile(self, request: QoSProfileId, context: grpc.ServicerContext) -> QoSProfile:
        qos_profile = get_qos_profile(self.db_engine, request.qos_profile_id.uuid)
        if qos_profile is None:
            context.set_details(f'QoSProfile {request.qos_profile_id.uuid} not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return QoSProfile()
        return qos_profile

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetQoSProfiles(self, request: Empty, context: grpc.ServicerContext) -> QoSProfileList:
        return QoSProfileList(qos_profiles=get_qos_profiles(self.db_engine, request))

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetConstraintsFromQoSProfile(
        self, request: QoDConstraintsRequest, context: grpc.ServicerContext
    ) -> ConstraintList:
        LOGGER.debug('[GetConstraintsFromQoSProfile] request={:s}'.format(grpc_message_to_json_string(request)))
        qos_profile = get_qos_profile(self.db_engine, request.qos_profile_id.qos_profile_id.uuid)
        if qos_profile is None:
            context.set_details(f'QoSProfile {request.qos_profile_id.qos_profile_id.uuid} not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return ConstraintList()

        reply = ConstraintList(constraints=[
            Constraint(**json_constraint_qos_profile(qos_profile.qos_profile_id, qos_profile.name)),
            Constraint(**json_constraint_schedule(request.start_timestamp, request.duration)),
        ])
        LOGGER.debug('[GetConstraintsFromQoSProfile] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply
