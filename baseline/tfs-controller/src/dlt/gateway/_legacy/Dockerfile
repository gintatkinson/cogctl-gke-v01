# Copyright 2022-2024 ETSI OSG/SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
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

FROM zenika/kotlin:1.4-jdk12

# Make working directory move to it and copy DLT Gateway code
RUN mkdir -p /var/teraflow/dlt/gateway
WORKDIR /var/teraflow/dlt/gateway
COPY src/dlt/gateway/. ./

# Make directory for proto files and copy them
RUN mkdir proto
COPY proto/*.proto ./proto/

# Build DLT Gateway
RUN ./gradlew build

EXPOSE 50051

# Create entrypoint.sh script
RUN echo "#!/bin/sh" > /entrypoint.sh
RUN echo "echo 195.37.154.24 peer0.org1.example.com >> /etc/hosts" >> /entrypoint.sh
RUN echo "echo 195.37.154.24 peer0.org2.example.com >> /etc/hosts" >> /entrypoint.sh
RUN echo "echo 195.37.154.24 orderer0.example.com   >> /etc/hosts" >> /entrypoint.sh
RUN echo "cd /var/teraflow/dlt/gateway" >> /entrypoint.sh
RUN echo "./gradlew runServer" >> /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Gateway entry point
ENTRYPOINT ["sh", "/entrypoint.sh"]
