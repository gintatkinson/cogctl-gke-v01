#!/usr/bin/env python3
#pylint: disable=invalid-name, missing-function-docstring, line-too-long, logging-fstring-interpolation, missing-class-docstring, missing-module-docstring
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

# Manage L2 services (with underlying XR connectivity) without need to use unit test
# files or excessive JSON definitions
#
# Run in this directory with PYTHONPATH=../../../../
# E.g.:
#   Create multi-layer service (L2 VPN over XR):
#     PYTHONPATH=../../../../  ./service-cli.py create 1 R1-EMU 13/1/2 500 2 R3-EMU 13/1/2 500
#   Single-layer (XR without services on top of it):
#     PYTHONPATH=../../../../  ./service-cli.py create-xr FooService X1-XR-CONSTELLATION  "XR HUB 1|XR-T1" "XR LEAF 2|XR-T1"
#   List services:
#     PYTHONPATH=../../../../  ./service-cli.py list
#   List possible endpoints:
#     PYTHONPATH=../../../../  ./service-cli.py list-endpoints
#   Delete service (if multi-layer, always deleter highest layer!)
#     PYTHONPATH=../../../../  ./service-cli.py delete 43a8046a-5dec-463d-82f7-7cc3442dbf4f

import argparse
import logging
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict
from contextlib import contextmanager

from common.Settings import get_setting
from context.client.ContextClient import ContextClient
from service.client.ServiceClient import ServiceClient
from tests.tools.mock_osm.MockOSM import MockOSM
from common.proto.context_pb2 import ContextId, ServiceTypeEnum, ServiceStatusEnum, Service, Empty, ServiceId
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Topology import json_topology_id
from common.tools.object_factory.ConfigRule import json_config_rule_set

LOGGER = logging.getLogger(__name__)

WIM_USERNAME = 'admin'
WIM_PASSWORD = 'admin'

@contextmanager
def make_context_client():
    try:
        _client = ContextClient(get_setting('CONTEXTSERVICE_SERVICE_HOST'), get_setting('CONTEXTSERVICE_SERVICE_PORT_GRPC'))
        yield _client
    finally:
        _client.close()

@contextmanager
def make_service_client():
    try:
        _client = ServiceClient(get_setting('SERVICESERVICE_SERVICE_HOST'), get_setting('SERVICESERVICE_SERVICE_PORT_GRPC'))
        yield _client
    finally:
        _client.close()

def make_osm_wim():
    wim_url = 'http://{:s}:{:s}'.format(
        get_setting('NBISERVICE_SERVICE_HOST'), str(get_setting('NBISERVICE_SERVICE_PORT_HTTP')))
    return MockOSM(wim_url, WIM_MAPPING, WIM_USERNAME, WIM_PASSWORD)

@dataclass
class DevInfo:
    name: str
    uuid: str
    endpoints: Dict[str, str] = field(default_factory= dict)
    endpoints_by_uuid: Dict[str, str] = field(default_factory= dict)

    def get_endpoint_uuid_or_exit(self, ep_name: str) -> str:
        if ep_name not in self.endpoints:
            print(f"Endpoint {ep_name} does not exist in device {self.name}. See \"service-cli.py list-endpoints\"")
            exit(-1)
        return self.endpoints[ep_name]

def get_devices(cc: ContextClient) -> Dict[str, DevInfo]:
    r = cc.ListDevices(Empty())
    # print(grpc_message_to_json_string(r))

    devices = dict()
    for dev in r.devices:
        di = DevInfo(dev.name, dev.device_id.device_uuid.uuid)
        for ep in dev.device_endpoints:
            di.endpoints[ep.name] = ep.endpoint_id.endpoint_uuid.uuid
            di.endpoints_by_uuid[ep.endpoint_id.endpoint_uuid.uuid] = ep.name
        devices[dev.name] = di
    return devices

def get_endpoint_map(devices: Dict[str, DevInfo]):
    ep_map = dict()
    for dev in devices.values():
        for ep_name, ep_uuid in dev.endpoints.items():
            ep_map[ep_uuid] = (dev.name, ep_name)
    return ep_map

logging.basicConfig(level=logging.ERROR)

parser = argparse.ArgumentParser(description='TF Service Management Utility')
subparsers = parser.add_subparsers(dest="command")
subparsers.required = True

create_parser = subparsers.add_parser('create')
create_parser.add_argument('site1', type=int, help='One endpoint of the service, e.g. 1')
create_parser.add_argument('device1', type=str, help='One endpoint of the service, e.g. R1-EMU')
create_parser.add_argument('interface1', type=str, help='One endpoint of the service, e.g. 13/1/2')
create_parser.add_argument('vlan1', type=int, help='VLAN in first endpoint, e.g. 500')

create_parser.add_argument('site2', type=int, help='One endpoint of the service, e.g. 2')
create_parser.add_argument('device2', type=str, help='One endpoint of the service, e.g. R3-EMU')
create_parser.add_argument('interface2', type=str, help='One endpoint of the service, e.g. 13/1/2')
create_parser.add_argument('vlan2', type=int, help='VLAN in first endpoint, e.g. 500')

delete_parser = subparsers.add_parser('delete')
delete_parser.add_argument('service_uuid', type=str, help='UUID of the service to be deleted')

list_parser = subparsers.add_parser('list')
list_parser = subparsers.add_parser('list-endpoints')

create_xr_parser = subparsers.add_parser('create-xr')
create_xr_parser.add_argument('service_name', type=str, help='Service Name')
create_xr_parser.add_argument('constellation', type=str, help='XR Constellation')
create_xr_parser.add_argument('interface1', type=str, help='One endpoint of the service')
create_xr_parser.add_argument('interface2', type=str, help='Second endpoint of the service')

args = parser.parse_args()

WIM_SERVICE_TYPE = 'ELINE'
CONTEXT_ID = {'context_uuid': {'uuid': 'admin'}}

if args.command == "create":
    endpoint1 = f"{args.device1}:{args.interface1}"
    endpoint2 = f"{args.device2}:{args.interface2}"

    WIM_MAPPING  = [
        {'device-id': args.device1, 'service_endpoint_id': endpoint1,
        'service_mapping_info': {'bearer': {'bearer-reference': endpoint1}, 'site-id': args.site1}},
        {'device-id': args.device2, 'service_endpoint_id': endpoint2,
        'service_mapping_info': {'bearer': {'bearer-reference': endpoint2}, 'site-id': args.site2}},
    ]
    WIM_SERVICE_CONNECTION_POINTS = [
        {'service_endpoint_id': endpoint1,
            'service_endpoint_encapsulation_type': 'dot1q',
            'service_endpoint_encapsulation_info': {'vlan': args.vlan1}},
        {'service_endpoint_id': endpoint2,
            'service_endpoint_encapsulation_type': 'dot1q',
            'service_endpoint_encapsulation_info': {'vlan': args.vlan2}},
    ]
else:
    WIM_MAPPING = []
    WIM_SERVICE_CONNECTION_POINTS = []

#print(str(args))
#print(f"=== WIM_SERVICE_TYPE: {WIM_SERVICE_TYPE}")
#print(f"=== WIM_SERVICE_CONNECTION_POINTS: {WIM_SERVICE_CONNECTION_POINTS}")
#print(f"=== WIM_MAPPING: {WIM_MAPPING}")

with make_context_client() as client:
    # We only permit one context on our demos/testing
    response = client.ListContextIds(Empty())
    assert len(response.context_ids) == 1
    context_uuid=json_context_id(response.context_ids[0].context_uuid.uuid)

    osm_wim = make_osm_wim()

    if args.command == "create":
        service_uuid = osm_wim.create_connectivity_service(WIM_SERVICE_TYPE, WIM_SERVICE_CONNECTION_POINTS)
        print(f"*** Create connectivity service --> {service_uuid}")
        status = osm_wim.get_connectivity_service_status(service_uuid)
        print(f"*** Get created service status --> {str(status)}")

    elif args.command == "delete":
        service_id = {
            "context_id": context_uuid,
            "service_uuid": {
                "uuid": args.service_uuid
            }
        }

        try:
            response = client.GetService(ServiceId(**service_id))
            #print(grpc_message_to_json_string(response))

            high_level_delete = response.service_type == ServiceTypeEnum.SERVICETYPE_L2NM or response.service_type == ServiceTypeEnum.SERVICETYPE_L3NM
            print(f"Deleting service {response.name}, type {ServiceTypeEnum.Name(response.service_type)}, {high_level_delete=}")

        except:
            print(f"No service with uuid {args.service_uuid} ({service_id})")
            exit(-1)

        if high_level_delete:
            osm_wim.wim.check_credentials()
            try:
                osm_wim.wim.delete_connectivity_service(args.service_uuid)
                print(f"*** Service {args.service_uuid} deleted (L2SM/L3SM layer)")
            except Exception as e:
                print(f"*** Failed to delete service {args.service_uuid}, {e}")
        else:
            with make_service_client() as service_client:
                try:
                    service_client.DeleteService(ServiceId(**service_id))
                    print(f"*** Service {args.service_uuid} deleted (low level)")
                except Exception as e:
                    print(f"*** Failed to delete service {args.service_uuid}, {e}")

    elif args.command == "create-xr":
        CONTEXT_NAME = 'admin'
        CONTEXT_ID   = json_context_id(CONTEXT_NAME)
        CONTEXT      = json_context(CONTEXT_NAME, name=CONTEXT_NAME)

        json_tapi_settings = {
            'capacity_value'  : 50.0,
            'capacity_unit'   : 'GHz',
            'layer_proto_name': 'PHOTONIC_MEDIA',
            'layer_proto_qual': 'tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC',
            'direction'       : 'UNIDIRECTIONAL',
        }
        config_rule = json_config_rule_set('/settings', json_tapi_settings)

        devices = get_devices(client)
        if args.constellation not in devices:
            print(f"Constellation {args.constellation} does not exist as a device. See \"service-cli.py list-endpoints\"")
            exit(-1)
        else:
            dev_info = devices[args.constellation]
            constellation_uuid = dev_info.uuid

        interface1_uuid = dev_info.get_endpoint_uuid_or_exit(args.interface1)
        interface2_uuid = dev_info.get_endpoint_uuid_or_exit(args.interface2)

        print(f"Constellation {args.constellation:40}: {constellation_uuid:36}")
        print(f"Interface 1   {args.interface1:40}: {interface1_uuid:36}")
        print(f"Interface 2   {args.interface2:40}: {interface2_uuid:36}")

        service_request = {
            "name": args.service_name,
            "service_id": {
                 "context_id": {"context_uuid": {"uuid": response.context_ids[0].context_uuid.uuid}},
                 "service_uuid": {"uuid": args.service_name}
            },
            'service_type'        : ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE,
            "service_endpoint_ids": [
                {'device_id': {'device_uuid': {'uuid': constellation_uuid}}, 'endpoint_uuid': {'uuid': interface1_uuid}, 'topology_id': json_topology_id("admin", context_id=context_uuid)},
                {'device_id': {'device_uuid': {'uuid': constellation_uuid}}, 'endpoint_uuid': {'uuid': interface2_uuid}, 'topology_id': json_topology_id("admin", context_id=context_uuid)}
            ],
            'service_status'      : {'service_status': ServiceStatusEnum.SERVICESTATUS_PLANNED},
            'service_constraints' : [],
        }

        with make_service_client() as service_client:
            sr = deepcopy(service_request)
            endpoints, sr['service_endpoint_ids'] = sr['service_endpoint_ids'], []
            create_response = service_client.CreateService(Service(**sr))
            print(f'CreateService: {grpc_message_to_json_string(create_response)}')

            sr['service_endpoint_ids'] = endpoints
            #sr['service_id']['service_uuid'] = create_response
            sr['service_config'] = {'config_rules': [config_rule]}

            update_response = service_client.UpdateService(Service(**sr))
            print(f'UpdateService: {grpc_message_to_json_string(update_response)}')

    elif args.command == "list":
        devices = get_devices(client)
        ep_map = get_endpoint_map(devices)

        response = client.ListServices(ContextId(**CONTEXT_ID))

        # print('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
        for service in response.services:
            scs = ""

            ep_list = []
            for ep in service.service_endpoint_ids:
                ep_uuid = ep.endpoint_uuid.uuid
                if ep_uuid in ep_map:
                    dev_name, ep_name = ep_map[ep_uuid]
                    ep_list.append(f"{dev_name}:{ep_name}")
            ep_list.sort()
            eps = ", ".join(ep_list)

            #print(f"{service.service_id.service_uuid.uuid:36}  {ServiceTypeEnum.Name(service.service_type):40}  {service.name:40}  {ServiceStatusEnum.Name(service.service_status.service_status)}  {scs}")
            print(f"{service.service_id.service_uuid.uuid:36}  {ServiceTypeEnum.Name(service.service_type):40}  {service.name:40}  {ServiceStatusEnum.Name(service.service_status.service_status):28}  {eps}")

    elif args.command == "list-endpoints":
        devices = get_devices(client)
        for name in sorted(devices.keys()):
            dev = devices[name]
            print(f"{name:40}    {dev.uuid:36}")
            for ep_name in sorted(dev.endpoints.keys()):
                print(f"    {ep_name:40}    {dev.endpoints[ep_name]:36}")
