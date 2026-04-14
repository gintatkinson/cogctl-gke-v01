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

import logging, socketio

LOGGER = logging.getLogger(__name__)

class HeartbeatClientNamespace(socketio.ClientNamespace):
    def __init__(self):
        self._num_heartbeats_received = 0
        super().__init__(namespace='/heartbeat')

    @property
    def num_heartbeats_received(self): return self._num_heartbeats_received

    def on_connect(self):
        LOGGER.info('[HeartbeatClientNamespace::on_connect] Connected')

    def on_disconnect(self, reason):
        MSG = '[HeartbeatClientNamespace::on_disconnect] Disconnected!, reason: {:s}'
        LOGGER.info(MSG.format(str(reason)))

    def on_uptime(self, data):
        MSG = '[HeartbeatClientNamespace::on_uptime] data={:s}'
        LOGGER.info(MSG.format(str(data)))

        assert 'uptime_seconds' in data, 'Missing "uptime_seconds" in response'
        uptime = data['uptime_seconds']
        assert isinstance(uptime, (int, float)), '"uptime_seconds" is not a number'

        MSG = '[HeartbeatClientNamespace::on_uptime] Heartbeat: server uptime {:f} sec.'
        LOGGER.info(MSG.format(uptime))

        self._num_heartbeats_received += 1
