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

import random, time
from common.perf_eval_method_wrapper.Decorator import MetricsPool, meter_method

EXCEPTION_RATIO = 0.05

METRICS_POOL = MetricsPool(labels={'driver': 'dummy'})

class DummyDeviceDriver:
    def __init__(self) -> None:
        pass

    @meter_method(METRICS_POOL)
    def get_config(self):
        if random.random() < EXCEPTION_RATIO: raise Exception()
        time.sleep(random.random())

    @meter_method(METRICS_POOL)
    def set_config(self):
        if random.random() < EXCEPTION_RATIO: raise Exception()
        time.sleep(random.random())

    @meter_method(METRICS_POOL)
    def del_config(self):
        if random.random() < EXCEPTION_RATIO: raise Exception()
        time.sleep(random.random())
