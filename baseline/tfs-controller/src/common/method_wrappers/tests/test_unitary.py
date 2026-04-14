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

import grpc, logging, time
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
METRICS_POOL = MetricsPool('Context', 'RPC')

def test_database_instantiation():
    class TestServiceServicerImpl:
        @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
        def GetTopology(self, request, grpc_context : grpc.ServicerContext):
            print('doing funny things')
            time.sleep(0.1)
            return 'done'

    tssi = TestServiceServicerImpl()
    tssi.GetTopology(1, 2)

    for metric_name,metric in METRICS_POOL.metrics.items():
        if 'TFS_CONTEXT_RPC_GETTOPOLOGY_' not in metric_name: continue
        print(metric_name, metric._child_samples())
    raise Exception()
