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

import logging, math, queue, random, re, threading
from datetime import datetime
from typing import Optional, Tuple

LOGGER = logging.getLogger(__name__)

RE_GET_ENDPOINT_METRIC = re.compile(r'.*\/endpoint\[([^\]]+)\]\/state\/(.*)')

MSG_ERROR_PARSE = '[get] unable to extract endpoint-metric from monitoring_resource_key "{:s}"'
MSG_INFO = '[get] monitoring_resource_key={:s}, endpoint_uuid={:s}, metric={:s}, metric_sense={:s}'

class SyntheticSamplingParameters:
    def __init__(self) -> None:
        self.__lock = threading.Lock()
        self.__data = {}
        self.__configured_endpoints = set()

    def set_endpoint_configured(self, endpoint_uuid : str):
        with self.__lock:
            self.__configured_endpoints.add(endpoint_uuid)

    def unset_endpoint_configured(self, endpoint_uuid : str):
        with self.__lock:
            self.__configured_endpoints.discard(endpoint_uuid)

    def get(self, monitoring_resource_key : str) -> Optional[Tuple[float, float, float, float, float]]:
        with self.__lock:
            match = RE_GET_ENDPOINT_METRIC.match(monitoring_resource_key)
            if match is None:
                LOGGER.error(MSG_ERROR_PARSE.format(monitoring_resource_key))
                return None
            endpoint_uuid = match.group(1)

            # If endpoint is not configured, generate a flat synthetic traffic aligned at 0
            if endpoint_uuid not in self.__configured_endpoints: return (0, 0, 1, 0, 0)

            metric = match.group(2)
            metric_sense = metric.lower().replace('packets_', '').replace('bytes_', '')

            LOGGER.debug(MSG_INFO.format(monitoring_resource_key, endpoint_uuid, metric, metric_sense))

            parameters_key = '{:s}-{:s}'.format(endpoint_uuid, metric_sense)
            parameters = self.__data.get(parameters_key)
            if parameters is not None: return parameters

            # assume packets
            amplitude  = 1.e7 * random.random()
            phase      = 60 * random.random()
            period     = 3600 * random.random()
            offset     = 1.e8 * random.random() + amplitude
            avg_bytes_per_packet = random.randint(500, 1500)
            parameters = (amplitude, phase, period, offset, avg_bytes_per_packet)
            return self.__data.setdefault(parameters_key, parameters)

def do_sampling(
    synthetic_sampling_parameters : SyntheticSamplingParameters, monitoring_resource_key : str,
    out_samples : queue.Queue
) -> None:
    parameters = synthetic_sampling_parameters.get(monitoring_resource_key)
    if parameters is None: return
    amplitude, phase, period, offset, avg_bytes_per_packet = parameters

    if 'bytes' in monitoring_resource_key.lower():
        # convert to bytes
        amplitude = avg_bytes_per_packet * amplitude
        offset = avg_bytes_per_packet * offset

    timestamp = datetime.timestamp(datetime.utcnow())
    waveform  = amplitude * math.sin(2 * math.pi * timestamp / period + phase) + offset
    noise     = amplitude * random.random()
    value     = abs(0.95 * waveform + 0.05 * noise)
    out_samples.put_nowait((timestamp, monitoring_resource_key, value))
