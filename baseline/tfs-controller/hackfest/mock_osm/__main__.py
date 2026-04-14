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

import cmd, logging
from .MockOSM import MockOSM

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

WIM_URL = 'http://10.0.2.10:80'
WIM_USERNAME = 'admin'
WIM_PASSWORD = 'admin'

# Ref: https://osm.etsi.org/wikipub/index.php/WIM
def create_port_mapping(device_id, port_id, service_endpoint_id, site_id):
    bearer_ref = '{:s}:{:s}'.format(device_id, port_id)
    return {
        'device-id'           : device_id,              # pop_switch_dpid
        'service_endpoint_id' : service_endpoint_id,    # wan_service_endpoint_id
        'service_mapping_info': {                       # wan_service_mapping_info, other extra info
            'bearer': {'bearer-reference': bearer_ref},
            'site-id': site_id,
        },
    }

WIM_PORT_MAPPING  = [
    create_port_mapping('R1', '1/2', 'ep-R1-1/2', '1'),
    create_port_mapping('R1', '1/3', 'ep-R1-1/3', '1'),
    create_port_mapping('R2', '1/2', 'ep-R2-1/2', '2'),
    create_port_mapping('R2', '1/3', 'ep-R2-1/3', '2'),
    create_port_mapping('R3', '1/2', 'ep-R3-1/2', '3'),
    create_port_mapping('R3', '1/3', 'ep-R3-1/3', '3'),
    create_port_mapping('R4', '1/2', 'ep-R4-1/2', '4'),
    create_port_mapping('R4', '1/3', 'ep-R4-1/3', '4'),
]

SERVICE_TYPE = 'ELINE'
SERVICE_CONNECTION_POINTS = [
    {'service_endpoint_id': 'ep-R1-1/2',
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': 1234}},
    {'service_endpoint_id': 'ep-R4-1/3',
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': 1234}},
]

class MockOSMShell(cmd.Cmd):
    intro = 'Welcome to the MockOSM shell.\nType help or ? to list commands.\n'
    prompt = '(mock-osm) '

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mock_osm = MockOSM(WIM_URL, WIM_PORT_MAPPING, WIM_USERNAME, WIM_PASSWORD)

    def do_create(self, arg):
        'Create an ELINE (L2) service'
        service_uuid = self.mock_osm.create_connectivity_service(
            SERVICE_TYPE, SERVICE_CONNECTION_POINTS)
        print('Service {:s} created'.format(service_uuid))

    def do_status(self, arg):
        'Retrieve status of services'
        service_uuids = list(self.mock_osm.conn_info.keys())
        for service_uuid in service_uuids:
            status = self.mock_osm.get_connectivity_service_status(service_uuid)
            print('Status of Service {:s} is {:s}'.format(service_uuid, str(status)))

    def do_delete(self, arg):
        'Delete all services'
        service_uuids = list(self.mock_osm.conn_info.keys())
        for service_uuid in service_uuids:
            self.mock_osm.delete_connectivity_service(service_uuid)
            print('Service {:s} deleted'.format(service_uuid))

    def do_exit(self, arg):
        'Exit MockOSM'
        print('Bye!')
        return True

if __name__ == '__main__':
    MockOSMShell().cmdloop()
