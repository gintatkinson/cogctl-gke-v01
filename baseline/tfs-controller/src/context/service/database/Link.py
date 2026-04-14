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
    Empty, EventTypeEnum, Link, LinkId, LinkIdList, LinkList, TopologyId
)
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.tools.object_factory.Link import json_link_id
from .models.enums.LinkType import grpc_to_enum__link_type_enum
from .models.LinkModel import LinkModel, LinkEndPointModel
from .models.TopologyModel import TopologyLinkModel, TopologyModel
from .uuids.EndPoint import endpoint_get_uuid
from .uuids.Link import link_get_uuid
from .uuids.Topology import topology_get_uuid
from .Events import notify_event_context, notify_event_link, notify_event_topology

LOGGER = logging.getLogger(__name__)

def link_list_ids(db_engine : Engine) -> LinkIdList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[LinkModel] = session.query(LinkModel).all()
        return [obj.dump_id() for obj in obj_list]
    link_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    return LinkIdList(link_ids=link_ids)

def link_list_objs(db_engine : Engine) -> LinkList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[LinkModel] = session.query(LinkModel)\
            .options(selectinload(LinkModel.link_endpoints))\
            .all()
        return [obj.dump() for obj in obj_list]
    links = run_transaction(sessionmaker(bind=db_engine), callback)
    return LinkList(links=links)

def link_get(db_engine : Engine, request : LinkId) -> Link:
    link_uuid = link_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[LinkModel] = session.query(LinkModel)\
            .options(selectinload(LinkModel.link_endpoints))\
            .filter_by(link_uuid=link_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        raw_link_uuid = request.link_uuid.uuid
        raise NotFoundException('Link', raw_link_uuid, extra_details=[
            'link_uuid generated was: {:s}'.format(link_uuid)
        ])
    return Link(**obj)

def link_set(db_engine : Engine, messagebroker : MessageBroker, request : Link) -> LinkId:
    raw_link_uuid = request.link_id.link_uuid.uuid
    raw_link_name = request.name
    link_name = raw_link_uuid if len(raw_link_name) == 0 else raw_link_name
    link_uuid = link_get_uuid(request.link_id, link_name=link_name, allow_random=True)

    link_type = grpc_to_enum__link_type_enum(request.link_type)

    now = datetime.datetime.now(datetime.timezone.utc)

    topology_uuids : Set[str] = set()
    related_topologies : List[Dict] = list()

    # By default, always add link to default Context/Topology
    _,topology_uuid = topology_get_uuid(TopologyId(), allow_random=False, allow_default=True)
    related_topologies.append({
        'topology_uuid': topology_uuid,
        'link_uuid'    : link_uuid,
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
                'link_uuid'    : link_uuid,
            })
            topology_uuids.add(endpoint_topology_uuid)

    total_capacity_gbps, used_capacity_gbps = None, None
    is_bidirectional = False
    if request.HasField('attributes'):
        attributes = request.attributes

        # In proto3, HasField() does not work for scalar fields, using ListFields() instead.
        attribute_names = set([field.name for field,_ in attributes.ListFields()])

        if 'is_bidirectional' in attribute_names:
            is_bidirectional = attributes.is_bidirectional

        if 'total_capacity_gbps' in attribute_names:
            total_capacity_gbps = attributes.total_capacity_gbps

        if 'used_capacity_gbps' in attribute_names:
            used_capacity_gbps = attributes.used_capacity_gbps
        else:
            used_capacity_gbps = 0.0

    link_data = [{
        'link_uuid'           : link_uuid,
        'link_name'           : link_name,
        'link_type'           : link_type,
        'total_capacity_gbps' : total_capacity_gbps,
        'used_capacity_gbps'  : used_capacity_gbps,
        'is_bidirectional'    : is_bidirectional,
        'created_at'          : now,
        'updated_at'          : now,
    }]

    def callback(session : Session) -> Tuple[bool, List[Dict]]:
        stmt = insert(LinkModel).values(link_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[LinkModel.link_uuid],
            set_=dict(
                link_name           = stmt.excluded.link_name,
                link_type           = stmt.excluded.link_type,
                total_capacity_gbps = stmt.excluded.total_capacity_gbps,
                used_capacity_gbps  = stmt.excluded.used_capacity_gbps,
                is_bidirectional    = stmt.excluded.is_bidirectional,
                updated_at          = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(LinkModel.created_at, LinkModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()
        updated = updated_at > created_at

        updated_endpoints = False
        if len(link_endpoints_data) > 0:
            # TODO: manage add/remove of endpoints; manage changes in relations with topology
            stmt = insert(LinkEndPointModel).values(link_endpoints_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[LinkEndPointModel.link_uuid, LinkEndPointModel.endpoint_uuid]
            )
            link_endpoint_inserts = session.execute(stmt)
            updated_endpoints = int(link_endpoint_inserts.rowcount) > 0

        link_topology_ids = []
        if not updated or len(related_topologies) > 1:
            # Only update topology-link relations when link is created (not updated) or when endpoint_ids are
            # modified (len(related_topologies) > 1).
            stmt = insert(TopologyLinkModel).values(related_topologies)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[TopologyLinkModel.topology_uuid, TopologyLinkModel.link_uuid]
            )
            stmt = stmt.returning(TopologyLinkModel.topology_uuid)
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

        return updated or updated_endpoints, link_topology_ids

    updated, link_topology_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    link_id = json_link_id(link_uuid)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    notify_event_link(messagebroker, event_type, link_id)

    context_ids  : Dict[str, Dict] = dict()
    topology_ids : Dict[str, Dict] = dict()
    for topology_id in link_topology_ids:
        topology_uuid = topology_id['topology_uuid']['uuid']
        topology_ids[topology_uuid] = topology_id
        context_id = topology_id['context_id']
        context_uuid = context_id['context_uuid']['uuid']
        context_ids[context_uuid] = context_id

    for topology_id in topology_ids.values():
        notify_event_topology(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, topology_id)

    for context_id in context_ids.values():
        notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)

    return LinkId(**link_id)

def link_delete(db_engine : Engine, messagebroker : MessageBroker, request : LinkId) -> Empty:
    link_uuid = link_get_uuid(request, allow_random=False)
    def callback(session : Session) -> bool:
        query = session.query(TopologyLinkModel)
        query = query.filter_by(link_uuid=link_uuid)
        topology_link_list : List[TopologyLinkModel] = query.all()
        topology_ids = [obj.topology.dump_id() for obj in topology_link_list]
        num_deleted = session.query(LinkModel).filter_by(link_uuid=link_uuid).delete()
        return num_deleted > 0, topology_ids
    deleted, updated_topology_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    link_id = json_link_id(link_uuid)
    if deleted:
        notify_event_link(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, link_id)

        context_ids  : Dict[str, Dict] = dict()
        topology_ids : Dict[str, Dict] = dict()
        for topology_id in updated_topology_ids:
            topology_uuid = topology_id['topology_uuid']['uuid']
            topology_ids[topology_uuid] = topology_id
            context_id = topology_id['context_id']
            context_uuid = context_id['context_uuid']['uuid']
            context_ids[context_uuid] = context_id

        for topology_id in topology_ids.values():
            notify_event_topology(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, topology_id)

        for context_id in context_ids.values():
            notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)

    return Empty()
