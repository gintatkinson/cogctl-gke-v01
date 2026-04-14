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

import uuid
import json
from common.proto.kpi_manager_pb2        import KpiId
from common.proto.analytics_frontend_pb2 import ( AnalyzerOperationMode, AnalyzerId,
                                                Analyzer, AnalyzerFilter )

def create_analyzer_id():
    _create_analyzer_id                  = AnalyzerId()
    _create_analyzer_id.analyzer_id.uuid = str(uuid.uuid4())
    # _create_analyzer_id.analyzer_id.uuid = "efef4d95-1cf1-43c4-9742-95c283ddd7a6"
    # _create_analyzer_id.analyzer_id.uuid = "1e22f180-ba28-4641-b190-2287bf446666"
    return _create_analyzer_id

def create_analyzer():
    _create_analyzer                              = Analyzer()

    _create_analyzer.analyzer_id.analyzer_id.uuid = str(uuid.uuid4())
    # _create_analyzer.analyzer_id.analyzer_id.uuid = "1e22f180-ba28-4641-b190-2287bf446666"
    _create_analyzer.algorithm_name               = "Test_new_Threshold"
    _create_analyzer.operation_mode               = AnalyzerOperationMode.ANALYZEROPERATIONMODE_STREAMING
    
    # input IDs to analyze
    _kpi_id = KpiId()

    # _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _kpi_id.kpi_id.uuid              = "6e22f180-ba28-4641-b190-2287bf448888"
    _create_analyzer.input_kpi_ids.append(_kpi_id)

    # _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _kpi_id.kpi_id.uuid              = "1e22f180-ba28-4641-b190-2287bf446666"
    _create_analyzer.input_kpi_ids.append(_kpi_id)

    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _create_analyzer.input_kpi_ids.append(_kpi_id)
    
    # output IDs after analysis
    _kpi_id = KpiId()

    # _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _kpi_id.kpi_id.uuid              = "6e22f180-ba28-4641-b190-2287bf181818"
    _create_analyzer.output_kpi_ids.append(_kpi_id)

    # _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _kpi_id.kpi_id.uuid              = "1e22f180-ba28-4641-b190-2287bf441616"
    _create_analyzer.output_kpi_ids.append(_kpi_id)

    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _create_analyzer.output_kpi_ids.append(_kpi_id)

    # parameter
    # _threshold_dict = {
    #     'mean_value'  :[20, 30], 'min_value'   :[00, 10], 'max_value' :[45, 50],
    #     'first_value' :[00, 10], 'last_value'  :[40, 50], 'std_value' :[00, 10]
    #     }
    _threshold_dict = {
        "task_type": Handlers.AGGREGATION_HANDLER.value,
        "task_parameter": [
            {"last":  [40, 80], "variance": [300, 500]},
            {"count": [2,  4],  "max":      [70,  100]},
            {"min":   [10, 20], "avg":      [50,  70]},
        ],
    }

    _create_analyzer.parameters['thresholds']      = json.dumps(_threshold_dict)
    _create_analyzer.parameters['window_size']     = "0"   #   slider window size in seconds (Total time for aggeration processing) 
    _create_analyzer.parameters['window_slider']   = "0"    #   should be less than window size
    _create_analyzer.parameters['store_aggregate'] = str(False)  #   TRUE to store. No implemented yet

    # duration of the analyzer
    _create_analyzer.duration_s = 90

    # batch window size
    _create_analyzer.batch_min_duration_s = 20
    _create_analyzer.batch_max_duration_s = 50

    # batch size
    _create_analyzer.batch_min_size       = 5
    _create_analyzer.batch_max_size       = 10
    
    return _create_analyzer

def create_analyzer_filter():
    _create_analyzer_filter           = AnalyzerFilter()

    _analyzer_id_obj                  = AnalyzerId()
    # _analyzer_id_obj.analyzer_id.uuid = str(uuid.uuid4())
    _analyzer_id_obj.analyzer_id.uuid = "efef4d95-1cf1-43c4-9742-95c283ddd7a6"
    _create_analyzer_filter.analyzer_id.append(_analyzer_id_obj)

    _create_analyzer_filter.algorithm_names.append('Test_Aggergate_and_Threshold')

    # _input_kpi_id_obj                 = KpiId()
    # _input_kpi_id_obj.kpi_id.uuid     = str(uuid.uuid4())
    # _create_analyzer_filter.input_kpi_ids.append(_input_kpi_id_obj)
    # another input kpi Id
    # _input_kpi_id_obj.kpi_id.uuid     = str(uuid.uuid4())
    # _create_analyzer_filter.input_kpi_ids.append(_input_kpi_id_obj)

    # _output_kpi_id_obj                = KpiId()
    # _output_kpi_id_obj.kpi_id.uuid    = str(uuid.uuid4())
    # _create_analyzer_filter.output_kpi_ids.append(_output_kpi_id_obj)
    # # another output kpi Id
    # _output_kpi_id_obj.kpi_id.uuid     = str(uuid.uuid4())
    # _create_analyzer_filter.input_kpi_ids.append(_output_kpi_id_obj)

    return _create_analyzer_filter


# Added for testing to remove the dependency on the backend service
from enum import Enum
class Handlers(Enum):
    AGGREGATION_HANDLER = "AggregationHandler"
    UNSUPPORTED_HANDLER = "UnsupportedHandler"
