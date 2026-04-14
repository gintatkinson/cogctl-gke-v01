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


import json, math, threading, time
from dataclasses import dataclass
from kafka import KafkaProducer
from typing import Dict, Optional, Union
from common.tools.kafka.Variables import KafkaConfig
from simap_connector.service.simap_updater.SimapClient import SimapClient
from .data.AggregationCache import AggregationCache
from ._Worker import _Worker, WorkerTypeEnum


KAFKA_BOOT_SERVERS = KafkaConfig.get_kafka_address()

WAIT_LOOP_GRANULARITY = 0.5


@dataclass
class ServerSentEvent:
    event_data : Union[str, Dict]
    event_type : Optional[str] = None
    event_id   : Optional[int] = None

    def format(self) -> str:
        # SSE specs <https://html.spec.whatwg.org/multipage/server-sent-events.html>
        event_data = self.event_data
        if not isinstance(event_data, str):
            event_data = json.dumps(event_data)

        lines = [
            'data: {:s}'.format(line)
            for line in event_data.splitlines()
        ]

        if self.event_type:
            lines.insert(0, 'event: {:s}'.format(str(self.event_type)))

        if self.event_id:
            lines.append('id: {:d}'.format(int(self.event_id)))

        return '\n'.join(lines) + '\n\n'


class AggregatorWorker(_Worker):
    def __init__(
        self, worker_name : str, simap_client : SimapClient, network_id : str, link_id : str,
        parent_subscription_id : int, aggregation_cache : AggregationCache, topic : str,
        sampling_interval : float, terminate : Optional[threading.Event] = None
    ) -> None:
        super().__init__(WorkerTypeEnum.AGGREGATOR, worker_name, terminate=terminate)
        self._simap_client = simap_client
        self._network_id = network_id
        self._link_id = link_id
        self._parent_subscription_id = parent_subscription_id
        self._aggregation_cache = aggregation_cache
        self._topic = topic
        self._sampling_interval = sampling_interval


    def run(self) -> None:
        self._logger.info('[run] Starting...')

        kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_BOOT_SERVERS)
        update_counter = 1

        try:
            while not self._stop_event.is_set() and not self._terminate.is_set():
                #self._logger.debug('[run] Aggregating...')

                link_sample = self._aggregation_cache.aggregate()

                data = {'notification': {
                    'eventTime': link_sample.timestamp.isoformat() + 'Z',
                    'push-update': {
                        'id': update_counter,
                        'datastore-contents': {'simap-telemetry:simap-telemetry': {
                            'bandwidth-utilization': '{:.2f}'.format(link_sample.bandwidth_utilization),
                            'latency'              : '{:.3f}'.format(link_sample.latency),
                            'related-service-ids'  : list(link_sample.related_service_ids),
                        }}
                    }
                }}

                event = ServerSentEvent(
                    event_data=data, event_id=update_counter, event_type='push-update'
                )
                str_event = event.format()

                kafka_producer.send(
                    self._topic, key=self._topic.encode('utf-8'),
                    value=str_event.encode('utf-8')
                )
                kafka_producer.flush()

                simap_link = self._simap_client.network(self._network_id).link(self._link_id)
                simap_link.telemetry.update(
                    link_sample.bandwidth_utilization, link_sample.latency,
                    related_service_ids=list(link_sample.related_service_ids)
                )

                update_counter += 1

                # Make wait responsible to terminations
                iterations = int(math.ceil(self._sampling_interval / WAIT_LOOP_GRANULARITY))
                for _ in range(iterations):
                    if self._stop_event.is_set(): break
                    if self._terminate.is_set() : break
                    time.sleep(WAIT_LOOP_GRANULARITY)
        except Exception:
            self._logger.exception('[run] Unhandled Exception')
        finally:
            self._logger.info('[run] Terminated')
