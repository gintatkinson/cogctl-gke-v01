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

#!/bin/bash
cd netphony-topology/
"/home/ubuntu/downloads/apache-maven-3.8.8/bin/mvn" clean package -P bgp-ls-speaker assembly:single -DskipTests
cd ..
sudo java -jar netphony-topology/target/bgp-ls-speaker-jar-with-dependencies.jar BGP4Parameters_3.xml