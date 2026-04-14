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

import threading
import logging
from kpi_value_writer.service.MetricWriterToPrometheus import MetricWriterToPrometheus
from kpi_value_writer.tests.test_messages import create_kpi_descriptor_request, create_kpi_value_request

LOGGER = logging.getLogger(__name__)

def test_metric_writer_to_prometheus():
    LOGGER.info(' >>> test_metric_writer_to_prometheus START <<< ')
    metric_writer_obj = MetricWriterToPrometheus()
    metric_writer_obj.create_and_expose_cooked_kpi(
                        create_kpi_descriptor_request(),
                        create_kpi_value_request()
        )
