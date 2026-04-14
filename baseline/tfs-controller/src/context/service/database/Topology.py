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
from typing import Dict, List, Optional, Set
from common.proto.context_pb2 import (
    ContextId, Empty, EventTypeEnum, Topology, TopologyDetails, TopologyId, TopologyIdList, TopologyList)
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.Config import ALLOW_EXPLICIT_ADD_DEVICE_TO_TOPOLOGY, ALLOW_EXPLICIT_ADD_LINK_TO_TOPOLOGY
from .models.DeviceModel import DeviceModel
from .models.LinkModel import LinkModel
from .models.OpticalLinkModel import OpticalLinkModel
from .models.TopologyModel import TopologyDeviceModel, TopologyLinkModel, TopologyModel, TopologyOpticalLinkModel
from .uuids.Context import context_get_uuid
from .uuids.Device import device_get_uuid
from .uuids.Link import link_get_uuid
from .uuids.Topology import topology_get_uuid
from .Events import notify_event_context, notify_event_topology

LOGGER = logging.getLogger(__name__)

def topology_list_ids(db_engine : Engine, request : ContextId) -> TopologyIdList:
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        obj_list : List[TopologyModel] = session.query(TopologyModel).filter_by(context_uuid=context_uuid).all()
        return [obj.dump_id() for obj in obj_list]
    topology_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    return TopologyIdList(topology_ids=topology_ids)

def topology_list_objs(db_engine : Engine, request : ContextId) -> TopologyList:
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        obj_list : List[TopologyModel] = session.query(TopologyModel)\
            .options(selectinload(TopologyModel.topology_devices))\
            .options(selectinload(TopologyModel.topology_links))\
            .filter_by(context_uuid=context_uuid).all()
        return [obj.dump() for obj in obj_list]
    topologies = run_transaction(sessionmaker(bind=db_engine), callback)
    return TopologyList(topologies=topologies)

def topology_get(db_engine : Engine, request : TopologyId) -> Topology:
    _,topology_uuid = topology_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[TopologyModel] = session.query(TopologyModel)\
            .options(selectinload(TopologyModel.topology_devices))\
            .options(selectinload(TopologyModel.topology_links))\
            .filter_by(topology_uuid=topology_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        context_uuid = context_get_uuid(request.context_id, allow_random=False)
        raw_topology_uuid = '{:s}/{:s}'.format(request.context_id.context_uuid.uuid, request.topology_uuid.uuid)
        raise NotFoundException('Topology', raw_topology_uuid, extra_details=[
            'context_uuid generated was: {:s}'.format(context_uuid),
            'topology_uuid generated was: {:s}'.format(topology_uuid),
        ])
    return Topology(**obj)

def topology_get_details(db_engine : Engine, request : TopologyId) -> TopologyDetails:
    _,topology_uuid = topology_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[TopologyModel] = session.query(TopologyModel)\
            .options(selectinload(TopologyModel.topology_devices, TopologyDeviceModel.device, DeviceModel.endpoints))\
            .options(selectinload(TopologyModel.topology_links, TopologyLinkModel.link, LinkModel.link_endpoints))\
            .options(selectinload(TopologyModel.topology_optical_links, TopologyOpticalLinkModel.optical_link, OpticalLinkModel.opticallink_endpoints))\
            .filter_by(topology_uuid=topology_uuid).one_or_none()
            #.options(selectinload(DeviceModel.components))\
        return None if obj is None else obj.dump_details()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        context_uuid = context_get_uuid(request.context_id, allow_random=False)
        raw_topology_uuid = '{:s}/{:s}'.format(request.context_id.context_uuid.uuid, request.topology_uuid.uuid)
        raise NotFoundException('Topology', raw_topology_uuid, extra_details=[
            'context_uuid generated was: {:s}'.format(context_uuid),
            'topology_uuid generated was: {:s}'.format(topology_uuid),
        ])
    return TopologyDetails(**obj)

def topology_set(db_engine : Engine, messagebroker : MessageBroker, request : Topology) -> TopologyId:
    topology_name = request.name
    if len(topology_name) == 0: topology_name = request.topology_id.topology_uuid.uuid
    context_uuid,topology_uuid = topology_get_uuid(request.topology_id, topology_name=topology_name, allow_random=True)

    # By default, ignore request.device_ids and request.link_ids. They are used for retrieving
    # devices and links added into the topology. Explicit addition into the topology is done
    # automatically when creating the devices and links, based on the topologies specified in
    # the endpoints associated with the devices and links.
    # In some cases, it might be needed to add them explicitly; to allow that, activate flags
    # ALLOW_EXPLICIT_ADD_DEVICE_TO_TOPOLOGY and/or ALLOW_EXPLICIT_ADD_LINK_TO_TOPOLOGY.

    related_devices : List[Dict] = list()
    if ALLOW_EXPLICIT_ADD_DEVICE_TO_TOPOLOGY:
        device_uuids : Set[str] = set()
        for device_id in request.device_ids:
            device_uuid = device_get_uuid(device_id)
            if device_uuid not in device_uuids: continue
            related_devices.append({'topology_uuid': topology_uuid, 'device_uuid': device_uuid})
            device_uuids.add(device_uuid)
    else:
        if len(request.device_ids) > 0: # pragma: no cover
            MSG = 'ALLOW_EXPLICIT_ADD_DEVICE_TO_TOPOLOGY={:s}; '.format(str(ALLOW_EXPLICIT_ADD_DEVICE_TO_TOPOLOGY))
            MSG += 'Items in field "device_ids" ignored. This field is used for retrieval purposes only.'
            LOGGER.warning(MSG)

    related_links : List[Dict] = list()
    if ALLOW_EXPLICIT_ADD_LINK_TO_TOPOLOGY:
        link_uuids : Set[str] = set()
        for link_id in request.link_ids:
            link_uuid = link_get_uuid(link_id)
            if link_uuid not in link_uuids: continue
            related_links.append({'topology_uuid': topology_uuid, 'link_uuid': link_uuid})
            link_uuids.add(link_uuid)
    else:
        if len(request.link_ids) > 0:   # pragma: no cover
            MSG = 'ALLOW_EXPLICIT_ADD_LINK_TO_TOPOLOGY={:s}; '.format(str(ALLOW_EXPLICIT_ADD_LINK_TO_TOPOLOGY))
            MSG += 'Items in field "link_ids" ignored. This field is used for retrieval purposes only.'
            LOGGER.warning(MSG)

    now = datetime.datetime.now(datetime.timezone.utc)

    topology_data = [{
        'context_uuid' : context_uuid,
        'topology_uuid': topology_uuid,
        'topology_name': topology_name,
        'created_at'   : now,
        'updated_at'   : now,
    }]

    def callback(session : Session) -> bool:
        stmt = insert(TopologyModel).values(topology_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[TopologyModel.topology_uuid],
            set_=dict(
                topology_name = stmt.excluded.topology_name,
                updated_at    = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(TopologyModel.created_at, TopologyModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()

        updated = updated_at > created_at

        updated_topology_device = False
        if len(related_devices) > 0:
            stmt = insert(TopologyDeviceModel).values(related_devices)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[TopologyDeviceModel.topology_uuid, TopologyDeviceModel.device_uuid]
            )
            topology_device_inserts = session.execute(stmt)
            updated_topology_device = int(topology_device_inserts.rowcount) > 0

        updated_topology_link = False
        if len(related_links) > 0:
            stmt = insert(TopologyLinkModel).values(related_links)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[TopologyLinkModel.topology_uuid, TopologyLinkModel.link_uuid]
            )
            topology_link_inserts = session.execute(stmt)
            updated_topology_link = int(topology_link_inserts.rowcount) > 0

        return updated or updated_topology_device or updated_topology_link

    updated = run_transaction(sessionmaker(bind=db_engine), callback)
    context_id = json_context_id(context_uuid)
    topology_id = json_topology_id(topology_uuid, context_id=context_id)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    notify_event_topology(messagebroker, event_type, topology_id)
    notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)
    return TopologyId(**topology_id)

def topology_delete(db_engine : Engine, messagebroker : MessageBroker, request : TopologyId) -> Empty:
    context_uuid,topology_uuid = topology_get_uuid(request, allow_random=False)
    def callback(session : Session) -> bool:
        num_deleted = session.query(TopologyModel).filter_by(topology_uuid=topology_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    context_id = json_context_id(context_uuid)
    topology_id = json_topology_id(topology_uuid, context_id=context_id)
    if deleted:
        notify_event_topology(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, topology_id)
        notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)
    return Empty()
