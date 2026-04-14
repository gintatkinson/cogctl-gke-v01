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

import asyncio
import logging
import os
import signal
import time
from sys import stdout

import grpc
import numpy as np

from common.proto.context_pb2 import ContextId, Empty, ServiceTypeEnum
from common.proto.context_pb2_grpc import ContextServiceStub
from common.proto.l3_centralizedattackdetector_pb2 import (
    ConnectionMetadata,
    Feature,
    L3CentralizedattackdetectorBatchInput,
    L3CentralizedattackdetectorMetrics,
)
from common.proto.l3_centralizedattackdetector_pb2_grpc import L3CentralizedattackdetectorStub

# Setup LOGGER
LOGGER = logging.getLogger("dad_LOGGER")
LOGGER.setLevel(logging.INFO)
logFormatter = logging.Formatter(fmt="%(levelname)-8s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
LOGGER.addHandler(consoleHandler)

# Define constants
TSTAT_DIR_NAME = "piped/"
CONTROLLER_IP = "192.168.165.78"  # Change this to the IP of the controller
CONTEXT_ID = "admin"  # Change this to the context ID to be used
CONTEXT_CHANNEL = f"{CONTROLLER_IP}:1010"
CENTRALIZED_ATTACK_DETECTOR = f"{CONTROLLER_IP}:10001"
JSON_BLANK = {
    "ip_o": "",  # Client IP
    "port_o": "",  # Client port
    "ip_d": "",  # Server ip
    "port_d": "",  # Server port
    "flow_id": "",  # Identifier: c_ip,c_port, s_ip,s_port, time_start
    "protocol": "",  # Connection protocol
    "time_start": 0.0,  # Start of connection
    "time_end": 0.0,  # Time of last packet
}
STOP = False
IGNORE_FIRST_LINE_TSTAT = True
PROFILING = False
SEND_DATA_IN_BATCHES = False
BATCH_SIZE = 10


class l3_distributedattackdetector:
    def __init__(self):
        """
        Initializes a Distributed Attack Detector.

        This method initializes a Distributed Attack Detector by setting up instance variables, connecting to the Centralized Attack Detector, obtaining feature IDs, and starting the process traffic loop. It also sets up a signal handler for handling keyboard interrupts.

        Args:
            None.

        Returns:
            None.
        """
    
        LOGGER.info("Creating Distributed Attack Detector")

        self.feature_ids = []

        self.cad_features = {}
        self.conn_id = ()

        self.connections_dict = {}  # Dictionary for storing all connections data
        self.new_connections = {}  # Dictionary for storing new connections data

        self.known_attack_ips = self.read_kwnown_attack_ips()

        signal.signal(signal.SIGINT, self.handler)

        with grpc.insecure_channel(CENTRALIZED_ATTACK_DETECTOR) as channel:
            self.cad = L3CentralizedattackdetectorStub(channel)
            LOGGER.info("Connected to the Centralized Attack Detector")

            LOGGER.info("Obtaining features Ids. from the Centralized Attack Detector...")
            self.feature_ids = self.get_features_ids()
            LOGGER.info("Features Ids.: {:s}".format(str(self.feature_ids)))

            asyncio.run(self.process_traffic())
    
    def read_kwnown_attack_ips(self):
        """
        Reads a list of known attack IPs from a CSV file.

        This method reads a list of known attack IPs from a CSV file named "known_attack_ips.csv". The method returns a list of strings containing the IP addresses.

        Args:
            None.

        Returns:
            List[str]: A list of strings containing the IP addresses of known attack sources.
        """
        
        # Initialize an empty list to store the known attack IPs
        known_attack_ips = []

        # Open the known attack IPs CSV file
        with open("known_attack_ips.csv", "r") as f:
            # Read the contents of the file and split it into a list of strings
            known_attack_ips = f.read().split(",")

        # Return the list of known attack IPs
        return known_attack_ips
        
    def handler(self):
        """
        Handles a keyboard interrupt signal.

        This method handles a keyboard interrupt signal by setting the `STOP` flag to `True` and logging a message indicating that the program is stopping gracefully.

        Args:
            None.

        Returns:
            None.
        """
        
        # Set the STOP flag to True
        if STOP:
            exit()
        STOP = True

        # Log a message indicating that the program is stopping gracefully
        LOGGER.info("Gracefully stopping...")

    def follow(self, logfile, time_sleep):
        """
        Generator function that yields new lines in a log file.

        This method reads a file object and yields new lines as they are added to the file. The method uses an infinite loop to continuously read the last line of the file. If the file hasn't been updated, the method sleeps for the specified `time_sleep` interval. If the last line of the file doesn't end with a newline character, the method appends the line to a `chunk` variable. When a newline character is encountered, the method yields the line, possibly appending the `chunk` variable to the line if it contains a partial line. The method returns an iterator that yields lines from the file.

        Args:
            file (TextIO): The file object to read from.
            time_sleep (float): The time to sleep if the file hasn't been updated.

        Yields:
            str: The next line in the file.

        Returns:
            None.
        """

        # seek the end of the file
        # logfile.seek(0, os.SEEK_END)

        chunk = ""

        # start an infinite loop
        while True:
            # read last line of the file
            line = logfile.readline()

            # sleep if the file hasn't been updated
            if not line:
                time.sleep(time_sleep)
                continue

            if line[-1] != "\n":
                chunk += line
            else:
                if chunk != "":
                    line = chunk + line
                    chunk = ""

                yield line

    def load_file(self, dirname=TSTAT_DIR_NAME):
        """
        Loads the latest Tstat log file.

        This method loads the latest Tstat log file by searching for the most recent directory in the specified `dirname` directory. If a directory is found, the method returns the path to the `log_tcp_temp_complete` file in that directory. If no directory is found, the method logs a message and waits for 5 seconds before trying again.

        Args:
            dirname (str): The name of the directory to search for Tstat log files. Defaults to `TSTAT_DIR_NAME`.

        Returns:
            str: The path to the latest Tstat log file.
        """
        
        while True:
            # Get the path to the Tstat directory
            here = os.path.dirname(os.path.abspath(__file__))
            tstat_piped = os.path.join(here, dirname)

            # Get a list of all directories in the Tstat directory
            tstat_dirs = os.listdir(tstat_piped)

            # If there are directories in the Tstat directory, find the most recent one and return the path to the log file
            if len(tstat_dirs) > 0:
                tstat_dirs.sort()
                new_dir = tstat_dirs[-1]
                tstat_file = tstat_piped + new_dir + "/log_tcp_temp_complete"

                LOGGER.info("Following: {:s}".format(str(tstat_file)))

                return tstat_file
            # If there are no directories in the Tstat directory, log a message and wait for 5 seconds before trying again
            else:
                LOGGER.info("No Tstat directory found. Waiting...")
                time.sleep(5)

    def process_line(self, line):
        """
        Processes a single line of input data and returns a list of feature values.

        Args:
            line (str): A single line of input data containing feature values separated by spaces.

        Returns:
            List[float]: A list of feature values extracted from the input line.

        Raises:
            IndexError: If the input line does not contain enough feature values.
        """
        
        line = line.split(" ")

        try:
            values = []
            for feature_id in self.feature_ids:
                feature_id = int(feature_id)
                feature = feature_id - 1
                values.append(float(line[feature]))
        except IndexError:
            LOGGER.error("IndexError: {0}".format(line))

        return values

    def get_services(self, context_id_str):
        """
        Gets the services for a given context ID.

        This method gets the services for a given context ID by calling the ListServices method of the ContextService gRPC stub.

        Args:
            context_id_str (str): The context ID to get services for.

        Returns:
            ListServicesResponse: A response object containing the services.
        """
        
        with grpc.insecure_channel(CONTEXT_CHANNEL) as channel:
            stub = ContextServiceStub(channel)
            context_id = ContextId()
            context_id.context_uuid.uuid = context_id_str

            return stub.ListServices(context_id)

    def get_service_id(self, context_id):
        """
        Gets the service ID for a given context ID.

        This method gets the service ID for a given context ID by calling the get_services method and searching for the first service in the list with the service type of SERVICETYPE_L3NM.

        Args:
            context_id (str): The context ID to get the service ID for.

        Returns:
            str: The service ID.
        """
    
        service_list = self.get_services(context_id)
        service_id = None

        for s in service_list.services:
            if s.service_type == ServiceTypeEnum.SERVICETYPE_L3NM:
                service_id = s.service_id
                break
            else:
                pass

        return service_id

    def get_endpoint_id(self, context_id):
        """
        Gets the endpoint ID for a given context ID.

        This method gets the endpoint ID for a given context ID by calling the get_services method and searching for the first service in the list with the service type of SERVICETYPE_L3NM.

        Args:
            context_id (str): The context ID to get the endpoint ID for.

        Returns:
            str: The endpoint ID.
        """
    
        service_list = self.get_services(context_id)
        endpoint_id = None

        for s in service_list.services:
            if s.service_type == ServiceTypeEnum.SERVICETYPE_L3NM:
                endpoint_id = s.service_endpoint_ids[0]
                break

        return endpoint_id

    def get_features_ids(self):
        """
        Gets the feature IDs used by the Centralized Attack Detector model.

        This method gets the feature IDs used by the Centralized Attack Detector model by calling the GetFeaturesIds method of the Centralized Attack Detector gRPC stub.

        Args:
            None.

        Returns:
            list: A list of feature IDs.
        """
        
        return self.cad.GetFeaturesIds(Empty()).auto_features

    def check_types(self):
        """
        Checks the types of the features that will be sent to the Centralized Attack Detector.

        This method checks the types of the Centralized Attack Detector features to ensure that they are of the correct type. If any of the types are incorrect, the method raises an AssertionError.

        Args:
            None.

        Returns:
            None.
        """
    
        for feature in self.cad_features["features"]:
            assert isinstance(feature, float)

        assert isinstance(self.cad_features["connection_metadata"]["ip_o"], str)
        assert isinstance(self.cad_features["connection_metadata"]["port_o"], str)
        assert isinstance(self.cad_features["connection_metadata"]["ip_d"], str)
        assert isinstance(self.cad_features["connection_metadata"]["port_d"], str)
        assert isinstance(self.cad_features["connection_metadata"]["flow_id"], str)
        assert isinstance(self.cad_features["connection_metadata"]["protocol"], str)
        assert isinstance(self.cad_features["connection_metadata"]["time_start"], float)
        assert isinstance(self.cad_features["connection_metadata"]["time_end"], float)

    def insert_connection(self):
        """
        Inserts a new connection into the `connections_dict` instance variable.

        This method inserts a new connection into the `connections_dict` instance variable. The method uses the `conn_id` instance variable to create a new dictionary entry for the connection. If the connection already exists in the dictionary, the method updates the `time_end` value of the existing entry. If the connection doesn't exist in the dictionary, the method creates a new entry with the following keys:
        - "ip_o": The source IP address of the connection.
        - "port_o": The source port of the connection.
        - "ip_d": The destination IP address of the connection.
        - "port_d": The destination port of the connection.
        - "flow_id": The flow ID of the connection.
        - "service_id": The service ID of the connection.
        - "endpoint_id": The endpoint ID of the connection.
        - "protocol": The protocol of the connection.
        - "time_start": The start time of the connection.
        - "time_end": The end time of the connection.

        Args:
            None.

        Returns:
            None.
        """
        
        try:
            self.connections_dict[self.conn_id]["time_end"] = time.time()
        except KeyError:
            self.connections_dict[self.conn_id] = JSON_BLANK.copy()
            self.connections_dict[self.conn_id]["time_start"] = time.time()
            self.connections_dict[self.conn_id]["time_end"] = time.time()
            self.connections_dict[self.conn_id]["ip_o"] = self.conn_id[0]
            self.connections_dict[self.conn_id]["port_o"] = self.conn_id[1]
            self.connections_dict[self.conn_id]["flow_id"] = ":".join(self.conn_id)
            self.connections_dict[self.conn_id]["service_id"] = self.get_service_id(CONTEXT_ID)
            self.connections_dict[self.conn_id]["endpoint_id"] = self.get_endpoint_id(CONTEXT_ID)
            self.connections_dict[self.conn_id]["protocol"] = "TCP"
            self.connections_dict[self.conn_id]["ip_d"] = self.conn_id[2]
            self.connections_dict[self.conn_id]["port_d"] = self.conn_id[3]

    def check_if_connection_is_attack(self):
        """
        Checks if a connection is an attack based on known attack IP addresses.

        This method checks if a connection is an attack based on known attack IP addresses. The method uses the `conn_id` and `known_attack_ips` instance variables to determine if the source or destination IP address of the connection is in the list of known attack IP addresses. If either IP address is in the list, the method logs a message indicating that an attack has been detected.

        Args:
            None.

        Returns:
            None.
        """
    
        if self.conn_id[0] in self.known_attack_ips or self.conn_id[2] in self.known_attack_ips:
            LOGGER.info("Attack detected. Origin IP address: {0}, destination IP address: {1}".format(self.conn_id[0], self.conn_id[2]))

    def create_cad_features(self):
        """
        Creates a dictionary of features and connection metadata for the Centralized Attack Detector.

        This method creates a dictionary of features and connection metadata for the Centralized Attack Detector. The method uses the `new_connections` and `connections_dict` instance variables to obtain the necessary data. The resulting dictionary contains the following keys:
        - "features": A list of the first 10 features of the connection.
        - "connection_metadata": A dictionary containing the following keys:
            - "ip_o": The source IP address of the connection.
            - "port_o": The source port of the connection.
            - "ip_d": The destination IP address of the connection.
            - "port_d": The destination port of the connection.
            - "flow_id": The flow ID of the connection.
            - "service_id": The service ID of the connection.
            - "endpoint_id": The endpoint ID of the connection.
            - "protocol": The protocol of the connection.
            - "time_start": The start time of the connection.
            - "time_end": The end time of the connection.

        Args:
            None.

        Returns:
            None.
        """
        
        self.cad_features = {
            "features": self.new_connections[self.conn_id][0:10],
            "connection_metadata": {
                "ip_o": self.connections_dict[self.conn_id]["ip_o"],
                "port_o": self.connections_dict[self.conn_id]["port_o"],
                "ip_d": self.connections_dict[self.conn_id]["ip_d"],
                "port_d": self.connections_dict[self.conn_id]["port_d"],
                "flow_id": self.connections_dict[self.conn_id]["flow_id"],
                "service_id": self.connections_dict[self.conn_id]["service_id"],
                "endpoint_id": self.connections_dict[self.conn_id]["endpoint_id"],
                "protocol": self.connections_dict[self.conn_id]["protocol"],
                "time_start": self.connections_dict[self.conn_id]["time_start"],
                "time_end": self.connections_dict[self.conn_id]["time_end"],
            },
        }

    async def send_batch_async(self, metrics_list_pb):
        """
        Sends a batch of traffic data to a Centralized Attack Detector.

        This method sends a batch of traffic data to a Centralized Attack Detector for analysis. The method creates a `L3CentralizedattackdetectorBatchInput` object from the provided `metrics_list_pb`, and sends the batch using an executor to run the `AnalyzeBatchConnectionStatistics` method in a separate thread. The method returns `None`.

        Args:
            metrics_list_pb (List[L3CentralizedattackdetectorMetrics]): A list of traffic metrics to send to the Centralized Attack Detector.

        Returns:
            None.
        """
        
        loop = asyncio.get_running_loop()

        # Create metrics batch
        metrics_batch = L3CentralizedattackdetectorBatchInput()
        metrics_batch.metrics.extend(metrics_list_pb)

        # Send batch
        future = loop.run_in_executor(None, self.cad.AnalyzeBatchConnectionStatistics, metrics_batch)

        try:
            await future
        except Exception as e:
            LOGGER.error(f"Error sending batch: {e}")

    async def send_data(self, metrics_list_pb, send_data_times):
        """
        Sends traffic data to a Centralized Attack Detector.

        This method sends traffic data to a Centralized Attack Detector for analysis. If the `SEND_DATA_IN_BATCHES` flag is set to `True`, the data is sent in batches of size `BATCH_SIZE`. Otherwise, the data is sent one metric at a time. The method returns the updated `metrics_list_pb` and `send_data_times` arrays.

        Args:
            metrics_list_pb (List[L3CentralizedattackdetectorMetrics]): A list of traffic metrics to send to the Centralized Attack Detector.
            send_data_times (np.ndarray): An array of times it took to send each batch of data.

        Returns:
            Tuple[List[L3CentralizedattackdetectorMetrics], np.ndarray]: A tuple containing the updated `metrics_list_pb` and `send_data_times` arrays.
        """
        
        if SEND_DATA_IN_BATCHES:
            if len(metrics_list_pb) == BATCH_SIZE:
                send_data_time_start = time.time()
                await self.send_batch_async(metrics_list_pb)
                metrics_list_pb = []

                send_data_time_end = time.time()
                send_data_time = send_data_time_end - send_data_time_start
                send_data_times = np.append(send_data_times, send_data_time)

        else:
            send_data_time_start = time.time()
            self.cad.AnalyzeConnectionStatistics(metrics_list_pb[-1])

            send_data_time_end = time.time()
            send_data_time = send_data_time_end - send_data_time_start
            send_data_times = np.append(send_data_times, send_data_time)

        return metrics_list_pb, send_data_times

    async def process_traffic(self):
        """ Processes traffic data from a Tstat log file.
        This method reads traffic data from a Tstat log file, processes each line of data, and sends the resulting metrics to a Centralized Attack Detector. It runs indefinitely until the `STOP` flag is set to `True`.

        Args:
            None.
        Returns:
            None.
        """
        
        LOGGER.info("Loading Tstat log file...")
        logfile = open(self.load_file(), "r")

        LOGGER.info("Following Tstat log file...")
        loglines = self.follow(logfile, 5)

        process_time = []
        num_lines = 0

        send_data_times = np.array([])
        metrics_list_pb = []

        LOGGER.info("Starting to process data...")

        index = 0
        while True:
            line = next(loglines, None)

            while line is None:
                LOGGER.info("Waiting for new data...")

                time.sleep(1 / 100)
                line = next(loglines, None)

            if index == 0 and IGNORE_FIRST_LINE_TSTAT:
                index = index + 1
                continue

            if STOP:
                break

            num_lines += 1
            start = time.time()
            line_id = line.split(" ")

            self.conn_id = (line_id[0], line_id[1], line_id[14], line_id[15])
            self.new_connections[self.conn_id] = self.process_line(line)

            self.check_if_connection_is_attack()
            self.insert_connection()
            self.create_cad_features()
            self.check_types()

            connection_metadata = ConnectionMetadata(**self.cad_features["connection_metadata"])
            metrics = L3CentralizedattackdetectorMetrics()

            for feature in self.cad_features["features"]:
                feature_obj = Feature()
                feature_obj.feature = feature
                metrics.features.append(feature_obj)

            metrics.connection_metadata.CopyFrom(connection_metadata)
            metrics_list_pb.append(metrics)

            metrics_list_pb, send_data_times = await self.send_data(metrics_list_pb, send_data_times)

            index += 1

            process_time.append(time.time() - start)

            if num_lines % 10 == 0:
                LOGGER.info(f"Number of lines: {num_lines} - Average processing time: {sum(process_time) / num_lines}")
