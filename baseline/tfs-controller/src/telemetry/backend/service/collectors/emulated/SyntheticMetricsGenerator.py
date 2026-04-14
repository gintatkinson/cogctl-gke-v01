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

import numpy as np
import random
import logging
import queue
import time

LOGGER = logging.getLogger(__name__)

class SyntheticMetricsGenerator():
    """
    This collector class generates synthetic network metrics based on the current network state.
    The metrics include packet_in, packet_out, bytes_in, bytes_out, packet_loss (percentage), packet_drop_count, byte_drop_count, and latency.
    The network state can be 'good', 'moderate', or 'poor', and it affects the generated metrics accordingly.
    """
    def __init__(self, metric_queue=None, network_state="good"):
        LOGGER.info("Initiaitng Emulator")
        super().__init__()
        self.metric_queue        = metric_queue if metric_queue is not None else queue.Queue()
        self.network_state       = network_state
        self.running             = True
        self.set_initial_parameter_values()  # update this method to set the initial values for the parameters

    def set_initial_parameter_values(self):
        self.bytes_per_pkt       = random.uniform(65, 150)
        self.states              = ["good", "moderate", "poor"]
        self.state_probabilities = {
            "good"    : [0.9, 0.1, 0.0],
            "moderate": [0.2, 0.7, 0.1],
            "poor"    : [0.0, 0.3, 0.7]
        }
        if self.network_state   == "good":
            self.packet_in = random.uniform(700, 900)
        elif self.network_state == "moderate":
            self.packet_in = random.uniform(300, 700)
        else:
            self.packet_in = random.uniform(100, 300)

    def generate_synthetic_data_point(self, resource_key, sample_type_ids):
        """
        Generates a synthetic data point based on the current network state.

        Parameters:
        resource_key (str): The key associated with the resource for which the data point is generated.

        Returns:
        tuple: A tuple containing the timestamp, resource key, and a dictionary of generated metrics.
        """
        if self.network_state   == "good":
            packet_loss  = random.uniform(0.01, 0.1)  
            random_noise = random.uniform(1,10)
            latency      = random.uniform(5, 25)
        elif self.network_state == "moderate":
            packet_loss  = random.uniform(0.1, 1)
            random_noise = random.uniform(10, 40)
            latency      = random.uniform(25, 100)
        elif self.network_state == "poor":
            packet_loss  = random.uniform(1, 3)
            random_noise = random.uniform(40, 100)
            latency      = random.uniform(100, 300)
        else:
            raise ValueError("Invalid network state. Must be 'good', 'moderate', or 'poor'.")

        period            = 60 * 60 * random.uniform(10, 100)
        amplitude         = random.uniform(50, 100) 
        sin_wave          = amplitude  * np.sin(2 * np.pi   * 100 / period) + self.packet_in
        packet_in         = sin_wave   + ((sin_wave/100)    * random_noise)
        packet_out        = packet_in  - ((packet_in / 100) * packet_loss)
        bytes_in          = packet_in  * self.bytes_per_pkt
        bytes_out         = packet_out * self.bytes_per_pkt
        packet_drop_count = packet_in  * (packet_loss / 100)
        byte_drop_count   = packet_drop_count * self.bytes_per_pkt

        state_prob = self.state_probabilities[self.network_state]
        self.network_state = random.choices(self.states, state_prob)[0]
        print (self.network_state)

        generated_samples = {
            "packet_in" : int(packet_in),   "packet_out" : int(packet_out),    "bytes_in"          : float(bytes_in),
            "bytes_out" : float(bytes_out), "packet_loss": float(packet_loss), "packet_drop_count" : int(packet_drop_count),
            "latency"   : float(latency),   "byte_drop_count": float(byte_drop_count)
        }
        requested_metrics = self.metric_id_mapper(sample_type_ids, generated_samples)
        # generated_samples = {metric: generated_samples[metric] for metric in requested_metrics}

        return (time.time(), resource_key, requested_metrics)

    def metric_id_mapper(self, sample_type_ids, metric_dict):   # TODO: Add a dynamic mappper from kpi_sample_type ID to name...
        """
        Maps the sample type IDs to the corresponding metric names.

        Parameters:
        sample_type_ids (list): A list of sample type IDs.

        Returns:
        list: A list of metric names.
        """
        metric_names = []
        for sample_type_id in sample_type_ids:
            if sample_type_id == 102:
                metric_names.append(metric_dict["packet_in"])
            elif sample_type_id == 101:
                metric_names.append(metric_dict["packet_out"])
            elif sample_type_id == 103:
                metric_names.append(metric_dict["packet_drop_count"])
            elif sample_type_id == 202:
                metric_names.append(metric_dict["bytes_in"])
            elif sample_type_id == 201:
                metric_names.append(metric_dict["bytes_out"])
            elif sample_type_id == 203:
                metric_names.append(metric_dict["byte_drop_count"])
            elif sample_type_id == 701:
                metric_names.append(metric_dict["latency"])
            else:
                raise ValueError(f"Invalid sample type ID: {sample_type_id}")
        return metric_names
