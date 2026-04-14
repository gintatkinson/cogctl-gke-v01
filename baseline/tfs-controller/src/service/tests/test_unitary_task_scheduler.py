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
#from common.proto.context_pb2 import Connection, Service
from common.proto.pathcomp_pb2 import PathCompReply
from common.tools.grpc.Tools import grpc_message_to_json_string
from service.service.service_handler_api.ServiceHandlerFactory import ServiceHandlerFactory
from service.service.task_scheduler.TaskScheduler import TasksScheduler
from .PrepareTestScenario import context_client # pylint: disable=unused-import

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def test_task_scheduler():
    # test: add services and connections that depend on each other
    #       then, check if they are properly resolved.
    # - service MAIN, depends on connection PKT-1, TAPI, and PKT-2
    # - connection PKT-1, depends on nothing
    # - connection TAPI, depends on service TAPI-1 and TAPI-2
    # - connection PKT-2, depends on nothing
    # - service TAPI-1, depends on connection TAPI-1
    # - service TAPI-2, depends on connection TAPI-2

    pathcomp_reply = PathCompReply()

    service_main = pathcomp_reply.services.add()
    service_main.service_id.context_id.context_uuid.uuid = 'admin'
    service_main.service_id.service_uuid.uuid = 'MAIN'

    service_tapi1 = pathcomp_reply.services.add()
    service_tapi1.service_id.context_id.context_uuid.uuid = 'admin'
    service_tapi1.service_id.service_uuid.uuid = 'TAPI-1'

    service_tapi2 = pathcomp_reply.services.add()
    service_tapi2.service_id.context_id.context_uuid.uuid = 'admin'
    service_tapi2.service_id.service_uuid.uuid = 'TAPI-2'

    connection_pkt1 = pathcomp_reply.connections.add()
    connection_pkt1.connection_id.connection_uuid.uuid = 'PKT-1'
    connection_pkt1.service_id.CopyFrom(service_main.service_id)

    connection_tapi = pathcomp_reply.connections.add()
    connection_tapi.connection_id.connection_uuid.uuid = 'TAPI'
    connection_tapi.service_id.CopyFrom(service_main.service_id)

    connection_pkt2 = pathcomp_reply.connections.add()
    connection_pkt2.connection_id.connection_uuid.uuid = 'PKT-2'
    connection_pkt2.service_id.CopyFrom(service_main.service_id)

    connection_tapi1 = pathcomp_reply.connections.add()
    connection_tapi1.connection_id.connection_uuid.uuid = 'TAPI-1'
    connection_tapi1.service_id.CopyFrom(service_tapi1.service_id)
    connection_tapi.sub_service_ids.append(service_tapi1.service_id)

    connection_tapi2 = pathcomp_reply.connections.add()
    connection_tapi2.connection_id.connection_uuid.uuid = 'TAPI-2'
    connection_tapi2.service_id.CopyFrom(service_tapi2.service_id)
    connection_tapi.sub_service_ids.append(service_tapi2.service_id)

    LOGGER.info('pathcomp_reply={:s}'.format(grpc_message_to_json_string(pathcomp_reply)))

    service_handler_factory = ServiceHandlerFactory([])
    task_scheduler = TasksScheduler(service_handler_factory)
    task_scheduler.compose_from_pathcompreply(pathcomp_reply)
    tasks_and_results = list(task_scheduler.execute_all(dry_run=True))

    LOGGER.info('tasks_and_results={:s}'.format(str(tasks_and_results)))

    CORRECT_ORDERED_TASK_KEYS = [
        'service(admin/MAIN):set_status(SERVICESTATUS_PLANNED)',
        'service(admin/TAPI-1):set_status(SERVICESTATUS_PLANNED)',
        'service(admin/TAPI-2):set_status(SERVICESTATUS_PLANNED)',
        'connection(PKT-1):configure',
        'connection(PKT-2):configure',
        'connection(TAPI-1):configure',
        'connection(TAPI-2):configure',
        'service(admin/TAPI-1):set_status(SERVICESTATUS_ACTIVE)',
        'service(admin/TAPI-2):set_status(SERVICESTATUS_ACTIVE)',
        'connection(TAPI):configure',
        'service(admin/MAIN):set_status(SERVICESTATUS_ACTIVE)'
    ]

    for (task_key,_),correct_key in zip(tasks_and_results, CORRECT_ORDERED_TASK_KEYS):
        assert task_key == correct_key
