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

import json, logging, queue, requests, threading, time
from typing import Any, Iterator, List, Optional, Tuple, Union, Dict
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from device.service.driver_api._Driver import _Driver

LOGGER = logging.getLogger(__name__)

DRIVER_NAME = 'morpheus'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class MorpheusApiDriver(_Driver):
    def __init__(self, address: str, port: int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        scheme = self.settings.get('scheme', 'http')
        self.__morpheus_root = '{:s}://{:s}:{:d}'.format(scheme, self.address, int(self.port))
        self.__timeout = int(self.settings.get('timeout', 120))
        self.__headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json'}

        self.__detection_thread = None
        self.__pipeline_error_thread = None

        size = self.settings.get('queue_events_size', 10)
        self.__pipeline_error_queue = queue.Queue(maxsize=size)
        self.__detection_queue = queue.Queue(maxsize=size)

    def Connect(self) -> bool:
        url = self.__morpheus_root + '/restconf/data/naudit-morpheus:morpheus'
        with self.__lock:
            if self.__started.is_set(): return True
            try:
                requests.get(url, headers=self.__headers, timeout=self.__timeout, verify=False)
                self.__started.set()
                return True
            except requests.exceptions.Timeout:
                LOGGER.exception('Timeout connecting {:s}'.format(str(self.__morpheus_root)))
                return False
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception('Exception connecting {:s}'.format(str(self.__morpheus_root)))
                return False

    def Disconnect(self) -> bool:
        with self.__lock:
            try:
                if self.__detection_thread and self.__detection_thread.is_alive():
                    self.__unsubscribe_detection_event()

                if self.__pipeline_error_thread and self.__pipeline_error_thread.is_alive():
                    self.__unsubscribe_pipeline_error()
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception('Error during disconnect')

            self.__terminate.set()
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        url = self.__morpheus_root + '/restconf/data/naudit-morpheus:morpheus/config'
        with self.__lock:
            try:
                response = requests.get(url, headers=self.__headers, timeout=self.__timeout, verify=False)
                if response.ok:
                    config = response.json()
                    result = []

                    for key, value in config.items():
                        result.append((key, value))

                    return  result
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception('Exception getting initial config {:s}'.format(str(self.__morpheus_root)))
            return []

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        url = self.__morpheus_root + '/restconf/data/naudit-morpheus:morpheus/config'
        with self.__lock:
            try:
                response = requests.get(url, headers=self.__headers, timeout=self.__timeout, verify=False)
                if response.ok:
                    config = response.json()
                    results = []

                    if not resource_keys:
                        for key, value in config.items():
                            results.append((key, value))
                        return results

                    for key in resource_keys:
                        try:
                            results.append((key, config[key]))
                        except Exception as e:  # pylint: disable=broad-except
                            results.append((key, e))
                    return results
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception('Error getting config')
                return [(key, e) for key in resource_keys]

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        url = self.__morpheus_root + '/restconf/data/naudit-morpheus:morpheus/config'
        results = []
        with self.__lock:
            config = dict(resources)
            try:
                response = requests.put(url,
                                        headers=self.__headers,
                                        json=config,
                                        timeout=self.__timeout,
                                        verify=False)
                results.append(response.ok)
            except Exception as e:
                results.append(e)
        return results

    def GetState(self, blocking=False, terminate: Optional[threading.Event] = None) -> Iterator[Tuple[float, str, Any]]:
        while True:
            if self.__terminate.is_set(): break
            if terminate is not None and terminate.is_set(): break

            internal_state = self.__get_state()
            if internal_state is not None:
                timestamp = time.time()
                yield(timestamp, 'state', internal_state)

            pipeline_error_empty = False
            detection_event_empty = False

            try:
                error = self.__pipeline_error_queue.get(block=False, timeout=0.1)
                if error is not None:
                    yield (error.get('eventTime', time.time()), 'pipeline_error', error.get('event'),)
            except queue.Empty:
                pipeline_error_empty = True

            try:
                event = self.__detection_queue.get(block=False, timeout=0.1)
                if event is not None:
                    yield (event.get('eventTime', time.time()), 'detection_event', event.get('event'),)
            except queue.Empty:
                detection_event_empty = True

            if pipeline_error_empty and detection_event_empty:
                if blocking:
                    continue
                return

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions: List[Tuple[str, float, float]]) -> List[Union[bool,Exception]]:
        results = []
        rollback_stack = []
        operations = [
                (self.__subscribe_detection_event, self.__unsubscribe_detection_event),
                (self.__subscribe_pipeline_error, self.__unsubscribe_pipeline_error),
                (self.__start_pipeline, self.__stop_pipeline),
        ]
        for _, (sub_op, unsub_op) in enumerate(operations):
            result = sub_op()
            results.append(result)
            if isinstance(result, Exception):
                while rollback_stack:
                    rollback_op = rollback_stack.pop()
                    try:
                        rollback_op()
                    except Exception as e:  # pylint: disable=broad-except
                        LOGGER.exception('Error during subscription rollback operation')

                return results

            rollback_stack.append(unsub_op)
        return results

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions: List[Tuple[str,float,float]]) -> List[Union[bool, Exception]]:
        results = []
        results.append(self.__stop_pipeline())
        results.append(self.__unsubscribe_pipeline_error())
        results.append(self.__unsubscribe_detection_event())
        return results

    def __start_pipeline(self) -> Union[bool, Exception]:
        url = self.__morpheus_root + '/restconf/data/naudit-morpheus:morpheus/start'
        with self.__lock:
            try:
                response = requests.post(url, headers=self.__headers, timeout=self.__timeout, verify=False)
                response.raise_for_status()
                return True
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception('Error starting pipeline')
                return e

    def __stop_pipeline(self) -> Union[bool, Exception]:
        url = self.__morpheus_root + '/restconf/data/naudit-morpheus:morpheus/stop'
        with self.__lock:
            try:
                response = requests.post(url, headers=self.__headers, timeout=self.__timeout, verify=False)
                response.raise_for_status()
                return True
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception('Error stopping pipeline')
                return e

    def __subscribe_detection_event(self) -> Union[bool, Exception]:
        url = self.__morpheus_root + '/restconf/streams/naudit-morpheus:morpheus/detection-event'
        with self.__lock:
            try:
                self.__detection_thread = threading.Thread(
                        target=self.__handle_notification_stream,
                        args=(url, self.__detection_queue),
                        daemon=True
                        )
                self.__detection_thread.start()
                return True
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception('Error subscribing to detection events')
                return e

    def __unsubscribe_detection_event(self) -> Union[bool, Exception]:
        try:
            if self.__detection_thread and self.__detection_thread.is_alive():
                self.__detection_thread.join(timeout=5)
            return True
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.exception('Error unsubscribing from detection events')
            return e

    def __subscribe_pipeline_error(self) -> Union[bool, Exception]:
        url = self.__morpheus_root + '/restconf/streams/naudit-morpheus:morpheus/pipeline-error'
        with self.__lock:
            try:
                self.__pipeline_error_thread = threading.Thread(
                        target=self.__handle_notification_stream,
                        args=(url, self.__pipeline_error_queue),
                        daemon=True
                        )
                self.__pipeline_error_thread.start()
                return True
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception('Error subscribing to pipeline errors')
                return e

    def __unsubscribe_pipeline_error(self) -> Union[bool, Exception]:
        try:
            if self.__pipeline_error_thread and self.__pipeline_error_thread.is_alive():
                self.__pipeline_error_thread.join(timeout=5)
            return True
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.exception('Error unsubscribing from pipeline errors')
            return e

    def __get_state(self) -> Dict:
        url = self.__morpheus_root + '/restconf/data/naudit-morpheus:morpheus/state'
        with self.__lock:
            try:
                response = requests.get(url, headers=self.__headers, timeout=self.__timeout, verify=False)
                if response.ok:
                    state = response.json()
                    return state
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception('Error getting internal state')
        return None


    def __handle_notification_stream(self, url: str, queue: queue.Queue[Any]) -> None:
        try:
            with requests.get(url,
                              headers=self.__headers,
                              stream=True,
                              verify=False,
                              timeout=(3.05, None)) as response:

                if not response.ok:
                    LOGGER.error(f'Error connecting to event stream: {response.status_code}')
                    return

                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    if line.startswith('data:'):
                        data = line[5:].strip()
                        LOGGER.error(f'Data received: {data}')
                        try:
                            event = json.loads(data)
                            queue.put(event['ietf-restconf:notification'])
                        except json.JSONDecodeError as e:
                            LOGGER.error(f'Error parsing event: {e}')
                        except KeyError as e:
                            LOGGER.error(f'Missing expected key in event: {e}')
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.exception('Error in notification stream handler')
