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

# PHASE 2: Gold Master Refactor
FROM us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs/python-base:2026-04-22

# Add component code
WORKDIR /var/teraflow
COPY src/device/ device/

# Standardize logs and entrypoint
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "-m", "device.service"]
