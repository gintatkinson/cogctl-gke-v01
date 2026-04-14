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

from grpc import RpcError, StatusCode
import logging, pytest
from .conftest import create_qos_profile_from_json
from common.proto.context_pb2 import Empty, Uuid, QoSProfileId
from common.tools.grpc.Tools import grpc_message_to_json_string
from qos_profile.client.QoSProfileClient import QoSProfileClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

qos_profile_data = {
  "qos_profile_id": "f00406f5-8e36-4abc-a0ec-b871c7f062b7",
  "name": "QCI_1_voice",
  "description": "QoS profile for video streaming",
  "status": "ACTIVE",
  "targetMinUpstreamRate": {
    "value": 10,
    "unit": "bps"
  },
  "maxUpstreamRate": {
    "value": 10,
    "unit": "bps"
  },
  "maxUpstreamBurstRate": {
    "value": 10,
    "unit": "bps"
  },
  "targetMinDownstreamRate": {
    "value": 10,
    "unit": "bps"
  },
  "maxDownstreamRate": {
    "value": 10,
    "unit": "bps"
  },
  "maxDownstreamBurstRate": {
    "value": 10,
    "unit": "bps"
  },
  "minDuration": {
    "value": 12,
    "unit": "Minutes"
  },
  "maxDuration": {
    "value": 12,
    "unit": "Minutes"
  },
  "priority": 20,
  "packetDelayBudget": {
    "value": 12,
    "unit": "Minutes"
  },
  "jitter": {
    "value": 12,
    "unit": "Minutes"
  },
  "packetErrorLossRate": 3
}

def test_create_qos_profile(qos_profile_client: QoSProfileClient):
    qos_profile = create_qos_profile_from_json(qos_profile_data)
    qos_profile_created = qos_profile_client.CreateQoSProfile(qos_profile)
    LOGGER.info('qos_profile_data = {:s}'.format(grpc_message_to_json_string(qos_profile_created)))
    assert qos_profile == qos_profile_created


def test_failed_create_qos_profile(qos_profile_client: QoSProfileClient):
    qos_profile = create_qos_profile_from_json(qos_profile_data)
    with pytest.raises(RpcError) as exc:
      qos_profile_created = qos_profile_client.CreateQoSProfile(qos_profile)
    assert exc.value.code() == StatusCode.ALREADY_EXISTS

def test_get_qos_profile(qos_profile_client: QoSProfileClient):
    qos_profile = create_qos_profile_from_json(qos_profile_data)
    qos_profile_got = qos_profile_client.GetQoSProfile(qos_profile.qos_profile_id)
    LOGGER.info('qos_profile_data = {:s}'.format(grpc_message_to_json_string(qos_profile_got)))
    assert qos_profile == qos_profile_got

def test_get_qos_profiles(qos_profile_client: QoSProfileClient):
    qos_profile = create_qos_profile_from_json(qos_profile_data)
    qos_profiles_got = qos_profile_client.GetQoSProfiles(Empty())
    LOGGER.info('qos_profile_data = {:s}'.format(grpc_message_to_json_string(qos_profiles_got)))
    the_qos_profile = [q for q in qos_profiles_got.qos_profiles if q.qos_profile_id == qos_profile.qos_profile_id]
    assert len(the_qos_profile) == 1
    assert qos_profile == the_qos_profile[0]

def test_update_qos_profile(qos_profile_client: QoSProfileClient):
    qos_profile = create_qos_profile_from_json(qos_profile_data)
    qos_profile.packetErrorLossRate = 5
    qos_profile_updated = qos_profile_client.UpdateQoSProfile(qos_profile)
    LOGGER.info('qos_profile_data = {:s}'.format(grpc_message_to_json_string(qos_profile_updated)))
    assert qos_profile_updated.packetErrorLossRate == 5

def test_failed_delete_qos_profiles(qos_profile_client: QoSProfileClient):
    qos_profile = create_qos_profile_from_json(qos_profile_data)
    with pytest.raises(RpcError) as exc:
      qos_profiles_deleted = qos_profile_client.DeleteQoSProfile(QoSProfileId(qos_profile_id=Uuid(uuid='f8b1c625-ac01-405c-b1f7-b5ee06e16282')))
    assert exc.value.code() == StatusCode.NOT_FOUND

def test_delete_qos_profiles(qos_profile_client: QoSProfileClient):
    qos_profile = create_qos_profile_from_json(qos_profile_data)
    qos_profiles_deleted = qos_profile_client.DeleteQoSProfile(qos_profile.qos_profile_id)
    assert qos_profiles_deleted == Empty()
