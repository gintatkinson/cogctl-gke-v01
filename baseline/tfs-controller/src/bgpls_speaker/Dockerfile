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

#
# Maven install stage
#
# ----------------------------------------------
# FROM alpine/git:latest AS repo

# WORKDIR /usr/src/app
# RUN git clone https://github.com/telefonicaid/netphony-network-protocols.git .

FROM maven:3.8.8-eclipse-temurin-17 AS build

WORKDIR /
COPY src/bgpls_speaker/service/java/netphony-topology/ netphony-topology/
COPY src/bgpls_speaker/service/java/netphony-topology/pom.xml netphony-topology/pom.xml

WORKDIR /netphony-topology/
RUN mvn clean compile -DskipTests -X
RUN mvn package assembly:single -P bgp-ls-speaker -DskipTests
WORKDIR /netphony-topology/target/
# ENTRYPOINT [ "ls" ,"-a"]
# -------------------------------------------
# jar created in  /netphony-topology/target/bgp-ls-speaker-jar-with-dependencies.jar

#
# Stage 2
#

FROM python:3.9-slim


# Install dependencies
RUN apt-get --yes --quiet --quiet update && \
    apt-get --yes --quiet --quiet install wget g++ && \
    rm -rf /var/lib/apt/lists/*

# Set Python to show logs as they occur
ENV PYTHONUNBUFFERED=0

# Download the gRPC health probe
RUN GRPC_HEALTH_PROBE_VERSION=v0.2.0 && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 && \
    chmod +x /bin/grpc_health_probe

# Get generic Python packages
RUN python3 -m pip install --upgrade 'pip==25.2'
RUN python3 -m pip install --upgrade 'setuptools==79.0.0' 'wheel==0.45.1'
RUN python3 -m pip install --upgrade 'pip-tools==7.3.0'

# Install OpenJDK-17
RUN apt-get update -y && \
    apt-get install -y openjdk-17-jre && \
    apt-get clean;

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
RUN mkdir -p /var/teraflow/bgpls_speaker
WORKDIR /var/teraflow/bgpls_speaker
COPY src/bgpls_speaker/requirements.in requirements.in
RUN pip-compile --quiet --output-file=requirements.txt requirements.in
RUN python3 -m pip install -r requirements.txt

# Java module necessary config files
WORKDIR /var/teraflow/bgpls_speaker
RUN mkdir -p /java
COPY src/bgpls_speaker/service/java/* /java/
COPY --from=build /netphony-topology/target/bgp-ls-speaker-jar-with-dependencies.jar /var/teraflow/bgpls_speaker/service/java/bgp_ls.jar

# Add component files into working directory
WORKDIR /var/teraflow
COPY src/context/__init__.py context/__init__.py
COPY src/context/client/. context/client/
COPY src/bgpls_speaker/. bgpls_speaker/

# Start the service
ENTRYPOINT ["python", "-m", "bgpls_speaker.service"]
# ENTRYPOINT [ "ls","-R" ]
