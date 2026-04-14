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

import grpc
from common.method_wrappers.Decorator import (MetricsPool,
                                              safe_and_metered_rpc_method)
from common.proto.optical_attack_mitigator_pb2 import (AttackDescription,
                                                       AttackResponse)
from common.proto.optical_attack_mitigator_pb2_grpc import \
    AttackMitigatorServicer

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool("OpticalAttackMitigator", "RPC")


class OpticalAttackMitigatorServiceServicerImpl(AttackMitigatorServicer):
    def __init__(self):
        LOGGER.debug("Creating Servicer...")
        LOGGER.debug("Servicer Created")

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def NotifyAttack(
        self, request: AttackDescription, context: grpc.ServicerContext
    ) -> AttackResponse:
        LOGGER.debug(f"NotifyAttack: {request}")
        response: AttackResponse = AttackResponse()
        response.response_strategy_description = (
            "The AttackMitigator has received the attack description."
        )
        return response
