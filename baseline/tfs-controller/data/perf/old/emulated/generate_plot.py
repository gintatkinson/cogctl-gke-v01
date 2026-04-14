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
    EXP1_DEVICE_DRIVER_EMU_L2NM       = 'exp1-dev-drv-emu-l2nm'
    EXP1_DEVICE_DRIVER_EMU_L3NM       = 'exp1-dev-drv-emu-l3nm'
    EXP1_DEVICE_DRIVER_TAPI           = 'exp1-dev-drv-tapi'
    EXP1_SERVICE_HANDLER_EMU_L2NM     = 'exp1-svc-hdl-l2nm-emu'
    EXP1_SERVICE_HANDLER_EMU_L3NM     = 'exp1-svc-hdl-l3nm-emu'
    EXP1_SERVICE_HANDLER_TAPI         = 'exp1-svc-hdl-tapi'
    EXP1_COMP_PATHCOMP_RPC_COMPUTE    = 'exp1-pathcomp-rpc-compute'

    EXP2_DEVICE_DRIVER_EMU            = 'exp2-device-driver-emu'
    EXP2_SERVICE_HANDLER_EMU_L2NM     = 'exp2-svc-hdl-l2nm-emu'
    EXP2_SERVICE_HANDLER_EMU_L3NM     = 'exp2-svc-hdl-l3nm-emu'

    EXP2_COMP_CONTEXT_DEVICE_RPCS     = 'exp2-context-device-rpcs'
    EXP2_COMP_CONTEXT_LINK_RPCS       = 'exp2-context-link-rpcs'
    EXP2_COMP_CONTEXT_SERVICE_RPCS    = 'exp2-context-service-rpcs'
    EXP2_COMP_CONTEXT_SLICE_RPCS      = 'exp2-context-slice-rpcs'
    EXP2_COMP_CONTEXT_TOPOLOGY_RPCS   = 'exp2-context-topology-rpcs'
    EXP2_COMP_CONTEXT_CONNECTION_RPCS = 'exp2-context-connection-rpcs'
    EXP2_COMP_DEVICE_RPCS             = 'exp2-device-rpcs'
    EXP2_COMP_SERVICE_RPCS            = 'exp2-service-rpcs'
    EXP2_COMP_SLICE_RPCS              = 'exp2-slice-rpcs'
    EXP2_COMP_PATHCOMP_RPCS           = 'exp2-pathcomp-rpcs'
    EXP2_COMP_DLT_RPCS                = 'exp2-dlt-rpcs'

plot_name = PlotName.__members__.get(sys.argv[1])
if plot_name is None: raise Exception('Unsupported plot: {:s}'.format(str(plot_name)))

PLOTS = {
    PlotName.EXP1_DEVICE_DRIVER_EMU_L2NM: (
        'Device Driver - Emulated (using L2NM services)', '0.0001-1', [
            ('GetConfig',    [0,27,252,212,160,261,26,2,3,9,19,11,2,1,0,0,0]),
            ('SetConfig',    [575,56,112,78,61,82,8,0,2,5,5,0,1,    0,0,0,0]),
            ('DeleteConfig', [606,96,150,66,29,31,5,0,0,1,1,0,    0,0,0,0,0]),
        ]),

    PlotName.EXP1_DEVICE_DRIVER_EMU_L3NM: (
        'Device Driver - Emulated (using L3NM services)', '0.0001-1', [
            ('GetConfig',    [0,1,40,83,127,460,132,24,13,39,36,31,9,5,1,0,0]),
            ('SetConfig',    [487,29,110,52,55,171,48,6,6,15,12,8,0,1, 0,0,0]),
            ('DeleteConfig', [510,86,79,43,26,120,70,20,6,9,15,8,5,3,  0,0,0]),
        ]),

    PlotName.EXP1_DEVICE_DRIVER_TAPI: (
        #'Device Driver - TAPI', '0.0001-1', [
        #    ('GetConfig',    [0,0,0,0,0,0,0,0,0,1,1,3,10,159,14, 0,0]),
        #    ('SetConfig',    [92,3,1,0,0,0,0,6,11,47,13,13,0,0,0,0,0]),
        #    ('DeleteConfig', [90,0,0,0,0,0,3,14,25,35,6,11,2,0,0,0,0]),
        #]),
        'Device Driver - TAPI', '0.0001-1', [
            ('GetConfig',    [0,0,0,0,0,0,0,0,0,1,1,3,10,159,14, 0,0]),
            ('SetConfig',    [0,0,0,0,0,0,0,6,11,47,13,13,0,0,0,0,0]),
            ('DeleteConfig', [0,0,0,0,0,0,3,14,25,35,6,11,2,0,0,0,0]),
        ]),

    PlotName.EXP1_SERVICE_HANDLER_EMU_L2NM: (
        'Service Handler - L2NM Emulated', '0.001-100', [
            ('SetEndpoint',    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,41,35,12,1,0]),
            ('DeleteEndpoint', [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,3,29,45,7,0,0]),
        ]),

    PlotName.EXP1_SERVICE_HANDLER_EMU_L3NM: (
        'Service Handler - L3NM Emulated', '0.001-100', [
            ('SetEndpoint',    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,8,27,29,15,11]),
            ('DeleteEndpoint', [0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,2,0,6,22,29,18,11]),
        ]),

    PlotName.EXP1_SERVICE_HANDLER_TAPI: (
        'Service Handler - TAPI', '0.001-100', [
            ('SetEndpoint',    [0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,79,2,0,0,0,0]),
            ('DeleteEndpoint', [0,0,0,0,0,0,0,0,0,0,0,0,5,0,3,1,73,12,0,0,0,0]),
        ]),

    PlotName.EXP1_COMP_PATHCOMP_RPC_COMPUTE: (
        'PathComp - Compute RPC', '0.01-5', [
            ('Compute (using L2NM services)', [0,0,20,32,14,22,0]),
            ('Compute (using L3NM services)', [0,1,1,10,17,59,2]),
            ('Compute (using TAPI services)', [3,70,10,3,2,6,0]),
        ]),

    PlotName.EXP2_DEVICE_DRIVER_EMU: (
        'Device Driver - Emulated', '0.0001-0.25', [
            ('GetConfig',    [0,21,198,247,190,332,28,5,3,7,14,8,0,0]),
            ('SetConfig',    [558,61,139,85,57,117,22,1,2,4,1,5,1,0]),
            ('DeleteConfig', [573,123,142,63,30,78,24,2,2,8,5,2,0,0]),
        ]),

    PlotName.EXP2_SERVICE_HANDLER_EMU_L2NM: (
        'Service Handler - L2NM Emulated', '0.001-100', [
            ('SetEndpoint',    [0,0,0,0,0,0,0,0,0,0,0,0,2,18,15,4,1,2,2,0,0,0]),
            ('DeleteEndpoint', [0,0,0,0,0,0,0,0,0,0,0,1,0,20,20,5,1,0,0,0,0,0]),
        ]),

    PlotName.EXP2_SERVICE_HANDLER_EMU_L3NM: (
        'Service Handler - L3NM Emulated', '0.001-100', [
            ('SetEndpoint',    [0,0,0,0,0,0,0,0,0,0,0,0,0,13,24,2,5,4,1,0,0,0]),
            ('DeleteEndpoint', [0,0,0,0,0,0,0,0,0,0,0,0,0,11,27,7,3,1,0,0,0,0]),
        ]),

    PlotName.EXP2_COMP_CONTEXT_DEVICE_RPCS: (
        'Context RPCs', '0.001-7.5', [
            ('GetDevice',        [0,0,0,0,6,130,348,305,382,578,76,7,6,0,0,0,0]),
            ('ListDevices',      [0,0,0,0,0,0,0,0,0,4,37,43,8,2,0,0,0]),
            ('SetDevice',        [0,0,0,0,0,42,236,158,179,380,46,9,0,0,0,0,0]),
        ]),

    PlotName.EXP2_COMP_CONTEXT_LINK_RPCS: (
        'Context RPCs', '0.001-7.5', [
            ('GetLink',          [0,1,9,5,1,1,0,0,0,0,0,0,0,0,0,0,0]),
            ('ListLinks',        [0,0,0,0,0,5,20,23,27,17,2,0,0,0,0,0,0]),
        ]),

    PlotName.EXP2_COMP_CONTEXT_SERVICE_RPCS: (
        'Context RPCs', '0.001-7.5', [
            ('GetService',       [124,120,42,55,80,167,62,34,14,33,9,2,1,0,0,0,0]),
            ('ListServices',     [0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0]),
            ('RemoveService',    [0,0,3,18,15,29,13,5,1,4,1,0,0,0,0,0,0]),
            ('SetService',       [6,90,59,51,63,165,70,32,5,12,8,2,0,0,0,0,0]),
        ]),

    PlotName.EXP2_COMP_CONTEXT_SLICE_RPCS: (
        'Context RPCs', '0.001-7.5', [
            ('GetSlice',         [30,75,48,24,32,118,56,34,12,19,8,2,0,0,0,0,0]),
            ('ListSlices',       [0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]),
            ('RemoveSlice',      [0,0,2,10,8,14,8,2,1,2,0,0,0,0,0,0,0]),
            ('SetSlice',         [6,29,22,18,21,70,25,12,11,13,1,0,0,0,0,0,0]),
            ('UnsetSlice',       [0,12,12,8,1,3,6,3,1,2,0,0,0,0,0,0,0]),
        ]),

    PlotName.EXP2_COMP_CONTEXT_TOPOLOGY_RPCS: (
        'Context RPCs', '0.001-7.5', [
            ('GetTopology',      [72,11,0,0,0,2,6,1,0,1,1,0,0,0,0,0,0]),
            ('ListTopologies',   [0,0,0,0,5,38,25,10,6,10,0,0,0,0,0,0,0]),
            ('ListTopologyIds',  [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
        ]),

    PlotName.EXP2_COMP_CONTEXT_CONNECTION_RPCS: (
        'Context RPCs', '0.001-7.5', [
            ('ListConnections',  [13,21,5,19,23,145,46,27,10,15,4,2,0,1,0,0,0]),
            ('ListContextIds',   [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
            ('RemoveConnection', [0,0,17,17,12,23,11,2,2,6,0,0,0,0,0,0,0]),
            ('SetConnection',    [0,0,17,26,9,18,4,7,2,5,4,2,0,0,0,0,0]),
        ]),

    PlotName.EXP2_COMP_DEVICE_RPCS: (
        'Device RPCs', '0.001-7.5', [
            ('AddDevice',       [0,0,0,0,0,0,0,1,2,4,0,0,0,0,0,0,0]),
            ('ConfigureDevice', [0,0,0,0,0,0,0,0,2,140,367,243,127,143,19,9,5]),
        ]),

    PlotName.EXP2_COMP_SERVICE_RPCS: (
        'Service RPCs', '0.001-7.5', [
            ('CreateService',   [0,0,0,9,11,32,13,10,4,7,3,2,1,0,0,0,0]),
            ('UpdateService',   [0,0,0,0,0,0,0,0,0,0,0,0,0,19,41,15,18]),
            ('DeleteService',   [0,0,0,0,0,0,0,0,0,0,0,0,1,23,45,21,6]),
        ]),

    PlotName.EXP2_COMP_SLICE_RPCS: (
        'Slice RPCs', '0.001-7.5', [
            ('CreateSlice',     [0,0,0,0,0,4,5,4,10,11,6,2,1,0,0,0,0]),
            ('UpdateSlice',     [0,0,0,0,0,0,0,0,0,0,0,0,0,6,20,10,10]),
            ('DeleteSice',      [0,0,0,0,0,0,0,0,0,0,0,0,0,9,21,15,2]),
        ]),

    PlotName.EXP2_COMP_PATHCOMP_RPCS: (
        'PathComp RPCs', '0.001-7.5', [
            ('Compute',         [0,0,0,0,0,0,0,0,0,0,13,43,22,14,0,0,0]),
        ]),

    PlotName.EXP2_COMP_DLT_RPCS: (
        'DLT RPCs', '0.001-7.5', [
            ('RecordDevice',    [0,0,0,0,0,0,0,1,4,5,6,6,0,26,71,94,306]),
            ('RecordLink',      [0,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0]),
            ('RecordService',   [0,0,0,0,0,0,0,0,0,0,0,0,0,5,15,30,184]),
            ('RecordSlice',     [0,0,0,0,0,0,0,0,2,3,1,2,1,6,19,23,82]),
        ]),
}

BINS_RANGES = {
    '0.0001-100'    : [0, 0.0001, 0.00025, 0.0005, 0.00075, 0.001, 0.0025, 0.005, 0.0075,
                        0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10,
                        25, 50, 75, 100, 200],
    '0.0001-1'      : [0, 0.0001, 0.00025, 0.0005, 0.00075, 0.001, 0.0025, 0.005, 0.0075,
                        0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1],
    '0.0001-0.25'   : [0, 0.0001, 0.00025, 0.0005, 0.00075, 0.001, 0.0025, 0.005, 0.0075,
                        0.01, 0.025, 0.05, 0.075, 0.1, 0.25],
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
ax.legend(loc='best')
ax.set_title(PLOTS[plot_name][0])
ax.set_xlabel('seconds')
ax.set_ylabel('Likelihood of occurrence')
plt.xscale('log')
plt.savefig('{:s}.png'.format(plot_name.value), dpi = (600)) 
plt.show()
