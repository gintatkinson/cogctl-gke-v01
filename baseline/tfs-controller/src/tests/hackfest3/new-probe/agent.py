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

#import copy, logging, pytest
#from common.tests.EventTools import EVENT_CREATE, EVENT_UPDATE, check_events
#from common.tools.object_factory.Context import json_context_id
#from common.tools.object_factory.Device import json_device_id
#from common.tools.object_factory.Service import json_service_id
#from common.tools.object_factory.Link import json_link_id
#from common.tools.object_factory.Topology import json_topology_id
#from context.client.EventsCollector import EventsCollector
#from common.proto.context_pb2 import Context, ContextId, Device, Empty, Link, Topology, Service, ServiceId
#from monitoring.client.MonitoringClient import MonitoringClient
#from common.proto.context_pb2 import ConfigActionEnum, Device, DeviceId, DeviceOperationalStatusEnum

import os, threading, time, socket
from common.Settings import get_setting
from common.proto.context_pb2 import Empty, Timestamp
from common.proto.monitoring_pb2 import KpiDescriptor, Kpi, KpiId, KpiValue
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from monitoring.client.MonitoringClient import MonitoringClient
from context.client.ContextClient import ContextClient

# ----- If you want to use .env file
#from dotenv import load_dotenv
#load_dotenv()
#def get_setting(key):
#    return os.getenv(key)


#### gRPC Clients
monitoring_client = MonitoringClient(get_setting('MONITORINGSERVICE_SERVICE_HOST'), get_setting('MONITORINGSERVICE_SERVICE_PORT_GRPC'))
context_client = ContextClient(get_setting('CONTEXTSERVICE_SERVICE_HOST'), get_setting('CONTEXTSERVICE_SERVICE_PORT_GRPC'))

### Locks and common variables
# Lock for kpi_id
kpi_id_lock = threading.Lock()
kpi_id = KpiId()
# Lock to know if we have registered a KPI or not
enabled_lock = threading.Lock()
enabled = False

### Define the path to the Unix socket
socket_path = "/home/teraflow/ngsdn-tutorial/tmp/sock"
if os.path.exists(socket_path):
    os.remove(socket_path)

def thread_context_func():
    global kpi_id
    global enabled
    while True:
##########################################################
################## YOUR INPUT HERE #######################
##########################################################
        # Listen for Context Service Events
        # Differentiate based on event type
        # if event_type == service created:
            # Create KpiDescriptor
            # Register Kpi and keep kpi_id
        # if event_type == service removed:
            # stop sending values
##########################################################
##################### UNTIL HERE #########################
##########################################################

def thread_kpi_func():
    global kpi_id
    global enabled
    try:
        # Create socket object
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # Bind the socket to the socket path
        server_socket.bind(socket_path)
        # Listen for incoming connections
        server_socket.listen(1)
        while True:
            print("Awaiting for new connection!")
            # Accept incoming connection
            connection, client_address = server_socket.accept()
            # Read data from the connection
            data = connection.recv(1024)
            if data:
                with enabled_lock:
                    if enabled: 
##########################################################
################## YOUR INPUT HERE #######################
##########################################################
                        # if we have registered a KPI
                        #store value to data
                        data = data.decode()
                        print(f"Received: {data}")
                        with kpi_id_lock:
                            # create Kpi
                            # send Kpi to Monitoring
##########################################################
##################### UNTIL HERE #########################
##########################################################
            # Close the connection 
            connection.close()
    except Exception as e:
        print(f"Error: {str(e)}")


def main():

    # Start Thread that listens to context events
    thread_context = threading.Thread(target=thread_context_func)
    thread_context.daemon = True
    thread_context.start()

    # Start Thread that listens to socket
    thread_kpi = threading.Thread(target=thread_kpi_func)
    thread_kpi.daemon = True
    thread_kpi.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        os.remove(socket_path)
        print("Script terminated.")

if __name__ == "__main__":
    main()
