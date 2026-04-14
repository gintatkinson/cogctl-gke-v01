<!-- Copyright 2022-2024 ETSI OSG/SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. -->

# Example 1: TM with XML Plugin and TAPI Plugin
- First of all, compile the full-jar if you have not done so
```bash
 mvn package -P generate-full-jar
```
Execute the server
```bash
sudo java -Dlog4j.configurationFile=target/examples/log4j2.xml  -jar target/topology-1.3.4-SNAPSHOT-shaded.jar target/TM_TAPI_example1/TMConfTAPI.xml
```
Make the query
```bash
curl http://localhost:8089/config/context/topology -X GET -i -H "Content-Type: application/json" -H "Accept: application/json"
```
