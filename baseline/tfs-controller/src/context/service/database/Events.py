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

import enum, json, logging, time
from typing import Dict, Iterator, Set
from common.message_broker.Message import Message
from common.message_broker.MessageBroker import MessageBroker
from common.proto.context_pb2 import (
    AnyEvent, ConnectionEvent, ContextEvent, DeviceEvent, EventTypeEnum, LinkEvent,
    ServiceEvent, SliceEvent, TopologyEvent, OpticalConfigEvent
)

class EventTopicEnum(enum.Enum):
    CONNECTION    = 'connection'
    CONTEXT       = 'context'
    DEVICE        = 'device'
    LINK          = 'link'
    POLICY_RULE   = 'policy-rule'
    SERVICE       = 'service'
    SLICE         = 'slice'
    TOPOLOGY      = 'topology'
    OPTICALCONFIG = 'optical-config'
    ALL           = 'all'
  

TOPIC_TO_EVENTCLASS = {
    EventTopicEnum.CONNECTION.value    : ConnectionEvent,
    EventTopicEnum.CONTEXT.value       : ContextEvent,
    EventTopicEnum.DEVICE.value        : DeviceEvent,
    EventTopicEnum.LINK.value          : LinkEvent,
    #EventTopicEnum.POLICY_RULE.value   : PolicyRuleEvent,  # Not defined in proto files
    EventTopicEnum.SERVICE.value       : ServiceEvent,
    EventTopicEnum.SLICE.value         : SliceEvent,
    EventTopicEnum.TOPOLOGY.value      : TopologyEvent,
    EventTopicEnum.OPTICALCONFIG.value : OpticalConfigEvent,
}

CONSUME_TIMEOUT = 0.5 # seconds

LOGGER = logging.getLogger(__name__)

# NOTE: Forced to use a single "ALL" topic so that we ensure all messages are kept ordered.
#       Consumer filters appropriate ones while delivering.
# TODO: Upgrade this schema with proper in-topic filters to enhance performance.

def notify_event(
    messagebroker : MessageBroker, topic_enum : EventTopicEnum, event_type : EventTypeEnum, fields : Dict[str, str]
) -> None:
    event = {'event': {'timestamp': {'timestamp': time.time()}, 'event_type': event_type}}
    for field_name, field_value in fields.items():
        event[field_name] = field_value
    #messagebroker.publish(Message(topic_enum.value, json.dumps(event)))
    messagebroker.publish(Message(EventTopicEnum.ALL.value, json.dumps(event)))

def notify_event_context(messagebroker : MessageBroker, event_type : EventTypeEnum, context_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.CONTEXT, event_type, {'context_id': context_id})

def notify_event_topology(messagebroker : MessageBroker, event_type : EventTypeEnum, topology_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.TOPOLOGY, event_type, {'topology_id': topology_id})

def notify_event_device(messagebroker : MessageBroker, event_type : EventTypeEnum, device_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.DEVICE, event_type, {'device_id': device_id})

def notify_event_opticalconfig(messagebroker : MessageBroker, event_type : EventTypeEnum, opticalconfig_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.DEVICE, event_type, {'opticalconfig_id': opticalconfig_id})

def notify_event_link(messagebroker : MessageBroker, event_type : EventTypeEnum, link_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.LINK, event_type, {'link_id': link_id})

def notify_event_service(messagebroker : MessageBroker, event_type : EventTypeEnum, service_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.SERVICE, event_type, {'service_id': service_id})

def notify_event_slice(messagebroker : MessageBroker, event_type : EventTypeEnum, slice_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.SLICE, event_type, {'slice_id': slice_id})

def notify_event_connection(messagebroker : MessageBroker, event_type : EventTypeEnum, connection_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.CONNECTION, event_type, {'connection_id': connection_id})

def notify_event_policy_rule(messagebroker : MessageBroker, event_type : EventTypeEnum, policyrule_id : Dict) -> None:
    notify_event(messagebroker, EventTopicEnum.POLICY_RULE, event_type, {'policyrule_id': policyrule_id})

def consume_events(
    messagebroker : MessageBroker, topic_enums : Set[EventTopicEnum], consume_timeout : float = CONSUME_TIMEOUT
) -> Iterator:
    #topic_names = [topic_enum.value for topic_enum in topic_enums]
    topic_names = [EventTopicEnum.ALL.value]
    for message in messagebroker.consume(topic_names, consume_timeout=consume_timeout):
        #event_class = TOPIC_TO_EVENTCLASS.get(message.topic)
        #if event_class is None:
        #    MSG = 'No EventClass defined for Topic({:s}). Ignoring...'
        #    LOGGER.warning(MSG.format(str(message.topic)))
        #    continue
        data = json.loads(message.content)
        if 'context_id' in data:
            if EventTopicEnum.CONTEXT not in topic_enums: continue
            yield ContextEvent(**data)
        elif 'topology_id' in data:
            if EventTopicEnum.TOPOLOGY not in topic_enums: continue
            yield TopologyEvent(**data)
        elif 'device_id' in data:
            if EventTopicEnum.DEVICE not in topic_enums: continue
            yield DeviceEvent(**data)
        elif 'opticalconfig_id' in data:
            if EventTopicEnum.OPTICALCONFIG not in topic_enums: continue
            yield DeviceEvent(**data)
        elif 'link_id' in data:
            if EventTopicEnum.LINK not in topic_enums: continue
            yield LinkEvent(**data)
        elif 'service_id' in data:
            if EventTopicEnum.SERVICE not in topic_enums: continue
            yield ServiceEvent(**data)
        elif 'slice_id' in data:
            if EventTopicEnum.SLICE not in topic_enums: continue
            yield SliceEvent(**data)
        elif 'connection_id' in data:
            if EventTopicEnum.CONNECTION not in topic_enums: continue
            yield ConnectionEvent(**data)
        else:
            MSG = 'Unable to identify EventClass for Message({:s}). Ignoring...'
            LOGGER.warning(MSG.format(str(message)))
            continue

def consume_all_events(
    messagebroker : MessageBroker, consume_timeout : float = CONSUME_TIMEOUT
) -> Iterator[AnyEvent]:
    topic_names = [EventTopicEnum.ALL.value]
    for message in messagebroker.consume(topic_names, consume_timeout=consume_timeout):
        data = json.loads(message.content)
        if 'context_id' in data:
            yield AnyEvent(context=data)
        elif 'topology_id' in data:
            yield AnyEvent(topology=data)
        elif 'device_id' in data:
            yield AnyEvent(device=data)
        elif 'opticalconfig_id' in data:
            yield AnyEvent(device=data)
        elif 'link_id' in data:
            yield AnyEvent(link=data)
        elif 'service_id' in data:
            yield AnyEvent(service=data)
        elif 'slice_id' in data:
            yield AnyEvent(slice=data)
        elif 'connection_id' in data:
            yield AnyEvent(connection=data)
        else:
            MSG = 'Unable to identify EventClass for Message({:s}). Ignoring...'
            LOGGER.warning(MSG.format(str(message)))
            continue
