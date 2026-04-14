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

# Test program for CmConnection
import argparse
import signal
import logging
import traceback
import threading
from typing import Tuple
from cm.cm_connection import CmConnection, ConsistencyMode, ErrorFromIpm
from cm.tf_service import TFService
from cm.transport_capacity import TransportCapacity
from cm.connection import Connection
import cm.tf as tf
import asyncio
import websockets
import ssl
import time

logging.basicConfig(level=logging.WARNING)

parser = argparse.ArgumentParser(description='CM Connectin Test Utility')
parser.add_argument('ip', help='CM IP address or domain name')
parser.add_argument('port', help='CM port', type=int)
parser.add_argument('username', help='Username')
parser.add_argument('password', help='Password')

parser.add_argument('--monitor-errors', action='store_true')
parser.add_argument('--list-constellations', action='store_true')
parser.add_argument('--show-constellation-by-hub-name', nargs='?', type=str)
parser.add_argument('--create-connection', nargs='?', type=str, help="uuid;ifname;ifname;capacity")
parser.add_argument('--modify-connection', nargs='?', type=str, help="href;uuid;ifname;ifname;capacity")
parser.add_argument('--show-connection-by-name', nargs='?', type=str)
parser.add_argument('--list-connections', action='store_true')
parser.add_argument('--delete-connection', nargs='?', type=str, help="connection id, e.g. \"/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03\"")
parser.add_argument('--list-transport-capacities', action='store_true')
parser.add_argument('--create-transport-capacity', nargs='?', type=str, help="uuid;ifname;ifname;capacity")
parser.add_argument('--emulate-tf-set-config-service', nargs='?', type=str, help="hubmodule;uuid;ifname;ifname;capacity or hubmodule;uuid;ifname;ifname;capacity;FORCE-VTI-ON")
parser.add_argument('--consistency-mode', nargs='?', type=str, help="asynchronous|synchronous|lifecycle;RETRY_INTERVAL_FLOAT_AS_S")
parser.add_argument('--timeout', help='REST call timeout in seconds (per request and total for consistency validation)', type=int, default=60)

args = parser.parse_args()

def cli_create_string_to_tf_service(cli_create_str: str) -> TFService:
    sargs = cli_create_str.split(";")
    if len(sargs) == 3:
        return TFService(*sargs, 0)
    if len(sargs) == 4:
        sargs[-1] = int(sargs[-1])
        return TFService(*sargs)
    print("Invalid object create arguments. Expecting \"oid;ifname1;ifname2;bandwidthgbits\" or \"oid;ifname1;ifname2\", where ifname is form \"MODULE|PORT\"")
    exit(-1)

def cli_modify_string_to_tf_service(cli_create_str: str) -> Tuple[str, TFService]:
    sargs = cli_create_str.split(";")
    if len(sargs) == 4:
        return (sargs[0], TFService(*sargs[1:], 0))
    if len(sargs) == 5:
        sargs[-1] = int(sargs[-1])
        return (sargs[0], TFService(*sargs[1:]))
    print("Invalid object create arguments. Expecting \"href;oid;ifname1;ifname2;bandwidthgbits\" or \"href;oid;ifname1;ifname2\", where ifname is form \"MODULE|PORT\"")
    exit(-1)

if args.consistency_mode:
    ca = args.consistency_mode.split(";")
    if 2 != len(ca):
        print("Invalid consistency mode specification. Expecting \"asynchronous|synchronous|lifecycle;RETRY_INTERVAL_FLOAT_AS_S\"")
        exit(-1)
    consistency_mode = ConsistencyMode.from_str(ca[0])
    try:
        retry_interval = float(ca[1])
    except ValueError:
        print("Invalid consistency mode retry interval (non-float)")
        exit(-1)
else:
    consistency_mode = ConsistencyMode.lifecycle
    retry_interval = 0.2

cm = CmConnection(args.ip, args.port, args.username, args.password, timeout=args.timeout, tls_verify=False, consistency_mode=consistency_mode, retry_interval=retry_interval)

terminate = threading.Event()
def signal_handler(sig, frame):
    cm.stop_monitoring_errors()
    terminate.set()

signal.signal(signal.SIGINT, signal_handler)

try:
    if not cm.Connect():
        exit(-1)

    if args.list_constellations:
        constellations = cm.list_constellations()
        for constellation in constellations:
            print("Constellation:", constellation.constellation_id)
            for if_name in constellation.ifnames():
                print(f"    {if_name}")

    if args.show_constellation_by_hub_name:
        constellation = cm.get_constellation_by_hub_name(args.show_constellation_by_hub_name)
        if constellation:
            print(f"Constellation: {constellation.constellation_id},  traffic-mode: {constellation.traffic_mode}")
            for if_name in constellation.ifnames():
                print(f"    {if_name}")

    if args.create_connection:
        tf_service = cli_create_string_to_tf_service(args.create_connection)
        connection = Connection(from_tf_service=tf_service)
        try:
            created_service = cm.create_connection(connection)
            if created_service:
                print(f"Created {created_service} for {connection}")
            else:
                print(f"Failed to create {connection}")
        except ErrorFromIpm as ipm_err:
            print(f"Failed to create {connection}: {str(ipm_err)}")

    if args.modify_connection:
        href, tf_service = cli_modify_string_to_tf_service(args.modify_connection)
        mc_args = args.modify_connection.split(";")
        connection = Connection(from_tf_service=tf_service)
        result = cm.update_connection(href, connection)
        if result:
            print(f"Updated {href} for {connection}")
        else:
            print(f"Failed to update {href} for {connection}")

    if args.show_connection_by_name:
        connection = cm.get_connection_by_name(args.show_connection_by_name)
        if connection:
            print(str(connection))

    if args.list_connections:
        connections = cm.get_connections()
        for c in connections:
            print(str(c))

    if args.delete_connection:
        was_deleted = cm.delete_connection(args.delete_connection)
        if was_deleted:
            print(f"Successfully deleted {args.delete_connection}")
        else:
            print(f"Failed to delete {args.delete_connection}")

    if args.list_transport_capacities:
        tcs = cm.get_transport_capacities()
        for tc in tcs:
            print(str(tc))

    if args.create_transport_capacity:
        tf_service = cli_create_string_to_tf_service(args.create_transport_capacity)
        tc = TransportCapacity(from_tf_service=tf_service)
        created_service = cm.create_transport_capacity(tc)
        if created_service:
            print(f"Created {created_service} for {tc}")
        else:
            print(f"Failed to create {tc}")

    if args.emulate_tf_set_config_service:
        eargs = args.emulate_tf_set_config_service.split(";")
        if len(eargs) < 5:
            print("Mandatory tokens missing for --emulate-tf-set-config-service")
            exit(-1)

        hub_module_name, uuid, input_sip, output_sip, capacity_value  = eargs[0:5]
        capacity_value = int(capacity_value)
        config = {
            "input_sip_name": input_sip,
            "output_sip_name": output_sip,
            "capacity_value": capacity_value,
            "capacity_unit": "gigabit"
        }

        constellation = cm.get_constellation_by_hub_name(hub_module_name)

        # Allow testing some of the VTI code before we have CM that has VTI
        if len(eargs) > 5 and eargs[5] == "FORCE-VTI-ON":
            constellation.traffic_mode = "VTIMode"

        if constellation is None:
            print(f"Unable to find constellation for hub-module {hub_module_name}")
            exit(-1)
        result = tf.set_config_for_service(cm, constellation, uuid, config)
        print(f"Emulated SetConfig() for service result: {result}")
        if isinstance(result, Exception):
            traceback.print_exception(result)

    if args.monitor_errors:
        cm.print_received_errors = True
        terminate.wait()

finally:
# Delete subscriptions. It will end monitoring thread and ensure that program terminates normally
    cm.stop_monitoring_errors()
