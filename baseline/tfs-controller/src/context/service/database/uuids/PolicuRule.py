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

from common.proto.policy_pb2 import PolicyRuleId
from common.method_wrappers.ServiceExceptions import InvalidArgumentException
from ._Builder import get_uuid_from_string, get_uuid_random

def policyrule_get_uuid(
    policyrule_id : PolicyRuleId, allow_random : bool = False
) -> str:
    policyrule_uuid = policyrule_id.uuid.uuid

    if len(policyrule_uuid) > 0:
        return get_uuid_from_string(policyrule_uuid)
    if allow_random: return get_uuid_random()

    raise InvalidArgumentException(
        'policyrule_id.uuid.uuid', policyrule_uuid, extra_details=['Required to produce a PolicyRule UUID'])
