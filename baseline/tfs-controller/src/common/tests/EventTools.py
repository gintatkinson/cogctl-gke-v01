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

import json, logging
from typing import Dict, List, Tuple
from common.proto.context_pb2 import (
    ConnectionEvent, ContextEvent, DeviceEvent, EventTypeEnum, LinkEvent, ServiceEvent, SliceEvent, TopologyEvent)
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.EventsCollector import EventsCollector

LOGGER = logging.getLogger(__name__)

EVENT_CREATE = EventTypeEnum.EVENTTYPE_CREATE
EVENT_UPDATE = EventTypeEnum.EVENTTYPE_UPDATE
EVENT_REMOVE = EventTypeEnum.EVENTTYPE_REMOVE

def class_to_classname(klass): return klass.__name__
def instance_to_classname(instance): return type(instance).__name__

CLASSNAME_CONTEXT_EVENT    = class_to_classname(ContextEvent)
CLASSNAME_TOPOLOGY_EVENT   = class_to_classname(TopologyEvent)
CLASSNAME_DEVICE_EVENT     = class_to_classname(DeviceEvent)
CLASSNAME_LINK_EVENT       = class_to_classname(LinkEvent)
CLASSNAME_SLICE_EVENT      = class_to_classname(SliceEvent)
CLASSNAME_SERVICE_EVENT    = class_to_classname(ServiceEvent)
CLASSNAME_CONNECTION_EVENT = class_to_classname(ConnectionEvent)

EVENT_CLASS_NAME__TO__ENTITY_ID_SELECTOR = {
    CLASSNAME_CONTEXT_EVENT   : lambda event: event.context_id,
    CLASSNAME_TOPOLOGY_EVENT  : lambda event: event.topology_id,
    CLASSNAME_DEVICE_EVENT    : lambda event: event.device_id,
    CLASSNAME_LINK_EVENT      : lambda event: event.link_id,
    CLASSNAME_SLICE_EVENT     : lambda event: event.slice_id,
    CLASSNAME_SERVICE_EVENT   : lambda event: event.service_id,
    CLASSNAME_CONNECTION_EVENT: lambda event: event.connection_id,
}

def event_to_key(event):
    event_class_name = instance_to_classname(event)
    entity_id_selector_function = EVENT_CLASS_NAME__TO__ENTITY_ID_SELECTOR.get(event_class_name)
    entity_id = entity_id_selector_function(event)
    return (event_class_name, event.event.event_type, grpc_message_to_json_string(entity_id))

def check_events(
    events_collector : EventsCollector, expected_events : List[Tuple[str, int, Dict]],
    fail_if_missing_events : bool = True, fail_if_unexpected_events : bool = False,
    timeout_per_event = 1.0, max_wait_time = 30.0
) -> None:
    expected_events_map = {}
    num_expected_events = 0
    for event_classname, event_type_id, event_ids in expected_events:
        event_key = (event_classname, event_type_id, json.dumps(event_ids, sort_keys=True))
        event_count = expected_events_map.get(event_key, 0)
        expected_events_map[event_key] = event_count + 1
        num_expected_events += 1

    i, wait_time = 0, 0
    while num_expected_events > 0:
        event_received = events_collector.get_event(block=True, timeout=timeout_per_event)
        if event_received is None:
            wait_time += timeout_per_event
            if wait_time > max_wait_time: break
            continue
        LOGGER.info('event_received[{:d}] = {:s}'.format(i, str(event_received)))
        event_key = event_to_key(event_received)
        event_count = expected_events_map.pop(event_key, 0)
        if event_count > 0: num_expected_events -= 1
        event_count -= 1
        if event_count != 0: expected_events_map[event_key] = event_count

    if len(expected_events_map) == 0:
        LOGGER.info('EventsCheck passed')
    else:
        missing_events = {}
        unexpected_events = {}
        for event_key,event_count in expected_events_map.items():
            if event_count > 0:
                missing_events[event_key] = event_count
            if event_count < 0:
                unexpected_events[event_key] = -event_count
        msg_except = ['EventCheck failed:']
        msg_logger = ['EventCheck:']
        if len(missing_events) > 0:
            msg = 'missing_events={:s}'.format(str(missing_events))
            if fail_if_missing_events: msg_except.append(msg)
            msg_logger.append(msg)
        if len(unexpected_events) > 0:
            msg = 'unexpected_events={:s}'.format(str(unexpected_events))
            if fail_if_unexpected_events: msg_except.append(msg)
            msg_logger.append(msg)
        if len(msg_logger) > 1: LOGGER.warning(' '.join(msg_logger))
        if len(msg_except) > 1: raise Exception(' '.join(msg_except))
