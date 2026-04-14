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

import copy, logging, socketio
from typing import Dict
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import Service, ServiceId
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Service import json_service_id
from service.client.ServiceClient import ServiceClient
from .._Dispatcher import _Dispatcher
from .ClientNamespace import ClientNamespace
from .Recommendation import Recommendation, RecommendationAction
from .Tools import compose_optical_service

LOGGER = logging.getLogger(__name__)

class RecommendationDispatcher(_Dispatcher):

    def register(self, sio_client : socketio.Client) -> None:
        sio_client.register_namespace(ClientNamespace(self.dispatcher_queue))

    def process_request(self, request : Recommendation) -> Dict:
        LOGGER.info('[process_request] request={:s}'.format(str(request)))

        if request.action == RecommendationAction.VLINK_CREATE:
            vlink_optical_service = compose_optical_service(request.data)
            vlink_optical_service_add = copy.deepcopy(vlink_optical_service)
            vlink_optical_service_add.pop('service_endpoint_ids', None)
            vlink_optical_service_add.pop('service_constraints',  None)
            vlink_optical_service_add.pop('service_config',       None)

            service_client = ServiceClient()
            service_id = service_client.CreateService(Service(**vlink_optical_service_add))
            service_uuid = service_id.service_uuid.uuid
            vlink_optical_service['service_id']['service_uuid']['uuid'] = service_uuid
            service_id = service_client.UpdateService(Service(**vlink_optical_service))

            result = {'event': 'vlink_created', 'vlink_uuid': service_uuid}
        elif request.action == RecommendationAction.VLINK_REMOVE:
            vlink_service_uuid = request.data['link_uuid']['uuid']
            context_id = json_context_id(DEFAULT_CONTEXT_NAME)
            vlink_optical_service_id = json_service_id(vlink_service_uuid, context_id=context_id)

            service_client = ServiceClient()
            service_id = service_client.DeleteService(ServiceId(**vlink_optical_service_id))

            if vlink_service_uuid == 'IP1/PORT-xe1==IP2/PORT-xe1':
                service_id = service_client.DeleteService(ServiceId(**vlink_optical_service_id))

            result = {'event': 'vlink_removed'}
        else:
            MSG = 'RecommendationAction not supported in Recommendation({:s})'
            raise NotImplementedError(MSG.format(str(request)))

        return result
