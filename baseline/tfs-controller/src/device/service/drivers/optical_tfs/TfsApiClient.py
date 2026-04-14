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
from typing import Dict, List, Optional, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import ServiceStatusEnum, ServiceTypeEnum
from common.tools.rest_api.client.RestApiClient import RestApiClient
from common.tools.object_factory.Constraint import json_constraint_custom
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from common.tools.object_factory.Service import json_service
from device.service.driver_api.ImportTopologyEnum import ImportTopologyEnum

CONTEXT_IDS_URL = '/tfs-api/context_ids'
TOPOLOGY_URL    = '/tfs-api/context/{context_uuid:s}/topology_details/{topology_uuid:s}'
SERVICES_URL    = '/tfs-api/context/{context_uuid:s}/services'
SERVICE_URL     = '/tfs-api/context/{context_uuid:s}/service/{service_uuid:s}'

MAPPING_STATUS = {
    'DEVICEOPERATIONALSTATUS_UNDEFINED': 0,
    'DEVICEOPERATIONALSTATUS_DISABLED' : 1,
    'DEVICEOPERATIONALSTATUS_ENABLED'  : 2,
}

MAPPING_DRIVER = {
    'DEVICEDRIVER_UNDEFINED'            : 0,
    'DEVICEDRIVER_OPENCONFIG'           : 1,
    'DEVICEDRIVER_TRANSPORT_API'        : 2,
    'DEVICEDRIVER_P4'                   : 3,
    'DEVICEDRIVER_IETF_NETWORK_TOPOLOGY': 4,
    'DEVICEDRIVER_ONF_TR_532'           : 5,
    'DEVICEDRIVER_XR'                   : 6,
    'DEVICEDRIVER_IETF_L2VPN'           : 7,
    'DEVICEDRIVER_GNMI_OPENCONFIG'      : 8,
    'DEVICEDRIVER_OPTICAL_TFS'          : 9,
    'DEVICEDRIVER_IETF_ACTN'            : 10,
    'DEVICEDRIVER_OC'                   : 11,
    'DEVICEDRIVER_QKD'                  : 12,
    'DEVICEDRIVER_IETF_L3VPN'           : 13,
    'DEVICEDRIVER_IETF_SLICE'           : 14,
    'DEVICEDRIVER_NCE'                  : 15,
    'DEVICEDRIVER_SMARTNIC'             : 16,
    'DEVICEDRIVER_MORPHEUS'             : 17,
    'DEVICEDRIVER_RYU'                  : 18,
    'DEVICEDRIVER_GNMI_NOKIA_SRLINUX'   : 19,
    'DEVICEDRIVER_OPENROADM'            : 20,
    'DEVICEDRIVER_RESTCONF_OPENCONFIG'  : 21,
}

LOGGER = logging.getLogger(__name__)

class TfsApiClient(RestApiClient):
    def __init__(
        self, address : str, port : int, scheme : str = 'http',
        username : Optional[str] = None, password : Optional[str] = None,
        timeout : Optional[int] = 30
    ) -> None:
        super().__init__(
            address, port, scheme=scheme, username=username, password=password,
            timeout=timeout, verify_certs=False, allow_redirects=True, logger=LOGGER
        )

    def check_credentials(self) -> None:
        self.get(CONTEXT_IDS_URL)
        LOGGER.info('Credentials checked')

    def get_devices_endpoints(
        self, import_topology : ImportTopologyEnum = ImportTopologyEnum.DEVICES
    ) -> List[Dict]:
        LOGGER.debug('[get_devices_endpoints] begin')
        MSG = '[get_devices_endpoints] import_topology={:s}'
        LOGGER.debug(MSG.format(str(import_topology)))

        if import_topology == ImportTopologyEnum.DISABLED:
            MSG = 'Unsupported import_topology mode: {:s}'
            raise Exception(MSG.format(str(import_topology)))

        topology = self.get(TOPOLOGY_URL.format(
            context_uuid=DEFAULT_CONTEXT_NAME, topology_uuid=DEFAULT_TOPOLOGY_NAME
        ))

        result = list()
        for json_device in topology['devices']:
            device_uuid : str = json_device['device_id']['device_uuid']['uuid']
            device_type : str = json_device['device_type']
            #if not device_type.startswith('emu-'): device_type = 'emu-' + device_type
            device_status = json_device['device_operational_status']
            device_url = '/devices/device[{:s}]'.format(device_uuid)
            device_data = {
                'uuid': json_device['device_id']['device_uuid']['uuid'],
                'name': json_device['name'],
                'type': device_type,
                'status': MAPPING_STATUS[device_status],
                'drivers': [
                    MAPPING_DRIVER[driver]
                    for driver in json_device['device_drivers']
                ],
            }
            result.append((device_url, device_data))

            for json_endpoint in json_device['device_endpoints']:
                endpoint_uuid = json_endpoint['endpoint_id']['endpoint_uuid']['uuid']
                endpoint_url = '/endpoints/endpoint[{:s}]'.format(endpoint_uuid)
                endpoint_data = {
                    'device_uuid': device_uuid,
                    'uuid': endpoint_uuid,
                    'name': json_endpoint['name'],
                    'type': json_endpoint['endpoint_type'],
                }
                result.append((endpoint_url, endpoint_data))

        if import_topology == ImportTopologyEnum.DEVICES:
            LOGGER.debug('[get_devices_endpoints] devices only; returning')
            return result

        for json_link in topology['links']:
            link_uuid : str = json_link['link_id']['link_uuid']['uuid']
            link_url = '/links/link[{:s}]'.format(link_uuid)
            link_endpoint_ids = [
                (
                    json_endpoint_id['device_id']['device_uuid']['uuid'],
                    json_endpoint_id['endpoint_uuid']['uuid'],
                )
                for json_endpoint_id in json_link['link_endpoint_ids']
            ]
            link_data = {
                'uuid': json_link['link_id']['link_uuid']['uuid'],
                'name': json_link['name'],
                'endpoints': link_endpoint_ids,
            }
            result.append((link_url, link_data))

        for json_link in topology['optical_links']:
            link_uuid : str = json_link['link_id']['link_uuid']['uuid']
            link_url = '/links/link[{:s}]'.format(link_uuid)
            link_endpoint_ids = [
                (
                    json_endpoint_id['device_id']['device_uuid']['uuid'],
                    json_endpoint_id['endpoint_uuid']['uuid'],
                )
                for json_endpoint_id in json_link['link_endpoint_ids']
            ]
            link_data = {
                'uuid': json_link['link_id']['link_uuid']['uuid'],
                'name': json_link['name'],
                'endpoints': link_endpoint_ids,
            }
            result.append((link_url, link_data))

        LOGGER.debug('[get_devices_endpoints] topology; returning')
        return result

    def setup_service(self, resource_value : Dict) -> None:
        service_uuid      = resource_value['service_uuid'     ]
        service_name      = resource_value['service_name'     ]
        src_device_uuid   = resource_value['src_device_uuid'  ]
        src_endpoint_uuid = resource_value['src_endpoint_uuid']
        dst_device_uuid   = resource_value['dst_device_uuid'  ]
        dst_endpoint_uuid = resource_value['dst_endpoint_uuid']
        bitrate           = resource_value['bitrate'          ]
        bidir             = resource_value['bidir'            ]
        ob_width          = resource_value['ob_width'         ]

        endpoint_ids = [
            json_endpoint_id(json_device_id(src_device_uuid), src_endpoint_uuid),
            json_endpoint_id(json_device_id(dst_device_uuid), dst_endpoint_uuid),
        ]
        constraints = [
            json_constraint_custom('bandwidth[gbps]',  str(bitrate)),
            json_constraint_custom('bidirectionality', '1' if bidir else '0'),
        ]
        if service_name == 'IP1/PORT-xe1==IP2/PORT-xe1':
            constraints.append(json_constraint_custom('optical-band-width[GHz]', str(ob_width)))

        service_add = json_service(
            service_uuid,
            ServiceTypeEnum.Name(ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY),
            context_id = json_context_id(DEFAULT_CONTEXT_NAME),
            name = service_name,
            status = ServiceStatusEnum.Name(ServiceStatusEnum.SERVICESTATUS_PLANNED),
        )
        services_url = SERVICES_URL.format(context_uuid=DEFAULT_CONTEXT_NAME)
        service_ids = self.post(services_url, body=service_add)
        assert len(service_ids) == 1
        service_id = service_ids[0]
        service_uuid = service_id['service_uuid']['uuid']

        service_upd = json_service(
            service_uuid,
            ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY,
            context_id = json_context_id(DEFAULT_CONTEXT_NAME),
            name = service_name, endpoint_ids = endpoint_ids, constraints = constraints,
            status = ServiceStatusEnum.Name(ServiceStatusEnum.SERVICESTATUS_PLANNED),
        )
        service_url = SERVICE_URL.format(context_uuid=DEFAULT_CONTEXT_NAME, service_uuid=service_uuid)
        self.put(service_url, body=service_upd)

    def teardown_service(self, resource_value : Dict) -> None:
        service_uuid = resource_value['service_uuid']
        service_name = resource_value['service_name']

        service_url = SERVICE_URL.format(context_uuid=DEFAULT_CONTEXT_NAME, service_uuid=service_uuid)
        self.delete(service_url)
        if service_name == 'IP1/PORT-xe1==IP2/PORT-xe1':
            self.delete(service_url)

    @staticmethod
    def parse_service(service : Dict) -> Tuple[str, Dict]:
        service_uuid = service['service_id']['service_uuid']['uuid']
        src_endpoint_id = service['service_endpoint_ids'][ 0]
        dst_endpoint_id = service['service_endpoint_ids'][-1]
        parsed_service = {
            'service_uuid'     : service_uuid,
            'service_name'     : service['name'],
            'src_device_uuid'  : src_endpoint_id['device_id']['device_uuid']['uuid'],
            'src_endpoint_uuid': src_endpoint_id['endpoint_uuid']['uuid'],
            'dst_device_uuid'  : dst_endpoint_id['device_id']['device_uuid']['uuid'],
            'dst_endpoint_uuid': dst_endpoint_id['endpoint_uuid']['uuid'],
        }

        for constraint in service.get('service_constraints', list()):
            if 'custom' not in constraint: continue
            constraint_type  = constraint['custom']['constraint_type']
            constraint_value = constraint['custom']['constraint_value']
            if constraint_type == 'bandwidth[gbps]':
                parsed_service['bitrate'] = int(float(constraint_value))
            if constraint_type == 'bidirectionality':
                parsed_service['bidir'] = int(constraint_value) == 1
            if constraint_type == 'optical-band-width[GHz]':
                parsed_service['ob_width'] = int(constraint_value)

        resource_key = '/services/service[{:s}]'.format(service_uuid)
        return resource_key, parsed_service

    def get_services(self) -> List[Tuple[str, Dict]]:
        services_url = SERVICES_URL.format(context_uuid=DEFAULT_CONTEXT_NAME)
        _services = self.get(services_url)
        OPTICAL_CONNECTIVITY_SERVICE_TYPES = {
            'SERVICETYPE_OPTICAL_CONNECTIVITY',
            ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY
        }
        return [
            TfsApiClient.parse_service(service)
            for service in _services['services']
            if service['service_type'] in OPTICAL_CONNECTIVITY_SERVICE_TYPES
        ]

    def get_service(self, service_uuid : str) -> Tuple[str, Dict]:
        service_url = SERVICE_URL.format(context_uuid=DEFAULT_CONTEXT_NAME, service_uuid=service_uuid)
        service = self.get(service_url)
        return TfsApiClient.parse_service(service)
