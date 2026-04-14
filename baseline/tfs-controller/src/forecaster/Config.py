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

import os

# FORECAST_TO_HISTORY_RATIO indicates the size of the trainset.
# For example a history ratio of 10 would imply that the train-set will be 10 times bigger
# than the forecast period and the test-set.
DEFAULT_FORECAST_TO_HISTORY_RATIO = 10
FORECAST_TO_HISTORY_RATIO = int(os.environ.get('FORECAST_TO_HISTORY_RATIO', DEFAULT_FORECAST_TO_HISTORY_RATIO))
