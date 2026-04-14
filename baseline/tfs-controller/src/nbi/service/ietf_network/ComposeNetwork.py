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

import logging, re
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import TopologyDetails
from .bindings.networks.network import network
from .ComposeLink import compose_link
from .ComposeNode import compose_node
from .NameMapping import NameMappings
from .NetworkTypeEnum import NetworkTypeEnum, get_network_topology_type

LOGGER = logging.getLogger(__name__)

IGNORE_DEVICE_TYPES = {
    DeviceTypeEnum.EMULATED_CLIENT.value,
    DeviceTypeEnum.EMULATED_COMPUTER.value,
    DeviceTypeEnum.EMULATED_DATACENTER.value,
    DeviceTypeEnum.EMULATED_VIRTUAL_MACHINE.value,

    DeviceTypeEnum.EMULATED_IP_SDN_CONTROLLER,
    DeviceTypeEnum.EMULATED_MICROWAVE_RADIO_SYSTEM.value,
    DeviceTypeEnum.EMULATED_OPEN_LINE_SYSTEM.value,
    DeviceTypeEnum.EMULATED_XR_CONSTELLATION.value,
    DeviceTypeEnum.IP_SDN_CONTROLLER,
    DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM.value,
    DeviceTypeEnum.NETWORK.value,
    DeviceTypeEnum.OPEN_LINE_SYSTEM.value,
    DeviceTypeEnum.XR_CONSTELLATION.value,
}

IGNORE_DEVICE_NAMES = {
    NetworkTypeEnum.TE_OTN_TOPOLOGY: {
        'nce-t', '128.32.10.1', '128.32.33.5', '128.32.20.5', '128.32.20.1', '128.32.10.5',
    },
    NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY: {
        'nce-t',
    },
}

TE_TOPOLOGY_NAME = 'Huawei-Network'

def compose_network(ietf_network_obj : network, te_topology_name : str, topology_details : TopologyDetails) -> None:
    ietf_network_obj.te.name = TE_TOPOLOGY_NAME

    #te_topology_name = topology_details.name
    match = re.match(r'providerId\-([^\-]*)-clientId-([^\-]*)-topologyId-([^\-]*)', te_topology_name)
    if match is not None:
        provider_id, client_id, topology_id = match.groups()
        ietf_network_obj.te_topology_identifier.provider_id = int(provider_id)
        ietf_network_obj.te_topology_identifier.client_id   = int(client_id)
        ietf_network_obj.te_topology_identifier.topology_id = str(topology_id)
    else:
        ietf_network_obj.te_topology_identifier.provider_id = 10
        ietf_network_obj.te_topology_identifier.client_id   = 0
        ietf_network_obj.te_topology_identifier.topology_id = '0'

    ietf_network_obj.network_types.te_topology._set_present()
    # TODO: resolve setting of otn_topology/eth_tran_topology network type; not working in bindings.
    # See "../ManualFixes.py".
    topology_id = ietf_network_obj.te_topology_identifier.topology_id
    topology_id = {
        '1': NetworkTypeEnum.TE_OTN_TOPOLOGY.value,
        '2': NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY.value,
    }.get(topology_id, topology_id)
    network_type = get_network_topology_type(topology_id)
    if network_type == NetworkTypeEnum.TE_OTN_TOPOLOGY:
        #ietf_network_obj.network_types.te_topology.otn_topology._set_present()
        pass
    elif network_type == NetworkTypeEnum.TE_ETH_TRAN_TOPOLOGY:
        #ietf_network_obj.network_types.te_topology.eth_tran_topology._set_present()
        pass
    else:
        raise Exception('Unsupported TopologyId({:s})'.format(str(topology_id)))

    name_mappings = NameMappings()

    ignore_device_uuids = set()

    for device in topology_details.devices:
        device_uuid = device.device_id.device_uuid.uuid

        device_type = device.device_type
        if device_type in IGNORE_DEVICE_TYPES:
            ignore_device_uuids.add(device_uuid)
            continue

        device_name = device.name
        if device_name in IGNORE_DEVICE_NAMES.get(network_type, set()):
            ignore_device_uuids.add(device_uuid)
            continue

        ietf_node_obj = ietf_network_obj.node.add(device_name)
        compose_node(ietf_node_obj, device, name_mappings, network_type)

    for link in topology_details.links:
        link_device_uuids = {
            endpoint_id.device_id.device_uuid.uuid
            for endpoint_id in link.link_endpoint_ids
        }
        if len(ignore_device_uuids.intersection(link_device_uuids)) > 0:
            continue
        link_name = link.name
        ietf_link_obj = ietf_network_obj.link.add(link_name)
        compose_link(ietf_link_obj, link, name_mappings, network_type)
