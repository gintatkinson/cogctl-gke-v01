#!/bin/bash
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


wget -q -O- http://localhost:8001
wget -q -O- http://localhost:8002

curl -X POST -d @scripts/data/oc_acl_block_8001.json http://127.0.0.1:8888/restconf/data/openconfig-acl:acl
curl -X POST -d @scripts/data/oc_acl_block_8002.json http://127.0.0.1:8888/restconf/data/openconfig-acl:acl
curl -X POST -d @scripts/data/oc_acl_multi_rule.json http://127.0.0.1:8888/restconf/data/openconfig-acl:acl

wget -q -O- http://localhost:8001
wget -q -O- http://localhost:8002

curl -X DELETE http://172.17.0.1:8888/restconf/data/openconfig-acl:acl/acl-sets/acl-set=drop-8001-host
curl -X DELETE http://172.17.0.1:8888/restconf/data/openconfig-acl:acl/acl-sets/acl-set=drop-8002-ext
