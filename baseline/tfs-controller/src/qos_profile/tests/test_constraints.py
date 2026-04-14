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

import logging
from google.protobuf.json_format import MessageToDict

from common.proto.qos_profile_pb2 import QoDConstraintsRequest
from common.tools.grpc.Tools import grpc_message_to_json_string
from qos_profile.client.QoSProfileClient import QoSProfileClient

from .conftest import create_qos_profile_from_json

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

qos_profile_data = {
  "qos_profile_id": "0afc905f-f1f0-4ae2-9925-9df17140b8bf",
  "name": "QCI_2_voice",
  "description": "QoS profile for game streaming",
  "status": "ACTIVE",
  "targetMinUpstreamRate": {
    "value": 5,
    "unit": "bps"
  },
  "maxUpstreamRate": {
    "value": 5,
    "unit": "bps"
  },
  "maxUpstreamBurstRate": {
    "value": 5,
    "unit": "bps"
  },
  "targetMinDownstreamRate": {
    "value": 5,
    "unit": "bps"
  },
  "maxDownstreamRate": {
    "value": 5,
    "unit": "bps"
  },
  "maxDownstreamBurstRate": {
    "value": 5,
    "unit": "bps"
  },
  "minDuration": {
    "value": 5,
    "unit": "Minutes"
  },
  "maxDuration": {
    "value": 6,
    "unit": "Minutes"
  },
  "priority": 5,
  "packetDelayBudget": {
    "value": 5,
    "unit": "Minutes"
  },
  "jitter": {
    "value": 5,
    "unit": "Minutes"
  },
  "packetErrorLossRate": 3
}


def test_get_constraints(qos_profile_client: QoSProfileClient):
    qos_profile = create_qos_profile_from_json(qos_profile_data)
    qos_profile_created = qos_profile_client.CreateQoSProfile(qos_profile)
    LOGGER.info('qos_profile_data = {:s}'.format(grpc_message_to_json_string(qos_profile_created)))
    constraints = qos_profile_client.GetConstraintsFromQoSProfile(
        QoDConstraintsRequest(
            qos_profile_id=qos_profile.qos_profile_id, start_timestamp=1726063284.25332, duration=86400
        )
    )
    assert len(constraints.constraints) == 2

    constraint_1 = constraints.constraints[0]
    assert constraint_1.WhichOneof('constraint') == 'qos_profile'
    assert constraint_1.qos_profile.qos_profile_id == qos_profile.qos_profile_id
    assert constraint_1.qos_profile.qos_profile_name == 'QCI_2_voice'

    constraint_2 = constraints.constraints[1]
    assert constraint_2.WhichOneof('constraint') == 'schedule'
    assert constraint_2.schedule.start_timestamp == 1726063284.25332
    assert constraint_2.schedule.duration_days == 1

    qos_profile_client.DeleteQoSProfile(qos_profile.qos_profile_id)
