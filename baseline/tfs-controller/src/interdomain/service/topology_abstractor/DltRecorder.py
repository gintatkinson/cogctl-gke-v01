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

import logging, threading, asyncio, time
from typing import Dict, Optional
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME
from common.proto.context_pb2 import (
    ContextEvent, ContextId, DeviceEvent, DeviceId, LinkId, LinkEvent, TopologyId, TopologyEvent
)
from common.tools.context_queries.Context import create_context
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from .DltRecordSender import DltRecordSender
from .Types import EventTypes

LOGGER = logging.getLogger(__name__)

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))
INTERDOMAIN_TOPOLOGY_ID = TopologyId(**json_topology_id(INTERDOMAIN_TOPOLOGY_NAME, context_id=ADMIN_CONTEXT_ID))


class DLTRecorder(threading.Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.terminate = threading.Event()
        self.context_client = ContextClient()
        self.context_event_collector = EventsCollector(self.context_client)
        self.topology_cache: Dict[str, TopologyId] = {}

        # Queues for each event type
        self.create_event_queue = asyncio.Queue()
        self.update_event_queue = asyncio.Queue()
        self.remove_event_queue = asyncio.Queue()

    def stop(self):
        self.terminate.set()

    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        self.context_client.connect()
        create_context(self.context_client, DEFAULT_CONTEXT_NAME)
        #self.create_topologies()
        self.context_event_collector.start()

        batch_timeout = 1  # Time in seconds to wait before processing whatever tasks are available
        last_task_time = time.time()

        while not self.terminate.is_set():
            event = self.context_event_collector.get_event(timeout=0.1)
            if event:
                LOGGER.info('Received Event({:s})...'.format(grpc_message_to_json_string(event)))

                # Prioritize the event based on its type
                if event.event.event_type == 1:  # CREATE
                    await self.create_event_queue.put(event)
                elif event.event.event_type == 2:  # UPDATE
                    await self.update_event_queue.put(event)
                elif event.event.event_type == 3:  # REMOVE
                    await self.remove_event_queue.put(event)

            # Check if it's time to process the tasks or if we have enough tasks
            current_time = time.time()
            if current_time - last_task_time >= batch_timeout:
                await self.process_events()
                last_task_time = current_time  # Reset the timer after processing

        self.context_event_collector.stop()
        self.context_client.close()

    async def process_events(self):
        # Process CREATE events first
        await self.process_queue(self.create_event_queue)
        # Then process UPDATE events
        await self.process_queue(self.update_event_queue)
        # Finally, process REMOVE events
        await self.process_queue(self.remove_event_queue)

    async def process_queue(self, queue : asyncio.Queue):
        tasks = []
        while not queue.empty():
            event = await queue.get()
            LOGGER.info('Processing Event({:s}) from queue...'.format(grpc_message_to_json_string(event)))
            task = asyncio.create_task(self.update_record(event))
            tasks.append(task)

        # Execute tasks concurrently
        if tasks:
            try:
                await asyncio.gather(*tasks)
            except Exception as e:
                LOGGER.error(f"Error while processing tasks: {e}")

    async def update_record(self, event : EventTypes) -> None:
        dlt_record_sender = DltRecordSender(self.context_client)
        await dlt_record_sender.initialize()  # Ensure DltRecordSender is initialized asynchronously
        LOGGER.debug('STARTING processing event: {:s}'.format(grpc_message_to_json_string(event)))

        if isinstance(event, ContextEvent):
            LOGGER.debug('Processing ContextEvent({:s})'.format(grpc_message_to_json_string(event)))
            LOGGER.warning('Ignoring ContextEvent({:s})'.format(grpc_message_to_json_string(event)))

        elif isinstance(event, TopologyEvent):
            LOGGER.debug('Processing TopologyEvent({:s})'.format(grpc_message_to_json_string(event)))
            self.process_topology_event(event, dlt_record_sender)

        elif isinstance(event, DeviceEvent):
            LOGGER.debug('Processing DeviceEvent ASYNC({:s})'.format(grpc_message_to_json_string(event)))
            self.process_device_event(event, dlt_record_sender)

        elif isinstance(event, LinkEvent):
            LOGGER.debug('Processing LinkEvent({:s})'.format(grpc_message_to_json_string(event)))
            self.process_link_event(event, dlt_record_sender)

        else:
            LOGGER.warning('Unsupported Event({:s})'.format(grpc_message_to_json_string(event)))

        await dlt_record_sender.commit()
        #await asyncio.sleep(2)  # Simulates processing time
        LOGGER.debug('Finished processing event: {:s}'.format(grpc_message_to_json_string(event)))


    def process_topology_event(self, event : TopologyEvent, dlt_record_sender : DltRecordSender) -> None:
        topology_id = event.topology_id
        topology_uuid = topology_id.topology_uuid.uuid
        context_id = topology_id.context_id
        context_uuid = context_id.context_uuid.uuid
        topology_uuids = {DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME}

        context = self.context_client.GetContext(context_id)
        context_name = context.name

        topology_details = self.context_client.GetTopologyDetails(topology_id)
        topology_name = topology_details.name

        self.topology_cache[topology_uuid] = topology_id

        LOGGER.debug('TOPOLOGY Details({:s})'.format(grpc_message_to_json_string(topology_details)))

        if ((context_uuid == DEFAULT_CONTEXT_NAME) or (context_name == DEFAULT_CONTEXT_NAME)) and \
                (topology_uuid not in topology_uuids) and (topology_name not in topology_uuids):
            LOGGER.debug('DEVICES({:s})'.format(grpc_message_to_json_string(topology_details.devices)))
            for device in topology_details.devices:
                LOGGER.debug('DEVICE_INFO_TOPO({:s})'.format(grpc_message_to_json_string(device)))
                dlt_record_sender.add_device(topology_id, device)

            for link in topology_details.links:
                dlt_record_sender.add_link(topology_id, link)

        else:
            MSG = 'Ignoring ({:s}/{:s})({:s}/{:s}) TopologyEvent({:s})'
            args = context_uuid, context_name, topology_uuid, topology_name, grpc_message_to_json_string(event)
            LOGGER.warning(MSG.format(*args))

    def find_topology_for_device(self, device_id : DeviceId) -> Optional[TopologyId]:
        for topology_uuid, topology_id in self.topology_cache.items():
            details = self.context_client.GetTopologyDetails(topology_id)
            for device in details.devices:
                if device.device_id == device_id:
                    return topology_id
        return None

    def find_topology_for_link(self, link_id : LinkId) -> Optional[TopologyId]:
        for topology_uuid, topology_id in self.topology_cache.items():
            details = self.context_client.GetTopologyDetails(topology_id)
            for link in details.links:
                if link.link_id == link_id:
                    return topology_id
        return None

    def process_device_event(self, event : DeviceEvent, dlt_record_sender : DltRecordSender) -> None:
        device_id = event.device_id
        device = self.context_client.GetDevice(device_id)
        topology_id = self.find_topology_for_device(device_id)
        if topology_id:
            LOGGER.debug('DEVICE_INFO({:s}), DEVICE_ID ({:s})'.format(
                str(device.device_id.device_uuid.uuid),
                grpc_message_to_json_string(device_id)
            ))
            dlt_record_sender.add_device(topology_id, device)
        else:
            LOGGER.warning("Topology not found for device {:s}".format(str(device_id.device_uuid.uuid)))

    def process_link_event(self, event: LinkEvent, dlt_record_sender: DltRecordSender) -> None:
        link_id = event.link_id
        link = self.context_client.GetLink(link_id)
        topology_id = self.find_topology_for_link(link_id)
        if topology_id:
            dlt_record_sender.add_link(topology_id, link)
        else:
            LOGGER.warning("Topology not found for link {:s}".format(str(link_id.link_uuid.uuid)))
