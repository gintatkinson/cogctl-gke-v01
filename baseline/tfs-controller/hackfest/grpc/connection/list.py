#! /usr/bin/env python3
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
import connection_pb2
import sys


# Iterates though all connections in the ConnectionList and prints info about them.
def ListConnections(connectionList):
  for connection in connectionList.connection:
    print("connectionID:", connection.connectionId)
    print("  sourceNode:", connection.sourceNode)
    print("  targetNode:", connection.targetNode)
    print("  sourcePort:", connection.sourcePort)  
    print("  targetPort:", connection.targetPort)
    print("  bandwidth:", connection.bandwidth)       
    if connection.layerProtocolName == connection_pb2.Connection.ETH:
      print("  layerProtocolName:ETH")
    elif connection.layerProtocolName == connection_pb2.Connection.OPTICAL:
      print("  layerProtocolName:OPTICAL")


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "CONNECTION_FILE")
    sys.exit(-1)
  
  connectionList = connection_pb2.ConnectionList()
  
  # Read the existing address book.
  with open(sys.argv[1], "rb") as f:
    connectionList.ParseFromString(f.read())
  
  ListConnections(connectionList)
