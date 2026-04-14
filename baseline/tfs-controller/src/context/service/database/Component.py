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

import datetime, json, logging
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Set
from common.proto.context_pb2 import Component
from common.proto.context_pb2 import ConfigRule
from common.tools.grpc.Tools import grpc_message_to_json_string
from .models.ComponentModel import ComponentModel
from .uuids._Builder import get_uuid_from_string
from .uuids.EndPoint import endpoint_get_uuid
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, selectinload, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from .models.ComponentModel import ComponentModel

LOGGER = logging.getLogger(__name__)

def compose_components_data(
    components : List[Component], now : datetime.datetime,
    device_uuid : Optional[str] = None, service_uuid : Optional[str] = None, slice_uuid : Optional[str] = None
) -> List[Dict]:
    dict_components : List[Dict] = list()
    for position,component in enumerate(components):
        str_kind = component.WhichOneof('config_rule')
        message  = (grpc_message_to_json_string(getattr(component, str_kind, {})))
        data     = json.loads(message)
        resource_key   = data["resource_key"]
        resource_value = data["resource_value"]
        if '/inventory' in resource_key:
            resource_value_data = json.loads(resource_value)
            name                = resource_value_data.pop('name', None)
            type_               = resource_value_data.pop('class', None)
            parent              = resource_value_data.pop('parent-component-references', None)
            attributes          = resource_value_data.pop('attributes', {})
            if len(resource_value_data) > 0:
                LOGGER.warning('Discarding Component Leftovers: {:s}'.format(str(resource_value_data)))

            attributes = {
                attr_name:json.dumps(attr_value)
                for attr_name,attr_value in attributes.items()
            }
            component_uuid = get_uuid_from_string(component.custom.resource_key, prefix_for_name=device_uuid)            
            dict_component = {
                'component_uuid': component_uuid,
                'device_uuid'   : device_uuid,
                'name'          : name,
                'type'          : type_,
                'attributes'    : json.dumps(attributes),
                'parent'        : parent,
                'created_at'    : now,
                'updated_at'    : now,
            }
            dict_components.append(dict_component)
    return dict_components
