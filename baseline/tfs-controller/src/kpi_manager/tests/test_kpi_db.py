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
from kpi_manager.database.KpiDB import KpiDB
from kpi_manager.database.KpiModel import Kpi as KpiModel

LOGGER = logging.getLogger(__name__)

def test_verify_databases_and_Tables():
    LOGGER.info('>>> test_verify_Tables : START <<< ')
    kpiDBobj = KpiDB(KpiModel)
    # kpiDBobj.drop_database()
    # kpiDBobj.verify_tables()
    kpiDBobj.create_database()
    kpiDBobj.create_tables()
    kpiDBobj.verify_tables()
