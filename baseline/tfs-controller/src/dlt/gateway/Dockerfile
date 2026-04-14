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

# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory in the container
WORKDIR /usr/dltApp

# Create proto directory before copying the .proto files
RUN mkdir -p ./proto

# Copy package.json and package-lock.json
COPY src/dlt/gateway/dltApp/package*.json ./

# Copy tsconfig.json
COPY src/dlt/gateway/dltApp/tsconfig*.json ./
# Copy the proto folder contents
COPY proto/acl.proto ./proto/acl.proto
COPY proto/kpi_sample_types.proto ./proto/kpi_sample_types.proto
COPY proto/context.proto ./proto/context.proto
COPY proto/dlt_gateway.proto ./proto/dlt_gateway.proto

# Copy the src folder
COPY src/dlt/gateway/dltApp/src/ ./src

# Install dependencies
RUN npm install

# Expose the port that the gRPC service runs on
EXPOSE 50051

# Command to run the service
CMD ["node", "src/dltGateway.js"]
