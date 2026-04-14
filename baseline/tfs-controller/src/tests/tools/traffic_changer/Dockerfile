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

## Install dependencies
#RUN apt-get --yes --quiet --quiet update && \
#    apt-get --yes --quiet --quiet install --no-install-recommends build-essential && \
#    rm -rf /var/lib/apt/lists/*

# Set Python to show logs as they occur
ENV PYTHONUNBUFFERED=0

# Get generic Python packages
RUN python3 -m pip install --upgrade 'pip==25.2'
RUN python3 -m pip install --upgrade 'setuptools==79.0.0' 'wheel==0.45.1'
RUN python3 -m pip install --upgrade 'pip-tools==7.3.0'

# Get specific Python packages
RUN mkdir -p /var/teraflow/
WORKDIR /var/teraflow/
COPY src/tests/tools/traffic_changer/requirements.in ./requirements.in
RUN pip-compile --quiet --output-file=requirements.txt requirements.in
RUN python3 -m pip install -r requirements.txt

# Get component files
COPY src/tests/tools/traffic_changer/templates ./traffic_changer/templates
COPY src/tests/tools/traffic_changer/*.py ./traffic_changer/

# Configure Flask for production
ENV FLASK_ENV="production"

# Start the service
ENTRYPOINT ["gunicorn", "--workers", "1", "--worker-class", "eventlet", "--bind", "0.0.0.0:8080", "traffic_changer.app:app"]
