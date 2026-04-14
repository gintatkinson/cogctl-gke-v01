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


import json, math, requests, threading, time
from requests.exceptions import ReadTimeout
from typing import Optional
from .data.AggregationCache import AggregationCache, LinkSample
from ._Worker import _Worker, WorkerTypeEnum


CONTROLLER_TO_ADDRESS_PORT = {
    'TFS-E2E' : ('10.254.0.10', 80),
    'TFS-AGG' : ('10.254.0.11', 80),
    'TFS-IP'  : ('10.254.0.12', 80),
    'NCE-T'   : ('10.254.0.9',  8082),
    'NCE-FAN' : ('10.254.0.9',  8081),
    'SIMAP'   : ('10.254.0.9',  8080),
}

WAIT_LOOP_GRANULARITY = 0.5


class CollectorWorker(_Worker):
    def __init__(
        self, worker_name : str, controller_uuid : Optional[str],
        network_id : str, link_id : str, target_uri : str,
        aggregation_cache : AggregationCache, sampling_interval : float,
        terminate : Optional[threading.Event] = None
    ) -> None:
        super().__init__(WorkerTypeEnum.COLLECTOR, worker_name, terminate=terminate)
        self._controller_uuid = controller_uuid
        self._network_id = network_id
        self._link_id = link_id
        self._target_uri = target_uri
        self._aggregation_cache = aggregation_cache
        self._sampling_interval = sampling_interval

    def run(self) -> None:
        self._logger.info('[run] Starting...')

        try:
            address_port = CONTROLLER_TO_ADDRESS_PORT.get(self._controller_uuid)
            if address_port is None:
                address, port = CONTROLLER_TO_ADDRESS_PORT['SIMAP']
                self.direct_simap_polling(address, port)
            else:
                address, port = address_port
                self.underlay_subscription_stream(address, port)
        except Exception:
            self._logger.exception('[run] Unhandled Exception')
        finally:
            self._logger.info('[run] Terminated')

    def underlay_subscription_stream(self, address : str, port : int) -> None:
        stream_url = 'http://{:s}:{:d}{:s}'.format(address, port, self._target_uri)
        MSG = '[underlay_subscription_stream] Opening stream "{:s}"...'
        self._logger.info(MSG.format(str(stream_url)))

        session = requests.Session()
        try:
            # NOTE: Trick: we set 1-second read_timeout to force the loop to give control
            # back and be able to check termination events.
            # , timeout=(10, 1)
            with session.get(stream_url, stream=True) as reply:
                reply.raise_for_status()

                it_lines = reply.iter_lines(decode_unicode=True, chunk_size=1024)

                while not self._stop_event.is_set() and not self._terminate.is_set():
                    try:
                        line = next(it_lines)  # may block until read_timeout
                    except StopIteration:
                        break  # server closed
                    except ReadTimeout:
                        continue  # no data this tick; loop to check termination conditions

                    if line is None: continue
                    if len(line) == 0: continue

                    #MSG = '[underlay_subscription_stream] ==> {:s}'
                    #self._logger.debug(MSG.format(str(line)))
                    if not line.startswith('data:'): continue
                    data = json.loads(line[5:])

                    if 'notification' not in data:
                        MSG = 'Field(notification) missing: {:s}'
                        raise Exception(MSG.format(str(data)))
                    notification = data['notification']

                    if 'push-update' not in notification:
                        MSG = 'Field(notification/push-update) missing: {:s}'
                        raise Exception(MSG.format(str(data)))
                    push_update = notification['push-update']

                    if 'datastore-contents' not in push_update:
                        MSG = 'Field(notification/push-update/datastore-contents) missing: {:s}'
                        raise Exception(MSG.format(str(data)))
                    datastore_contents = push_update['datastore-contents']

                    if 'simap-telemetry:simap-telemetry' not in datastore_contents:
                        MSG = (
                            'Field(notification/push-update/datastore-contents'
                            '/simap-telemetry:simap-telemetry) missing: {:s}'
                        )
                        raise Exception(MSG.format(str(data)))
                    simap_telemetry = datastore_contents['simap-telemetry:simap-telemetry']

                    bandwidth_utilization = float(simap_telemetry['bandwidth-utilization'])
                    latency               = float(simap_telemetry['latency'])
                    related_service_ids   = simap_telemetry['related-service-ids']

                    link_sample = LinkSample(
                        network_id            = self._network_id,
                        link_id               = self._link_id,
                        bandwidth_utilization = bandwidth_utilization,
                        latency               = latency,
                        related_service_ids   = related_service_ids,
                    )
                    self._aggregation_cache.update(link_sample)
        finally:
            if session is not None:
                session.close()

    def direct_simap_polling(self, address : str, port : int) -> None:
        simap_url = 'http://{:s}:{:d}/restconf/data{:s}'.format(address, port, self._target_uri)

        while not self._stop_event.is_set() and not self._terminate.is_set():
            MSG = '[direct_simap_polling] Requesting "{:s}"...'
            self._logger.info(MSG.format(str(simap_url)))

            with requests.get(simap_url, timeout=10) as reply:
                reply.raise_for_status()
                data = reply.json()

            if 'simap-telemetry:simap-telemetry' not in data:
                MSG = 'Field(simap-telemetry:simap-telemetry) missing: {:s}'
                raise Exception(MSG.format(str(data)))
            simap_telemetry = data['simap-telemetry:simap-telemetry']

            bandwidth_utilization = float(simap_telemetry['bandwidth-utilization'])
            latency               = float(simap_telemetry['latency'])
            related_service_ids   = simap_telemetry.get('related-service-ids', list())

            link_sample = LinkSample(
                network_id            = self._network_id,
                link_id               = self._link_id,
                bandwidth_utilization = bandwidth_utilization,
                latency               = latency,
                related_service_ids   = related_service_ids,
            )
            self._aggregation_cache.update(link_sample)

            # Make wait responsible to terminations
            iterations = int(math.ceil(self._sampling_interval / WAIT_LOOP_GRANULARITY))
            for _ in range(iterations):
                if self._stop_event.is_set(): break
                if self._terminate.is_set() : break
                time.sleep(WAIT_LOOP_GRANULARITY)
