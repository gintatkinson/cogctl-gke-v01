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

# Install dependencies
RUN apt-get --yes --quiet --quiet update && \
    apt-get --yes --quiet --quiet install git build-essential cmake libpcre2-dev python3-dev python3-cffi && \
    rm -rf /var/lib/apt/lists/*

# Download, build and install libyang. Note that APT package is outdated
# - Ref: https://github.com/CESNET/libyang
# - Ref: https://github.com/CESNET/libyang-python/
RUN mkdir -p /var/libyang
RUN git clone https://github.com/CESNET/libyang.git /var/libyang
WORKDIR /var/libyang
RUN git fetch
RUN git checkout v2.1.148
RUN mkdir -p /var/libyang/build
WORKDIR /var/libyang/build
RUN cmake -D CMAKE_BUILD_TYPE:String="Release" ..
RUN make
RUN make install
RUN ldconfig

# Set Python to show logs as they occur
ENV PYTHONUNBUFFERED=0

# Get generic Python packages
RUN python3 -m pip install --upgrade 'pip==25.2'
RUN python3 -m pip install --upgrade 'setuptools==79.0.0' 'wheel==0.45.1'
RUN python3 -m pip install --upgrade 'pip-tools==7.3.0'

# Get specific Python packages
RUN mkdir -p /var/teraflow/
WORKDIR /var/teraflow/
COPY src/common/tools/rest_conf/server/requirements.in ./requirements.in
RUN pip-compile --quiet --output-file=requirements.txt requirements.in
RUN python3 -m pip install -r requirements.txt

# Get component files
RUN mkdir -p /var/teraflow/common/tools/
WORKDIR /var/teraflow/
COPY src/common/tools/rest_api/ ./common/tools/rest_api/
COPY src/common/tools/rest_conf/ ./common/tools/rest_conf/
COPY src/tests/tools/mock_nce_fan_ctrl/nce_fan_ctrl/*.py ./nce_fan_ctrl/
COPY src/tests/tools/mock_nce_fan_ctrl/yang/. ./yang/
COPY src/tests/tools/mock_nce_fan_ctrl/startup.json ./startup.json

# Configure RESTCONF Server
ENV RESTCONF_PREFIX="/restconf"
ENV YANG_SEARCH_PATH="./yang"
ENV STARTUP_FILE="./startup.json"

# Configure Flask for production
ENV FLASK_ENV="production"

# Start the service
ENTRYPOINT ["gunicorn", "--workers", "1", "--worker-class", "eventlet", "--bind", "0.0.0.0:8080", "nce_fan_ctrl.app:app"]
