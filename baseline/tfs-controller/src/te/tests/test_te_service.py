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

# Simple script to test GRPC calls to the TE service.
# First get the TE service IP using:
# > kubectl -n tfs get services
# Change it in this script and run with:
# > PYTHONPATH=./src python test_te_service.py

import json, sys
from common.proto.context_pb2 import ConfigActionEnum, Service, ServiceStatusEnum, ServiceTypeEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from service.client.TEServiceClient import TEServiceClient

#  {"name": "", 
#     "service_config": {
#        "config_rules": [
#           {
#             "action": "CONFIGACTION_SET",
#              "custom": {
#                 "resource_key": "/lsp-fw",
#                 "resource_value": "{\n\"binding_label\": 1111,\n\"symbolic_name\": \"foo\"\n}"}},
#           {
#              "action": "CONFIGACTION_SET",
#              "custom": {
#                 "resource_key": "/lsp-bw",
#                 "resource_value": "{\n\"binding_label\": 6666,\n\"symbolic_name\": \"bar\"\n}"}}]},
#        "service_constraints": [],
#        "service_endpoint_ids": [
#           {"device_id": {"device_uuid": {"uuid": "RT1"}}, "endpoint_uuid": {"uuid": "eth-src"}},
#           {"device_id": {"device_uuid": {"uuid": "RT6"}}, "endpoint_uuid": {"uuid": "eth-dst"}}],
#        "service_id": {"context_id": {"context_uuid": {"uuid": "admin"}},
#        "service_uuid": {"uuid": "2c025055-bf6c-4250-8560-cf62f2d29e72"}},
#        "service_status": {"service_status": "SERVICESTATUS_PLANNED"},
#        "service_type": "SERVICETYPE_TE"}

service = Service()
service.service_id.context_id.context_uuid.uuid = 'admin'
service.service_id.service_uuid.uuid = 'test-te-service'

service.service_type = ServiceTypeEnum.SERVICETYPE_TE
service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED

# SRC Endpoint:
src_endpoint_id = service.service_endpoint_ids.add()
src_endpoint_id.device_id.device_uuid.uuid = 'RT1'
src_endpoint_id.endpoint_uuid.uuid = 'eth-src'

# DST Endpoint:
dst_endpoint_id = service.service_endpoint_ids.add()
dst_endpoint_id.device_id.device_uuid.uuid = 'RT6'
dst_endpoint_id.endpoint_uuid.uuid = 'eth-dst'

# # Capacity SLA
# sla_capacity = service.service_constraints.add()
# sla_capacity.sla_capacity.capacity_gbps = 10.0

# # Latency SLA
# sla_latency = service.service_constraints.add()
# sla_latency.sla_latency.e2e_latency_ms = 20.0

# Example config rules:
config_rule_1 = service.service_config.config_rules.add()
config_rule_1.action = ConfigActionEnum.CONFIGACTION_SET
config_rule_1.custom.resource_key = '/lsp-fw'
config_rule_1.custom.resource_value = json.dumps({
    'binding_label': 1111, 'symbolic_name': "foo"
})

config_rule_2 = service.service_config.config_rules.add()
config_rule_2.action = ConfigActionEnum.CONFIGACTION_SET
config_rule_2.custom.resource_key = '/lsp-bw'
config_rule_2.custom.resource_value = json.dumps({
    'binding_label': 6666, 'symbolic_name': "bar"
})

def main():
    # Connect:
    te_service_client = TEServiceClient(host='XXX.XXX.XXX.XXX', port=10030)

    # RequestLSP
    print('request:', grpc_message_to_json_string(service))
    service_status = te_service_client.RequestLSP(service)
    print('response:', grpc_message_to_json_string(service_status))

    # DeleteLSP
    #print('request:', grpc_message_to_json_string(service))
    #service_status = te_service_client.DeleteLSP(service)
    #print('response:', grpc_message_to_json_string(service_status))

    # Close:
    te_service_client.close()

    return 0

if __name__ == '__main__':
    sys.exit(main())
