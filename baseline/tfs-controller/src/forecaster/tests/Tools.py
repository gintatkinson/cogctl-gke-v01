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

import logging, math, pandas
from typing import Dict
from common.tools.object_factory.Context import json_context
from common.tools.object_factory.Device import (
    json_device_emulated_connect_rules, json_device_emulated_packet_router_disabled, json_device_id
)
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_id
from common.tools.object_factory.Link import json_link
from common.tools.object_factory.Topology import json_topology
from common.tools.timestamp.Converters import timestamp_datetime_to_int, timestamp_utcnow_to_float

LOGGER = logging.getLogger(__name__)

def read_csv(csv_file : str) -> pandas.DataFrame:
    LOGGER.info('Using Data File "{:s}"...'.format(csv_file))

    LOGGER.info('Loading...')
    df = pandas.read_csv(csv_file)
    LOGGER.info('  DONE')

    LOGGER.info('Parsing and Adapting columns...')
    if 'dataset.csv' in csv_file:
        df.rename(columns={'linkid': 'link_id', 'ds': 'timestamp', 'y': 'used_capacity_gbps'}, inplace=True)
        df[['source', 'destination']] = df['link_id'].str.split('_', expand=True)
    #elif 'dataset2.csv' in csv_file:
    #    df.drop(columns=['Unnamed: 0'], inplace=True)
    #    df.rename(columns={
    #        'target': 'destination', 'id': 'link_id', 'ds': 'timestamp', 'demandValue': 'used_capacity_gbps'
    #    }, inplace=True)
    LOGGER.info('  DONE')

    LOGGER.info('Updating timestamps...')
    df['timestamp'] = pandas.to_datetime(df['timestamp'])
    max_timestamp = timestamp_datetime_to_int(df['timestamp'].max())
    now_timestamp = timestamp_utcnow_to_float()
    df['timestamp'] = df['timestamp'] + pandas.offsets.Second(now_timestamp - max_timestamp)
    LOGGER.info('  DONE')

    LOGGER.info('Sorting...')
    df.sort_values('timestamp', ascending=True, inplace=True)
    LOGGER.info('  DONE')

    return df

def compose_descriptors(df : pandas.DataFrame, num_client_endpoints : int = 0) -> Dict:
    devices = dict()
    links = dict()

    LOGGER.info('Discovering Devices and Links...')
    #df1.groupby(['A','B']).size().reset_index().rename(columns={0:'count'})
    df_links = df[['link_id', 'source', 'destination']].drop_duplicates()
    for row in df_links.itertuples(index=False):
        #print(row)
        link_uuid = row.link_id
        src_device_uuid = row.source
        dst_device_uuid = row.destination
        src_port_uuid = row.destination
        dst_port_uuid = row.source

        if src_device_uuid not in devices:
            endpoints = set()
            for num_client_endpoint in range(num_client_endpoints):
                endpoints.add('client:{:d}'.format(num_client_endpoint))
            devices[src_device_uuid] = {'id': src_device_uuid, 'endpoints': endpoints}
        devices[src_device_uuid]['endpoints'].add(src_port_uuid)

        if dst_device_uuid not in devices:
            endpoints = set()
            for num_client_endpoint in range(num_client_endpoints):
                endpoints.add('client:{:d}'.format(num_client_endpoint))
            devices[dst_device_uuid] = {'id': dst_device_uuid, 'endpoints': endpoints}
        devices[dst_device_uuid]['endpoints'].add(dst_port_uuid)

        if link_uuid not in links:
            total_capacity_gbps = df[df.link_id==link_uuid]['used_capacity_gbps'].max()
            total_capacity_gbps = math.ceil(total_capacity_gbps / 100) * 100 # round up in steps of 100
            used_capacity_gbps  = df[df.link_id==link_uuid].used_capacity_gbps.iat[-1] # get last value
            links[link_uuid] = {
                'id': link_uuid,
                'src_dev': src_device_uuid, 'src_port': src_port_uuid,
                'dst_dev': dst_device_uuid, 'dst_port': dst_port_uuid,
                'total_capacity_gbps': total_capacity_gbps, 'used_capacity_gbps': used_capacity_gbps,
            }
    LOGGER.info('  Found {:d} devices and {:d} links...'.format(len(devices), len(links)))

    LOGGER.info('Composing Descriptors...')
    _context  = json_context('admin', name='admin')
    _topology = json_topology('admin', name='admin', context_id=_context['context_id'])
    descriptor = {
        'dummy_mode': True, # inject the descriptors directly into the Context component
        'contexts': [_context],
        'topologies': [_topology],
        'devices': [
            json_device_emulated_packet_router_disabled(
                device_uuid, name=device_uuid, endpoints=[
                    json_endpoint(json_device_id(device_uuid), endpoint_uuid, 'copper')
                    for endpoint_uuid in device_data['endpoints']
                ], config_rules=json_device_emulated_connect_rules([]))
            for device_uuid,device_data in devices.items()
        ],
        'links': [
            json_link(link_uuid, [
                json_endpoint_id(json_device_id(link_data['src_dev']), link_data['src_port']),
                json_endpoint_id(json_device_id(link_data['dst_dev']), link_data['dst_port']),
            ], name=link_uuid, total_capacity_gbps=link_data['total_capacity_gbps'],
            used_capacity_gbps=link_data['used_capacity_gbps'])
            for link_uuid,link_data in links.items()
        ],
    }
    LOGGER.info('  DONE')
    return descriptor
