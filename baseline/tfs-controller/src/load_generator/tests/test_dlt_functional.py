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

import sys
from common.proto.context_pb2 import (
    DEVICEOPERATIONALSTATUS_ENABLED, Device, DeviceId, LinkId, ServiceId, SliceId, TopologyId)
from common.proto.dlt_connector_pb2 import DltDeviceId, DltLinkId, DltServiceId, DltSliceId
from common.tools.object_factory.Device import json_device
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from dlt.connector.client.DltConnectorClient import DltConnectorClient

def record_device_to_dlt(
    dlt_connector_client : DltConnectorClient, domain_id : TopologyId, device_id : DeviceId, delete : bool = False
) -> None:
    dlt_device_id = DltDeviceId()
    dlt_device_id.topology_id.CopyFrom(domain_id)       # pylint: disable=no-member
    dlt_device_id.device_id.CopyFrom(device_id)         # pylint: disable=no-member
    dlt_device_id.delete = delete
    dlt_connector_client.RecordDevice(dlt_device_id)

def record_link_to_dlt(
    dlt_connector_client : DltConnectorClient, domain_id : TopologyId, link_id : LinkId, delete : bool = False
) -> None:
    dlt_link_id = DltLinkId()
    dlt_link_id.topology_id.CopyFrom(domain_id)         # pylint: disable=no-member
    dlt_link_id.link_id.CopyFrom(link_id)               # pylint: disable=no-member
    dlt_link_id.delete = delete
    dlt_connector_client.RecordLink(dlt_link_id)

def record_service_to_dlt(
    dlt_connector_client : DltConnectorClient, domain_id : TopologyId, service_id : ServiceId, delete : bool = False
) -> None:
    dlt_service_id = DltServiceId()
    dlt_service_id.topology_id.CopyFrom(domain_id)      # pylint: disable=no-member
    dlt_service_id.service_id.CopyFrom(service_id)      # pylint: disable=no-member
    dlt_service_id.delete = delete
    dlt_connector_client.RecordService(dlt_service_id)

def record_slice_to_dlt(
    dlt_connector_client : DltConnectorClient, domain_id : TopologyId, slice_id : SliceId, delete : bool = False
) -> None:
    dlt_slice_id = DltSliceId()
    dlt_slice_id.topology_id.CopyFrom(domain_id)        # pylint: disable=no-member
    dlt_slice_id.slice_id.CopyFrom(slice_id)            # pylint: disable=no-member
    dlt_slice_id.delete = delete
    dlt_connector_client.RecordSlice(dlt_slice_id)

def main():
    context_client = ContextClient()
    dlt_connector_client = DltConnectorClient()

    device = Device(**json_device('test-device', 'packet-router', DEVICEOPERATIONALSTATUS_ENABLED))
    device_id = context_client.SetDevice(device)

    dlt_domain_id = TopologyId(**json_topology_id('dlt-func-test'))
    record_device_to_dlt(dlt_connector_client, dlt_domain_id, device_id, delete=False)

    return 0

if __name__ == '__main__':
    sys.exit(main())
