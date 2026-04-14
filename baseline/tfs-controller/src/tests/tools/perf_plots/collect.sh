#!/bin/bash
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

# First choose experiment to report in:
#   src/tests/tools/perf_plots/experiments/Experiment.py
# ... and set prometheus host and port in a new file named as:
#   src/tests/tools/perf_plots/AddressesCredentials.py
# LoadGen_Requests requires manual settings in the script.

PYTHONPATH=./src python -m tests.tools.perf_plots.Component_RPC_Methods
PYTHONPATH=./src python -m tests.tools.perf_plots.Device_Driver_Details
PYTHONPATH=./src python -m tests.tools.perf_plots.Device_Driver_Methods
PYTHONPATH=./src python -m tests.tools.perf_plots.Service_Handler_Methods
PYTHONPATH=./src python -m tests.tools.perf_plots.LoadGen_Requests
