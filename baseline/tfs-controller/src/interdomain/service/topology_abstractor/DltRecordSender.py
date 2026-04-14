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

import asyncio, logging
from typing import Dict, List, Tuple
from common.proto.context_pb2 import Device, Link, Service, Slice, TopologyId
from common.proto.dlt_connector_pb2 import DltDeviceId, DltLinkId, DltServiceId, DltSliceId
from context.client.ContextClient import ContextClient
from dlt.connector.client.DltConnectorClientAsync import DltConnectorClientAsync

LOGGER = logging.getLogger(__name__)

class DltRecordSender:
    def __init__(self, context_client : ContextClient) -> None:
        self.context_client = context_client
        LOGGER.debug('Creating Servicer...')
        self.dlt_connector_client = DltConnectorClientAsync()
        LOGGER.debug('Servicer Created')
        self.dlt_record_uuids : List[str] = list()
        self.dlt_record_uuid_to_data : Dict[str, Tuple[TopologyId, object]] = dict()

    async def initialize(self):
        await self.dlt_connector_client.connect()

    def _add_record(self, record_uuid : str, data : Tuple[TopologyId, object]) -> None:
        if record_uuid in self.dlt_record_uuid_to_data: return
        self.dlt_record_uuid_to_data[record_uuid] = data
        self.dlt_record_uuids.append(record_uuid)

    def add_device(self, topology_id : TopologyId, device : Device) -> None:
        topology_uuid = topology_id.topology_uuid.uuid
        device_uuid = device.device_id.device_uuid.uuid
        record_uuid = '{:s}:device:{:s}'.format(topology_uuid, device_uuid)
        self._add_record(record_uuid, (topology_id, device))

    def add_link(self, topology_id : TopologyId, link : Link) -> None:
        topology_uuid = topology_id.topology_uuid.uuid
        link_uuid = link.link_id.link_uuid.uuid
        record_uuid = '{:s}:link:{:s}'.format(topology_uuid, link_uuid)
        self._add_record(record_uuid, (topology_id, link))

    def add_service(self, topology_id : TopologyId, service : Service) -> None:
        topology_uuid = topology_id.topology_uuid.uuid
        context_uuid = service.service_id.context_id.context_uuid.uuid
        service_uuid = service.service_id.service_uuid.uuid
        record_uuid = '{:s}:service:{:s}/{:s}'.format(topology_uuid, context_uuid, service_uuid)
        self._add_record(record_uuid, (topology_id, service))

    def add_slice(self, topology_id : TopologyId, slice_ : Slice) -> None:
        topology_uuid = topology_id.topology_uuid.uuid
        context_uuid = slice_.slice_id.context_id.context_uuid.uuid
        slice_uuid = slice_.slice_id.slice_uuid.uuid
        record_uuid = '{:s}:slice:{:s}/{:s}'.format(topology_uuid, context_uuid, slice_uuid)
        self._add_record(record_uuid, (topology_id, slice_))

    async def commit(self) -> None:
        if not self.dlt_connector_client:
            LOGGER.error('DLT Connector Client is None, cannot commit records.')
            return

        tasks = []  # List to hold all the async tasks

        for dlt_record_uuid in self.dlt_record_uuids:
            topology_id, dlt_record = self.dlt_record_uuid_to_data[dlt_record_uuid]
            if isinstance(dlt_record, Device):
                device_id = dlt_record.device_id
                if self.dlt_connector_client is None: continue
                dlt_device_id = DltDeviceId()
                dlt_device_id.topology_id.CopyFrom(topology_id)     # pylint: disable=no-member
                dlt_device_id.device_id.CopyFrom(device_id)         # pylint: disable=no-member
                tasks.append(self.dlt_connector_client.RecordDevice(dlt_device_id))
            elif isinstance(dlt_record, Link):
                link_id = dlt_record.link_id
                if self.dlt_connector_client is None: continue
                dlt_link_id = DltLinkId()
                dlt_link_id.topology_id.CopyFrom(topology_id)       # pylint: disable=no-member
                dlt_link_id.link_id.CopyFrom(link_id)               # pylint: disable=no-member
                tasks.append(self.dlt_connector_client.RecordLink(dlt_link_id))
            elif isinstance(dlt_record, Service):
                service_id = dlt_record.service_id
                if self.dlt_connector_client is None: continue
                dlt_service_id = DltServiceId()
                dlt_service_id.topology_id.CopyFrom(topology_id)    # pylint: disable=no-member
                dlt_service_id.service_id.CopyFrom(service_id)      # pylint: disable=no-member
                tasks.append(self.dlt_connector_client.RecordService(dlt_service_id))
            elif isinstance(dlt_record, Slice):
                slice_id = dlt_record.slice_id
                if self.dlt_connector_client is None: continue
                dlt_slice_id = DltSliceId()
                dlt_slice_id.topology_id.CopyFrom(topology_id)      # pylint: disable=no-member
                dlt_slice_id.slice_id.CopyFrom(slice_id)            # pylint: disable=no-member
                tasks.append(self.dlt_connector_client.RecordSlice(dlt_slice_id))
            else:
                LOGGER.error(f'Unsupported Record({str(dlt_record)})')

        if tasks:
            await asyncio.gather(*tasks)  # Run all the tasks concurrently
