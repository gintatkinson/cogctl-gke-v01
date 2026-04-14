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

import enum, functools
from common.proto.policy_pb2 import PolicyRuleStateEnum
from ._GrpcToEnum import grpc_to_enum

# IMPORTANT: Entries of enum class ORM_PolicyRuleStateEnum should be named as in
#            the proto files removing the prefixes. For example, proto item
#            PolicyRuleStateEnum.POLICY_INSERTED should be declared as INSERTED.
#            In this case, since the entries in the proto enum have a different prefix
#            than that specified in class ORM_PolicyRuleStateEnum, we force the prefix
#            using argument grpc_enum_prefix. If item name does not match, automatic
#            mapping of proto enums to database enums will fail.
class ORM_PolicyRuleStateEnum(enum.Enum):
    UNDEFINED   = PolicyRuleStateEnum.POLICY_UNDEFINED   # Undefined rule state
    FAILED      = PolicyRuleStateEnum.POLICY_FAILED      # Rule failed
    INSERTED    = PolicyRuleStateEnum.POLICY_INSERTED    # Rule is just inserted
    VALIDATED   = PolicyRuleStateEnum.POLICY_VALIDATED   # Rule content is correct
    PROVISIONED = PolicyRuleStateEnum.POLICY_PROVISIONED # Rule subscribed to Monitoring
    ACTIVE      = PolicyRuleStateEnum.POLICY_ACTIVE      # Rule is currently active (alarm is just thrown by Monitoring)
    ENFORCED    = PolicyRuleStateEnum.POLICY_ENFORCED    # Rule action is successfully enforced
    INEFFECTIVE = PolicyRuleStateEnum.POLICY_INEFFECTIVE # The applied rule action did not work as expected
    EFFECTIVE   = PolicyRuleStateEnum.POLICY_EFFECTIVE   # The applied rule action did work as expected
    UPDATED     = PolicyRuleStateEnum.POLICY_UPDATED     # Operator requires a policy to change
    REMOVED     = PolicyRuleStateEnum.POLICY_REMOVED     # Operator requires to remove a policy

grpc_to_enum__policyrule_state = functools.partial(
    grpc_to_enum, PolicyRuleStateEnum, ORM_PolicyRuleStateEnum, grpc_enum_prefix='POLICY_')
