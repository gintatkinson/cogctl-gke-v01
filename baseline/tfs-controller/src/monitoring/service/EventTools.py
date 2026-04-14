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

import grpc, json, logging, queue, threading
from typing import Dict
from common.method_wrappers.ServiceExceptions import ServiceException
from common.proto import monitoring_pb2
from common.proto.context_pb2 import ConfigActionEnum, DeviceOperationalStatusEnum, Empty, EventTypeEnum
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from monitoring.client.MonitoringClient import MonitoringClient
from monitoring.service.MonitoringServiceServicerImpl import LOGGER
from monitoring.service.NameMapping import NameMapping

LOGGER = logging.getLogger(__name__)

DEVICE_OP_STATUS_UNDEFINED   = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_UNDEFINED
DEVICE_OP_STATUS_DISABLED    = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED
DEVICE_OP_STATUS_ENABLED     = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED
DEVICE_OP_STATUS_NOT_ENABLED = {DEVICE_OP_STATUS_UNDEFINED, DEVICE_OP_STATUS_DISABLED}
KPISAMPLETYPE_UNKNOWN        = KpiSampleType.KPISAMPLETYPE_UNKNOWN

class EventsDeviceCollector:
    def __init__(self, name_mapping : NameMapping) -> None: # pylint: disable=redefined-outer-name
        self._events_queue = queue.Queue()

        self._context_client_grpc = ContextClient()
        self._device_stream     = self._context_client_grpc.GetDeviceEvents(Empty())
        self._context_client    = self._context_client_grpc
        self._channel           = self._context_client_grpc.channel
        self._monitoring_client = MonitoringClient(host='127.0.0.1')

        self._device_thread   = threading.Thread(target=self._collect, args=(self._device_stream,), daemon=False)

        #self._device_to_state : Dict[str, DeviceOperationalStatusEnum] = dict()
        self._device_endpoint_monitored : Dict[str, Dict[str, bool]] = dict()
        self._name_mapping = name_mapping

    def grpc_server_on(self):
        try:
            grpc.channel_ready_future(self._channel).result(timeout=15)
            return True
        except grpc.FutureTimeoutError:
            return False

    def _collect(self, events_stream):
        try:
            for event in events_stream:
                self._events_queue.put_nowait(event)
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.CANCELLED: # pylint: disable=no-member
                raise # pragma: no cover

    def start(self):
        try:
            self._device_thread.start()
        except RuntimeError:
            LOGGER.exception('Start EventTools exception')

    def get_event(self, block : bool = True, timeout : float = 0.1):
        return self._events_queue.get(block=block, timeout=timeout)

    def stop(self):
        self._device_stream.cancel()
        self._device_thread.join()

    def listen_events(self):
        try:
            kpi_id_list = []

            while True:
                try:
                    event = self.get_event(block=True, timeout=0.5)

                    event_type = event.event.event_type
                    device_uuid = event.device_id.device_uuid.uuid
                    if event_type in {EventTypeEnum.EVENTTYPE_REMOVE}:
                        LOGGER.debug('Ignoring REMOVE event: {:s}'.format(grpc_message_to_json_string(event)))
                        self._device_endpoint_monitored.pop(device_uuid, None)
                        continue

                    if event_type not in {EventTypeEnum.EVENTTYPE_CREATE, EventTypeEnum.EVENTTYPE_UPDATE}:
                        LOGGER.debug('Ignoring UNKNOWN event type: {:s}'.format(grpc_message_to_json_string(event)))
                        continue

                    device = self._context_client.GetDevice(event.device_id)
                    self._name_mapping.set_device_name(device_uuid, device.name)

                    device_op_status = device.device_operational_status
                    if device_op_status != DEVICE_OP_STATUS_ENABLED:
                        LOGGER.debug('Ignoring Device not enabled: {:s}'.format(grpc_message_to_json_string(device)))
                        continue

                    enabled_endpoint_names = set()
                    for config_rule in device.device_config.config_rules:
                        if config_rule.action != ConfigActionEnum.CONFIGACTION_SET: continue
                        if config_rule.WhichOneof('config_rule') != 'custom': continue
                        str_resource_key = str(config_rule.custom.resource_key)
                        if str_resource_key.startswith('/interface[') or str_resource_key.startswith('/endpoints/endpoint['):
                            json_resource_value = json.loads(config_rule.custom.resource_value)
                            if 'name' not in json_resource_value: continue
                            if 'enabled' in json_resource_value:
                                if not json_resource_value['enabled']: continue
                                enabled_endpoint_names.add(json_resource_value['name'])
                            if 'oper-status' in json_resource_value:
                                if str(json_resource_value['oper-status']).upper() != 'UP': continue
                                enabled_endpoint_names.add(json_resource_value['name'])

                    endpoints_monitored = self._device_endpoint_monitored.setdefault(device_uuid, dict())
                    for endpoint in device.device_endpoints:
                        endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
                        endpoint_name_or_uuid = endpoint.name
                        if endpoint_name_or_uuid is None or len(endpoint_name_or_uuid) == 0:
                            endpoint_name_or_uuid = endpoint_uuid

                        self._name_mapping.set_endpoint_name(endpoint_uuid, endpoint.name)

                        endpoint_was_monitored = endpoints_monitored.get(endpoint_uuid, False)
                        endpoint_is_enabled = (endpoint_name_or_uuid in enabled_endpoint_names)

                        if not endpoint_was_monitored and not endpoint_is_enabled:
                            # endpoint is idle, do nothing
                            pass
                        elif not endpoint_was_monitored and endpoint_is_enabled:
                            # activate
                            for value in endpoint.kpi_sample_types:
                                if value == KPISAMPLETYPE_UNKNOWN: continue

                                kpi_descriptor = monitoring_pb2.KpiDescriptor()
                                kpi_descriptor.kpi_description = device.device_type
                                kpi_descriptor.kpi_sample_type = value
                                kpi_descriptor.device_id.CopyFrom(device.device_id)         # pylint: disable=no-member
                                kpi_descriptor.endpoint_id.CopyFrom(endpoint.endpoint_id)   # pylint: disable=no-member

                                kpi_id = self._monitoring_client.SetKpi(kpi_descriptor)
                                kpi_id_list.append(kpi_id)
                            endpoints_monitored[endpoint_uuid] = True
                        else:
                            MSG = 'Not implemented condition: event={:s} device={:s} endpoint={:s}' + \
                                  ' endpoint_was_monitored={:s} endpoint_is_enabled={:s}'
                            LOGGER.warning(MSG.format(
                                grpc_message_to_json_string(event), grpc_message_to_json_string(device),
                                grpc_message_to_json_string(endpoint), str(endpoint_was_monitored),
                                str(endpoint_is_enabled)
                            ))

                except queue.Empty:
                    break

            return kpi_id_list
        except ServiceException:
            LOGGER.exception('ListenEvents exception')
        except Exception:  # pragma: no cover # pylint: disable=broad-except
            LOGGER.exception('ListenEvents exception')
