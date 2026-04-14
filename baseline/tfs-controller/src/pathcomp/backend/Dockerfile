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

# Multi-stage Docker image build

# Stage 1
FROM ubuntu:20.04 AS builder
ARG DEBIAN_FRONTEND=noninteractive

# Install build software
RUN apt-get update -y && apt-get install build-essential curl gcovr libglib2.0-dev -y
RUN apt-get install valgrind -y

# mkdir
RUN mkdir -p /var/teraflow

# Define working directory
WORKDIR /var/teraflow

# Copy every file in working directory
COPY src/pathcomp/backend/. ./

# Build release version and move it to bin folder
RUN make release
RUN mkdir /var/teraflow/bin
RUN mv pathComp /var/teraflow/bin

# Build code coverage version
RUN make clean
RUN make coverage
#RUN make debug

EXPOSE 8081

# builder defines coverage version of pathcomp by default
# coverage entrypoint:
ENTRYPOINT [ "./pathComp-cvr", "config/pathcomp.conf", "screen_only" ]
# debug entrypoint:
#ENTRYPOINT [ "./pathComp-dbg", "config/pathcomp.conf", "screen_only" ]
# debug entrypoint with memory tracking:
#ENTRYPOINT [ "valgrind", "--leak-check=full", "--show-leak-kinds=all", "--track-origins=yes", "--show-error-list=yes", "./pathComp-dbg", "config/pathcomp.conf", "screen_only" ]


# Stage 2
FROM ubuntu:20.04 AS release
ARG DEBIAN_FRONTEND=noninteractive

# Install build software
RUN apt-get update -y && apt-get install curl libglib2.0-bin -y

# mkdir
RUN mkdir -p /var/teraflow/config

# Define working directory
WORKDIR /var/teraflow

# We make four distinct layers so if there are application changes the library layers can be re-used
COPY --from=builder /var/teraflow/bin/pathComp .
COPY --from=builder /var/teraflow/config/pathcomp.conf ./config
COPY --from=builder /var/teraflow/tests/. ./tests

# release entrypoint:
ENTRYPOINT [ "./pathComp", "config/pathcomp.conf", "screen_only" ]
