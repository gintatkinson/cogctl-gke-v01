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
import uuid

from opticalattackmanager.utils.monitor import delegate_services


LOGGER = logging.getLogger(__name__)


def test_delegate_services():
    service_list = [
        {
            "context": uuid.uuid4(),
            "service": uuid.uuid4(),
            "kpi": 10,
        }
        for _ in range(10)]
    delegate_services(
        service_list=service_list,
        start_index=0,
        end_index=9,
        host="127.0.0.1",
        port="10006",
        monitoring_interval=10,
    )
