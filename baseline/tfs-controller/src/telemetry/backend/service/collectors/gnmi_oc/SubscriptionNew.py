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


from google.protobuf.json_format import MessageToDict
from pygnmi.client import gNMIclient  # type: ignore
from queue import Queue
from typing import Callable, Tuple, Optional, List
import grpc
import logging
import threading

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


class Subscription:
    """
    Handles a gNMI *Subscribe* session.
    It receives a **list of candidate paths**; if the target rejects one
    (INVALID_ARGUMENT / unknown path), the thread automatically tries the
    next path until it works or the list is exhausted.
    """

    def __init__(
        self,
        sub_id:                str,
        gnmi_client:           gNMIclient,
        path_list:             List[str],
        metric_queue:          Queue,
        mode:                  str        = "stream",
        sample_interval_ns:    int        = 10_000_000_000,
        heartbeat_interval_ns: Optional[int] = None,  # ← NEW
        encoding:              str        = "json_ietf",
        on_update:             Optional[Callable[[dict], None]] = None,
    ) -> None:

        self.sub_id        = sub_id
        self.gnmi_client   = gnmi_client
        self._queue: Queue = metric_queue
        self._stop_event   = threading.Event()

        self._thread       = threading.Thread(
            target = self._run,
            args   = (
                path_list, mode,
                sample_interval_ns, heartbeat_interval_ns, encoding, on_update,
            ),
            name=f"gnmi-sub-{sub_id[:8]}",
            daemon=True,
        )
        self._thread.start()
        logger.info("Started subscription %s",sub_id)

    # --------------------------------------------------------------#
    #  Public helpers                                               #
    # --------------------------------------------------------------#
    def get(self, timeout: Optional[float] = None) -> dict:
        return self._queue.get(timeout=timeout)

    def stop(self) -> None:
        self._stop_event.set()
        self._thread.join(2)
        logger.info("Stopped subscription %s", self.sub_id)

    # --------------------------------------------------------------#
    #  Internal loop                                                #
    # --------------------------------------------------------------#
    def _run(
        self,
        path_list: List[str],
        mode: str,
        sample_interval_ns: int,
        heartbeat_interval_ns: Optional[int],
        encoding: str,
        on_update: Optional[Callable[[dict], None]],
    ) -> None:  # pragma: no cover
        """
        Try each candidate path until the Subscribe RPC succeeds.

        * Top level mode: STREAM / ONCE / POLL  (here we always stream)
        * Per entry mode: SAMPLE / ON_CHANGE
        """
        # --- pick the correct gNMI enum strings -------------------------
        top_mode = "stream"  # explicitly stream mode
        entry_mode = mode.lower()

        for path in path_list:
            if self._stop_event.is_set():
                break

            entry: dict = {"path": path}

            if entry_mode == "sample":
                entry["mode"] = "sample"
                entry["sample_interval"] = sample_interval_ns
            elif entry_mode == "on_change":
                entry["mode"] = "on_change"
                if heartbeat_interval_ns:
                    entry["heartbeat_interval"] = heartbeat_interval_ns
            else:
                entry["mode"] = "target_defined"

            request = {
                "subscription": [entry],
                "mode": top_mode,
                "encoding": encoding,
            }
            logger.debug("Subscription %s to be requested: %s", self.sub_id, request)
            try:
                logger.debug("Sub %s attempting path %s", self.sub_id, path)
                for stream in self.gnmi_client.subscribe(request):
                    msg_dict = MessageToDict(stream)
                    # logger.debug("Stream: %s", msg_dict)
                    
                    # Process any update data
                    if msg_dict.get('update'): # 'update' in msg_dict:
                        logger.debug("Sub %s got update data", self.sub_id)
                        if on_update:
                            on_update(msg_dict)
                        else:
                            self._queue.put(msg_dict)
                            # logger.debug("The update added in queue  → %s", msg_dict)
                    # Put a dummy update if syncResponse is received to prevent timeout
                    elif msg_dict.get('syncResponse'):  # 'syncResponse' in msg_dict:
                        logger.debug("Sub %s received sync response", self.sub_id)
                        # Optional: put a notification about the sync
                        if not on_update:
                            self._queue.put({"type": "sync_response", "value": True})
                    else:
                        logger.warning("Sub %s received unknown message: %s", self.sub_id, msg_dict)

            except grpc.RpcError as err:
                if err.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    logger.warning("Path '%s' rejected (%s) -- trying next",
                                  path, err.details())
                    continue
                logger.exception("Subscription %s hit gRPC error: %s",
                                self.sub_id, err)
                break

            except Exception as exc:  # pylint: disable=broad-except
                logger.exception("Subscription %s failed: %s", self.sub_id, exc)
                break

        logger.info("Subscription thread %s terminating", self.sub_id)
