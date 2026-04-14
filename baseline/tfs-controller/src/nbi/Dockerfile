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
    apt-get --yes --quiet --quiet install g++ git build-essential cmake libpcre2-dev python3-dev python3-cffi && \
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

# Get common Python packages
# Note: this step enables sharing the previous Docker build steps among all the Python components
WORKDIR /var/teraflow
COPY common_requirements.in common_requirements.in
RUN pip-compile --quiet --output-file=common_requirements.txt common_requirements.in
RUN python3 -m pip install -r common_requirements.txt

# Add common files into working directory
WORKDIR /var/teraflow/common
COPY src/common/. ./
RUN rm -rf proto

# Create proto sub-folder, copy .proto files, and generate Python code
RUN mkdir -p /var/teraflow/common/proto
WORKDIR /var/teraflow/common/proto
RUN touch __init__.py
COPY proto/*.proto ./
RUN python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. *.proto
RUN rm *.proto
RUN find . -type f -exec sed -i -E 's/^(import\ .*)_pb2/from . \1_pb2/g' {} \;

# Create component sub-folders, get specific Python packages
RUN mkdir -p /var/teraflow/nbi
WORKDIR /var/teraflow/nbi
COPY src/nbi/requirements.in requirements.in
RUN pip-compile --quiet --output-file=requirements.txt requirements.in
RUN python3 -m pip install -r requirements.txt

# Add component files into working directory
WORKDIR /var/teraflow
COPY src/nbi/. nbi/
COPY src/context/__init__.py context/__init__.py
COPY src/context/client/. context/client/
COPY src/device/__init__.py device/__init__.py
COPY src/device/client/. device/client/
COPY src/osm_client/__init__.py osm_client/__init__.py
COPY src/osm_client/client/. osm_client/client/
COPY src/pluggables/__init__.py pluggables/__init__.py
COPY src/pluggables/client/. pluggables/client/
COPY src/qkd_app/__init__.py qkd_app/__init__.py
COPY src/qkd_app/client/. qkd_app/client/
COPY src/qos_profile/__init__.py qos_profile/__init__.py
COPY src/qos_profile/client/. qos_profile/client/
COPY src/service/__init__.py service/__init__.py
COPY src/service/client/. service/client/
COPY src/simap_connector/__init__.py simap_connector/__init__.py
COPY src/simap_connector/client/. simap_connector/client/
COPY src/slice/__init__.py slice/__init__.py
COPY src/slice/client/. slice/client/
COPY src/vnt_manager/__init__.py vnt_manager/__init__.py
COPY src/vnt_manager/client/. vnt_manager/client/
RUN mkdir -p /var/teraflow/tests/tools
COPY src/tests/tools/mock_osm/. tests/tools/mock_osm/

# Start the service
# NOTE: Configured single worker to prevent issues with multi-worker synchronization. To be invetsigated.
ENTRYPOINT ["gunicorn", "--workers", "8", "--worker-class", "eventlet", "--bind", "0.0.0.0:8080", "nbi.service.app:app"]
