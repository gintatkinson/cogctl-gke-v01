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

import grpc, json, logging, threading
from typing import Any, Dict, Set
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME
from common.proto.context_pb2 import ContextId, Device, EventTypeEnum, Link, Slice, TopologyId
from common.proto.dlt_connector_pb2 import DltSliceId
from common.proto.dlt_gateway_pb2 import DltRecordEvent, DltRecordOperationEnum, DltRecordTypeEnum
from common.tools.context_queries.Context import create_context
from common.tools.context_queries.Device import add_device_to_topology
from common.tools.context_queries.Link import add_link_to_topology
from common.tools.context_queries.Topology import create_topology
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from dlt.connector.client.DltConnectorClient import DltConnectorClient
from dlt.connector.client.DltEventsCollector import DltEventsCollector
from dlt.connector.client.DltGatewayClient import DltGatewayClient
from interdomain.client.InterdomainClient import InterdomainClient

LOGGER = logging.getLogger(__name__)

GET_EVENT_TIMEOUT = 0.5

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))

class Clients:
    def __init__(self) -> None:
        self.context_client = ContextClient()
        self.dlt_connector_client = DltConnectorClient()
        self.dlt_gateway_client = DltGatewayClient()
        self.interdomain_client = InterdomainClient()

    def close(self) -> None:
        self.interdomain_client.close()
        self.dlt_gateway_client.close()
        self.dlt_connector_client.close()
        self.context_client.close()

class DltEventDispatcher(threading.Thread):
    def __init__(self) -> None:
        LOGGER.debug('Creating connector...')
        super().__init__(name='DltEventDispatcher', daemon=True)
        self._terminate = threading.Event()
        LOGGER.debug('Connector created')

    def start(self) -> None:
        self._terminate.clear()
        return super().start()

    def stop(self):
        self._terminate.set()

    def run(self) -> None:
        clients = Clients()
        create_context(clients.context_client, DEFAULT_CONTEXT_NAME)
        create_topology(clients.context_client, DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME)
        create_topology(clients.context_client, DEFAULT_CONTEXT_NAME, INTERDOMAIN_TOPOLOGY_NAME)

        dlt_events_collector = DltEventsCollector(clients.dlt_gateway_client, log_events_received=True)
        dlt_events_collector.start()

        while not self._terminate.is_set():
            event = dlt_events_collector.get_event(block=True, timeout=GET_EVENT_TIMEOUT)
            if event is None: continue

            existing_topology_ids = clients.context_client.ListTopologyIds(ADMIN_CONTEXT_ID)
            local_domain_uuids = {
                topology_id.topology_uuid.uuid for topology_id in existing_topology_ids.topology_ids
            }
            local_domain_uuids.discard(DEFAULT_TOPOLOGY_NAME)
            local_domain_uuids.discard(INTERDOMAIN_TOPOLOGY_NAME)

            self.dispatch_event(clients, local_domain_uuids, event)

        dlt_events_collector.stop()
        clients.close()

    def dispatch_event(self, clients : Clients, local_domain_uuids : Set[str], event : DltRecordEvent) -> None:
        record_type : DltRecordTypeEnum = event.record_id.type # {UNDEFINED/CONTEXT/TOPOLOGY/DEVICE/LINK/SERVICE/SLICE}
        if record_type == DltRecordTypeEnum.DLTRECORDTYPE_DEVICE:
            self._dispatch_device(clients, local_domain_uuids, event)
        elif record_type == DltRecordTypeEnum.DLTRECORDTYPE_LINK:
            self._dispatch_link(clients, local_domain_uuids, event)
        elif record_type == DltRecordTypeEnum.DLTRECORDTYPE_SLICE:
            self._dispatch_slice(clients, local_domain_uuids, event)
        else:
            raise NotImplementedError('EventType: {:s}'.format(grpc_message_to_json_string(event)))

    def _dispatch_device(self, clients : Clients, local_domain_uuids : Set[str], event : DltRecordEvent) -> None:
        domain_uuid : str = event.record_id.domain_uuid.uuid

        if domain_uuid in local_domain_uuids:
            MSG = '[_dispatch_device] Ignoring DLT event received (local): {:s}'
            LOGGER.info(MSG.format(grpc_message_to_json_string(event)))
            return

        MSG = '[_dispatch_device] DLT event received (remote): {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(event)))

        event_type : EventTypeEnum = event.event.event_type # {UNDEFINED/CREATE/UPDATE/REMOVE}
        if event_type in {EventTypeEnum.EVENTTYPE_CREATE, EventTypeEnum.EVENTTYPE_UPDATE}:
            LOGGER.info('[_dispatch_device] event.record_id={:s}'.format(grpc_message_to_json_string(event.record_id)))
            record = clients.dlt_gateway_client.GetFromDlt(event.record_id)
            LOGGER.info('[_dispatch_device] record={:s}'.format(grpc_message_to_json_string(record)))

            create_context(clients.context_client, domain_uuid)
            create_topology(clients.context_client, domain_uuid, DEFAULT_TOPOLOGY_NAME)
            device = Device(**json.loads(record.data_json))
            clients.context_client.SetDevice(device)
            device_uuid = device.device_id.device_uuid.uuid # pylint: disable=no-member
            add_device_to_topology(clients.context_client, ADMIN_CONTEXT_ID, INTERDOMAIN_TOPOLOGY_NAME, device_uuid)
            domain_context_id = ContextId(**json_context_id(domain_uuid))
            add_device_to_topology(clients.context_client, domain_context_id, DEFAULT_TOPOLOGY_NAME, device_uuid)
        elif event_type in {EventTypeEnum.EVENTTYPE_DELETE}:
            raise NotImplementedError('Delete Device')

    def _dispatch_link(self, clients : Clients, local_domain_uuids : Set[str], event : DltRecordEvent) -> None:
        domain_uuid : str = event.record_id.domain_uuid.uuid

        if domain_uuid in local_domain_uuids:
            MSG = '[_dispatch_link] Ignoring DLT event received (local): {:s}'
            LOGGER.info(MSG.format(grpc_message_to_json_string(event)))
            return

        MSG = '[_dispatch_link] DLT event received (remote): {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(event)))

        event_type : EventTypeEnum = event.event.event_type # {UNDEFINED/CREATE/UPDATE/REMOVE}
        if event_type in {EventTypeEnum.EVENTTYPE_CREATE, EventTypeEnum.EVENTTYPE_UPDATE}:
            LOGGER.info('[_dispatch_link] event.record_id={:s}'.format(grpc_message_to_json_string(event.record_id)))
            record = clients.dlt_gateway_client.GetFromDlt(event.record_id)
            LOGGER.info('[_dispatch_link] record={:s}'.format(grpc_message_to_json_string(record)))

            link = Link(**json.loads(record.data_json))
            clients.context_client.SetLink(link)
            link_uuid = link.link_id.link_uuid.uuid # pylint: disable=no-member
            add_link_to_topology(clients.context_client, ADMIN_CONTEXT_ID, INTERDOMAIN_TOPOLOGY_NAME, link_uuid)
        elif event_type in {EventTypeEnum.EVENTTYPE_DELETE}:
            raise NotImplementedError('Delete Link')

    def _dispatch_slice(self, clients : Clients, local_domain_uuids : Set[str], event : DltRecordEvent) -> None:
        event_type  : EventTypeEnum = event.event.event_type # {UNDEFINED/CREATE/UPDATE/REMOVE}
        domain_uuid : str = event.record_id.domain_uuid.uuid

        LOGGER.info('[_dispatch_slice] event.record_id={:s}'.format(grpc_message_to_json_string(event.record_id)))
        record = clients.dlt_gateway_client.GetFromDlt(event.record_id)
        LOGGER.info('[_dispatch_slice] record={:s}'.format(grpc_message_to_json_string(record)))

        slice_ = Slice(**json.loads(record.data_json))

        context_uuid = slice_.slice_id.context_id.context_uuid.uuid
        owner_uuid = slice_.slice_owner.owner_uuid.uuid
        create_context(clients.context_client, context_uuid)
        create_topology(clients.context_client, context_uuid, DEFAULT_TOPOLOGY_NAME)

        if domain_uuid in local_domain_uuids:
            # it is for "me"
            if event_type in {EventTypeEnum.EVENTTYPE_CREATE, EventTypeEnum.EVENTTYPE_UPDATE}:
                try:
                    db_slice = clients.context_client.GetSlice(slice_.slice_id)
                    # exists
                    db_json_slice = grpc_message_to_json_string(db_slice)
                except grpc.RpcError:
                    # not exists
                    db_json_slice = None

                _json_slice = grpc_message_to_json_string(slice_)
                if db_json_slice != _json_slice:
                    # not exists or is different...
                    slice_id = clients.interdomain_client.RequestSlice(slice_)
                    topology_id = TopologyId(**json_topology_id(domain_uuid))
                    dlt_slice_id = DltSliceId()
                    dlt_slice_id.topology_id.CopyFrom(topology_id)  # pylint: disable=no-member
                    dlt_slice_id.slice_id.CopyFrom(slice_id)        # pylint: disable=no-member
                    clients.dlt_connector_client.RecordSlice(dlt_slice_id)

            elif event_type in {EventTypeEnum.EVENTTYPE_DELETE}:
                raise NotImplementedError('Delete Slice')
        elif owner_uuid in local_domain_uuids:
            # it is owned by me
            # just update it locally
            LOGGER.info('[_dispatch_slice] updating locally')

            local_slice = Slice()
            local_slice.CopyFrom(slice_)

            # pylint: disable=no-member
            del local_slice.slice_service_ids[:]    # they are from remote domains so will not be present locally
            del local_slice.slice_subslice_ids[:]   # they are from remote domains so will not be present locally

            clients.context_client.SetSlice(local_slice)
        else:
            MSG = '[_dispatch_slice] Ignoring DLT event received (remote): {:s}'
            LOGGER.info(MSG.format(grpc_message_to_json_string(event)))

