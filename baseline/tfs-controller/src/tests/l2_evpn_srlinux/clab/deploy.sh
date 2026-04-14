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


# Ensure you get elevated privileges
sudo true

# Check if the topology exists and destroy it to build our new topology again
sudo containerlab destroy --topo evpn01.clab.yml
echo "Topology destroyed successfully."

sudo rm -rf clab-evpn01 .evpn01.clab.yml.bak

# Build the new topology
sudo containerlab deploy --topo evpn01.clab.yml
echo "Topology deployed successfully."
