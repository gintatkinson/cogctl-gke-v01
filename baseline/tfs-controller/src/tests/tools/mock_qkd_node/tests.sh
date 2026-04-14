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


echo "[QKD-NODE-01] Reading data on startup..."
curl http://172.254.250.101:8080/restconf/data/etsi-qkd-sdn-node:
echo
echo

echo "[QKD-NODE-01] Updating location (from root)..."
curl -X PATCH -d '{"qkd_node":{"qkdn_location_id":"new-loc"}}' http://172.254.250.101:8080/restconf/data/etsi-qkd-sdn-node:
echo

echo "[QKD-NODE-01] Reading after update 1..."
curl http://172.254.250.101:8080/restconf/data/etsi-qkd-sdn-node:
echo
echo

echo "[QKD-NODE-01] Updating location (from path)..."
curl -X PATCH -d '{"qkdn_location_id":"new-loc-2"}' http://172.254.250.101:8080/restconf/data/etsi-qkd-sdn-node:qkd_node
echo

echo "[QKD-NODE-01] Reading final value..."
curl http://172.254.250.101:8080/restconf/data/etsi-qkd-sdn-node:
echo
echo

