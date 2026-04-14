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

from __future__ import annotations
import collections.abc
import threading
import logging
import json
import time
import asyncio
import websockets
import ssl
from typing import Optional, List, Dict, Union
import re
import requests
import urllib3
from enum import Enum
from .connection import Connection
from .transport_capacity import TransportCapacity
from .constellation import Constellation

# https://confluence.infinera.com/display/CR/XR+Network+Service
# https://confluence.infinera.com/pages/viewpage.action?spaceKey=CR&title=XR+Network+Connection+Service#XRNetworkConnectionService-North-boundInterface
# https://bitbucket.infinera.com/projects/XRCM/repos/cm-api/browse/yaml/ncs/v1/ncs.yaml

LOGGER = logging.getLogger(__name__)

class ExpiringValue:
    def __init__(self, value, expiry):
        self.__value = value
        self.__expiry = expiry
        self.__created = time.monotonic()

    def get_value(self):
        return self.__value

    def is_valid_for(self, duration):
        if self.__created + self.__expiry >= time.monotonic()+duration:
            return True
        else:
            return False

class UnexpectedEmptyBody(Exception):
    pass

class ExternalError(Exception):
    pass

class ApiErrorFromIpm(Exception):
    pass

class ErrorFromIpm(ExternalError):
    def __init__(self, err_dict):
        msg = str(err_dict)
        # Try to extract a short error message
        try:
            # Only look at first message
            err_messages = err_dict["errors"]["errors"][0]["messages"]
            for err_msg in err_messages:
                if err_msg["lang"] == "en":
                    msg = err_msg["message"]
        except KeyError:
            pass
        except IndexError:
            pass
        super().__init__(msg)

class CreateConsistencyError(Exception):
    pass

class ErrorStore:
    def __init__(self):
        self.__lock = threading.Lock()
        self.__db={}
        self.__enabled=False

    def get_error(self, uri: str) -> Optional[dict]:
        with self.__lock:
            return self.__db.pop(uri, None)

    def set_error(self, uri: str, err_dict: dict):
        with self.__lock:
            if self.__enabled:
                self.__db[uri] = err_dict

    def enable(self):
        with self.__lock:
            self.__enabled = True

    def disable(self):
        with self.__lock:
            self.__enabled = False
            self.__db.clear()

# This is enum, not a regular class, see https://docs.python.org/3/library/enum.html
# String based enums require python 3.11, so use nunber based and custom parser
class ConsistencyMode(Enum):
    asynchronous = 0
    synchronous = 1
    lifecycle = 2

    @staticmethod
    def from_str(s: str) -> ConsistencyMode:
        if "synchronous" == s:
            return ConsistencyMode.synchronous
        elif "lifecycle" == s:
            return ConsistencyMode.lifecycle
        # Async is the default
        return ConsistencyMode.asynchronous

class HttpResult:
    def __init__(self, method: str, url: str, params: Dict[str, any] = None):
        self.method = method
        self.url = url
        self.text = None
        self.json = None
        self.status_code = None
        self.params = params
        self.exception = None

    def __str__(self):
        status_code = self.status_code if self.status_code is not None else "<not executed>"
        if self.text:
            if len(self.text) > 1024:
                body_text = self.text[:1024] + "..."
            else:
                body_text = self.text
        else:
            body_text = "NONE"
        return f"{self.method} {self.url} {self.params},  status {status_code}, body {body_text}"

    def process_http_response(self, response: requests.Response, permit_empty_body:bool = False):
        LOGGER.info(f"process_http_response(): {self.method}: {self.url} qparams={self.params} ==> {response.status_code}")
        self.status_code  = response.status_code
        if  response.content != b'null' and len(response.text):
            self.text = response.text

            try:
                r_json = json.loads(response.text)
                self.json = r_json
            except json.JSONDecodeError as json_err:
                LOGGER.info(f"{self.method}: {self.url}  ==> response json decode error: {str(json_err)}")
                self.exception = json_err
        elif not permit_empty_body:
            raise UnexpectedEmptyBody(f"No body in HTTP response for {self.method} {self.url} (status code {response.status_code}")

    def __bool__(self):
        # Error codes start at 400, codes below it are successes
        return self.status_code is not None and self.text is not None and self.status_code < 400 and self.exception is None

    def is_valid_with_status_ignore_body(self, expected_status_code: int) -> bool:
        return self.status_code is not None and self.status_code == expected_status_code and self.exception is None

    def is_valid_json_with_status(self, expected_status_code: int) -> bool:
        return bool(self) and self.status_code == expected_status_code and self.json is not None

    def is_valid_json_list_with_status(self, expected_status_code: int, min_entries=-1, max_entries=-1) -> bool:
        if not self.is_valid_json_with_status(expected_status_code):
            return False
        if not isinstance(self.json, collections.abc.Sequence):
            return False

        if min_entries >=0 and len(self.json) < min_entries:
            return False

        if max_entries >=0 and len(self.json) > max_entries:
            return False
        return True

    def is_valid_json_obj_with_status(self, expected_status_code: int) -> bool:
        if not self.is_valid_json_with_status(expected_status_code):
            return False
        if not isinstance(self.json, collections.abc.Mapping):
            return False

        return True

    def raise_as_exception(self):
        if self.exception is not None:
            raise ExternalError(f"Failure for request {str(self)}") from self.exception

        status_code = self.status_code if self.status_code is not None else "<not executed>"

        # Try to get error message from IPM
        if self.json is not None and "errors" in self.json:
            err_list = self.json["errors"]
            if len(err_list) > 0 and "message" in err_list[0]:
                err_msg = err_list[0]["message"]
                raise ApiErrorFromIpm(f"{self.method} {self.url} {self.params},  status {status_code}, IPM reported error: {err_msg}")
            
        raise ExternalError(str(self))

class CmConnection:
    CONSISTENCY_WAIT_LOG_INTERVAL = 1.0

    def __init__(self, address: str, port: int, username: str, password: str, timeout=30, tls_verify=True, consistency_mode: ConsistencyMode = ConsistencyMode.asynchronous, retry_interval: float=0.2, max_consistency_tries:int = 100_000, monitor_error_stream: bool = True) -> None:
        self.__tls_verify = tls_verify
        if not tls_verify:
            urllib3.disable_warnings()

        self.__consistency_mode = consistency_mode
        self.__timeout = timeout
        self.__retry_interval = retry_interval if retry_interval > 0.01 else 0.01
        # Consistency tries limit is mostly useful for testing where it can be use to make
        # test cases faster without timing dependency
        self.__max_consistency_tries = max_consistency_tries
        self.__username = username
        self.__password = password
        self.__cm_root = 'https://' + address + ':' + str(port)
        self.__cm_ws_root = 'wss://' + address + ':' + str(port)
        self.__access_token = None
        self.__monitor_error_stream = monitor_error_stream
        self.__err_store=ErrorStore()
        self.__err_monitor_thread = None
        self.__err_monitor_connected = threading.Event()
        self.__err_monitor_sub_id = None
        self.__err_monitor_terminate = threading.Event()
        self.print_received_errors = False

    def __del__(self):
        self.stop_monitoring_errors()

    def __perform_request(self, http_result: HttpResult, permit_empty_body: bool,  fn, *args, **kwargs):
        try:
            response = fn(*args, **kwargs)
            http_result.process_http_response(response, permit_empty_body)
        except requests.exceptions.Timeout as e:
            LOGGER.info(f"{http_result} ==> timeout")
            http_result.exception = e
        except Exception as e:  # pylint: disable=broad-except
            es=str(e)
            LOGGER.info(f"{http_result} ==> unexpected exception: {es}")
            http_result.exception = e
        return http_result

    def __post_w_headers(self, path, data, headers, data_as_json=True) -> HttpResult:
        url = self.__cm_root + path
        rv = HttpResult("POST", url)
        if data_as_json:
            self.__perform_request(rv, False, requests.post, url, headers=headers, json=data, timeout=self.__timeout, verify=self.__tls_verify)
        else:
            self.__perform_request(rv, False, requests.post, url, headers=headers, data=data, timeout=self.__timeout, verify=self.__tls_verify)
        return rv

    def __post(self, path, data, data_as_json=True) -> HttpResult:
        return self.__post_w_headers(path, data, self.__http_headers(), data_as_json=data_as_json)

    def __put(self, path: str, data: Union[str,Dict[str, any]], data_as_json:bool =True, permit_empty_body:bool =True) -> HttpResult:
        url = self.__cm_root + path
        rv = HttpResult("PUT", url)
        if data_as_json:
            self.__perform_request(rv, permit_empty_body, requests.put, url, headers=self.__http_headers(), json=data, timeout=self.__timeout, verify=self.__tls_verify)
        else:
            self.__perform_request(rv, permit_empty_body, requests.put, url, headers=self.__http_headers(), data=data, timeout=self.__timeout, verify=self.__tls_verify)
        return rv

    def __get(self, path, params: Dict[str, any]=None) -> HttpResult:
        url = self.__cm_root + path
        rv = HttpResult("GET", url, params)
        self.__perform_request(rv, False, requests.get, url, headers=self.__http_headers(), timeout=self.__timeout,verify=self.__tls_verify, params=params)
        return rv

    def __delete(self, path, data=None) -> HttpResult:
        url = self.__cm_root + path
        rv = HttpResult("DELETE", url)
        self.__perform_request(rv, True, requests.delete, url, headers=self.__http_headers(), data=data, timeout=self.__timeout, verify=self.__tls_verify)
        return rv

    def __http_headers(self):
        self.__ensure_valid_access_token()
        if self.__access_token:
            return {'Authorization': 'Bearer '+ self.__access_token.get_value()}
        else:
            return {}

    def __acquire_access_token(self):
        path = '/realms/xr-cm/protocol/openid-connect/token'
        req = {
            "username": self.__username,
            "password": self.__password,
            "grant_type": "password",
            "client_secret": "xr-web-client",
            "client_id": "xr-web-client"
        }
        resp = self.__post_w_headers(path, req, None, data_as_json=False)
        # Slightly more verbose check/logging of failures for authentication to help
        # diagnose connectivity problems
        if resp.status_code is None:
            LOGGER.error("Failed to contact authentication API endpoint")
            return False
        if not resp.is_valid_json_obj_with_status(200):
            LOGGER.error(f"Authentication failure, status code {resp.status_code}, data {resp.text}")
            return False
        if 'access_token' not in resp.json:
            LOGGER.error(f"Authentication failure: missing access_token in JSON, status code {resp.status_code}, data {resp.text}")
            return False
        access_token = resp.json['access_token']
        expires = int(resp.json["expires_in"]) if "expires_in" in resp.json else 0
        LOGGER.info(f"Obtained access token {access_token}, expires in {expires}")
        self.__access_token = ExpiringValue(access_token, expires)
        return True

    def __ensure_valid_access_token(self):
        if not self.__access_token or not self.__access_token.is_valid_for(60):
            self.__acquire_access_token()

    def Connect(self) -> bool:
        if not self.__acquire_access_token():
            return False
        return self.monitor_errors() if self.__monitor_error_stream else True

    def subscribe_errors(self):
        sub = [
            {
                "subscriptionName": "TfXrDriverErrorMonitopr",
                "subscriptionFilters": [
                    {
                        "requestedNotificationTypes": [ "Error" ],
                        "requestedResources": [
                            {
                                "resourceType": "cm.network-connection",
                            }
                        ]
                    },
                ]
            }
        ]

        r = self.__post("/api/v1/subscriptions/events", sub)
        #print(r.status_code, r.text)
        if not r.is_valid_json_list_with_status(201) or len(r.json) != 1:
            return None, None
        try:
            return self.__cm_ws_root + r.json[0]["notificationChannel"]["streamAddress"], r.json[0]["subscriptionId"]
        except KeyError:
            return None, None

    def unsubscribe(self, sub_id: str):
        resp = self.__delete(f"/api/v1/subscriptions/events/{sub_id}")
        if resp.is_valid_with_status_ignore_body(202):
            LOGGER.info(f"Deleted subscription {sub_id=}")
            return True
        else:
            LOGGER.info(f"Deleting subscription {sub_id=} failed, status {resp.status_code}")
            return False

    def monitor_errors(self) -> bool:
        uri, sub_id = self.subscribe_errors()
        if not uri or not sub_id:
            return False
        self.__err_monitor_sub_id = sub_id

        def err_monitor_thread():
            LOGGER.info(f"Listening errors via {uri}")

            ctx = ssl.create_default_context()
            if not self.__tls_verify:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

            async def receive_websock(uri, ssl_ctx):
                while not self.__err_monitor_terminate.is_set():
                    try:
                        async with websockets.connect(uri, ssl=ssl_ctx) as websocket:
                            LOGGER.info(f"err_monitor_thread(): WebSock connected to {uri}")
                            self.__err_monitor_connected.set()
                            while not self.__err_monitor_terminate.is_set():
                                # 5s timeout is used for forced checking of terminate flag
                                # In normal termmination timeout is not experienced, as
                                # we unsubscribe and that will trigger server to close the
                                # connection. This timeout exists purely as backup
                                # in case unsubscribe fails
                                try:
                                    msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                                except asyncio.exceptions.TimeoutError:
                                    continue
                                if self.print_received_errors:
                                    print(f"RX: {msg}")
                                try:
                                    msg_json = json.loads(msg)
                                    href = msg_json["href"]
                                    LOGGER.debug(f"err_monitor_thread(): RX [{href}]: {msg}")
                                    self.__err_store.set_error(href, msg_json)
                                except json.JSONDecodeError as json_err:
                                    LOGGER.error(f"err_monitor_thread(): Invalid message received: {msg}, JSON decode error {str(json_err)}")
                                except KeyError:
                                    LOGGER.error(f"err_monitor_thread(): Missing href in message: {msg}")
                    except asyncio.CancelledError as e:
                        LOGGER.debug("err_monitor_thread(): monitoring cancelled")
                        raise e
                    except Exception as e:
                        if not self.__err_monitor_terminate.is_set():
                            LOGGER.error(f"err_monitor_thread(): exception {str(e)}, reconnecting")
                            time.sleep(1)

            asyncio.run(receive_websock(uri, ctx))
            LOGGER.debug("err_monitor_thread(): thread terminating")

        assert self.__err_monitor_thread is None
        self.__err_monitor_terminate.clear()
        self.__err_monitor_thread = threading.Thread(target=err_monitor_thread)
        self.__err_monitor_thread.start()
        # If we can get connection soon, wait for it, otherwise proceed without delay
        # Not waiting for connection may miss some errors (-->timeout later), waiting too long
        # makes for bad experience
        self.__err_monitor_connected.wait(0.5)

        return True

    def stop_monitoring_errors(self):
        self.__err_monitor_terminate.set()

        if self.__err_monitor_sub_id:
            LOGGER.debug(f"Disabling error subscribtion {self.__err_monitor_sub_id }")
            self.unsubscribe(self.__err_monitor_sub_id)
            self.__err_monitor_sub_id = None

        if self.__err_monitor_thread is not None:
            LOGGER.debug("Terminating error monitoring thread")
            self.__err_monitor_thread.join()
            LOGGER.info("Error monitoring thread terminated")
            self.__err_monitor_thread = None

    def list_constellations(self) -> List[Constellation]:
        r = self.__get("/api/v1/xr-networks?content=expanded")
        if not r.is_valid_json_list_with_status(200):
            return []
        return [Constellation(c) for c in r.json]

    def get_constellation_by_hub_name(self, hub_module_name: str) -> Optional[Constellation]:
        qparams = [
            ('content', 'expanded'),
            ('q', '{"hubModule.state.module.moduleName": "' + hub_module_name + '"}')
        ]
        r = self.__get("/api/v1/xr-networks?content=expanded", params=qparams)
        if not r.is_valid_json_list_with_status(200, 1, 1):
            return None
        return Constellation(r.json[0])

    def get_transport_capacities(self) -> List[TransportCapacity]:
        r= self.__get("/api/v1/transport-capacities?content=expanded")
        if not r.is_valid_json_list_with_status(200):
            return []
        return [TransportCapacity(from_json=t) for t in r.json]

    def get_transport_capacity_by_name(self, tc_name: str) -> Optional[Connection]:
        qparams = [
            ('content', 'expanded'),
            ('q', '{"state.name": "' + tc_name + '"}')
        ]
        r = self.__get("/api/v1/transport-capacities?content=expanded", params=qparams)
        if not r.is_valid_json_list_with_status(200, 1, 1):
            return TransportCapacity(from_json=r.json[0])
        else:
            return None

    def get_transport_capacity_by_teraflow_uuid(self, uuid: str) -> Optional[Connection]:
        return self.get_transport_capacity_by_name(f"TF:{uuid}")

    def create_transport_capacity(self, tc: TransportCapacity) -> Optional[str]:
        # Create wants a list, so wrap connection to list
        tc_config = [tc.create_config()]
        resp = self.__post("/api/v1/transport-capacities", tc_config)
        if resp.is_valid_json_list_with_status(202, 1, 1) and "href" in resp.json[0]:
            tc.href = resp.json[0]["href"]
            LOGGER.info(f"Created transport-capcity {tc}")
            #LOGGER.info(self.__get(f"/api/v1/transport-capacities{tc.href}?content=expanded"))
            return tc.href
        else:
            return None

    def delete_transport_capacity(self, href: str) -> bool:
        resp = self.__delete(f"/api/v1/transport-capacities{href}")

        # Returns empty body
        if resp.is_valid_with_status_ignore_body(202):
            LOGGER.info(f"Deleted transport-capacity {href=}")
            return True
        else:
            LOGGER.info(f"Deleting transport-capacity {href=} failed, status {resp.status_code}")
            return False

    def apply_create_consistency(self, obj, get_fn):
        # Asynchronous, no validation
        if self.__consistency_mode == ConsistencyMode.asynchronous:
            return obj

        ts_start = time.perf_counter()
        log_ts = ts_start
        get_result = get_fn()
        valid = False
        limit = self.__max_consistency_tries
        while True:
            if get_result:
                if self.__consistency_mode == ConsistencyMode.synchronous:
                    valid = True
                    break
                if get_result.life_cycle_info.is_terminal_state():
                    valid = True
                    break
                else:
                    ts = time.perf_counter()
                    if ts - log_ts >= self.CONSISTENCY_WAIT_LOG_INTERVAL:
                        log_ts = ts
                        LOGGER.info(f"apply_create_consistency(): waiting for life cycle state progress for {get_result}, current: {str(get_result.life_cycle_info)}, ellapsed time {ts-ts_start} seconds")
            else:
                err_info = self.__err_store.get_error(obj.href)
                if err_info is not None:
                    LOGGER.info(f"apply_create_consistency(): asynchronous error reported for {obj}: {str(err_info)}")
                    raise ErrorFromIpm(err_info)

                ts = time.perf_counter()
                if ts - log_ts >= self.CONSISTENCY_WAIT_LOG_INTERVAL:
                    log_ts = ts
                    LOGGER.info(f"apply_create_consistency(): waiting for REST API object for {obj}, ellapsed time {ts-ts_start} seconds")
            limit -= 1
            if limit < 0 or time.perf_counter() - ts_start > self.__timeout:
                break
            time.sleep(self.__retry_interval)
            get_result = get_fn()

        duration = time.perf_counter() - ts_start
        if not valid:
            if get_result:
                msg = f"Failed to apply create consistency for {get_result}, insufficient life-cycle-state progress ({str(get_result.life_cycle_info)}), duration {duration} seconds"
                LOGGER.info(msg)
                raise CreateConsistencyError(msg)
            else:
                msg = f"Failed to apply create consistency for {obj}, REST object did not appear, duration {duration} seconds"
                LOGGER.info(msg)
                raise CreateConsistencyError(msg)
        else:
            LOGGER.info(f"Applied create consistency for {get_result}, final life-cycle-state {str(get_result.life_cycle_info)}, duration {duration} seconds")

        return get_result

    def apply_delete_consistency(self, href: str, get_fn):
        # Asynchronous, no validation
        if self.__consistency_mode == ConsistencyMode.asynchronous:
            return None

        ts_start = time.perf_counter()
        log_ts = ts_start
        get_result = get_fn()
        valid = False
        limit = self.__max_consistency_tries
        while True:
            if not get_result:
                # Object no longer exist, so this is completely successful operation
                valid = True
                break
            else:
                # In delete, treat terminal life cycle state as criteria for ConsistencyMode.synchronous:
                # This is unobvious, but in delete non-existence is stronger guarantee than just lifecycle
                # (so this is exact opposite )
                if get_result.life_cycle_info.is_terminal_state() and self.__consistency_mode == ConsistencyMode.synchronous:
                    valid = True
                    break
                else:
                    ts = time.perf_counter()
                    if ts - log_ts >= self.CONSISTENCY_WAIT_LOG_INTERVAL:
                        log_ts = ts
                        if get_result.life_cycle_info.is_terminal_state():
                            LOGGER.info(f"apply_delete_consistency(): waiting for delete to be reflected in REST API for {get_result}, current life-cycle-state: {str(get_result.life_cycle_info)}, ellapsed time {ts-ts_start} seconds")
                        else:
                            LOGGER.info(f"apply_delete_consistency(): waiting for life cycle state progress for {get_result}, current: {str(get_result.life_cycle_info)}, ellapsed time {ts-ts_start} seconds")

            limit -= 1
            if limit < 0 or time.perf_counter() - ts_start > self.__timeout:
                break
            time.sleep(self.__retry_interval)
            get_result = get_fn()

        duration = time.perf_counter() - ts_start
        if not valid:
            if get_result:
                if not get_result.life_cycle_info.is_terminal_state():
                    LOGGER.info(f"Failed to apply create delete for {get_result}, insufficient life-cycle-state progress ({str(get_result.life_cycle_info)}), duration {duration} seconds")
                else:
                    LOGGER.info(f"Failed to apply delete consistency for {get_result}, REST object did not dissappear, duration {duration} seconds")
        else:
            LOGGER.info(f"Applied delete consistency for {href}, duration {duration} seconds")

        return get_result

    def create_connection(self, connection: Connection) -> Optional[str]:
        # Create wants a list, so wrap connection to list
        cfg = [connection.create_config()]

        self.__err_store.enable()
        try:
            resp = self.__post("/api/v1/network-connections", cfg)
            if resp.is_valid_json_list_with_status(202, 1, 1) and "href" in resp.json[0]:
                connection.href = resp.json[0]["href"]
                LOGGER.info(f"IPM accepted create request for connection {connection}")
                new_connection = self.apply_create_consistency(connection, lambda: self.get_connection_by_href(connection.href))
                if new_connection:
                    LOGGER.info(f"Created connection {new_connection}")
                    return new_connection.href
                else:
                    LOGGER.error(f"Consistency failure for connection {connection}, result {resp}")
                    return None
            else:
                LOGGER.error(f"Create failure for connection {connection}, result {resp}")
                resp.raise_as_exception()
        finally:
            self.__err_store.disable()

    def update_connection(self, href: str, connection: Connection, existing_connection: Optional[Connection]=None) -> Optional[str]:
        cfg = connection.create_config()

        # Endpoint updates
        # Current CM implementation returns 501 (not implemented) for all of these actions

        # CM does not accept endpoint updates properly in same format that is used in initial creation.
        # Instead we work around by using more granular APIs.
        if "endpoints" in cfg:
            del cfg["endpoints"]
        if existing_connection is None:
            existing_connection = self.get_connection_by_href(href)
        ep_deletes, ep_creates, ep_updates = connection.get_endpoint_updates(existing_connection)
        #print(ep_deletes)
        #print(ep_creates)
        #print(ep_updates)

        # Perform deletes
        for ep_href in ep_deletes:
            resp = self.__delete(f"/api/v1{ep_href}")
            if resp.is_valid_with_status_ignore_body(202):
                LOGGER.info(f"update_connection: EP-UPDATE: Deleted connection endpoint {ep_href}")
            else:
                LOGGER.info(f"update_connection: EP-UPDATE: Failed to delete connection endpoint {ep_href}: {resp}")

        # Update capacities for otherwise similar endpoints
        for ep_href, ep_cfg in ep_updates:
            resp = self.__put(f"/api/v1{ep_href}", ep_cfg)
            if resp.is_valid_with_status_ignore_body(202):
                LOGGER.info(f"update_connection: EP-UPDATE: Updated connection endpoint {ep_href} with {ep_cfg}")
            else:
                LOGGER.info(f"update_connection: EP-UPDATE: Failed to update connection endpoint {ep_href} with {ep_cfg}: {resp}")

        # Perform adds
        resp = self.__post(f"/api/v1{href}/endpoints", ep_creates)
        if resp.is_valid_json_list_with_status(202, 1, 1) and "href" in resp.json[0]:
            LOGGER.info(f"update_connection: EP-UPDATE: Created connection endpoints {resp.json[0]} with {ep_creates}")
        else:
            LOGGER.info(f"update_connection: EP-UPDATE: Failed to create connection endpoints {resp.json[0] if resp.json else None} with {ep_creates}: {resp}")

        # Connection update (excluding endpoints)
        resp = self.__put(f"/api/v1{href}", cfg)
        # Returns empty body
        if resp.is_valid_with_status_ignore_body(202):
            LOGGER.info(f"update_connection: Updated connection {connection}")
            # Return href used for update to be consisten with create
            return href
        else:
            LOGGER.error(f"update_connection: Update failure for connection {connection}, result {resp}")
            return None

    def delete_connection(self, href: str) -> bool:
        resp = self.__delete(f"/api/v1{href}")
        #print(resp)
        # Returns empty body
        if resp.is_valid_with_status_ignore_body(202):
            self.apply_delete_consistency(href, lambda: self.get_connection_by_href(href))
            LOGGER.info(f"Deleted connection {href=}")
            return True
        else:
            return False

    # Always does the correct thing, that is update if present, otherwise create
    def create_or_update_connection(self, connection: Connection) -> Optional[str]:
        existing_connection = self.get_connection_by_name(connection.name)
        if existing_connection:
            return self.update_connection(existing_connection.href, connection, existing_connection)
        else:
            return self.create_connection(connection)

    def get_connection_by_name(self, connection_name: str) -> Optional[Connection]:
        qparams = [
            ('content', 'expanded'),
            ('q', '{"state.name": "' + connection_name + '"}')
        ]
        r = self.__get("/api/v1/network-connections", params=qparams)
        if r.is_valid_json_list_with_status(200, 1, 1):
            return Connection(from_json=r.json[0])
        else:
            return None

    def get_connection_by_href(self, href: str) -> Optional[Connection]:
        qparams = [
            ('content', 'expanded'),
        ]
        r = self.__get(f"/api/v1{href}", params=qparams)
        if r.is_valid_json_obj_with_status(200):
            return Connection(from_json=r.json)
        else:
            return None

    def get_connection_by_teraflow_uuid(self, uuid: str) -> Optional[Connection]:
        return self.get_connection_by_name(f"TF:{uuid}")

    def get_connections(self):
        r = self.__get("/api/v1/network-connections?content=expanded")
        if r.is_valid_json_list_with_status(200):
            return [Connection(from_json=c) for c in r.json]
        else:
            return []

    def service_uuid(self, key: str) -> Optional[str]:
        service = re.match(r"^(?:/services)/service\[(.+)\]$", key)
        if service:
            return service.group(1)
        else:
            return None
