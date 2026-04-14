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

FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends git iproute2 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
# NOTE: Ryu 4.34 expects eventlet.wsgi.ALREADY_HANDLED, which disappears in Eventlet ≥ 0.30.3.
RUN pip install --no-cache-dir "setuptools" "wheel" "git+https://github.com/faucetsdn/ryu.git@v4.34" "eventlet<0.30.3"

#COPY apps/ /opt/ryu-apps/  # Copy Ryu Apps, if any
WORKDIR /opt/ryu-apps

# --- OpenFlow & Ryu REST API ports ---
EXPOSE 6653/tcp 8080/tcp

CMD ["ryu-manager", "--verbose", "--observe-links", "ryu.app.ofctl_rest", "ryu.app.gui_topology.gui_topology"]
