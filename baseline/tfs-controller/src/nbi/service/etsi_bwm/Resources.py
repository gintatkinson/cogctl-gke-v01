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

import copy, deepmerge, json, logging
from typing import Dict
from flask_restful import Resource, request
from werkzeug.exceptions import UnsupportedMediaType
from common.Constants import DEFAULT_CONTEXT_NAME
from context.client.ContextClient import ContextClient
from service.client.ServiceClient import ServiceClient
from .Tools import (
    format_grpc_to_json, grpc_context_id, grpc_service_id, bwInfo_2_service, service_2_bwInfo
)

LOGGER = logging.getLogger(__name__)


class _Resource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.client = ContextClient()
        self.service_client = ServiceClient()


class BwInfo(_Resource):
    def get(self):
        service_list = self.client.ListServices(grpc_context_id(DEFAULT_CONTEXT_NAME))
        bw_allocations = [service_2_bwInfo(service) for service in service_list.services]
        return bw_allocations

    def post(self):
        if not request.is_json:
            raise UnsupportedMediaType('JSON payload is required')
        request_data: Dict = request.get_json()
        service = bwInfo_2_service(self.client, request_data)
        stripped_service = copy.deepcopy(service)
        stripped_service.ClearField('service_endpoint_ids')
        stripped_service.ClearField('service_constraints')
        stripped_service.ClearField('service_config')

        try:
            response = format_grpc_to_json(self.service_client.CreateService(stripped_service))
            response = format_grpc_to_json(self.service_client.UpdateService(service))
        except Exception as e: # pylint: disable=broad-except
            return e

        return response


class BwInfoId(_Resource):

    def get(self, allocationId: str):
        service = self.client.GetService(grpc_service_id(DEFAULT_CONTEXT_NAME, allocationId))
        return service_2_bwInfo(service)

    def put(self, allocationId: str):
        json_data = json.loads(request.get_json())
        service = bwInfo_2_service(self.client, json_data)
        self.service_client.UpdateService(service)
        service = self.client.GetService(grpc_service_id(DEFAULT_CONTEXT_NAME, json_data['appInsId']))
        response_bwm = service_2_bwInfo(service)

        return response_bwm

    def patch(self, allocationId: str):
        json_data = request.get_json()
        if not 'appInsId' in json_data:
            json_data['appInsId'] = allocationId
        
        service = self.client.GetService(grpc_service_id(DEFAULT_CONTEXT_NAME, json_data['appInsId']))
        current_bwm = service_2_bwInfo(service)
        new_bmw = deepmerge.always_merger.merge(current_bwm, json_data)
        
        service = bwInfo_2_service(self.client, new_bmw)
        self.service_client.UpdateService(service)

        service = self.client.GetService(grpc_service_id(DEFAULT_CONTEXT_NAME, json_data['appInsId']))
        response_bwm = service_2_bwInfo(service)

        return response_bwm

    def delete(self, allocationId: str):
        self.service_client.DeleteService(grpc_service_id(DEFAULT_CONTEXT_NAME, allocationId))
