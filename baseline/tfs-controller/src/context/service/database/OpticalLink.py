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

import datetime, logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, selectinload, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from typing import Dict, List, Optional, Set, Tuple
from common.proto.context_pb2 import (
    Empty, EventTypeEnum, OpticalLink, LinkId, OpticalLinkList, TopologyId
)
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.tools.object_factory.Link import json_link_id
from .models.OpticalLinkModel import OpticalLinkModel,OpticalLinkEndPointModel 
from .models.TopologyModel import TopologyOpticalLinkModel, TopologyModel
from .uuids.EndPoint import endpoint_get_uuid
from .uuids.Link import link_get_uuid
from .uuids.Topology import topology_get_uuid
from .Events import notify_event_link

LOGGER = logging.getLogger(__name__)


def optical_link_list_objs(db_engine : Engine) -> OpticalLinkList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[OpticalLinkModel] = session.query(OpticalLinkModel)\
            .options(selectinload(OpticalLinkModel.opticallink_endpoints))\
            .all()
        return [obj.dump() for obj in obj_list]
    links = run_transaction(sessionmaker(bind=db_engine), callback)
    return OpticalLinkList(optical_links=links)

def optical_link_get(db_engine : Engine, request : LinkId) -> OpticalLink:
    link_uuid = link_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[OpticalLinkModel] = session.query(OpticalLinkModel)\
            .options(selectinload(OpticalLinkModel.opticallink_endpoints))\
            .filter_by(opticallink_uuid=link_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        raw_link_uuid = request.link_uuid.uuid
        raise NotFoundException('Optical Link', raw_link_uuid, extra_details=[
            'link_uuid generated was: {:s}'.format(link_uuid)
        ])
    return OpticalLink(**obj)

def optical_link_set(db_engine : Engine, messagebroker : MessageBroker, request : OpticalLink) -> LinkId:
    raw_link_uuid = request.link_id.link_uuid.uuid
    raw_link_name = request.name
    link_name = raw_link_uuid if len(raw_link_name) == 0 else raw_link_name
    link_uuid = link_get_uuid(request.link_id, link_name=link_name, allow_random=True)

    now = datetime.datetime.now(datetime.timezone.utc)

    topology_uuids : Set[str] = set()
    related_topologies : List[Dict] = list()

    # By default, always add link to default Context/Topology
    _,topology_uuid = topology_get_uuid(TopologyId(), allow_random=False, allow_default=True)
    related_topologies.append({
        'topology_uuid': topology_uuid,
        'optical_link_uuid'    : link_uuid,
    })
    topology_uuids.add(topology_uuid)

    link_endpoints_data : List[Dict] = list()
    for i,endpoint_id in enumerate(request.link_endpoint_ids):
        endpoint_topology_uuid, _, endpoint_uuid = endpoint_get_uuid(
            endpoint_id, allow_random=False)

        link_endpoints_data.append({
            'link_uuid'    : link_uuid,
            'endpoint_uuid': endpoint_uuid,
            'position'     : i,
        })

        if endpoint_topology_uuid not in topology_uuids:
            related_topologies.append({
                'topology_uuid': endpoint_topology_uuid,
                'optical_link_uuid'    : link_uuid,
            })
            topology_uuids.add(endpoint_topology_uuid)

    optical_link_data = [{
        'opticallink_uuid'     : link_uuid,
        'name'                 : link_name,
        'created_at'           : now,
        'updated_at'           : now,
        'length'               : request.optical_details.length,
        "src_port"             : request.optical_details.src_port,
        "dst_port"             : request.optical_details.dst_port,
        "local_peer_port"      : request.optical_details.local_peer_port,
        "remote_peer_port"     : request.optical_details.remote_peer_port,
        "used"                 : request.optical_details.used,
        "c_slots"              : request.optical_details.c_slots ,
        "l_slots"              : request.optical_details.l_slots,
        "s_slots"              : request.optical_details.s_slots,
    }]

    def callback(session : Session) -> Tuple[bool, List[Dict]]:
        stmt = insert(OpticalLinkModel).values(optical_link_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[OpticalLinkModel.opticallink_uuid],
            set_=dict(
                updated_at          = stmt.excluded.updated_at,
                src_port            = stmt.excluded.src_port,
                dst_port            = stmt.excluded.dst_port,  
                local_peer_port     = stmt.excluded.local_peer_port,
                remote_peer_port    = stmt.excluded.remote_peer_port,
                used                = stmt.excluded.used ,
                c_slots             = stmt.excluded.c_slots,
                l_slots             = stmt.excluded.l_slots,
                s_slots             = stmt.excluded.s_slots
            )
        )
        stmt = stmt.returning(OpticalLinkModel.created_at, OpticalLinkModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()
        updated = updated_at > created_at

        updated_endpoints = False
        if len(link_endpoints_data) > 0:
            stmt = insert(OpticalLinkEndPointModel).values(link_endpoints_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[OpticalLinkEndPointModel.link_uuid, OpticalLinkEndPointModel.endpoint_uuid]
            )
            link_endpoint_inserts = session.execute(stmt)
            updated_endpoints = int(link_endpoint_inserts.rowcount) > 0

        if not updated or len(related_topologies) > 1:
            # Only update topology-link relations when link is created (not updated) or when endpoint_ids are
            # modified (len(related_topologies) > 1).
            stmt = insert(TopologyOpticalLinkModel).values(related_topologies)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[TopologyOpticalLinkModel.topology_uuid, TopologyOpticalLinkModel.optical_link_uuid]
            )
            stmt = stmt.returning(TopologyOpticalLinkModel.topology_uuid)
            topology_uuids = session.execute(stmt).fetchall()

            #LOGGER.warning('RAW topology_uuids={:s}'.format(str(topology_uuids)))
            if len(topology_uuids) > 0:
                topology_uuids = [topology_uuid[0] for topology_uuid in topology_uuids]
                #LOGGER.warning('NEW topology_uuids={:s}'.format(str(topology_uuids)))
                query = session.query(TopologyModel)
                query = query.filter(TopologyModel.topology_uuid.in_(topology_uuids))
                link_topologies : List[TopologyModel] = query.all()
                link_topology_ids = [obj.dump_id() for obj in link_topologies]
                #LOGGER.warning('link_topology_ids={:s}'.format(str(link_topology_ids)))
        return updated or updated_endpoints

    updated = run_transaction(sessionmaker(bind=db_engine), callback )
    link_id = json_link_id(link_uuid)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    notify_event_link(messagebroker, event_type, link_id)

    return LinkId(**link_id)

def optical_link_delete(db_engine : Engine, messagebroker : MessageBroker, request : LinkId) -> Empty:
    link_uuid = link_get_uuid(request, allow_random=False)

    def callback(session : Session) -> bool:
        num_deleted = session.query(OpticalLinkModel).filter_by(opticallink_uuid=link_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)

    link_id = json_link_id(link_uuid)
    if deleted:
        notify_event_link(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, link_id)

    return Empty()
