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


# Enable eventlet for async networking
# NOTE: monkey_patch needs to be executed before importing any other module.
import eventlet
eventlet.monkey_patch()

#pylint: disable=wrong-import-position
import logging, requests, socketio
from nbi.service.NbiApplication import NbiApplication
from .Constants import NBI_SERVICE_BASE_URL
from .HeartbeatClientNamespace import HeartbeatClientNamespace
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    nbi_application, do_rest_get_request
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def test_restapi_get_healthz(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    nbi_application.dump_configuration()
    do_rest_get_request('/healthz', expected_status_codes={requests.codes['OK']})


def test_websocket_get_heartbeat(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    nbi_application.dump_configuration()

    heartbeat_client_namespace = HeartbeatClientNamespace()

    sio = socketio.Client(logger=True, engineio_logger=True)
    sio.register_namespace(heartbeat_client_namespace)
    sio.connect(NBI_SERVICE_BASE_URL)
    #sio.send('Hello WebSocket!', namespace='/heartbeat')
    #sio.emit('message', 'Hello WebSocket!', namespace='/heartbeat')
    sio.sleep(10)
    #sio.wait()
    sio.shutdown()

    # Ensure we get ~1 heartbeat/second
    num_heartbeats_received = heartbeat_client_namespace.num_heartbeats_received
    assert num_heartbeats_received >= 9 and num_heartbeats_received <= 11
