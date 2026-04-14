# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import grpc

import topologyService_pb2
import topologyService_pb2_grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
try:
  raw_input          # Python 2
except NameError:
  raw_input = input  # Python 3


def getTopology():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = topologyService_pb2_grpc.TopologyServiceStub(channel)
        response = stub.GetTopology(google_dot_protobuf_dot_empty__pb2.Empty())
    print("TopologyService client received: " + str(response) )

if __name__ == '__main__':
    getTopology()
