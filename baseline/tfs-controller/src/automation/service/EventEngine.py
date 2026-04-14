# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, logging, queue, threading
from typing import Dict, Optional
from automation.service.Tools import create_kpi_descriptor, start_collector
from common.proto.context_pb2 import (
    ConfigActionEnum, DeviceEvent, DeviceOperationalStatusEnum, Empty, ServiceEvent
)
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.grpc.BaseEventCollector import BaseEventCollector
from common.tools.grpc.BaseEventDispatcher import BaseEventDispatcher
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from kpi_manager.client.KpiManagerClient import KpiManagerClient
from telemetry.frontend.client.TelemetryFrontendClient import TelemetryFrontendClient

LOGGER = logging.getLogger(__name__)

DEVICE_OP_STATUS_UNDEFINED   = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_UNDEFINED
DEVICE_OP_STATUS_DISABLED    = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED
DEVICE_OP_STATUS_ENABLED     = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED
DEVICE_OP_STATUS_NOT_ENABLED = {DEVICE_OP_STATUS_UNDEFINED, DEVICE_OP_STATUS_DISABLED}

KPISAMPLETYPE_UNKNOWN        = KpiSampleType.KPISAMPLETYPE_UNKNOWN

class EventCollector(BaseEventCollector):
    pass

class EventDispatcher(BaseEventDispatcher):
    def __init__(
        self, events_queue : queue.PriorityQueue,
        terminate : Optional[threading.Event] = None
    ) -> None:
        super().__init__(events_queue, terminate)
        self._context_client     = ContextClient()
        self._kpi_manager_client = KpiManagerClient()
        self._telemetry_client   = TelemetryFrontendClient()
        self._device_endpoint_monitored : Dict[str, Dict[str, bool]] = dict()

    def dispatch_device_create(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Create: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))
        self._device_activate_monitoring(device_event)

    def dispatch_device_update(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Update: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))
        self._device_activate_monitoring(device_event)

    def dispatch_device_remove(self, device_event : DeviceEvent) -> None:
        MSG = 'Processing Device Remove: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(device_event)))

    def dispatch_service_create(self, service_event : ServiceEvent) -> None:
        MSG = 'Processing Service Create: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(service_event)))

    def dispatch_service_update(self, service_event : ServiceEvent) -> None:
        MSG = 'Processing Service Update: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(service_event)))

    def dispatch_service_remove(self, service_event : ServiceEvent) -> None:
        MSG = 'Processing Service Remove: {:s}'
        LOGGER.info(MSG.format(grpc_message_to_json_string(service_event)))

    def _device_activate_monitoring(self, device_event : DeviceEvent) -> None:
        device_id = device_event.device_id
        device_uuid = device_id.device_uuid.uuid
        device = self._context_client.GetDevice(device_id)

        device_op_status = device.device_operational_status
        if device_op_status != DEVICE_OP_STATUS_ENABLED:
            LOGGER.debug('Ignoring Device not enabled: {:s}'.format(grpc_message_to_json_string(device)))
            return

        enabled_endpoint_names = set()
        for config_rule in device.device_config.config_rules:
            if config_rule.action != ConfigActionEnum.CONFIGACTION_SET: continue
            if config_rule.WhichOneof('config_rule') != 'custom': continue
            str_resource_key = str(config_rule.custom.resource_key)
            if not str_resource_key.startswith('/interface['): continue
            json_resource_value = json.loads(config_rule.custom.resource_value)
            if 'name' not in json_resource_value: continue
            if 'enabled' not in json_resource_value: continue
            if not json_resource_value['enabled']: continue
            enabled_endpoint_names.add(json_resource_value['name'])

        endpoints_monitored = self._device_endpoint_monitored.setdefault(device_uuid, dict())
        for endpoint in device.device_endpoints:
            endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
            endpoint_name_or_uuid = endpoint.name
            if endpoint_name_or_uuid is None or len(endpoint_name_or_uuid) == 0:
                endpoint_name_or_uuid = endpoint_uuid

            endpoint_was_monitored = endpoints_monitored.get(endpoint_uuid, False)
            endpoint_is_enabled = (endpoint_name_or_uuid in enabled_endpoint_names)

            if not endpoint_was_monitored and endpoint_is_enabled:
                # activate
                for kpi_sample_type in endpoint.kpi_sample_types:
                    if kpi_sample_type == KPISAMPLETYPE_UNKNOWN: continue

                    kpi_id = create_kpi_descriptor(
                        self._kpi_manager_client, kpi_sample_type,
                        device_id=device.device_id,
                        endpoint_id=endpoint.endpoint_id,
                    )

                    duration_seconds = 86400
                    interval_seconds = 10
                    collector_id = start_collector(
                        self._telemetry_client, kpi_id,
                        duration_seconds, interval_seconds
                    )

                endpoints_monitored[endpoint_uuid] = True
            else:
                MSG = 'Not implemented condition: event={:s} device={:s} endpoint={:s}' + \
                        ' endpoint_was_monitored={:s} endpoint_is_enabled={:s}'
                LOGGER.warning(MSG.format(
                    grpc_message_to_json_string(device_event), grpc_message_to_json_string(device),
                    grpc_message_to_json_string(endpoint), str(endpoint_was_monitored),
                    str(endpoint_is_enabled)
                ))

class EventEngine:
    def __init__(
        self, terminate : Optional[threading.Event] = None
    ) -> None:
        self._terminate = threading.Event() if terminate is None else terminate

        self._context_client = ContextClient()
        self._event_collector = EventCollector(terminate=self._terminate)
        self._event_collector.install_collector(
            self._context_client.GetDeviceEvents, Empty(),
            log_events_received=True
        )
        self._event_collector.install_collector(
            self._context_client.GetServiceEvents, Empty(),
            log_events_received=True
        )

        self._event_dispatcher = EventDispatcher(
            self._event_collector.get_events_queue(),
            terminate=self._terminate
        )

    def start(self) -> None:
        self._context_client.connect()
        self._event_collector.start()
        self._event_dispatcher.start()

    def stop(self) -> None:
        self._terminate.set()
        self._event_dispatcher.stop()
        self._event_collector.stop()
        self._context_client.close()
