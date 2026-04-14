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

# Set Python to show logs as they occur
ENV PYTHONUNBUFFERED=0

# Get Python dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools wheel
RUN python3 -m pip install https://github.com/freeconf/lang/releases/download/v0.1.0-alpha/freeconf-0.1.0-py3-none-any.whl
RUN fc-lang-install -v

# Create component sub-folders, and copy content
RUN mkdir -p /var/mock_qkd_node/
WORKDIR /var/mock_qkd_node
COPY ./yang ./yang
COPY ./startup.json ./startup.json
COPY ./qkd_node.py ./qkd_node.py

# Start the service
ENTRYPOINT ["python", "qkd_node.py"]
