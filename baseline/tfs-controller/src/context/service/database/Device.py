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
from common.method_wrappers.ServiceExceptions import InvalidArgumentException, NotFoundException
from common.message_broker.MessageBroker import MessageBroker
from common.proto.context_pb2 import (
    Device, DeviceDriverEnum, DeviceFilter, DeviceId, DeviceIdList, DeviceList,
    Empty, EventTypeEnum, TopologyId
)
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Device import json_device_id
from context.service.database.uuids.Topology import topology_get_uuid
from .models.DeviceModel import DeviceModel
from .models.EndPointModel import EndPointModel
from .models.ComponentModel import ComponentModel
from .models.TopologyModel import TopologyDeviceModel, TopologyModel
from .models.enums.DeviceDriver import grpc_to_enum__device_driver
from .models.enums.DeviceOperationalStatus import grpc_to_enum__device_operational_status
from .models.enums.KpiSampleType import grpc_to_enum__kpi_sample_type
from .uuids.Device import device_get_uuid
from .uuids.EndPoint import endpoint_get_uuid
from .ConfigRule import compose_config_rules_data, upsert_config_rules
from .Component import compose_components_data
from .Events import notify_event_context, notify_event_device, notify_event_topology

LOGGER = logging.getLogger(__name__)

def device_list_ids(db_engine : Engine) -> DeviceIdList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[DeviceModel] = session.query(DeviceModel).all()
        return [obj.dump_id() for obj in obj_list]
    device_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    return DeviceIdList(device_ids=device_ids)

def device_list_objs(db_engine : Engine) -> DeviceList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[DeviceModel] = session.query(DeviceModel)\
            .options(selectinload(DeviceModel.endpoints))\
            .options(selectinload(DeviceModel.config_rules))\
            .options(selectinload(DeviceModel.components))\
            .all()
        return [obj.dump() for obj in obj_list]
    devices = run_transaction(sessionmaker(bind=db_engine), callback)
    return DeviceList(devices=devices)

def device_get(db_engine : Engine, request : DeviceId) -> Device:
    device_uuid = device_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[DeviceModel] = session.query(DeviceModel)\
            .options(selectinload(DeviceModel.endpoints))\
            .options(selectinload(DeviceModel.config_rules))\
            .options(selectinload(DeviceModel.components))\
            .filter_by(device_uuid=device_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        raw_device_uuid = request.device_uuid.uuid
        raise NotFoundException('Device', raw_device_uuid, extra_details=[
            'device_uuid generated was: {:s}'.format(device_uuid)
        ])
    return Device(**obj)

def device_set(db_engine : Engine, messagebroker : MessageBroker, request : Device) -> DeviceId:
    raw_device_uuid = request.device_id.device_uuid.uuid
    raw_device_name = request.name
    device_name = raw_device_uuid if len(raw_device_name) == 0 else raw_device_name
    device_uuid = device_get_uuid(request.device_id, device_name=device_name, allow_random=True)

    if len(request.controller_id.device_uuid.uuid) > 0:
        controller_uuid = device_get_uuid(request.controller_id, allow_random=False)
    else:
        controller_uuid = None

    device_type = request.device_type
    oper_status = grpc_to_enum__device_operational_status(request.device_operational_status)
    device_drivers = [grpc_to_enum__device_driver(d) for d in request.device_drivers]

    now = datetime.datetime.now(datetime.timezone.utc)

    topology_uuids : Set[str] = set()
    related_topologies : List[Dict] = list()

    # By default, always add device to default Context/Topology
    _,topology_uuid = topology_get_uuid(TopologyId(), allow_random=False, allow_default=True)
    related_topologies.append({
        'topology_uuid': topology_uuid,
        'device_uuid'  : device_uuid,
    })
    topology_uuids.add(topology_uuid)

    is_oc_driver = DeviceDriverEnum.DEVICEDRIVER_OC in set(request.device_drivers)
    #optical_endpoints_data : List[Dict] = list()

    endpoints_data : List[Dict] = list()
    for i, endpoint in enumerate(request.device_endpoints):
        endpoint_device_uuid = endpoint.endpoint_id.device_id.device_uuid.uuid
        if len(endpoint_device_uuid) == 0 or is_oc_driver : endpoint_device_uuid = device_uuid
        if endpoint_device_uuid not in {raw_device_uuid, device_uuid}:
            raise InvalidArgumentException(
                'request.device_endpoints[{:d}].device_id.device_uuid.uuid'.format(i), endpoint_device_uuid,
                ['should be == request.device_id.device_uuid.uuid({:s})'.format(raw_device_uuid)]
            )

        raw_endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
        raw_endpoint_name = endpoint.name
        endpoint_topology_uuid, endpoint_device_uuid, endpoint_uuid = endpoint_get_uuid(
            endpoint.endpoint_id, endpoint_name=raw_endpoint_name, allow_random=True)
        endpoint_name = raw_endpoint_uuid if len(raw_endpoint_name) == 0 else raw_endpoint_name

        kpi_sample_types = [grpc_to_enum__kpi_sample_type(kst) for kst in endpoint.kpi_sample_types]

        endpoints_data.append({
            'endpoint_uuid'    : endpoint_uuid,
            'device_uuid'      : endpoint_device_uuid,
            'topology_uuid'    : endpoint_topology_uuid,
            'name'             : endpoint_name,
            'endpoint_type'    : endpoint.endpoint_type,
            'kpi_sample_types' : kpi_sample_types,
            'endpoint_location': grpc_message_to_json_string(endpoint.endpoint_location),
            'created_at'       : now,
            'updated_at'       : now,
        })
        # # ------------------- Experimental -----------------------
       
        # if is_oc_driver:
            
        #     optical_endpoints_data.append({
        #             'endpoint_uuid'    : endpoint_uuid,
        #             'device_uuid'      : endpoint_device_uuid,
        #             'name'             : endpoint_name,
        #             'endpoint_type'    : endpoint.endpoint_type,
        #             'created_at'       : now,
        #             'updated_at'       : now,
        #     })

        if endpoint_topology_uuid not in topology_uuids:
            related_topologies.append({
                'topology_uuid': endpoint_topology_uuid,
                'device_uuid'  : device_uuid,
            })
            topology_uuids.add(endpoint_topology_uuid)

    components_data = compose_components_data(request.device_config.config_rules, now, device_uuid=device_uuid)
    config_rules    = compose_config_rules_data(request.device_config.config_rules, now, device_uuid=device_uuid)

    device_data = [{
        'device_uuid'              : device_uuid,
        'device_name'              : device_name,
        'device_type'              : device_type,
        'device_operational_status': oper_status,
        'device_drivers'           : device_drivers,
        'created_at'               : now,
        'updated_at'               : now,
    }]

    if controller_uuid is not None:
        device_data[0]['controller_uuid'] = controller_uuid

    def callback(session : Session) -> Tuple[bool, List[Dict]]:
        stmt = insert(DeviceModel).values(device_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[DeviceModel.device_uuid],
            set_=dict(
                device_name               = stmt.excluded.device_name,
                device_type               = stmt.excluded.device_type,
                device_operational_status = stmt.excluded.device_operational_status,
                device_drivers            = stmt.excluded.device_drivers,
                updated_at                = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(DeviceModel.created_at, DeviceModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()
        updated = updated_at > created_at

        updated_endpoints = False
        if len(endpoints_data) > 0:
            stmt = insert(EndPointModel).values(endpoints_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=[EndPointModel.endpoint_uuid],
                set_=dict(
                    name             = stmt.excluded.name,
                    endpoint_type    = stmt.excluded.endpoint_type,
                    kpi_sample_types = stmt.excluded.kpi_sample_types,
                    updated_at       = stmt.excluded.updated_at,
                )
            )
            stmt = stmt.returning(EndPointModel.created_at, EndPointModel.updated_at)
            endpoint_updates = session.execute(stmt).fetchall()
            updated_endpoints = any([(updated_at > created_at) for created_at,updated_at in endpoint_updates])
        
        #---------------------- Experimental ---------------------------------
        
        # if len(optical_endpoints_data) > 0:
        #     LOGGER.info(f"Optical endpoint data_ device_model {optical_endpoints_data}")
        #     stmt = insert(OpticalEndPointModel).values(optical_endpoints_data)
        #     stmt = stmt.on_conflict_do_update(
        #         index_elements=[OpticalEndPointModel.endpoint_uuid],
        #         set_=dict(
        #             name             = stmt.excluded.name,
        #             endpoint_type    = stmt.excluded.endpoint_type,
        #             updated_at       = stmt.excluded.updated_at,
        #         )
        #     )
        #     stmt = stmt.returning(OpticalEndPointModel.created_at, OpticalEndPointModel.updated_at)
        #     optical_endpoint_updates = session.execute(stmt).fetchall()
        #     updated_optical_endpoints = any([(updated_at > created_at) for created_at,updated_at in endpoint_updates])    

        device_topology_ids = []
        if not updated or len(related_topologies) > 1:
            # Only update topology-device relations when device is created (not updated) or when endpoints are
            # modified (len(related_topologies) > 1).
            stmt = insert(TopologyDeviceModel).values(related_topologies)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[TopologyDeviceModel.topology_uuid, TopologyDeviceModel.device_uuid]
            )
            stmt = stmt.returning(TopologyDeviceModel.topology_uuid)
            topology_uuids = session.execute(stmt).fetchall()

            #LOGGER.warning('RAW topology_uuids={:s}'.format(str(topology_uuids)))
            if len(topology_uuids) > 0:
                topology_uuids = [topology_uuid[0] for topology_uuid in topology_uuids]
                #LOGGER.warning('NEW topology_uuids={:s}'.format(str(topology_uuids)))
                query = session.query(TopologyModel)
                query = query.filter(TopologyModel.topology_uuid.in_(topology_uuids))
                device_topologies : List[TopologyModel] = query.all()
                device_topology_ids = [obj.dump_id() for obj in device_topologies]
                #LOGGER.warning('device_topology_ids={:s}'.format(str(device_topology_ids)))

        updated_components = False
        
        if len(components_data) > 0:
            stmt = insert(ComponentModel).values(components_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=[ComponentModel.component_uuid],
                set_=dict(
                    name             = stmt.excluded.name,
                    type             = stmt.excluded.type,
                    attributes       = stmt.excluded.attributes,
                    parent           = stmt.excluded.parent,
                    updated_at       = stmt.excluded.updated_at,
                )
            )
            stmt = stmt.returning(ComponentModel.created_at, ComponentModel.updated_at)
            component_updates = session.execute(stmt).fetchall()
            updated_components = any([(updated_at > created_at) for created_at,updated_at in component_updates])
        
        changed_config_rules = upsert_config_rules(session, config_rules, device_uuid=device_uuid)

        return updated or updated_endpoints or updated_components or changed_config_rules, device_topology_ids

    updated, device_topology_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    device_id = json_device_id(device_uuid)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    notify_event_device(messagebroker, event_type, device_id)

    context_ids  : Dict[str, Dict] = dict()
    topology_ids : Dict[str, Dict] = dict()
    for topology_id in device_topology_ids:
        topology_uuid = topology_id['topology_uuid']['uuid']
        topology_ids[topology_uuid] = topology_id
        context_id = topology_id['context_id']
        context_uuid = context_id['context_uuid']['uuid']
        context_ids[context_uuid] = context_id

    for topology_id in topology_ids.values():
        notify_event_topology(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, topology_id)

    for context_id in context_ids.values():
        notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)

    return DeviceId(**device_id)

def device_delete(db_engine : Engine, messagebroker : MessageBroker, request : DeviceId) -> Empty:
    device_uuid = device_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Tuple[bool, List[Dict]]:
        query = session.query(TopologyDeviceModel)
        query = query.filter_by(device_uuid=device_uuid)
        topology_device_list : List[TopologyDeviceModel] = query.all()
        topology_ids = [obj.topology.dump_id() for obj in topology_device_list]
        num_deleted = session.query(DeviceModel).filter_by(device_uuid=device_uuid).delete()
        return num_deleted > 0, topology_ids
    deleted, updated_topology_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    device_id = json_device_id(device_uuid)
    if deleted:
        notify_event_device(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, device_id)

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

def device_select(db_engine : Engine, request : DeviceFilter) -> DeviceList:
    device_uuids = [
        device_get_uuid(device_id, allow_random=False)
        for device_id in request.device_ids.device_ids
    ]
    dump_params = dict(
        include_endpoints   =request.include_endpoints,
        include_config_rules=request.include_config_rules,
        include_components  =request.include_components,
    )
    def callback(session : Session) -> List[Dict]:
        query = session.query(DeviceModel)
        if request.include_endpoints   : query = query.options(selectinload(DeviceModel.endpoints))
        if request.include_config_rules: query = query.options(selectinload(DeviceModel.config_rules))
        #if request.include_components  : query = query.options(selectinload(DeviceModel.components))
        obj_list : List[DeviceModel] = query.filter(DeviceModel.device_uuid.in_(device_uuids)).all()
        return [obj.dump(**dump_params) for obj in obj_list]
    devices = run_transaction(sessionmaker(bind=db_engine), callback)
    return DeviceList(devices=devices)
