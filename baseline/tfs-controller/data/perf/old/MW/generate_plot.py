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

import enum, sys
import numpy as np
import matplotlib.pyplot as plt

class PlotName(enum.Enum):
    DEVICE_DRIVER_MW = 'dev-drv-mw'
    SERVICE_HANDLER_MW = 'srv-hlr-mw'

plot_name = PlotName.__members__.get(sys.argv[1])
if plot_name is None: raise Exception('Unsupported plot: {:s}'.format(str(plot_name)))

PLOTS = {
    PlotName.DEVICE_DRIVER_MW: (
        #'Device Driver - MicroWave', '0.0001-100', [
        #    ('GetConfig',    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,10,172,0,1,0,0,0,0,0,0]),
        #    ('SetConfig',    [89,1,0,0,0,0,0,0,0,0,0,0,0,0,0,6,34,50,1,0,0,0,0,0,0,0]),
        #    ('DeleteConfig', [90,1,0,0,0,0,0,0,0,0,0,0,0,0,2,3,0,4,72,12,0,0,0,0,0,0]),
        #]),
        'Device Driver - MicroWave', '0.1-10', [
            ('GetConfig',    [0,1,0,10,172,0,1,0]),
            ('SetConfig',    [0,0,6,34,50,1,0,0]),
            ('DeleteConfig', [0,2,3,0,4,72,12,0]),
        ]),
    PlotName.SERVICE_HANDLER_MW: (
        'Service Handler - L2NM MicroWave', '1-100', [
            ('SetEndpoint',    [0,1,0,1,5,75,6,0]),
            ('DeleteEndpoint', [0,0,0,0,1,77,17,0]),
        ]),
}

BINS_RANGES = {
    '0.0001-100'    : [0, 0.0001, 0.00025, 0.0005, 0.00075, 0.001, 0.0025, 0.005, 0.0075,
                        0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10,
                        25, 50, 75, 100, 200],
    '0.1-10'    : [0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10],
    '0.0001-1'      : [0, 0.0001, 0.00025, 0.0005, 0.00075, 0.001, 0.0025, 0.005, 0.0075,
                        0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1],
    '0.0001-0.25'   : [0, 0.0001, 0.00025, 0.0005, 0.00075, 0.001, 0.0025, 0.005, 0.0075,
                        0.01, 0.025, 0.05, 0.075, 0.1, 0.25],
    '1-100'     : [1, 2.5, 5, 7.5, 10, 25, 50, 75, 100],
    '0.001-100'     : [0, 0.001, 0.0025, 0.005, 0.0075, 0.01, 0.025, 0.05, 0.075,
                        0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10, 25, 50, 75, 100, 200],
    '0.001-7.5'     : [0, 0.001, 0.0025, 0.005, 0.0075, 0.01, 0.025, 0.05, 0.075,
                        0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10],
    '0.01-5'        : [0, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5],
}

# plot the cumulative histogram
fig, ax = plt.subplots(figsize=(8, 8))

bins = PLOTS[plot_name][1]
if isinstance(bins, str): bins = BINS_RANGES[PLOTS[plot_name][1]]
bins = np.array(bins).astype(float)

for label, counts in PLOTS[plot_name][2]:
    counts = np.array(counts).astype(float)
    assert len(bins) == len(counts) + 1
    centroids = (bins[1:] + bins[:-1]) / 2
    ax.hist(centroids, bins=bins, weights=counts, range=(min(bins), max(bins)), density=True,
            histtype='step', cumulative=True, label=label)

ax.grid(True)
ax.legend(loc='upper left')
ax.set_title(PLOTS[plot_name][0])
ax.set_xlabel('seconds')
ax.set_ylabel('Likelihood of occurrence')
plt.xscale('log')
plt.savefig('{:s}.png'.format(plot_name.value), dpi = (600)) 
plt.show()
