# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Tuple
from common.proto.qkd_app_pb2 import AppId
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from ._Builder import get_uuid_from_string, get_uuid_random
from .Context import context_get_uuid

def app_get_uuid(
    app_id : AppId, app_name : str = '', allow_random : bool = False
) -> Tuple[str, str]:
    """
    Retrieves or generates the UUID for an app.
    
    :param application_id: AppId object that contains the app UUID
    :param application_name: string that contains optional app name
    :param allow_random: If True, generates a random UUID if app_uuid is not set
    :return: Context UUID as a string , App UUID as a string
    """
    context_uuid = context_get_uuid(app_id.context_id, allow_random=False, allow_default=True)
    raw_app_uuid = app_id.app_uuid.uuid

    if len(raw_app_uuid) > 0:
        return context_uuid, get_uuid_from_string(raw_app_uuid, prefix_for_name=context_uuid)

    if len(app_name) > 0:
        return context_uuid, get_uuid_from_string(app_name, prefix_for_name=context_uuid)

    if allow_random:
        return context_uuid, get_uuid_random()

    raise InvalidArgumentsException([
        ('app_id.app_uuid.uuid', raw_app_uuid),
        ('name', app_name),
    ], extra_details=['At least one is required to produce a App UUID'])
