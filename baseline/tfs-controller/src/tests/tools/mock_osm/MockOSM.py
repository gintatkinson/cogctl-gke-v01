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

import logging
from .WimconnectorIETFL2VPN import WimconnectorIETFL2VPN

LOGGER = logging.getLogger(__name__)

class MockOSM:
    def __init__(self, url, mapping, username, password):
        wim = {'wim_url': url}
        wim_account = {'user': username, 'password': password}
        config = {'mapping_not_needed': False, 'service_endpoint_mapping': mapping}
        self.wim = WimconnectorIETFL2VPN(wim, wim_account, config=config)
        self.conn_info = {} # internal database emulating OSM storage provided to WIM Connectors

    def create_connectivity_service(self, service_type, connection_points):
        LOGGER.info('[create_connectivity_service] service_type={:s}'.format(str(service_type)))
        LOGGER.info('[create_connectivity_service] connection_points={:s}'.format(str(connection_points)))
        self.wim.check_credentials()
        result = self.wim.create_connectivity_service(service_type, connection_points)
        LOGGER.info('[create_connectivity_service] result={:s}'.format(str(result)))
        service_uuid, conn_info = result
        self.conn_info[service_uuid] = conn_info
        return service_uuid

    def get_connectivity_service_status(self, service_uuid):
        LOGGER.info('[get_connectivity_service] service_uuid={:s}'.format(str(service_uuid)))
        conn_info = self.conn_info.get(service_uuid)
        if conn_info is None: raise Exception('ServiceId({:s}) not found'.format(str(service_uuid)))
        LOGGER.info('[get_connectivity_service] conn_info={:s}'.format(str(conn_info)))
        self.wim.check_credentials()
        result = self.wim.get_connectivity_service_status(service_uuid, conn_info=conn_info)
        LOGGER.info('[get_connectivity_service] result={:s}'.format(str(result)))
        return result

    def edit_connectivity_service(self, service_uuid, connection_points):
        LOGGER.info('[edit_connectivity_service] service_uuid={:s}'.format(str(service_uuid)))
        LOGGER.info('[edit_connectivity_service] connection_points={:s}'.format(str(connection_points)))
        conn_info = self.conn_info.get(service_uuid)
        if conn_info is None: raise Exception('ServiceId({:s}) not found'.format(str(service_uuid)))
        LOGGER.info('[edit_connectivity_service] conn_info={:s}'.format(str(conn_info)))
        self.wim.edit_connectivity_service(service_uuid, conn_info=conn_info, connection_points=connection_points)

    def delete_connectivity_service(self, service_uuid):
        LOGGER.info('[delete_connectivity_service] service_uuid={:s}'.format(str(service_uuid)))
        conn_info = self.conn_info.get(service_uuid)
        if conn_info is None: raise Exception('ServiceId({:s}) not found'.format(str(service_uuid)))
        LOGGER.info('[delete_connectivity_service] conn_info={:s}'.format(str(conn_info)))
        self.wim.check_credentials()
        self.wim.delete_connectivity_service(service_uuid, conn_info=conn_info)
