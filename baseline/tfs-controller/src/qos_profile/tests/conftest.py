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

import os, pytest, sqlalchemy
from _pytest.config import Config
from _pytest.terminal import TerminalReporter
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    get_env_var_name, get_service_port_grpc
)
from common.proto.context_pb2 import Uuid, QoSProfileId
from common.proto.qos_profile_pb2 import QoSProfileValueUnitPair, QoSProfile
from common.method_wrappers.Decorator import MetricsPool
from qos_profile.client.QoSProfileClient import QoSProfileClient
from qos_profile.service.QoSProfileService import QoSProfileService
from qos_profile.service.database.Engine import Engine
from qos_profile.service.database.models._Base import rebuild_database

LOCAL_HOST = '127.0.0.1'
GRPC_PORT = 10000 + int(get_service_port_grpc(ServiceNameEnum.QOSPROFILE))  # avoid privileged ports

os.environ[get_env_var_name(ServiceNameEnum.QOSPROFILE, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.QOSPROFILE, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(GRPC_PORT)

@pytest.fixture(scope='session')
def qosprofile_db(request) -> sqlalchemy.engine.Engine:   # pylint: disable=unused-argument
    _db_engine = Engine.get_engine()
    Engine.drop_database(_db_engine)
    Engine.create_database(_db_engine)
    rebuild_database(_db_engine)
    yield _db_engine

RAW_METRICS : MetricsPool = None

@pytest.fixture(scope='session')
def qosprofile_service(
    qosprofile_db : sqlalchemy.engine.Engine    # pylint: disable=redefined-outer-name
):
    global RAW_METRICS # pylint: disable=global-statement
    _service = QoSProfileService(qosprofile_db)
    RAW_METRICS = _service.qos_profile_servicer._get_metrics()
    _service.start()
    yield _service
    _service.stop()

@pytest.fixture(scope='session')
def qos_profile_client(qosprofile_service : QoSProfileService): # pylint: disable=redefined-outer-name,unused-argument
    _client = QoSProfileClient()
    yield _client
    _client.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(
    terminalreporter : TerminalReporter, exitstatus : int, config : Config  # pylint: disable=unused-argument
):
    yield

    if RAW_METRICS is not None:
        print('')
        print('Performance Results:')
        print(RAW_METRICS.get_pretty_table().get_string())

def create_qos_profile_from_json(qos_profile_data: dict) -> QoSProfile:
    def create_QoSProfileValueUnitPair(data) -> QoSProfileValueUnitPair:
        return QoSProfileValueUnitPair(value=data['value'], unit=data['unit'])
    qos_profile = QoSProfile()
    qos_profile.qos_profile_id.CopyFrom(QoSProfileId(qos_profile_id=Uuid(uuid=qos_profile_data['qos_profile_id'])))
    qos_profile.name = qos_profile_data['name']
    qos_profile.description = qos_profile_data['description']
    qos_profile.status = qos_profile_data['status']
    qos_profile.targetMinUpstreamRate.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['targetMinUpstreamRate']))
    qos_profile.maxUpstreamRate.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['maxUpstreamRate']))
    qos_profile.maxUpstreamBurstRate.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['maxUpstreamBurstRate']))
    qos_profile.targetMinDownstreamRate.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['targetMinDownstreamRate']))
    qos_profile.maxDownstreamRate.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['maxDownstreamRate']))
    qos_profile.maxDownstreamBurstRate.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['maxDownstreamBurstRate']))
    qos_profile.minDuration.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['minDuration']))
    qos_profile.maxDuration.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['maxDuration']))
    qos_profile.priority = qos_profile_data['priority']
    qos_profile.packetDelayBudget.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['packetDelayBudget']))
    qos_profile.jitter.CopyFrom(create_QoSProfileValueUnitPair(qos_profile_data['jitter']))
    qos_profile.packetErrorLossRate = qos_profile_data['packetErrorLossRate']
    return qos_profile
