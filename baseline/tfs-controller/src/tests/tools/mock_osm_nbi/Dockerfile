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

FROM python:3.10.16-slim

# Set Python to show logs as they occur
ENV PYTHONUNBUFFERED=0

# Get Python dependencies
RUN python3 -m pip install --upgrade 'pip==25.2'
RUN python3 -m pip install --upgrade 'setuptools==79.0.0' 'wheel==0.45.1'
RUN python3 -m pip install --upgrade 'pip-tools==7.3.0'

# Create component sub-folders, and get requirements
RUN mkdir -p /var/mock_osm_nbi
WORKDIR /var/mock_osm_nbi
COPY ./*.in .

# Get specific Python packages
RUN pip-compile --quiet --output-file=requirements.txt requirements.in
RUN python3 -m pip install -r requirements.txt

# Copy component code
COPY ./*.py .

# Start the service
WORKDIR /var
ENTRYPOINT ["python", "-m", "mock_osm_nbi"]
