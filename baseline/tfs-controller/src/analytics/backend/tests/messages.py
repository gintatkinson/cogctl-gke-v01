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
from common.proto.analytics_frontend_pb2 import ( AnalyzerOperationMode,
                                                Analyzer, AnalyzerId )

def get_kpi_id_list():
    return ["6e22f180-ba28-4641-b190-2287bf448888", "1e22f180-ba28-4641-b190-2287bf446666"]

def get_operation_list():
    return [ 'avg', 'max' ]     # possibilities ['avg', 'min', 'max', 'first', 'last', 'stdev']

def get_threshold_dict():
    threshold_dict = {
        'avg_value'    : (20, 30),
        'min_value'    : (00, 10), 
        'max_value'    : (45, 50),
        'first_value'  : (00, 10),
        'last_value'   : (40, 50),
        'stdev_value'  : (00, 10),
    }
    # Filter threshold_dict based on the operation_list
    return {
        op + '_value': threshold_dict[op+'_value'] for op in get_operation_list() if op + '_value' in threshold_dict
    }

def create_analyzer_id():
    _create_analyzer_id                  = AnalyzerId()
    # _create_analyzer_id.analyzer_id.uuid = str(uuid.uuid4())
    # _create_analyzer_id.analyzer_id.uuid = "efef4d95-1cf1-43c4-9742-95c283ddd7a6"
    _create_analyzer_id.analyzer_id.uuid = "1e22f180-ba28-4641-b190-2287bf446666"
    return _create_analyzer_id


def create_analyzer():
    _create_analyzer                              = Analyzer()
    # _create_analyzer.analyzer_id.analyzer_id.uuid = str(uuid.uuid4())
    _create_analyzer.analyzer_id.analyzer_id.uuid = "20540c4f-6797-45e5-af70-6491b49283f9"
    _create_analyzer.algorithm_name               = "Test_Aggergate_and_Threshold"
    _create_analyzer.operation_mode               = AnalyzerOperationMode.ANALYZEROPERATIONMODE_STREAMING
    
    # input IDs to analyze
    _kpi_id = KpiId()
    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _kpi_id.kpi_id.uuid              = "5716c369-932b-4a02-b4c7-6a2e808b92d7"
    _create_analyzer.input_kpi_ids.append(_kpi_id)
    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _kpi_id.kpi_id.uuid              = "8f70d908-cc48-48de-8664-dc9be2de0089"
    _create_analyzer.input_kpi_ids.append(_kpi_id)
    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _create_analyzer.input_kpi_ids.append(_kpi_id)

    # output IDs after analysis
    _kpi_id = KpiId()
    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _create_analyzer.output_kpi_ids.append(_kpi_id)
    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _create_analyzer.output_kpi_ids.append(_kpi_id)
    
    # parameter
    _threshold_dict = {
        # 'avg_value'   :(20, 30), 'min_value'   :(00, 10), 'max_value'   :(45, 50),
        'first_value' :(00, 10), 'last_value'  :(40, 50), 'stdev_value':(00, 10)}
    _create_analyzer.parameters['thresholds']      = json.dumps(_threshold_dict)
    _create_analyzer.parameters['window_size']     = "60 seconds"     # Such as "10 seconds", "2 minutes", "3 hours", "4 days" or "5 weeks" 
    _create_analyzer.parameters['window_slider']   = "30 seconds"     # should be less than window size
    _create_analyzer.parameters['store_aggregate'] = str(False)       # TRUE to store. No implemented yet

    return _create_analyzer

def create_analyzer_dask():
    _create_analyzer                              = Analyzer()
    _create_analyzer.analyzer_id.analyzer_id.uuid = str(uuid.uuid4())
    # _create_analyzer.analyzer_id.analyzer_id.uuid = "1e22f180-ba28-4641-b190-2287bf446666"
    _create_analyzer.algorithm_name               = "Test_Aggergate_and_Threshold"
    _create_analyzer.operation_mode               = AnalyzerOperationMode.ANALYZEROPERATIONMODE_STREAMING
    
    _kpi_id = KpiId()
    # input IDs to analyze
    # _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _kpi_id.kpi_id.uuid              = "6e22f180-ba28-4641-b190-2287bf448888" 
    _create_analyzer.input_kpi_ids.append(_kpi_id)
    # _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _kpi_id.kpi_id.uuid              = "1e22f180-ba28-4641-b190-2287bf446666"
    _create_analyzer.input_kpi_ids.append(_kpi_id)
    # _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _create_analyzer.input_kpi_ids.append(_kpi_id)
    # output IDs after analysis
    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _create_analyzer.output_kpi_ids.append(_kpi_id)
    _kpi_id.kpi_id.uuid              = str(uuid.uuid4())
    _create_analyzer.output_kpi_ids.append(_kpi_id)
    # parameter

    _threshold_dict = {
        'mean_latency'  :(20, 30),  'min_latency'   :(00, 10),  'max_latency' :(45, 50),#}
        'first_value'   :(00, 50),  'last_value'    :(50, 100), 'std_value' :(0, 90)}
    _create_analyzer.parameters['thresholds']      = json.dumps(_threshold_dict)
    _create_analyzer.parameters['oper_list']       = json.dumps([key.split('_')[0] for key in _threshold_dict.keys()])
    _create_analyzer.parameters['window_size']     = "10s"     # Such as "10 seconds", "2 minutes", "3 hours", "4 days" or "5 weeks" 
    _create_analyzer.parameters['window_slider']   = "5s"     # should be less than window size
    _create_analyzer.parameters['store_aggregate'] = str(False)       # TRUE to store. No implemented yet
    return _create_analyzer
