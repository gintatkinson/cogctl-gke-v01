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

import grpc
from common.database.api.Database import Database
from common.database.api.context.slice.Slice import Slice
from common.exceptions.ServiceException import ServiceException

def check_slice_exists(database : Database, context_id : str, slice_id : str) -> Slice:
    db_context = database.context(context_id).create()
    if db_context.slices.contains(slice_id): return db_context.slice(slice_id)
    msg = 'Context({})/Slice({}) does not exist in the database.'
    msg = msg.format(context_id, slice_id)
    raise ServiceException(grpc.StatusCode.NOT_FOUND, msg)

def check_slice_not_exists(database : Database, context_id : str, slice_id : str):
    db_context = database.context(context_id).create()
    if not db_context.slices.contains(slice_id): return
    msg = 'Context({})/Slice({}) already exists in the database.'
    msg = msg.format(context_id, slice_id)
    raise ServiceException(grpc.StatusCode.ALREADY_EXISTS, msg)
