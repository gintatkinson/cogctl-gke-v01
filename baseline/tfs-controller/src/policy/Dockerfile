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

FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /var/teraflow
COPY proto/  proto/
COPY src/policy/  src/policy/
RUN mvn -f src/policy/pom.xml clean package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /var/teraflow
COPY --from=builder /var/teraflow/src/policy/target/quarkus-app/ /var/teraflow/quarkus-app/
ENTRYPOINT ["java", "-jar", "/var/teraflow/quarkus-app/quarkus-run.jar"]
