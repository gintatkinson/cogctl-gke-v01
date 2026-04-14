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


curl http://172.17.0.1:8888/restconf/data/openconfig-platform:components
curl http://172.17.0.1:8888/restconf/data/openconfig-interfaces:interfaces
curl http://172.17.0.1:8888/restconf/data/openconfig-acl:acl

curl -X POST -d @scripts/data/reject_30435_from_all.json http://127.0.0.1:8888/restconf/data/openconfig-acl:acl
curl -X POST -d @scripts/data/accept_30435_from_10_0_2_2.json http://127.0.0.1:8888/restconf/data/openconfig-acl:acl
curl -X POST -d @scripts/data/accept_30435_from_10_0_2_10.json http://127.0.0.1:8888/restconf/data/openconfig-acl:acl

curl http://172.17.0.1:8888/restconf/data/openconfig-acl:acl

curl -X DELETE http://172.17.0.1:8888/restconf/data/openconfig-acl:acl/acl-sets/acl-set=accept-30435-from-10-0-2-2
curl -X DELETE http://172.17.0.1:8888/restconf/data/openconfig-acl:acl/acl-sets/acl-set=accept-30435-from-10-0-2-10
curl -X DELETE http://172.17.0.1:8888/restconf/data/openconfig-acl:acl/acl-sets/acl-set=reject-30435-from-all

curl http://172.17.0.1:8888/restconf/data/openconfig-acl:acl
