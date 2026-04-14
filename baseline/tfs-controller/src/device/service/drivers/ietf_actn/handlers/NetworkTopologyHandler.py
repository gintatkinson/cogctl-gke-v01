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
from typing import Dict, List, Optional
from common.Constants import DEFAULT_TOPOLOGY_NAME
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import (
    DEVICEDRIVER_UNDEFINED, DEVICEOPERATIONALSTATUS_DISABLED,
    DEVICEOPERATIONALSTATUS_ENABLED
)
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from device.service.driver_api.ImportTopologyEnum import (
    ImportTopologyEnum, get_import_topology
)


LOGGER = logging.getLogger(__name__)


class NetworkTopologyHandler:
    def __init__(self, rest_conf_client : RestConfClient, **settings) -> None:
        self._rest_conf_client = rest_conf_client
        self._subpath_root = '/ietf-network:networks'
        self._subpath_item = self._subpath_root + '/network={network_id:s}'

        # Options are:
        #    disabled --> just import endpoints as usual
        #    devices  --> imports sub-devices but not links connecting them.
        #                 (a remotely-controlled transport domain might exist between them)
        #    topology --> imports sub-devices and links connecting them.
        #                 (not supported by XR driver)
        self._import_topology = get_import_topology(settings, default=ImportTopologyEnum.TOPOLOGY)


    def get(self, network_id : Optional[str] = None) -> List[Dict]:
        if network_id is None: network_id = DEFAULT_TOPOLOGY_NAME
        endpoint = self._subpath_item.format(network_id=network_id)
        reply = self._rest_conf_client.get(endpoint)

        if 'ietf-network:network' not in reply:
            raise Exception('Malformed reply. "ietf-network:network" missing')
        networks = reply['ietf-network:network']

        if len(networks) == 0:
            MSG = '[get] Network({:s}) not found; returning'
            LOGGER.debug(MSG.format(str(network_id)))
            return list()

        if len(networks) > 1:
            MSG = '[get] Multiple occurrences for Network({:s}); returning'
            LOGGER.debug(MSG.format(str(network_id)))
            return list()

        network = networks[0]

        MSG = '[get] import_topology={:s}'
        LOGGER.debug(MSG.format(str(self._import_topology)))

        result = list()
        if self._import_topology == ImportTopologyEnum.DISABLED:
            LOGGER.debug('[get] abstract controller; returning')
            return result

        device_type = DeviceTypeEnum.EMULATED_PACKET_SWITCH.value
        endpoint_type = ''
        if 'network-types' in network:
            nnt = network['network-types']
            if 'ietf-te-topology:te-topology' in nnt:
                nnt_tet = nnt['ietf-te-topology:te-topology']
                if 'ietf-otn-topology:otn-topology' in nnt_tet:
                    device_type = DeviceTypeEnum.OPTICAL_FGOTN.value
                    endpoint_type = 'optical'
                elif 'ietf-eth-te-topology:eth-tran-topology' in nnt_tet:
                    device_type = DeviceTypeEnum.EMULATED_PACKET_SWITCH.value
                    endpoint_type = 'copper'
                elif 'ietf-l3-unicast-topology:l3-unicast-topology' in nnt_tet:
                    device_type = DeviceTypeEnum.EMULATED_PACKET_ROUTER.value
                    endpoint_type = 'copper'

        for node in network['node']:
            node_id = node['node-id']
            
            node_name = node_id
            node_is_up = True
            if 'ietf-te-topology:te' in node:
                nte = node['ietf-te-topology:te']

                if 'oper-status' in nte:
                    node_is_up = nte['oper-status'] == 'up'

                if 'te-node-attributes' in nte:
                    ntea = nte['te-node-attributes']
                    if 'name' in ntea:
                        node_name = ntea['name']

            device_url = '/devices/device[{:s}]'.format(node_id)
            device_data = {
                'uuid': node_id,
                'name': node_name,
                'type': device_type,
                'status': DEVICEOPERATIONALSTATUS_ENABLED if node_is_up else DEVICEOPERATIONALSTATUS_DISABLED,
                'drivers': [DEVICEDRIVER_UNDEFINED],
            }
            result.append((device_url, device_data))

            for tp in node['ietf-network-topology:termination-point']:
                tp_id = tp['tp-id']

                tp_name = tp_id
                if 'ietf-te-topology:te' in tp:
                    tpte = tp['ietf-te-topology:te']
                    if 'name' in tpte:
                        tp_name = tpte['name']

                tp_ip_addr = '0.0.0.0'
                if 'ietf-te-topology:te-tp-id' in tp:
                    tp_ip_addr = tp['ietf-te-topology:te-tp-id']

                if node_name == 'O-PE1' and tp_name == '200':
                    site_location = 'access'
                elif node_name == 'O-PE2' and tp_name == '200':
                    site_location = 'cloud'
                else:
                    site_location = 'transport'

                endpoint_url = '/endpoints/endpoint[{:s}, {:s}]'.format(node_id, tp_id)
                endpoint_settings = {
                    'uuid'          : tp_id,
                    'name'          : tp_name,
                    'type'          : endpoint_type,
                    'address_ip'    : tp_ip_addr,
                    'address_prefix': '24',
                    'mtu'           : '1500',
                    'site_location' : site_location,
                }

                outer_tag_vlan_range : Optional[str] = (
                    tp
                    .get('ietf-eth-te-topology:eth-svc', dict())
                    .get('supported-classification', dict())
                    .get('vlan-classification', dict())
                    .get('outer-tag', dict())
                    .get('vlan-range')
                )
                if outer_tag_vlan_range is not None:
                    RE_NUMBER = re.compile(r'[0-9]+')
                    if RE_NUMBER.match(outer_tag_vlan_range) is not None:
                        endpoint_settings['vlan_tag'] = int(outer_tag_vlan_range)

                endpoint_data = {
                    'device_uuid': node_id,
                    'uuid': tp_id,
                    'name': tp_name,
                    'type': endpoint_type,
                    'settings': endpoint_settings,
                }
                result.append((endpoint_url, endpoint_data))

        if self._import_topology == ImportTopologyEnum.DEVICES:
            LOGGER.debug('[get] devices only; returning')
            return result

        for link in network['ietf-network-topology:link']:
            link_uuid = link['link-id']
            link_src  = link['source']
            link_dst  = link['destination']
            link_src_dev_id = link_src['source-node']
            link_src_ep_id  = link_src['source-tp']
            link_dst_dev_id = link_dst['dest-node']
            link_dst_ep_id  = link_dst['dest-tp']

            link_url = '/links/link[{:s}]'.format(link_uuid)
            link_endpoint_ids = [
                (link_src_dev_id, link_src_ep_id),
                (link_dst_dev_id, link_dst_ep_id),
            ]
            link_data = {
                'uuid': link_uuid,
                'name': link_uuid,
                'endpoints': link_endpoint_ids,
            }
            result.append((link_url, link_data))

        LOGGER.debug('[get] topology; returning')
        return result
