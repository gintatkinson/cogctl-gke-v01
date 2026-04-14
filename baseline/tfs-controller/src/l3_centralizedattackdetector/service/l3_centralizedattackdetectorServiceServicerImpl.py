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

from __future__ import print_function

import csv
import grpc
import logging
import numpy as np
import onnxruntime as rt
import os
import time
import uuid

from datetime import datetime, timedelta
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import Empty, Timestamp
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.l3_attackmitigator_pb2 import L3AttackmitigatorOutput
from common.proto.l3_centralizedattackdetector_pb2 import AttackIPs, AutoFeatures, L3CentralizedattackdetectorMetrics, L3CentralizedattackdetectorBatchInput, StatusMessage
from common.proto.l3_centralizedattackdetector_pb2_grpc import L3CentralizedattackdetectorServicer
from common.proto.monitoring_pb2 import Kpi, KpiDescriptor
from common.tools.timestamp.Converters import timestamp_utcnow_to_float
from l3_attackmitigator.client.l3_attackmitigatorClient import l3_attackmitigatorClient
from monitoring.client.MonitoringClient import MonitoringClient


LOGGER = logging.getLogger(__name__)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Environment variables
TEST_ML_MODEL = True if int(os.getenv("TEST_ML_MODEL", 0)) == 1 else False
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
METRICS_POOL = MetricsPool("l3_centralizedattackdetector", "RPC")


class ConnectionInfo:
    def __init__(self, ip_o, port_o, ip_d, port_d):
        self.ip_o = ip_o
        self.port_o = port_o
        self.ip_d = ip_d
        self.port_d = port_d

    def __eq__(self, other):
        return (
            self.ip_o == other.ip_o
            and self.port_o == other.port_o
            and self.ip_d == other.ip_d
            and self.port_d == other.port_d
        )

    def __str__(self):
        return f"ip_o: {self.ip_o}\nport_o: {self.port_o}\nip_d: {self.ip_d}\nport_d: {self.port_d}"


class l3_centralizedattackdetectorServiceServicerImpl(L3CentralizedattackdetectorServicer):
    def __init__(self):
        """
        Initializes the Centralized Attack Detector service.

        Args:
            None

        Returns:
            None
        """

        LOGGER.info("Creating Centralized Attack Detector Service")

        self.inference_values = []
        self.inference_results = []
        self.cryptomining_detector_path = os.path.join(current_dir, "ml_model/cryptomining_detector/")
        self.cryptomining_detector_file_name = os.listdir(self.cryptomining_detector_path)[0]
        self.cryptomining_detector_model_path = os.path.join(
            self.cryptomining_detector_path, self.cryptomining_detector_file_name
        )
        self.cryptomining_detector_model = rt.InferenceSession(self.cryptomining_detector_model_path)

        # Load cryptomining attack detector features metadata from ONNX file
        self.cryptomining_detector_features_metadata = list(
            self.cryptomining_detector_model.get_modelmeta().custom_metadata_map.values()
        )
        self.cryptomining_detector_features_metadata = [float(x) for x in self.cryptomining_detector_features_metadata]
        self.cryptomining_detector_features_metadata.sort()

        LOGGER.info(f"Cryptomining Attack Detector Features: {self.cryptomining_detector_features_metadata}")
        LOGGER.info(f"Batch size: {BATCH_SIZE}")

        self.input_name = self.cryptomining_detector_model.get_inputs()[0].name
        self.label_name = self.cryptomining_detector_model.get_outputs()[0].name
        self.prob_name = self.cryptomining_detector_model.get_outputs()[1].name

        # KPI values
        self.l3_security_status = 0
        self.l3_ml_model_confidence = 0
        self.l3_inferences_in_interval_counter = 0

        self.l3_ml_model_confidence_normal = 0
        self.l3_inferences_in_interval_counter_normal = 0

        self.l3_ml_model_confidence_crypto = 0
        self.l3_inferences_in_interval_counter_crypto = 0

        self.l3_attacks = []
        self.l3_unique_attack_conns = 0
        self.l3_unique_compromised_clients = 0
        self.l3_unique_attackers = 0

        self.l3_non_empty_time_interval = False

        self.active_requests = []

        self.monitoring_client = MonitoringClient()
        self.service_ids = []
        self.monitored_kpis = {
            "l3_security_status": {
                "kpi_id": None,
                "description": "L3 - Confidence of the cryptomining attack detector in the security status in the last time interval of the service {service_id}",
                "kpi_sample_type": KpiSampleType.KPISAMPLETYPE_L3_SECURITY_STATUS_CRYPTO,
                "service_ids": [],
            },
            "l3_ml_model_confidence": {
                "kpi_id": None,
                "description": "L3 - Security status of the service in a time interval of the service {service_id} (“0” if no attack has been detected on the service and “1” if a cryptomining attack has been detected)",
                "kpi_sample_type": KpiSampleType.KPISAMPLETYPE_ML_CONFIDENCE,
                "service_ids": [],
            },
            "l3_unique_attack_conns": {
                "kpi_id": None,
                "description": "L3 - Number of attack connections detected in a time interval of the service {service_id} (attacks of the same connection [origin IP, origin port, destination IP and destination port] are only considered once)",
                "kpi_sample_type": KpiSampleType.KPISAMPLETYPE_L3_UNIQUE_ATTACK_CONNS,
                "service_ids": [],
            },
            "l3_unique_compromised_clients": {
                "kpi_id": None,
                "description": "L3 - Number of unique compromised clients of the service in a time interval of the service {service_id} (attacks from the same origin IP are only considered once)",
                "kpi_sample_type": KpiSampleType.KPISAMPLETYPE_L3_UNIQUE_COMPROMISED_CLIENTS,
                "service_ids": [],
            },
            "l3_unique_attackers": {
                "kpi_id": None,
                "description": "L3 - number of unique attackers of the service in a time interval of the service {service_id} (attacks from the same destination IP are only considered once)",
                "kpi_sample_type": KpiSampleType.KPISAMPLETYPE_L3_UNIQUE_ATTACKERS,
                "service_ids": [],
            },
        }
        self.attackmitigator_client = l3_attackmitigatorClient()

        # Environment variables
        self.CLASSIFICATION_THRESHOLD = float(os.getenv("CAD_CLASSIFICATION_THRESHOLD", 0.5))
        self.MONITORED_KPIS_TIME_INTERVAL_AGG = int(os.getenv("MONITORED_KPIS_TIME_INTERVAL_AGG", 60))

        # Constants
        self.NORMAL_CLASS = 0
        self.CRYPTO_CLASS = 1

        self.kpi_test = None
        self.time_interval_start = None
        self.time_interval_end = None

        # CAD evaluation tests
        self.cad_inference_times = []
        self.cad_num_inference_measurements = 100

        # AM evaluation tests
        self.am_notification_times = []
        
        # List of attack connections IPs
        self.attack_ips = []

        # List of attack connections
        self.attack_connections = []

        self.correct_attack_conns = 0
        self.correct_predictions = 0
        self.total_predictions = 0
        self.false_positives = 0
        self.false_negatives = 0

        self.pod_id = uuid.uuid4()
        LOGGER.info(f"Pod Id.: {self.pod_id}")

        self.first_batch_request_time = 0
        self.last_batch_request_time = 0

        self.response_times_csv_file_path = "response_times.csv"
        col_names = ["timestamp_first_req", "timestamp_last_req", "total_time", "batch_size"]

        with open(self.response_times_csv_file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(col_names)

    def create_kpi(
        self,
        service_id,
        kpi_name,
        kpi_description,
        kpi_sample_type,
    ):
        """
        Creates a new KPI for a specific service and add it to the Monitoring client

        Args:
            service_id (ServiceID): The ID of the service.
            kpi_name (str): The name of the KPI.
            kpi_description (str): The description of the KPI.
            kpi_sample_type (KpiSampleType): The sample type of the KPI.

        Returns:
            kpi (Kpi): The created KPI.
        """

        kpidescriptor = KpiDescriptor()
        kpidescriptor.kpi_description = kpi_description
        kpidescriptor.service_id.service_uuid.uuid = service_id.service_uuid.uuid
        kpidescriptor.kpi_sample_type = kpi_sample_type
        kpi = self.monitoring_client.SetKpi(kpidescriptor)

        LOGGER.info("Created KPI {}".format(kpi_name))

        return kpi

    def create_kpis(self, service_id):
        """
        Creates the monitored KPIs for a specific service, adds them to the Monitoring client and stores their identifiers in the monitored_kpis dictionary

        Args:
            service_id (uuid): The ID of the service.

        Returns:
            None
        """

        LOGGER.info("Creating KPIs for service {}".format(service_id))

        # all the KPIs are created for all the services from which requests are received
        for kpi in self.monitored_kpis:
            created_kpi = self.create_kpi(
                service_id,
                kpi,
                self.monitored_kpis[kpi]["description"].format(service_id=service_id.service_uuid.uuid),
                self.monitored_kpis[kpi]["kpi_sample_type"],
            )
            self.monitored_kpis[kpi]["kpi_id"] = created_kpi.kpi_id
            self.monitored_kpis[kpi]["service_ids"].append(service_id.service_uuid.uuid)

        LOGGER.info("Created KPIs for service {}".format(service_id))

    def monitor_kpis(self):
        """
        Monitors KPIs for all the services from which requests are received

        Args:
            None

        Returns:
            None
        """

        monitor_inference_results = self.inference_results
        monitor_service_ids = self.service_ids

        self.assign_timestamp(monitor_inference_results)

        non_empty_time_interval = self.l3_non_empty_time_interval

        if non_empty_time_interval:
            for service_id in monitor_service_ids:
                LOGGER.debug("service_id: {}".format(service_id))
                
                self.monitor_compute_l3_kpi()
                LOGGER.debug("KPIs sent to monitoring server")
        else:
            LOGGER.debug("No KPIs sent to monitoring server")

    def assign_timestamp(self, monitor_inference_results):
        """
        Assigns a timestamp to the monitored inference results.

        Args:
            monitor_inference_results (list): A list of monitored inference results.

        Returns:
            None
        """

        time_interval = self.MONITORED_KPIS_TIME_INTERVAL_AGG

        # assign the timestamp of the first inference result to the time_interval_start
        if self.time_interval_start is None:
            self.time_interval_start = monitor_inference_results[0]["timestamp"]
            LOGGER.debug("self.time_interval_start: {}".format(self.time_interval_start))

            # add time_interval to the current time to get the time interval end
            LOGGER.debug("time_interval: {}".format(time_interval))
            LOGGER.debug(timedelta(seconds=time_interval))
            self.time_interval_end = self.time_interval_start + timedelta(seconds=time_interval)

        current_time = datetime.utcnow()

        LOGGER.debug("current_time: {}".format(current_time))

        if current_time >= self.time_interval_end:
            self.time_interval_start = self.time_interval_end
            self.time_interval_end = self.time_interval_start + timedelta(seconds=time_interval)
            self.l3_security_status = 0  # unnecessary
            self.l3_ml_model_confidence = 0
            self.l3_inferences_in_interval_counter = 0

            self.l3_ml_model_confidence_normal = 0
            self.l3_inferences_in_interval_counter_normal = 0

            self.l3_ml_model_confidence_crypto = 0
            self.l3_inferences_in_interval_counter_crypto = 0

            self.l3_attacks = []
            self.l3_unique_attack_conns = 0
            self.l3_unique_compromised_clients = 0
            self.l3_unique_attackers = 0

            self.l3_non_empty_time_interval = False

        LOGGER.debug("time_interval_start: {}".format(self.time_interval_start))
        LOGGER.debug("time_interval_end: {}".format(self.time_interval_end))

    def monitor_compute_l3_kpi(
        self,
    ):
        """
        Computes the monitored KPIs for a specific service and sends them to the Monitoring server

        Args:
            None

        Returns:
            None
        """

        # L3 security status
        kpi_security_status = Kpi()
        kpi_security_status.kpi_id.kpi_id.CopyFrom(self.monitored_kpis["l3_security_status"]["kpi_id"])
        kpi_security_status.kpi_value.int32Val = self.l3_security_status

        # L3 ML model confidence
        kpi_conf = Kpi()
        kpi_conf.kpi_id.kpi_id.CopyFrom(self.monitored_kpis["l3_ml_model_confidence"]["kpi_id"])
        kpi_conf.kpi_value.floatVal = self.monitor_ml_model_confidence()

        # L3 unique attack connections
        kpi_unique_attack_conns = Kpi()
        kpi_unique_attack_conns.kpi_id.kpi_id.CopyFrom(self.monitored_kpis["l3_unique_attack_conns"]["kpi_id"])
        kpi_unique_attack_conns.kpi_value.int32Val = self.l3_unique_attack_conns

        # L3 unique compromised clients
        kpi_unique_compromised_clients = Kpi()
        kpi_unique_compromised_clients.kpi_id.kpi_id.CopyFrom(
            self.monitored_kpis["l3_unique_compromised_clients"]["kpi_id"]
        )
        kpi_unique_compromised_clients.kpi_value.int32Val = self.l3_unique_compromised_clients

        # L3 unique attackers
        kpi_unique_attackers = Kpi()
        kpi_unique_attackers.kpi_id.kpi_id.CopyFrom(self.monitored_kpis["l3_unique_attackers"]["kpi_id"])
        kpi_unique_attackers.kpi_value.int32Val = self.l3_unique_attackers

        timestamp = Timestamp()
        timestamp.timestamp = timestamp_utcnow_to_float()

        kpi_security_status.timestamp.CopyFrom(timestamp)
        kpi_conf.timestamp.CopyFrom(timestamp)
        kpi_unique_attack_conns.timestamp.CopyFrom(timestamp)
        kpi_unique_compromised_clients.timestamp.CopyFrom(timestamp)
        kpi_unique_attackers.timestamp.CopyFrom(timestamp)

        LOGGER.debug("Sending KPIs to monitoring server")

        LOGGER.debug("kpi_security_status: {}".format(kpi_security_status))
        LOGGER.debug("kpi_conf: {}".format(kpi_conf))
        LOGGER.debug("kpi_unique_attack_conns: {}".format(kpi_unique_attack_conns))
        LOGGER.debug("kpi_unique_compromised_clients: {}".format(kpi_unique_compromised_clients))
        LOGGER.debug("kpi_unique_attackers: {}".format(kpi_unique_attackers))

        try:
            self.monitoring_client.IncludeKpi(kpi_security_status)
            self.monitoring_client.IncludeKpi(kpi_conf)
            self.monitoring_client.IncludeKpi(kpi_unique_attack_conns)
            self.monitoring_client.IncludeKpi(kpi_unique_compromised_clients)
            self.monitoring_client.IncludeKpi(kpi_unique_attackers)
        except Exception as e:
            LOGGER.debug("Error sending KPIs to monitoring server: {}".format(e))

    def monitor_ml_model_confidence(self):
        """
        Get the monitored KPI for the confidence of the ML model

        Args:
            None

        Returns:
            confidence (float): The monitored KPI for the confidence of the ML model
        """

        confidence = None

        if self.l3_security_status == 0:
            confidence = self.l3_ml_model_confidence_normal
        else:
            confidence = self.l3_ml_model_confidence_crypto

        return confidence

    def perform_inference(self, request):
        """
        Performs inference on the input data using the Cryptomining Attack Detector model to classify the connection as standard traffic or cryptomining attack.

        Args:
            request (L3CentralizedattackdetectorMetrics): A L3CentralizedattackdetectorMetrics object with connection features information.

        Returns:
            dict: A dictionary containing the predicted class, the probability of that class, and other relevant information required to block the attack.
        """

        x_data = np.array([[feature.feature for feature in request.features]])

        # Print input data shape
        LOGGER.debug("x_data.shape: {}".format(x_data.shape))

        # Get batch size
        batch_size = x_data.shape[0]
        inference_time_start = time.time()

        # Perform inference
        predictions = self.cryptomining_detector_model.run(
            [self.prob_name], {self.input_name: x_data.astype(np.float32)}
        )[0]

        inference_time_end = time.time()

        # Measure inference time
        inference_time = inference_time_end - inference_time_start
        self.cad_inference_times.append(inference_time)

        if len(self.cad_inference_times) > self.cad_num_inference_measurements:
            inference_times_np_array = np.array(self.cad_inference_times)
            np.save(f"inference_times_{batch_size}.npy", inference_times_np_array)

            avg_inference_time = np.mean(inference_times_np_array)
            max_inference_time = np.max(inference_times_np_array)
            min_inference_time = np.min(inference_times_np_array)
            std_inference_time = np.std(inference_times_np_array)
            median_inference_time = np.median(inference_times_np_array)

            LOGGER.debug("Average inference time: {}".format(avg_inference_time))
            LOGGER.debug("Max inference time: {}".format(max_inference_time))
            LOGGER.debug("Min inference time: {}".format(min_inference_time))
            LOGGER.debug("Standard deviation inference time: {}".format(std_inference_time))
            LOGGER.debug("Median inference time: {}".format(median_inference_time))

            with open(f"inference_times_stats_{batch_size}.txt", "w") as f:
                f.write("Average inference time: {}\n".format(avg_inference_time))
                f.write("Max inference time: {}\n".format(max_inference_time))
                f.write("Min inference time: {}\n".format(min_inference_time))
                f.write("Standard deviation inference time: {}\n".format(std_inference_time))
                f.write("Median inference time: {}\n".format(median_inference_time))

        # Gather the predicted class, the probability of that class and other relevant information required to block the attack
        output_message = {
            "confidence": None,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "ip_o": request.connection_metadata.ip_o,
            "ip_d": request.connection_metadata.ip_d,
            "tag_name": None,
            "tag": None,
            "flow_id": request.connection_metadata.flow_id,
            "protocol": request.connection_metadata.protocol,
            "port_o": request.connection_metadata.port_o,
            "port_d": request.connection_metadata.port_d,
            "ml_id": self.cryptomining_detector_file_name,
            "service_id": request.connection_metadata.service_id,
            "endpoint_id": request.connection_metadata.endpoint_id,
            "time_start": request.connection_metadata.time_start,
            "time_end": request.connection_metadata.time_end,
        }

        if predictions[0][1] >= self.CLASSIFICATION_THRESHOLD:
            output_message["confidence"] = predictions[0][1]
            output_message["tag_name"] = "Crypto"
            output_message["tag"] = self.CRYPTO_CLASS
        else:
            output_message["confidence"] = predictions[0][0]
            output_message["tag_name"] = "Normal"
            output_message["tag"] = self.NORMAL_CLASS

        return output_message

    def perform_batch_inference(self, requests):
        """
        Performs batch inference on the input data using the Cryptomining Attack Detector model to classify the connection as standard traffic or cryptomining attack.

        Args:
            requests (list): A list of L3CentralizedattackdetectorMetrics objects with connection features information.

        Returns:
            list: A list of dictionaries containing the predicted class, the probability of that class, and other relevant information required to block the attack for each request.
        """

        batch_size = len(requests)

        # Create an empty array to hold the input data
        x_data = np.empty((batch_size, len(requests[0].features)))

        # Fill in the input data array with features from each request
        for i, request in enumerate(requests):
            x_data[i] = [feature.feature for feature in request.features]

        # Print input data shape
        LOGGER.debug("x_data.shape: {}".format(x_data.shape))

        inference_time_start = time.time()

        # Perform inference
        predictions = self.cryptomining_detector_model.run(
            [self.prob_name], {self.input_name: x_data.astype(np.float32)}
        )[0]

        inference_time_end = time.time()

        # Measure inference time
        inference_time = inference_time_end - inference_time_start
        self.cad_inference_times.append(inference_time)

        if len(self.cad_inference_times) > self.cad_num_inference_measurements:
            inference_times_np_array = np.array(self.cad_inference_times)
            np.save(f"inference_times_{batch_size}.npy", inference_times_np_array)

            avg_inference_time = np.mean(inference_times_np_array)
            max_inference_time = np.max(inference_times_np_array)
            min_inference_time = np.min(inference_times_np_array)
            std_inference_time = np.std(inference_times_np_array)
            median_inference_time = np.median(inference_times_np_array)

            LOGGER.debug("Average inference time: {}".format(avg_inference_time))
            LOGGER.debug("Max inference time: {}".format(max_inference_time))
            LOGGER.debug("Min inference time: {}".format(min_inference_time))
            LOGGER.debug("Standard deviation inference time: {}".format(std_inference_time))
            LOGGER.debug("Median inference time: {}".format(median_inference_time))

            with open(f"inference_times_stats_{batch_size}.txt", "w") as f:
                f.write("Average inference time: {}\n".format(avg_inference_time))
                f.write("Max inference time: {}\n".format(max_inference_time))
                f.write("Min inference time: {}\n".format(min_inference_time))
                f.write("Standard deviation inference time: {}\n".format(std_inference_time))
                f.write("Median inference time: {}\n".format(median_inference_time))

        # Gather the predicted class, the probability of that class and other relevant information required to block the attack
        output_messages = []
        for i, request in enumerate(requests):
            output_messages.append(
                {
                    "confidence": None,
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "ip_o": request.connection_metadata.ip_o,
                    "ip_d": request.connection_metadata.ip_d,
                    "tag_name": None,
                    "tag": None,
                    "flow_id": request.connection_metadata.flow_id,
                    "protocol": request.connection_metadata.protocol,
                    "port_o": request.connection_metadata.port_o,
                    "port_d": request.connection_metadata.port_d,
                    "ml_id": self.cryptomining_detector_file_name,
                    "service_id": request.connection_metadata.service_id,
                    "endpoint_id": request.connection_metadata.endpoint_id,
                    "time_start": request.connection_metadata.time_start,
                    "time_end": request.connection_metadata.time_end,
                }
            )

            if predictions[i][1] >= self.CLASSIFICATION_THRESHOLD:
                output_messages[i]["confidence"] = predictions[i][1]
                output_messages[i]["tag_name"] = "Crypto"
                output_messages[i]["tag"] = self.CRYPTO_CLASS
            else:
                output_messages[i]["confidence"] = predictions[i][0]
                output_messages[i]["tag_name"] = "Normal"
                output_messages[i]["tag"] = self.NORMAL_CLASS

        return output_messages

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def AnalyzeConnectionStatistics(
        self, request : L3CentralizedattackdetectorMetrics, context : grpc.ServicerContext
    ) -> StatusMessage:
        """
        Analyzes the connection statistics sent in the request, performs batch inference on the
        input data using the Cryptomining Attack Detector model to classify the connection as
        standard traffic or cryptomining attack, and notifies the Attack Mitigator component in
        case of attack.

        Args:
            request (L3CentralizedattackdetectorMetrics): A L3CentralizedattackdetectorMetrics
                object with connection features information.
            context (grpc.ServicerContext): The context of the request.

        Returns:
            StatusMessage: An response indicating that the information was received and processed.
        """

        # Perform inference with the data sent in the request
        if len(self.active_requests) == 0:
            self.first_batch_request_time = time.time()

        self.active_requests.append(request)

        if len(self.active_requests) >= BATCH_SIZE:
            LOGGER.debug("Performing inference... {}".format(self.pod_id))

            inference_time_start = time.time()
            cryptomining_detector_output = self.perform_batch_inference(self.active_requests)
            inference_time_end = time.time()

            LOGGER.debug("Inference performed in {} seconds".format(inference_time_end - inference_time_start))
            LOGGER.info("Inference performed correctly")

            self.inference_results.append({"output": cryptomining_detector_output, "timestamp": datetime.now()})
            LOGGER.debug("inference_results length: {}".format(len(self.inference_results)))

            for i, req in enumerate(self.active_requests):
                service_id = req.connection_metadata.service_id

                # Check if a request of a new service has been received and, if so, create
                # the monitored KPIs for that service
                if service_id not in self.service_ids:
                    self.create_kpis(service_id)
                    self.service_ids.append(service_id)

                monitor_kpis_start = time.time()
                self.monitor_kpis()
                monitor_kpis_end = time.time()

                LOGGER.debug("Monitoring KPIs performed in {} seconds".format(monitor_kpis_end - monitor_kpis_start))
                LOGGER.debug("cryptomining_detector_output: {}".format(cryptomining_detector_output[i]))

                if TEST_ML_MODEL:
                    self.analyze_prediction_accuracy(cryptomining_detector_output[i]["confidence"])

                connection_info = ConnectionInfo(
                    req.connection_metadata.ip_o,
                    req.connection_metadata.port_o,
                    req.connection_metadata.ip_d,
                    req.connection_metadata.port_d,
                )

                self.l3_non_empty_time_interval = True

                if cryptomining_detector_output[i]["tag_name"] == "Crypto":
                    self.l3_security_status = 1

                    self.l3_inferences_in_interval_counter_crypto += 1
                    self.l3_ml_model_confidence_crypto = (
                        self.l3_ml_model_confidence_crypto * (self.l3_inferences_in_interval_counter_crypto - 1)
                        + cryptomining_detector_output[i]["confidence"]
                    ) / self.l3_inferences_in_interval_counter_crypto

                    if connection_info not in self.l3_attacks:
                        self.l3_attacks.append(connection_info)
                        self.l3_unique_attack_conns += 1

                    self.l3_unique_compromised_clients = len(set([conn.ip_o for conn in self.l3_attacks]))
                    self.l3_unique_attackers = len(set([conn.ip_d for conn in self.l3_attacks]))

                else:
                    self.l3_inferences_in_interval_counter_normal += 1
                    self.l3_ml_model_confidence_normal = (
                        self.l3_ml_model_confidence_normal * (self.l3_inferences_in_interval_counter_normal - 1)
                        + cryptomining_detector_output[i]["confidence"]
                    ) / self.l3_inferences_in_interval_counter_normal

                # Only notify Attack Mitigator when a cryptomining connection has been detected
                if cryptomining_detector_output[i]["tag_name"] == "Crypto":
                    if TEST_ML_MODEL:
                        self.attack_connections.append(connection_info)

                    if connection_info.ip_o in self.attack_ips or connection_info.ip_d in self.attack_ips:
                        self.correct_attack_conns += 1
                        self.correct_predictions += 1
                    else:
                        LOGGER.debug("False positive: {}".format(connection_info))
                        self.false_positives += 1

                    self.total_predictions += 1
                    notification_time_start = time.time()

                    LOGGER.debug("Crypto attack detected")

                    # Notify the Attack Mitigator component about the attack
                    LOGGER.info(
                        "Notifying the Attack Mitigator component about the attack in order to block the connection..."
                    )

                    try:
                        LOGGER.info("Sending the connection information to the Attack Mitigator component...")
                        message = L3AttackmitigatorOutput(**cryptomining_detector_output[i])

                        am_response = self.attackmitigator_client.PerformMitigation(message)
                        LOGGER.debug("AM response: {}".format(am_response))

                        notification_time_end = time.time()

                        self.am_notification_times.append(notification_time_end - notification_time_start)

                        LOGGER.debug(f"am_notification_times length: {len(self.am_notification_times)}")
                        LOGGER.debug(f"last am_notification_time: {self.am_notification_times[-1]}")

                        if len(self.am_notification_times) > 100:
                            am_notification_times_np_array = np.array(self.am_notification_times)
                            np.save("am_notification_times.npy", am_notification_times_np_array)

                            avg_notification_time = np.mean(am_notification_times_np_array)
                            max_notification_time = np.max(am_notification_times_np_array)
                            min_notification_time = np.min(am_notification_times_np_array)
                            std_notification_time = np.std(am_notification_times_np_array)
                            median_notification_time = np.median(am_notification_times_np_array)

                            LOGGER.debug("Average notification time: {}".format(avg_notification_time))
                            LOGGER.debug("Max notification time: {}".format(max_notification_time))
                            LOGGER.debug("Min notification time: {}".format(min_notification_time))
                            LOGGER.debug("Std notification time: {}".format(std_notification_time))
                            LOGGER.debug("Median notification time: {}".format(median_notification_time))

                            with open("am_notification_times_stats.txt", "w") as f:
                                f.write("Average notification time: {}\n".format(avg_notification_time))
                                f.write("Max notification time: {}\n".format(max_notification_time))
                                f.write("Min notification time: {}\n".format(min_notification_time))
                                f.write("Std notification time: {}\n".format(std_notification_time))
                                f.write("Median notification time: {}\n".format(median_notification_time))

                        LOGGER.info("Attack Mitigator notified")

                    except Exception as e:
                        LOGGER.error("Error notifying the Attack Mitigator component about the attack: ", e)
                        LOGGER.error("Couldn't find l3_attackmitigator")

                        return StatusMessage(message="Attack Mitigator not found")
                else:
                    LOGGER.info("No attack detected")

                    if cryptomining_detector_output[i]["tag_name"] != "Crypto":
                        if connection_info.ip_o not in self.attack_ips and connection_info.ip_d not in self.attack_ips:
                            self.correct_predictions += 1
                        else:
                            LOGGER.debug("False negative: {}".format(connection_info))
                            self.false_negatives += 1

                        self.total_predictions += 1

            self.active_requests = []
            self.last_batch_request_time = time.time()

            col_values = [
                self.first_batch_request_time,
                self.last_batch_request_time,
                self.last_batch_request_time - self.first_batch_request_time,
                BATCH_SIZE,
            ]

            LOGGER.debug("col_values: {}".format(col_values))

            with open(self.response_times_csv_file_path, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(col_values)

            return StatusMessage(message="Ok, metrics processed")

        return StatusMessage(message="Ok, information received")

    def analyze_prediction_accuracy(self, confidence):
        """
        Analyzes the prediction accuracy of the Centralized Attack Detector.

        Args:
            confidence (float): The confidence level of the Cryptomining Attack Detector model.

        Returns:
            None
        """

        LOGGER.info("Number of Attack Connections Correctly Classified: {}".format(self.correct_attack_conns))
        LOGGER.info("Number of Attack Connections: {}".format(len(self.attack_connections)))

        if self.total_predictions > 0:
            overall_detection_acc = self.correct_predictions / self.total_predictions
        else:
            overall_detection_acc = 0

        LOGGER.info("Overall Detection Accuracy: {}\n".format(overall_detection_acc))

        if len(self.attack_connections) > 0:
            cryptomining_attack_detection_acc = self.correct_attack_conns / len(self.attack_connections)
        else:
            cryptomining_attack_detection_acc = 0

        LOGGER.info("Cryptomining Attack Detection Accuracy: {}".format(cryptomining_attack_detection_acc))
        LOGGER.info("Cryptomining Attack Detector Confidence: {}".format(confidence))

        with open("prediction_accuracy.txt", "a") as f:
            LOGGER.debug("Exporting prediction accuracy and confidence")

            f.write("Overall Detection Accuracy: {}\n".format(overall_detection_acc))
            f.write("Cryptomining Attack Detection Accuracy: {}\n".format(cryptomining_attack_detection_acc))
            f.write("Total Predictions: {}\n".format(self.total_predictions))
            f.write("Total Positives: {}\n".format(len(self.attack_connections)))
            f.write("False Positives: {}\n".format(self.false_positives))
            f.write("True Negatives: {}\n".format(self.total_predictions - len(self.attack_connections)))
            f.write("False Negatives: {}\n".format(self.false_negatives))
            f.write("Cryptomining Attack Detector Confidence: {}\n\n".format(confidence))
            f.write("Timestamp: {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            f.close()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def AnalyzeBatchConnectionStatistics(
        self, request : L3CentralizedattackdetectorBatchInput, context : grpc.ServicerContext
    ) -> StatusMessage:
        """
        Analyzes a batch of connection statistics sent in the request, performs batch inference on the
        input data using the Cryptomining Attack Detector model to classify the connection as standard
        traffic or cryptomining attack, and notifies the Attack Mitigator component in case of attack.

        Args:
            request (L3CentralizedattackdetectorBatchInput): A L3CentralizedattackdetectorBatchInput
                object with connection features information.
            context (grpc.ServicerContext): The context of the request.

        Returns:
            StatusMessage: An StatusMessage indicating that the information was received and processed.
        """

        batch_time_start = time.time()

        for metric in request.metrics:
            self.AnalyzeConnectionStatistics(metric, context)
        batch_time_end = time.time()

        with open("batch_time.txt", "a") as f:
            f.write(f"{len(request.metrics)}\n")
            f.write(f"{batch_time_end - batch_time_start}\n\n")
            f.close()

        LOGGER.debug(f"Batch time: {batch_time_end - batch_time_start}")
        LOGGER.debug("Batch time: {}".format(batch_time_end - batch_time_start))

        return StatusMessage(message="OK, information received.")

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetFeaturesIds(self, request : Empty, context : grpc.ServicerContext) -> AutoFeatures:
        """
        Returns a list of feature IDs used by the Cryptomining Attack Detector model.

        Args:
            request (Empty): An empty request object.
            context (grpc.ServicerContext): The context of the request.

        Returns:
            features_ids (AutoFeatures): A list of feature IDs used by the Cryptomining Attack Detector model.
        """

        features_ids = AutoFeatures()

        for feature in self.cryptomining_detector_features_metadata:
            features_ids.auto_features.append(feature)

        return features_ids

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetAttackIPs(self, request : AttackIPs, context : grpc.ServicerContext) -> Empty:
        """
        Sets the list of attack IPs in order to be used to compute the prediction accuracy of the
        Centralized Attack Detector in case of testing the ML model.

        Args:
            request (AttackIPs): A list of attack IPs.
            context (grpc.ServicerContext): The context of the request.

        Returns:
            empty (Empty): An empty response object.
        """

        self.attack_ips = request.attack_ips
        LOGGER.debug(f"Succesfully set attack IPs: {self.attack_ips}")

        return Empty()
