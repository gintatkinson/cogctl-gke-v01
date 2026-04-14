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

import logging, threading
from typing import Optional, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, ServiceNameEnum
from common.DeviceTypes import DeviceTypeEnum
from common.Settings import get_service_host, get_service_port_grpc
from common.proto.context_pb2 import ConfigActionEnum, DeviceEvent
from common.proto.context_pb2 import TeraFlowController
from common.tools.context_queries.Device import get_device
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from interdomain.client.InterdomainClient import InterdomainClient

LOGGER = logging.getLogger(__name__)

def get_domain_data(context_client : ContextClient, event : DeviceEvent) -> Optional[Tuple[str, str, str, int]]:
    device_uuid = event.device_id.device_uuid.uuid
    device = get_device(
        context_client, device_uuid, include_endpoints=False,
        include_components=False, include_config_rules=True)
    if device.device_type != DeviceTypeEnum.NETWORK.value: return None
    idc_domain_uuid = device_uuid
    idc_domain_name = device.name
    idc_domain_address = None
    idc_domain_port = None
    for config_rule in device.device_config.config_rules:
        if config_rule.action != ConfigActionEnum.CONFIGACTION_SET: continue
        if config_rule.WhichOneof('config_rule') != 'custom': continue
        if config_rule.custom.resource_key == '_connect/address':
            idc_domain_address = config_rule.custom.resource_value
        if config_rule.custom.resource_key == '_connect/port':
            idc_domain_port = int(config_rule.custom.resource_value)
    if idc_domain_address is None: return None
    if idc_domain_port is None: return None
    return idc_domain_uuid, idc_domain_name, idc_domain_address, idc_domain_port

class RemoteDomainClients(threading.Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.terminate = threading.Event()
        self.lock = threading.Lock()
        self.peer_domains = {}
        self.context_client = ContextClient()
        self.context_event_collector = EventsCollector(self.context_client)

    def stop(self):
        self.terminate.set()

    def run(self) -> None:
        self.context_client.connect()
        self.context_event_collector.start()

        while not self.terminate.is_set():
            event = self.context_event_collector.get_event(timeout=0.1)
            if event is None: continue
            if not isinstance(event, DeviceEvent): continue
            LOGGER.info('Processing DeviceEvent({:s})...'.format(grpc_message_to_json_string(event)))
            domain_data = get_domain_data(self.context_client, event)
            if domain_data is None: continue
            domain_uuid, domain_name, domain_address, domain_port = domain_data
            try:
                self.add_peer(domain_uuid, domain_name, domain_address, domain_port)
            except: # pylint: disable=bare-except
                MSG = 'Unable to connect to remote domain {:s} {:s} ({:s}:{:d})'
                LOGGER.exception(MSG.format(domain_uuid, domain_name, domain_address, domain_port))

        self.context_event_collector.stop()
        self.context_client.close()

    def add_peer(
        self, domain_uuid : str, domain_name : str, domain_address : str, domain_port : int,
        context_uuid : str = DEFAULT_CONTEXT_NAME
    ) -> None:
        request = TeraFlowController()
        request.context_id.context_uuid.uuid = context_uuid # pylint: disable=no-member
        request.ip_address = get_service_host(ServiceNameEnum.INTERDOMAIN)
        request.port = int(get_service_port_grpc(ServiceNameEnum.INTERDOMAIN))

        interdomain_client = InterdomainClient(host=domain_address, port=domain_port)
        interdomain_client.connect()

        reply = interdomain_client.Authenticate(request)

        if not reply.authenticated:
            MSG = 'Authentication against {:s}:{:d} with Context({:s}) rejected'
            # pylint: disable=broad-exception-raised
            raise Exception(MSG.format(domain_address, domain_port, context_uuid))

        with self.lock:
            self.peer_domains[domain_uuid] = interdomain_client
            self.peer_domains[domain_name] = interdomain_client
            MSG = 'Added peer domain {:s} {:s} ({:s}:{:d})'
            LOGGER.info(MSG.format(domain_uuid, domain_name, domain_address, domain_port))

    def get_peer(self, domain_uuid_or_name : str) -> Optional[InterdomainClient]:
        with self.lock:
            LOGGER.debug('domain_uuid_or_name: {:s}'.format(str(domain_uuid_or_name)))
            LOGGER.debug('peers: {:s}'.format(str(self.peer_domains)))
            return self.peer_domains.get(domain_uuid_or_name)

    def remove_peer(self, domain_uuid_or_name : str) -> None:
        with self.lock:
            LOGGER.debug('domain_uuid_or_name: {:s}'.format(str(domain_uuid_or_name)))
            self.peer_domains.pop(domain_uuid_or_name, None)
            LOGGER.info('Removed peer domain {:s}'.format(domain_uuid_or_name))
