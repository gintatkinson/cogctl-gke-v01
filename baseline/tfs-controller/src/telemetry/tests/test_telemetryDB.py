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
from telemetry.database.Telemetry_DB import TelemetryDB
from telemetry.database.TelemetryModel import Collector as CollectorModel

LOGGER = logging.getLogger(__name__)

def test_verify_databases_and_tables():
    LOGGER.info('>>> test_verify_databases_and_tables : START <<< ')
    TelemetryDBobj = TelemetryDB(CollectorModel)
    # TelemetryDBobj.drop_database()
    # TelemetryDBobj.verify_tables()
    TelemetryDBobj.create_database()
    TelemetryDBobj.create_tables()
    TelemetryDBobj.verify_tables()
