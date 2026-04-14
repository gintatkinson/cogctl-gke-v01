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

# Convert the path defined as explicit hops with ingress and egress endpoints per device into a set of connections and
# compute the dependencies among them.
#
# Example:
# o-- int DC1 eth1 -- 10/1 CS1 1/2 -- 1/2 R2 2/1 -- a7.. OLS 60.. -- 2/1 R3 1/1 -- 1/1 CS2 10/1 -- eth1 DC2 int --o
#         APP              PKT            PKT            CTRL            PKT           PKT              APP
#
# path_hops = [
#     {'device': 'DC1-GW', 'ingress_ep': 'int', 'egress_ep': 'eth1'},
#     {'device': 'CS1-GW1', 'ingress_ep': '10/1', 'egress_ep': '1/2'},
#     {'device': 'TN-R2', 'ingress_ep': '1/2', 'egress_ep': '2/1'},
#     {'device': 'TN-OLS', 'ingress_ep': 'a7a80b23a703', 'egress_ep': '60519106029e'},
#     {'device': 'TN-R3', 'ingress_ep': '2/1', 'egress_ep': '1/1'},
#     {'device': 'CS2-GW1', 'ingress_ep': '1/1', 'egress_ep': '10/1'},
#     {'device': 'DC2-GW', 'ingress_ep': 'eth1', 'egress_ep': 'int'}
# ]
#
# connections=[
#     (UUID('7548edf7-ee7c-4adf-ac0f-c7a0c0dfba8e'), ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE, [
#             {'device': 'TN-OLS', 'ingress_ep': '833760219d0f', 'egress_ep': 'cf176771a4b9'}
#         ], []),
#     (UUID('c2e57966-5d82-4705-a5fe-44cf6487219e'), ServiceTypeEnum.SERVICETYPE_L2NM, [
#             {'device': 'CS1-GW1', 'ingress_ep': '10/1', 'egress_ep': '1/2'},
#             {'device': 'TN-R2', 'ingress_ep': '1/2', 'egress_ep': '2/1'},
#             {'device': 'TN-R3', 'ingress_ep': '2/1', 'egress_ep': '1/1'},
#             {'device': 'CS2-GW1', 'ingress_ep': '1/1', 'egress_ep': '10/1'}
#         ], [UUID('7548edf7-ee7c-4adf-ac0f-c7a0c0dfba8e')]),
#     (UUID('1e205c82-f6ea-4977-9e97-dc27ef1f4802'), ServiceTypeEnum.SERVICETYPE_L2NM, [
#             {'device': 'DC1-GW', 'ingress_ep': 'int', 'egress_ep': 'eth1'},
#             {'device': 'DC2-GW', 'ingress_ep': 'eth1', 'egress_ep': 'int'}
#         ], [UUID('c2e57966-5d82-4705-a5fe-44cf6487219e')])
# ]

import logging, queue
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import Device, ServiceTypeEnum
from common.tools.context_queries.Slice import get_uuid_from_string
from .ResourceGroups import IGNORED_DEVICE_TYPES, REMOTEDOMAIN_DEVICE_TYPES, get_resource_classification
from .ServiceTypes import get_service_type

LOGGER = logging.getLogger(__name__)

@dataclass
class ConnectionEntry:
    uuid: str = ''
    service_type : ServiceTypeEnum = ServiceTypeEnum.SERVICETYPE_UNKNOWN
    path_hops    : List[Dict] = field(default_factory=list)
    dependencies : List['ConnectionEntry'] = field(default_factory=list)

    def calculate_subservice_uuid(self, main_service_uuid: str) -> None:
        if self.uuid:
            return
        composed_string = main_service_uuid + '-'.join(
            f'{path_hop["device"]}/{path_hop["ingress_ep"]}/{path_hop["egress_ep"]}' for path_hop in self.path_hops
        )
        self.uuid = get_uuid_from_string(composed_string)

def convert_explicit_path_hops_to_connections(
    path_hops : List[Dict], device_dict : Dict[str, Tuple[Dict, Device]],
    main_service_uuid : str, main_service_type : ServiceTypeEnum
) -> List[Tuple[str, int, List[Dict], List[str]]]:

    LOGGER.debug('path_hops={:s}'.format(str(path_hops)))

    connection_stack = queue.LifoQueue()
    connections : List[ConnectionEntry] = list()
    prv_device_uuid = None
    prv_res_class : Tuple[Optional[int], Optional[DeviceTypeEnum], Optional[str]] = None, None, None

    for path_hop in path_hops:
        LOGGER.debug('path_hop={:s}'.format(str(path_hop)))
        device_uuid = path_hop['device']
        if prv_device_uuid == device_uuid: continue
        device_tuple = device_dict.get(device_uuid)
        if device_tuple is None: raise Exception('Device({:s}) not found'.format(str(device_uuid)))
        _,grpc_device = device_tuple

        res_class = get_resource_classification(grpc_device, device_dict)
        LOGGER.debug('  prv_res_class={:s}'.format(str(prv_res_class)))
        LOGGER.debug('  res_class={:s}'.format(str(res_class)))
        if res_class[1] in IGNORED_DEVICE_TYPES:
            LOGGER.debug('  ignored')
            continue

        if res_class[1] in REMOTEDOMAIN_DEVICE_TYPES:
            LOGGER.debug('  create and terminate underlying connection')

            # create underlying connection
            prv_service_type = connection_stack.queue[-1].service_type
            service_type = get_service_type(res_class[1], prv_service_type)
            connection_entry = ConnectionEntry(service_type=service_type, path_hops=[path_hop])
            connection_stack.put(connection_entry)

            # underlying connection ended
            connection: ConnectionEntry = connection_stack.get()
            connections.append(connection)
            connection_stack.queue[-1].dependencies.append(connection)
        elif prv_res_class[2] is None and res_class[2] is not None:
            # entering domain of a device controller, create underlying connection
            LOGGER.debug('  entering domain of a device controller, create underlying connection')

            if len(connection_stack.queue) == 0:
                LOGGER.debug('  synthetic path ingress')
                connection_entry = ConnectionEntry(
                    uuid=main_service_uuid, service_type=main_service_type, path_hops=[]
                )
                connection_stack.put(connection_entry)
            
            prv_service_type = connection_stack.queue[-1].service_type
            service_type = get_service_type(res_class[1], prv_service_type)
            connection_entry = ConnectionEntry(service_type=service_type, path_hops=[path_hop])
            connection_stack.put(connection_entry)
        elif prv_res_class[2] is not None and res_class[2] is None:
            # leaving domain of a device controller, terminate underlying connection
            LOGGER.debug('  leaving domain of a device controller, terminate underlying connection')
            connection = connection_stack.get()
            connections.append(connection)

            connection_stack.queue[-1].dependencies.append(connection)
            connection_stack.queue[-1].path_hops.append(path_hop)
        elif prv_res_class[2] is not None and res_class[2] is not None:
            if prv_res_class[2] == res_class[2]:
                # stay in domain of a device controller, connection continues
                LOGGER.debug('  stay in domain of a device controller, connection continues')
                connection_stack.queue[-1].path_hops.append(path_hop)
            else:
                # switching to different device controller, chain connections
                LOGGER.debug('  switching to different device controller, chain connections')
                connection = connection_stack.get()
                connections.append(connection)
                connection_stack.queue[-1].dependencies.append(connection)

                prv_service_type = connection_stack.queue[-1].service_type
                service_type = get_service_type(res_class[1], prv_service_type)
                connection_entry = ConnectionEntry(service_type=service_type, path_hops=[path_hop])
                connection_stack.put(connection_entry)
        elif prv_res_class[0] is None:
            # path ingress
            LOGGER.debug('  path ingress')
            connection_entry = ConnectionEntry(uuid=main_service_uuid, service_type=main_service_type, path_hops=[path_hop])
            connection_stack.put(connection_entry)
        elif prv_res_class[0] > res_class[0]:
            # create underlying connection
            LOGGER.debug('  create underlying connection')
            prv_service_type = connection_stack.queue[-1].service_type
            service_type = get_service_type(res_class[1], prv_service_type)
            connection_entry = ConnectionEntry(service_type=service_type, path_hops=[path_hop])
            connection_stack.put(connection_entry)
        elif prv_res_class[0] == res_class[0]:
            # same resource group kind
            LOGGER.debug('  same resource group kind')
            if prv_res_class[1] == res_class[1] and prv_res_class[2] == res_class[2]:
                # same device type and device controller: connection continues
                LOGGER.debug('  connection continues')
                connection_stack.queue[-1].path_hops.append(path_hop)
            else:
                # different device type or device controller: chain connections
                LOGGER.debug('  chain connections')
                connection = connection_stack.get()
                connections.append(connection)
                connection_stack.queue[-1].dependencies.append(connection)

                prv_service_type = connection_stack.queue[-1].service_type
                service_type = get_service_type(res_class[1], prv_service_type)
                connection_entry = ConnectionEntry(service_type=service_type, path_hops=[path_hop])
                connection_stack.put(connection_entry)
        elif prv_res_class[0] < res_class[0]:
            # underlying connection ended
            LOGGER.debug('  underlying connection ended')
            connection = connection_stack.get()
            connections.append(connection)
            connection_stack.queue[-1].dependencies.append(connection)
            connection_stack.queue[-1].path_hops.append(path_hop)
        else:
            raise Exception('Uncontrolled condition')

        prv_device_uuid = device_uuid
        prv_res_class = res_class


    while len(connection_stack.queue) > 1:
        LOGGER.debug('  synthetic path egress')
        connection = connection_stack.get()
        connections.append(connection)
        connection_stack.queue[-1].dependencies.append(connection)

    # path egress
    LOGGER.debug('  path egress')
    connections.append(connection_stack.get())
    LOGGER.debug('connections={:s}'.format(str(connections)))
    assert connection_stack.empty()
    for c in connections:
        c.calculate_subservice_uuid(main_service_uuid)
    return [(c.uuid, c.service_type, c.path_hops, [cd.uuid for cd in c.dependencies]) for c in connections]

def convert_explicit_path_hops_to_plain_connection(
    path_hops : List[Dict], main_service_uuid : str, main_service_type : ServiceTypeEnum
) -> List[Tuple[str, int, List[str], List[str]]]:

    connection : Tuple[str, int, List[str], List[str]] = \
        (main_service_uuid, main_service_type, [], [])

    prv_device_uuid = None
    for path_hop in path_hops:
        device_uuid = path_hop['device']
        if prv_device_uuid == device_uuid: continue
        connection[2].append(path_hop)
        prv_device_uuid = device_uuid

    return [connection]
