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

import copy, logging
from typing import Dict, List, Optional, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, INTERDOMAIN_TOPOLOGY_NAME
from common.proto.context_pb2 import ContextId, EndPointId, Link, LinkId
from common.tools.context_queries.Link import add_link_to_topology, get_existing_link_uuids
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Link import json_link, json_link_id
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

class AbstractLink:
    def __init__(self, link_uuid : str):
        self.__context_client = ContextClient()
        self.__link_uuid : str = link_uuid
        self.__link : Optional[Link] = None
        self.__link_id : Optional[LinkId] = None

        # Dict[(device_uuid, endpoint_uuid), abstract EndPointId]
        self.__device_endpoint_to_abstract : Dict[Tuple[str, str], EndPointId] = dict()

    def to_json(self) -> Dict:
        return {
            'link_uuid' : self.__link_uuid,
            'link' : self.__link,
            'link_id' : self.__link_id,
            'device_endpoint_to_abstract' : self.__device_endpoint_to_abstract,
        }

    @property
    def uuid(self) -> str: return self.__link_uuid

    @property
    def link_id(self) -> Optional[LinkId]: return self.__link_id

    @property
    def link(self) -> Optional[Link]: return self.__link

    @staticmethod
    def compose_uuid(
        device_uuid_a : str, endpoint_uuid_a : str, device_uuid_z : str, endpoint_uuid_z : str
    ) -> str:
        # sort endpoints lexicographically to prevent duplicities
        link_endpoint_uuids = sorted([
            (device_uuid_a, endpoint_uuid_a),
            (device_uuid_z, endpoint_uuid_z)
        ])
        link_uuid = '{:s}/{:s}=={:s}/{:s}'.format(
            link_endpoint_uuids[0][0], link_endpoint_uuids[0][1],
            link_endpoint_uuids[1][0], link_endpoint_uuids[1][1])
        return link_uuid

    def initialize(self) -> bool:
        if self.__link is not None: return False

        existing_link_uuids = get_existing_link_uuids(self.__context_client)

        create = self.__link_uuid not in existing_link_uuids
        if create:
            self._create_empty()
        else:
            self._load_existing()

        # Add abstract link to topologies [INTERDOMAIN_TOPOLOGY_NAME]
        context_id = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))
        topology_uuids = [INTERDOMAIN_TOPOLOGY_NAME]
        for topology_uuid in topology_uuids:
            add_link_to_topology(self.__context_client, context_id, topology_uuid, self.__link_uuid)

        return create

    def _create_empty(self) -> None:
        link = Link(**json_link(self.__link_uuid, endpoint_ids=[]))
        self.__context_client.SetLink(link)
        self.__link = link
        self.__link_id = self.__link.link_id
    
    def _load_existing(self) -> None:
        self.__link_id = LinkId(**json_link_id(self.__link_uuid))
        self.__link = self.__context_client.GetLink(self.__link_id)

        self.__device_endpoint_to_abstract = dict()

        # for each endpoint in abstract link, populate internal data structures and mappings
        for endpoint_id in self.__link.link_endpoint_ids:
            device_uuid : str = endpoint_id.device_id.device_uuid.uuid
            endpoint_uuid : str = endpoint_id.endpoint_uuid.uuid
            self.__device_endpoint_to_abstract.setdefault((device_uuid, endpoint_uuid), endpoint_id)

    def _add_endpoint(self, device_uuid : str, endpoint_uuid : str) -> None:
        endpoint_id = self.__link.link_endpoint_ids.add()
        endpoint_id.topology_id.topology_uuid.uuid = INTERDOMAIN_TOPOLOGY_NAME
        endpoint_id.topology_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
        endpoint_id.device_id.device_uuid.uuid = device_uuid
        endpoint_id.endpoint_uuid.uuid = endpoint_uuid
        self.__device_endpoint_to_abstract.setdefault((device_uuid, endpoint_uuid), endpoint_id)

    def _remove_endpoint(self, device_uuid : str, endpoint_uuid : str) -> None:
        device_endpoint_to_abstract = self.__device_endpoint_to_abstract.get(device_uuid, {})
        endpoint_id = device_endpoint_to_abstract.pop(endpoint_uuid, None)
        if endpoint_id is not None: self.__link.link_endpoint_ids.remove(endpoint_id)

    def update_endpoints(self, link_endpoint_uuids : List[Tuple[str, str]] = []) -> bool:
        updated = False

        # for each endpoint in abstract link that is not in link; remove from abstract link
        device_endpoint_to_abstract = copy.deepcopy(self.__device_endpoint_to_abstract)
        for device_uuid, endpoint_uuid in device_endpoint_to_abstract.keys():
            if (device_uuid, endpoint_uuid) in link_endpoint_uuids: continue
            # remove endpoint_id that is not in link
            self._remove_endpoint(device_uuid, endpoint_uuid)
            updated = True

        # for each endpoint in link that is not in abstract link; add to abstract link
        for device_uuid, endpoint_uuid in link_endpoint_uuids:
            # if already added; just check endpoint type is not modified
            if (device_uuid, endpoint_uuid) in self.__device_endpoint_to_abstract: continue
            # otherwise, add it to the abstract device
            self._add_endpoint(device_uuid, endpoint_uuid)
            updated = True

        return updated
