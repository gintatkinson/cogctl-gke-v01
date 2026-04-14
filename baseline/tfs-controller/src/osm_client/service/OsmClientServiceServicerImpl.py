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

import grpc, logging
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import Empty
from common.proto.osm_client_pb2 import (
    CreateRequest, CreateResponse, NsiListResponse, GetRequest, GetResponse,
    DeleteRequest, DeleteResponse , NsiObject
)
from common.proto.osm_client_pb2_grpc import OsmServiceServicer
from osmclient import client
#from osmclient.common.exceptions import ClientException
from osm_client.Config import (
    OSM_ADDRESS, OSM_PORT, OSM_USERNAME, OSM_PASSWORD, OSM_PROJECT, OSM_VERIFY_TLS
)


LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('OSMCLIENT', 'RPC')

class OsmClientServiceServicerImpl(OsmServiceServicer):
    def __init__(self):
        LOGGER.info('Creating Servicer...')
        self._osm_client = client.Client(
            host = OSM_ADDRESS, so_port = OSM_PORT, project = OSM_PROJECT,
            user = OSM_USERNAME, password = OSM_PASSWORD, verify = OSM_VERIFY_TLS
        )
        LOGGER.info('osmClient created')
        LOGGER.info('Servicer Created')


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def NsiCreate(self, request : CreateRequest, context : grpc.ServicerContext) -> CreateResponse:
        try:
            #OSM library doesn't return nsi ID, just an exception
            self._osm_client.nsi.create(request.nst_name, request.nsi_name, request.account)
        except Exception as e:
            resp = CreateResponse(succeded = False, errormessage = str(e))
        else:
            resp =  CreateResponse(succeded = True)
        return resp


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def NsiList(self, request : Empty, context : grpc.ServicerContext) -> NsiListResponse:
        LOGGER.debug("NsiList request: %s", request)

        try:
            nsi_list = self._osm_client.nsi.list()  # list[dict], each dict has "id", maybe others
            LOGGER.debug("OSM returned %d NSIs", len(nsi_list))

            seen = set()
            ids : list[str] = []
            for nsi in nsi_list or []:
                raw_id = nsi.get("id")
                if raw_id is None: continue
                sid = str(raw_id)
                if sid in seen: continue
                seen.add(sid)
                ids.append(sid)
            return NsiListResponse(id=ids)

        except Exception as e:
            LOGGER.exception("NsiList exception")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"NsiList failed: {e}")
            return NsiListResponse(id=[])


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def NsiGet(self, request : GetRequest, context : grpc.ServicerContext) -> GetResponse:
        try:
            nsi_data = self._osm_client.nsi.get(request.id)  # returns dict from OSM
            LOGGER.debug("Got NSI: %s", nsi_data)

            nsi_msg = NsiObject(
                nst_name = nsi_data.get("nstName", ""),
                nsi_name = nsi_data.get("name", ""),
                description = nsi_data.get("description", ""),
                VimAccountId = nsi_data.get("vimAccountId", ""),
                Netslice_Subnet_id = nsi_data.get("netslice-subnet-id", ""),
                Netslice_vld_ip = nsi_data.get("netslice-vld-ip", "")
            )

            return GetResponse(nsi=nsi_msg)

        except Exception as e:
            LOGGER.exception("NsiGet failed")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"NsiGet failed: {e}")
            return GetResponse()


    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def NsiDelete(self, request : DeleteRequest, context : grpc.ServicerContext) -> DeleteResponse:
        try:
            # OSM library doesn't return nsi ID, just an exception
            self._osm_client.nsi.delete(request.id, False, False)
        except Exception as e:
            resp = DeleteResponse(succeded = False, errormessage = str(e))
        else:
            resp = DeleteResponse(succeded = True)
        return resp
