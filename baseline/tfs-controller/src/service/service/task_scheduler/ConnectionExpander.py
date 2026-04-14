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

from typing import Dict, List, Optional, Tuple
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.proto.context_pb2 import Connection, Empty, EndPointId, Link
from context.client.ContextClient import ContextClient

class ConnectionExpander:
    def __init__(self) -> None:
        self.context_client = ContextClient()
        self.endpointkey_to_link : Dict[Tuple[str, str], Link] = dict()
        self.refresh_links()
    
    def refresh_links(self) -> None:
        links = self.context_client.ListLinks(Empty())
        for link in links.links:
            for link_endpoint_id in link.link_endpoint_ids:
                device_uuid = link_endpoint_id.device_id.device_uuid.uuid
                endpoint_uuid = link_endpoint_id.endpoint_uuid.uuid
                endpoint_key = (device_uuid, endpoint_uuid)
                self.endpointkey_to_link[endpoint_key] = link

    def get_link_from_endpoint_id(self, endpoint_id : EndPointId, raise_if_not_found : bool = False) -> Optional[Link]:
        device_uuid = endpoint_id.device_id.device_uuid.uuid
        endpoint_uuid = endpoint_id.endpoint_uuid.uuid
        endpoint_key = (device_uuid, endpoint_uuid)
        link = self.endpointkey_to_link.get(endpoint_key)
        if link is None and raise_if_not_found:
            str_endpoint_id = grpc_message_to_json_string(endpoint_id)
            raise Exception('Link for Endpoint({:s}) not found'.format(str_endpoint_id))
        return link

    def get_links(self, connection : Connection) -> List[Link]:
        path_links = list()
        last_link_uuid = None
        for endpoint_id in connection.path_hops_endpoint_ids:
            link = self.get_link_from_endpoint_id(endpoint_id, raise_if_not_found=True)
            link_uuid = link.link_id.link_uuid.uuid
            if last_link_uuid is None or last_link_uuid != link_uuid:
                path_links.append(link)
                last_link_uuid = link_uuid
        return path_links

    def get_endpoints_traversed(self, connection : Connection) -> List[EndPointId]:
        path_endpoint_ids = list()
        last_link_uuid = None
        for endpoint_id in connection.path_hops_endpoint_ids:
            link = self.get_link_from_endpoint_id(endpoint_id, raise_if_not_found=True)
            link_uuid = link.link_id.link_uuid.uuid
            if last_link_uuid is None or last_link_uuid != link_uuid:
                for link_endpoint_id in link.link_endpoint_ids:
                    path_endpoint_ids.append(link_endpoint_id)
                last_link_uuid = link_uuid
        return path_endpoint_ids
