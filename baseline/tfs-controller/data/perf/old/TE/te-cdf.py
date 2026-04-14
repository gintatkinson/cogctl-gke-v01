# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import matplotlib.pyplot as plt

flow_creation_us = [
    3.007065,3.007783,3.010780,3.007374,3.006519,3.006668,3.006303,3.006463,3.006758,3.007992,3.012198,3.001413,
    3.007289,3.006241,3.007523,3.007569,3.006643,3.006255,3.007058,3.006111,3.006918,3.007972,3.006829,3.007378,
    3.007666,3.003071,3.006774,3.006060,3.006731,3.005812
]

flow_update_us = [
    3.005123,3.004228,3.003897,3.006692,3.003767,3.003749,3.004626,3.004333,3.004449,3.003895,3.004092,3.003979,
    3.005099,3.213206,3.004625,3.004707,3.004187,3.004609,3.003885,3.004064,3.004308,3.004280,3.004423,3.211980,
    3.004138,3.004394,3.004018,3.004747,3.005719,3.003656
]

n_bins = 10
fig, ax = plt.subplots(figsize=(8, 8))

# plot the cumulative histograms
n, bins, _ = ax.hist(flow_creation_us, n_bins, density=True, histtype='step', cumulative=True, label='FlowCreate')
print(n, bins)
n, bins, _ = ax.hist(flow_update_us, n_bins, density=True, histtype='step', cumulative=True, label='FlowUpdate')
print(n, bins)

ax.grid(True)
ax.legend(loc='lower center')
ax.set_title('TE Flow Management Delay')
ax.set_xlabel('seconds')
ax.set_ylabel('Likelihood of occurrence')
plt.savefig('te-perf-eval.png', dpi = (600)) 
plt.show()
