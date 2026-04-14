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

"""
A mock P4Runtime service implementation.
"""

import queue
from google.rpc import code_pb2
from p4.v1 import p4runtime_pb2, p4runtime_pb2_grpc
from p4.config.v1 import p4info_pb2

try:
    from p4_client import STREAM_ATTR_ARBITRATION, STREAM_ATTR_PACKET
except ImportError:
    from device.service.drivers.p4.p4_client import STREAM_ATTR_ARBITRATION,\
        STREAM_ATTR_PACKET


class MockP4RuntimeServicerImpl(p4runtime_pb2_grpc.P4RuntimeServicer):
    """
    A P4Runtime service implementation for testing purposes.
    """

    def __init__(self):
        self.p4info = p4info_pb2.P4Info()
        self.p4runtime_api_version = "1.3.0"
        self.stored_packet_out = queue.Queue()

    def GetForwardingPipelineConfig(self, request, context):
        rep = p4runtime_pb2.GetForwardingPipelineConfigResponse()
        if self.p4info is not None:
            rep.config.p4info.CopyFrom(self.p4info)
        return rep

    def SetForwardingPipelineConfig(self, request, context):
        self.p4info.CopyFrom(request.config.p4info)
        return p4runtime_pb2.SetForwardingPipelineConfigResponse()

    def Write(self, request, context):
        return p4runtime_pb2.WriteResponse()

    def Read(self, request, context):
        yield p4runtime_pb2.ReadResponse()

    def StreamChannel(self, request_iterator, context):
        for req in request_iterator:
            if req.HasField(STREAM_ATTR_ARBITRATION):
                rep = p4runtime_pb2.StreamMessageResponse()
                rep.arbitration.CopyFrom(req.arbitration)
                rep.arbitration.status.code = code_pb2.OK
                yield rep
            elif req.HasField(STREAM_ATTR_PACKET):
                self.stored_packet_out.put(req)

    def Capabilities(self, request, context):
        rep = p4runtime_pb2.CapabilitiesResponse()
        rep.p4runtime_api_version = self.p4runtime_api_version
        return rep
