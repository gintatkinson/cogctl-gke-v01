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

import json
import warnings
from google import protobuf
from google.protobuf.json_format import MessageToDict

def grpc_message_to_json(
        message, including_default_value_fields=True, preserving_proto_field_name=True, use_integers_for_enums=False
    ):
    if not hasattr(message, 'DESCRIPTOR'): return json.dumps(str(message), sort_keys=True) # not a gRPC message
    if including_default_value_fields is not True:
        warnings.warn(
            "The 'including_default_value_fields' argument is deprecated and will have no effect in future versions.",
            DeprecationWarning,
            stacklevel=2
        )
    if protobuf.__version__ < '4.0.0':
        return MessageToDict(
                message, including_default_value_fields=including_default_value_fields,
                preserving_proto_field_name=preserving_proto_field_name, use_integers_for_enums=use_integers_for_enums)
    else:
        return MessageToDict(
            message,
            preserving_proto_field_name=preserving_proto_field_name, use_integers_for_enums=use_integers_for_enums)

def grpc_message_list_to_json(message_list):
    if message_list is None: return None
    return [grpc_message_to_json(message) for message in message_list]

def grpc_message_to_json_string(message):
    if message is None: return str(None)
    return json.dumps(grpc_message_to_json(message), sort_keys=True)

def grpc_message_list_to_json_string(message_list):
    if message_list is None: return str(None)
    return json.dumps(grpc_message_list_to_json(message_list), sort_keys=True)
