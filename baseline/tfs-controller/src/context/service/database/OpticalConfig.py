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

import json, logging ,datetime
from sqlalchemy.dialects.postgresql import insert
from common.message_broker.MessageBroker import MessageBroker
from common.DeviceTypes import DeviceTypeEnum
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from common.proto.context_pb2 import OpticalConfig, OpticalConfigId, Empty, EventTypeEnum
from .models.OpticalConfig.OpticalConfigModel import OpticalConfigModel
from .models.OpticalConfig.TransponderModel import  TransponderTypeModel, OpticalChannelModel, TransponderInterfaceModel
from .models.OpticalConfig.RoadmModel import RoadmTypeModel, ChannelModel, ORInterfaceModel


from context.service.database.uuids.OpticalConfig import (
  channel_get_uuid , opticalconfig_get_uuid ,transponder_get_uuid,roadm_get_uuid,
    interface_get_uuid , ob_get_uuid

)
from .Events import notify_event_opticalconfig
from .OpticalBand import set_optical_band
LOGGER = logging.getLogger(__name__)
now = datetime.datetime.utcnow()

def get_opticalconfig(db_engine : Engine):
    def callback(session:Session):
        optical_configs = list()
        results = session.query(OpticalConfigModel).all()
        for obj in results:
            optical_config = OpticalConfig()
            optical_config.config = json.dumps(obj.dump())
            ids_obj = obj.dump_id()
            optical_config.opticalconfig_id.opticalconfig_uuid = ids_obj["opticalconfig_uuid"]
            optical_config.device_id.device_uuid.uuid=ids_obj["device_uuid"]
            optical_configs.append(optical_config)
        return optical_configs
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    return obj

def set_opticalconfig(db_engine : Engine, request : OpticalConfig):
    opticalconfig_id = OpticalConfigId()
    device_id = request.device_id
    device_uuid =  request.device_id.device_uuid.uuid
    channels = []
    interfaces = []
    transponder = []
    roadms = []
    channel_namespace = None
    OpticalConfig_data = []
    config_type = None
    #is_transpondre = False
    opticalconfig_uuid = opticalconfig_get_uuid(device_id) 

    if request.config:
        config = json.loads(request.config)
        if 'channel_namespace' in config:
            channel_namespace=config['channel_namespace']
        if "type" in config:
            config_type= config["type"]
            if config_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_:
                is_transpondre = True
                transceivers = []
                
                if channel_namespace is None and  'channel_namespace' in config:
                    channel_namespace=config['channel_namespace']
               
                if 'interfaces' in config and len(config['interfaces']) > 0:
                    for interface in config['interfaces']:
                        interface_name=interface["name"] if "name" in interface else None
                        interfaces.append({
                            "transponder_uuid"   : transponder_get_uuid(device_id),
                            'interface_uuid'     : interface_get_uuid(interface_name,device_uuid),
                            "name"               : interface_name,
                            "status"             : interface["status"            ] if "status" in interface else None,
                            "operation_status"   : interface["operation_status"  ] if "operation_status" in interface else None,
                            "ifindex"            : interface["ifindex"           ] if "ifindex" in interface else None,
                            "in_octets"          : interface["in_octets"         ] if "in_octets" in interface else None,
                            "in_pkts"            : interface["in_pkts"           ] if "in_pkts" in interface else None,
                            "in_unicast_pkts"    : interface["in_unicast_pkts"   ] if "in_unicast_pkts" in interface else None,
                            "in_broadcast_pkts"  : interface["in_broadcast_pkts" ] if "in_broadcast_pkts" in interface else None,
                            "in_multicast_pkts"  : interface["in_multicast_pkts" ] if "in_multicast_pkts" in interface else None,
                            "out_discards"       : interface["out_discards"      ] if "out_discards" in interface else None,
                            "out_errors"         : interface["out_errors"        ] if "out_errors" in interface else None,
                            "in_discards"        : interface["in_discards"       ] if "in_discards" in interface else None,
                            "in_errors"          : interface["in_errors"         ] if "in_errors" in interface else None,
                            "out_octets"         : interface["out_octets"        ] if "out_octets" in interface else None,  
                            "out_pkts"           : interface["out_pkts"          ] if "out_pkts" in interface else None,
                            "out_unicast_pkts"   : interface["out_unicast_pkts"  ] if "out_unicast_pkts" in interface else None,
                            "out_broadcast_pkts" : interface["out_broadcast_pkts"] if "out_broadcast_pkts" in interface else None,
                            "out_multicast_pkts" : interface["out_multicast_pkts"] if "out_multicast_pkts" in interface  else None,
                            "last_clear"         : interface["last_clear"        ] if "last_clear" in interface else None
                        })

                if 'channels' in config and len(config['channels']) > 0:
                    #channels = [channel['name']['index'] for channel in config['channels']]
                    for channel_params in config['channels']:
                        channels.append({
                            # "opticalconfig_uuid":opticalconfig_uuid,
                            "transponder_uuid"   : transponder_get_uuid(device_id),
                            "channel_uuid"       : channel_get_uuid(channel_params['name']['index'],device_uuid),
                            "channel_name"       : channel_params['name']['index'],
                            "frequency"          : int(channel_params["frequency"]) if "frequency" in channel_params  else 0,
                            "operational_mode"   : int(channel_params["operational-mode"]) if "operational-mode" in channel_params else 0,
                            "target_output_power": channel_params["target-output-power"] if "target-output-power" in channel_params else '',
                            "status"             : channel_params["status"] if "status" in channel_params else ""
                        })

                transponder.append({
                    "transponder_uuid"  : transponder_get_uuid(device_id),
                    "transcievers"      : transceivers,
                    
                    "opticalconfig_uuid": opticalconfig_uuid,
                })

            if config_type == DeviceTypeEnum.OPTICAL_ROADM._value_:
                if channel_namespace is None and  'channel_namespace' in config:
                    channel_namespace=config['channel_namespace']
                if 'media_channels' in config and len(config['media_channels']) > 0:
                    #channels = [channel['name']['index'] for channel in config['channels']]
                    channel_num = 0
                    for channel_params in config['media_channels']:
                        channel_index = channel_params['channel_index'] if channel_params['channel_index'] is not None else None
                        channels.append({
                            # "opticalconfig_uuid":opticalconfig_uuid,
                            "roadm_uuid"          : roadm_get_uuid(device_id),
                            "channel_uuid"        : channel_get_uuid(f'media_channel_{channel_index}',device_uuid),
                            "band_name"           : channel_params['band_name'],
                            "lower_frequency"     : int(channel_params["lower_frequency"]) if "lower_frequency" in channel_params  else 0,
                            "upper_frequency"     : int(channel_params["upper_frequency"]) if "upper_frequency" in channel_params  else 0,
                            "dest_port"           : channel_params["dest_port"] if "dest_port" in channel_params else '',
                            "src_port"            : channel_params["src_port"] if "src_port" in channel_params else '',
                            "status"              : channel_params["status"] if "status" in channel_params else "",
                            "type"                : 'media_channel',
                            "optical_band_parent" : str(channel_params['optical_band_parent']) if 'optical_band_parent' in channel_params else None,
                            "channel_index"       : channel_index if channel_index is not None else None,
                        })
                if 'optical_bands' in config and len(config['optical_bands']) > 0:
                    #channels = [channel['name']['index'] for channel in config['channels']]
                    channel_num = 0
                    for channel_params in config['optical_bands']:
                        channel_num += 1
                        channels.append({
                            # "opticalconfig_uuid":opticalconfig_uuid,
                            "roadm_uuid"         : roadm_get_uuid(device_id),
                            "channel_uuid"       : channel_get_uuid(f'optical_bands_{channel_num}',device_uuid),
                            "band_name"          : channel_params['band_name'],
                            "lower_frequency"    : int(channel_params["lower_frequency"]) if "lower_frequency" in channel_params  else 0,
                            "upper_frequency"    : int(channel_params["upper_frequency"]) if "upper_frequency" in channel_params  else 0,
                            "dest_port"          : channel_params["dest_port"] if "dest_port" in channel_params else '',
                            "src_port"           : channel_params["src_port"] if "src_port" in channel_params else '',
                            "status"             : channel_params["status"] if "status" in channel_params else "",
                            "type"               : 'optical_band',
                            "channel_index"      : channel_params['channel_index'] if 'channel_index' in channel_params else None,
                            "optical_band_parent": None
                        })

                roadms.append({
                    "roadm_uuid"         : roadm_get_uuid(device_id),
                    "opticalconfig_uuid" : opticalconfig_uuid,
                })

            if config_type == DeviceTypeEnum.OPEN_ROADM._value_:
                if 'interfaces' in config:
                    for interface in config['interfaces']:
                        interfaces.append({
                            "interface_uuid"      : interface_get_uuid(interface['name'],device_uuid),
                            'name'                : interface["name"],
                            "type"                : interface["type"],
                            "administrative_state": interface["administrative_state"],
                            "circuit_pack_name"   : interface["circuit_pack_name"],
                            "port"                : interface["port"],
                            "interface_list"      : interface["interface_list"],
                            "frequency"           : interface["frequency"],
                            "width"               :  int(float(interface["width"])) if 'width' in interface else 0,
                            "roadm_uuid"          : roadm_get_uuid(device_id),
                        })
                if 'circuits' in config:
                    for interface in config['circuits']:
                        ports_g=''
                        if 'port' in interface :
                            for p in interface['port']:
                                if ports_g != '': ports_g +='/'
                                ports_g= ports_g+ p['port_name']
                            
                        interfaces.append({
                            "interface_uuid"      : interface_get_uuid(interface["interface_uuid"],device_uuid),
                            'name'                : interface["interface_list"] if 'interface_list' in interface else interface["interface_uuid"],
                            "type"                : "Null",
                            "administrative_state": interface["administrative_state"] if 'administrative_state' in interface else "not-in-service",
                            "circuit_pack_name"   : interface["circuit_pack_name"],
                            "port"                : ports_g,
                            "interface_list"      : interface["interface_list"] if 'interface_list' in interface else "Null",
                            "frequency"           : interface["frequency"] if 'frequency' in interface else 0.0,
                            "width"               :  int(float(interface["width"])) if 'width' in interface else 0,
                            "roadm_uuid"          : roadm_get_uuid(device_id),
                        })
                roadms.append({
                    "roadm_uuid"        : roadm_get_uuid(device_id),
                    "opticalconfig_uuid": opticalconfig_uuid,
                })          
                LOGGER.info(f"open_roadm")

        OpticalConfig_data.append({
            "opticalconfig_uuid" : opticalconfig_uuid,
            # "transcievers"      : transceivers,
            # "interfaces"        :"",
            "channel_namespace" : channel_namespace ,
            "endpoints"         : [json.dumps(endpoint) for endpoint in config.get("endpoints",[])],
            "device_uuid"       : device_uuid,
            "type"              : config_type
        })

        LOGGER.info(f"added OpticalConfig_data {OpticalConfig_data}")
        LOGGER.info(f"added interfaces {interfaces}")

    def callback(session:Session)->bool:
        stmt = insert(OpticalConfigModel).values(OpticalConfig_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[OpticalConfigModel.opticalconfig_uuid],
            set_=dict(
                channel_namespace = stmt.excluded.channel_namespace
            )
        )
        stmt = stmt.returning(OpticalConfigModel.opticalconfig_uuid)
        opticalconfig_id = session.execute(stmt).fetchone()
        if config_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_:
            if (len(transponder)>0):
                stmt = insert(TransponderTypeModel).values(transponder)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[TransponderTypeModel.transponder_uuid],
                    set_=dict(
                        transcievers = stmt.excluded.transcievers,
                    )
                )
                stmt = stmt.returning(TransponderTypeModel.transponder_uuid)
                transponder_id = session.execute(stmt).fetchone()

            if len(channels) > 0:
                stmt = insert(OpticalChannelModel).values(channels)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[OpticalChannelModel.channel_uuid],
                    set_=dict(
                        channel_name= stmt.excluded.channel_name ,
                        frequency = stmt.excluded.frequency,
                        operational_mode=stmt.excluded.operational_mode,
                        target_output_power=stmt.excluded.target_output_power,
                    )
                )
                stmt = stmt.returning(OpticalChannelModel.channel_uuid)
                channel_id = session.execute(stmt).fetchone()
            if (len(interfaces)>0) :
                        model_columns = inspect(TransponderInterfaceModel).c.keys()
                        stmt = insert(TransponderInterfaceModel).values(interfaces)
                        
                        stmt = stmt.on_conflict_do_update(
                            index_elements=[TransponderInterfaceModel.interface_uuid ],
                            set_={field: stmt.excluded[field] for field in model_columns if field != 'interface_uuid' }
                            
                        )
                        stmt = stmt.returning(TransponderInterfaceModel.interface_uuid)
                        interface_id = session.execute(stmt).fetchone()     
        

        if config_type == DeviceTypeEnum.OPTICAL_ROADM._value_:
            if len(roadms) > 0:
                stmt = insert(RoadmTypeModel).values(roadms)
                stmt = stmt.on_conflict_do_update(
                        index_elements=[RoadmTypeModel.roadm_uuid],
                        set_=dict(
                            opticalconfig_uuid = stmt.excluded.opticalconfig_uuid
                        )
                    )
                stmt = stmt.returning(RoadmTypeModel.roadm_uuid)
                roadm_id = session.execute(stmt).fetchone()

            if len(channels) > 0:
                stmt = insert(ChannelModel).values(channels)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[ChannelModel.channel_uuid],
                    set_=dict(
                        band_name           = stmt.excluded.band_name,
                        lower_frequency     = stmt.excluded.lower_frequency,
                        upper_frequency     = stmt.excluded.upper_frequency,
                        type                = stmt.excluded.type,
                        status              = stmt.excluded.status,
                        dest_port           = stmt.excluded.dest_port,
                        src_port            = stmt.excluded.src_port,
                        channel_index       = stmt.excluded.channel_index,
                        optical_band_parent = stmt.excluded.optical_band_parent,
                    )
                )
                stmt = stmt.returning(ChannelModel.channel_uuid)
                opticalChannel_id = session.execute(stmt).fetchone()
         
        if config_type == DeviceTypeEnum.OPEN_ROADM._value_:
            if len(roadms) > 0:
                stmt = insert(RoadmTypeModel).values(roadms)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[RoadmTypeModel.roadm_uuid],
                    set_=dict(
                        opticalconfig_uuid = stmt.excluded.opticalconfig_uuid
                    )
                )
                stmt = stmt.returning(RoadmTypeModel.roadm_uuid)
                roadm_id = session.execute(stmt).fetchone() 

            if len(interfaces) > 0:   
                ifc_uuids=[]  
                for ifc in interfaces :  
                    stmt = insert(ORInterfaceModel).values(**ifc)
                    update_stmt = stmt.on_conflict_do_update(
                        index_elements=[ORInterfaceModel.interface_uuid],
                        set_=dict(
                            name                 = stmt.excluded.name,
                            frequency            = stmt.excluded.frequency,
                            administrative_state = stmt.excluded.administrative_state,
                            type                 = stmt.excluded.type,
                            circuit_pack_name    = stmt.excluded.circuit_pack_name,
                            port                 = stmt.excluded.port,
                            interface_list       = stmt.excluded.interface_list,
                            width                = stmt.excluded.width,
                        )
                    ).returning(ORInterfaceModel.interface_uuid)
                    result = session.execute(update_stmt).fetchone()     
                    ifc_uuids.append(result)        
            else : 
                session.query(ORInterfaceModel).delete()         
    opticalconfig_id = run_transaction(sessionmaker(bind=db_engine), callback)
    return {'opticalconfig_uuid': opticalconfig_id}

def update_opticalconfig(db_engine : Engine, request : OpticalConfig):
    opticalconfig_id = OpticalConfigId()
    device_id = request.device_id
    device_uuid = request.device_id.device_uuid.uuid
    channels = []
    transponder = []
    roadms = []
    channel_namespace = None
    OpticalConfig_data = []
    config_type = None
    optical_bands = []
    interfaces=[]
    #is_transpondre = False
    opticalconfig_uuid = opticalconfig_get_uuid(device_id)
    is_optical_band=None
    if request.config :
        config = json.loads(request.config)

        if  'new_config' in config:
            if 'type' in config:
                config_type = config['type']
            if "type" in config['new_config'] and config_type is None:
                config_type = config['new_config']["type"]    
            if 'channel_namespace' in config['new_config']:
                channel_namespace = config['new_config'] ['channel_namespace']

            if config_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_:
                is_transpondre = True
                transceivers = []
                if channel_namespace is None and  'channel_namespace' in config:
                    channel_namespace=config['channel_namespace']

                if 'transceivers' in config['new_config'] and len(config['new_config']['transceivers']['transceiver']) > 0:
                    transceivers = [transceiver for transceiver in config['new_config'] ['transceivers']['transceiver']]
                    
                if 'interfaces' in config['new_config'] and len(config['new_config']['interfaces']) > 0:
                    for interface in config['new_config']['interfaces']:
                        interface_name=interface["name"] if "name" in interface else None
                        interfaces.append({
                            "transponder_uuid"    : transponder_get_uuid(device_id),
                            'interface_uuid'      : interface_get_uuid(interface_name,device_uuid),
                            "name"                : interface_name,
                            "status"              : interface["status"            ] if "status" in interface else None,
                            "operation_status"    : interface["operation_status"  ] if "operation_status" in interface else None,
                            "ifindex"             : interface["ifindex"           ] if "ifindex" in interface else None,
                            "in_octets"           : interface["in_octets"         ] if "in_octets" in interface else None,
                            "in_pkts"             : interface["in_pkts"           ] if "in_pkts" in interface else None,
                            "in_unicast_pkts"     : interface["in_unicast_pkts"   ] if "in_unicast_pkts" in interface else None,
                            "in_broadcast_pkts"   : interface["in_broadcast_pkts" ] if "in_broadcast_pkts" in interface else None,
                            "in_multicast_pkts"   : interface["in_multicast_pkts" ] if "in_multicast_pkts" in interface else None,
                            "out_discards"        : interface["out_discards"      ] if "out_discards" in interface else None,
                            "out_errors"          : interface["out_errors"        ] if "out_errors" in interface else None,
                            "in_discards"         : interface["in_discards"       ] if "in_discards" in interface else None,
                            "in_errors"           : interface["in_errors"         ] if "in_errors" in interface else None,
                            "out_octets"          : interface["out_octets"        ] if "out_octets" in interface else None,  
                            "out_pkts"            : interface["out_pkts"          ] if "out_pkts" in interface else None,
                            "out_unicast_pkts"    : interface["out_unicast_pkts"  ] if "out_unicast_pkts" in interface else None,
                            "out_broadcast_pkts"  : interface["out_broadcast_pkts"] if "out_broadcast_pkts" in interface else None,
                            "out_multicast_pkts"  : interface["out_multicast_pkts"] if "out_multicast_pkts" in interface  else None,
                            "last_clear"          : interface["last_clear"        ] if "last_clear" in interface else None
                        })    
                    
                if 'channels' in config['new_config'] and len(config['new_config']['channels']) > 0:
                    #channels = [channel['name']['index'] for channel in config['channels']]
            
                    for channel_params in config['new_config']['channels']:
                        channels.append({
                            # "opticalconfig_uuid":opticalconfig_uuid,
                            "transponder_uuid"    : transponder_get_uuid(device_id),
                            "channel_uuid"        : channel_get_uuid(channel_params['name']['index'],device_uuid),
                            "channel_name"        : channel_params['name']['index'],
                            "frequency"           : int(channel_params["frequency"]) if "frequency" in channel_params  else 0,
                            "operational_mode"    : int(channel_params["operational-mode"]) if "operational-mode" in channel_params else 0,
                            "target_output_power" : channel_params["target-output-power"] if "target-output-power" in channel_params else '',
                            "status"              : channel_params["status"] if "status" in channel_params else ""
                        })
                elif 'flow_handled' in config and 'new_config' in config :
                    target_config = config['new_config']
                    dest_pair = None
                    src = None
                    dst = None
                    src_pair = config['flow_handled'][0]
                    
                    src, dst = src_pair
                    if src_pair is None and len(config['flow_handled'])>1 :
                        dest_pair = config['flow_handled'][1]
                        src, dst = dest_pair
                    channel_index = src if src is not None and src !='0' else dst
                    channel_name = f"channel-{channel_index}"
                    channels.append({
                        # "opticalconfig_uuid":opticalconfig_uuid,
                        "transponder_uuid"    : transponder_get_uuid(device_id),
                        "channel_uuid"        : channel_get_uuid(channel_name,device_uuid),
                        "channel_name"        : channel_name,
                        "frequency"           : int(target_config["frequency"]) if "frequency" in target_config  else 0,
                        "operational_mode"    : int(target_config["operational-mode"]) if "operational-mode" in target_config else 0,
                        "target_output_power" : target_config["target-output-power"] if "target-output-power" in target_config else '',
                        "status"              : target_config["status"] if "status" in target_config else ""
                    })

                transponder.append({
                    "transponder_uuid"  : transponder_get_uuid(device_id),
                    "transcievers"      : transceivers,
                   
                    "opticalconfig_uuid": opticalconfig_uuid,
                })

            if config_type == DeviceTypeEnum.OPTICAL_ROADM._value_:
                if channel_namespace is None and  'channel_namespace' in config['new_config']:
                    channel_namespace=config['new_config']['channel_namespace']
                if 'is_opticalband' in config and not config['is_opticalband']:
                    is_optical_band=config['is_opticalband']
                    bidir = config['new_config']['bidir']
                    #channels = [channel['name']['index'] for channel in config['channels']]
                    if 'flow_handled' in config  and len(config['flow_handled'])>0 :
                        num = 0    
                        flow_id = config["new_config"]["flow_id"] if 'flow_id' in config['new_config'] else None
                        for flow in config['flow_handled']:
                            src_port, dest_port = flow
                            channel_index = flow_id + num
                            num += 1
                            channels.append({
                                # "opticalconfig_uuid":opticalconfig_uuid,
                                "roadm_uuid"          : roadm_get_uuid(device_id),
                                "channel_uuid"        : channel_get_uuid(f'media_channel_{channel_index}',device_uuid),
                                "band_name"           : config['new_config']['band_type'],
                                "lower_frequency"     : int(int(config['new_config']['frequency']) - (int(config['new_config']['band'])/2)) if "frequency" in config['new_config']  else 0,
                                "upper_frequency"     : int(int(config['new_config']['frequency']) + (int(config['new_config']['band'])/2)) if "frequency" in config['new_config']  else 0,
                                "dest_port"           : dest_port,
                                "src_port"            : src_port,
                                "status"              : config['new_config']["status"] if "status" in config['new_config'] else "",
                                "type"                : 'media_channel',
                                "optical_band_parent" : str( config['new_config']['ob_id']) if 'ob_id' in config['new_config'] else None,
                                "channel_index"       : str(channel_index) if channel_index is not None else None
                            })
                            if not bidir: break
                if 'is_opticalband' in config and config['is_opticalband']:
                    is_optical_band=config['is_opticalband']
                    #channels = [channel['name']['index'] for channel in config['channels']]
                    
                    if 'flow_handled' in config and len(config['flow_handled']) > 0:
                        ob_id = config['new_config']['ob_id'] if 'ob_id' in config['new_config'] else None
                        num = 0
                        for flow in config['flow_handled']:
                            src_port, dest_port = flow
                            channel_index = ob_id + num
                            num += 1
                            channels.append({
                                # "opticalconfig_uuid":opticalconfig_uuid,
                                "roadm_uuid"      : roadm_get_uuid(device_id),
                                "channel_uuid"    : channel_get_uuid(f'optical_bands_{channel_index}',device_uuid),
                                "band_name"       : config['new_config']['band_type'],
                                "lower_frequency" : int(config['new_config']["low-freq"]) if "low-freq" in config['new_config']  else 0,
                                "upper_frequency" : int(config['new_config']["up-freq"]) if "up-freq" in config['new_config']  else 0,
                                "dest_port"       : dest_port,
                                "src_port"        : src_port,
                                "status"          : config['new_config']["status"] if "status" in config['new_config'] else "",
                                "type"            : 'optical_band',
                                "channel_index"   : str( channel_index) if channel_index is not None else None
                            })
                            optical_bands.append ({
                                 "channel_uuid"    : channel_get_uuid(f'optical_bands_{channel_index}',device_uuid),
                                 'connection_uuid' : config['connection_uuid'],
                                 "ob_uuid" : ob_get_uuid (channel_index),
                                 'created_at':now
                                 
                            })

                roadms.append({
                    "roadm_uuid"        : roadm_get_uuid(device_id),
                    "opticalconfig_uuid": opticalconfig_uuid,
                })

        OpticalConfig_data.append({
            "opticalconfig_uuid": opticalconfig_uuid,
            # "transcievers"      : transceivers,
            # "interfaces"        :"",
            "channel_namespace" : channel_namespace ,
            "endpoints"         : [json.dumps(endpoint) for endpoint in config['new_config'].get("endpoints",[])],
            "device_uuid"       : device_uuid,
            "type"              : config_type
        })

    def callback(session:Session)->bool:
        stmt = insert(OpticalConfigModel).values(OpticalConfig_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[OpticalConfigModel.opticalconfig_uuid],
            set_=dict(
                channel_namespace=stmt.excluded.channel_namespace
            )
        )
        stmt = stmt.returning(OpticalConfigModel.opticalconfig_uuid)
        opticalconfig_id = session.execute(stmt).fetchone()
        if config_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_:
            if (len(transponder)>0):
                stmt = insert(TransponderTypeModel).values(transponder)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[TransponderTypeModel.transponder_uuid],
                    set_=dict(
                        transcievers = stmt.excluded.transcievers,
                    )
                )
                stmt = stmt.returning(TransponderTypeModel.transponder_uuid)
                transponder_id = session.execute(stmt).fetchone()
            if (len(interfaces)>0) :
                    model_columns = inspect(TransponderInterfaceModel).c.keys()
                    stmt = insert(TransponderInterfaceModel).values(interfaces)
                       
                    stmt = stmt.on_conflict_do_update(
                        index_elements=[TransponderInterfaceModel.interface_uuid ],
                        set_={field: stmt.excluded[field] for field in model_columns if field != 'interface_uuid' }
                        
                    )
                    stmt = stmt.returning(TransponderInterfaceModel.interface_uuid)
                    interface_id = session.execute(stmt).fetchone() 
    

            if len(channels) > 0:
                stmt = insert(OpticalChannelModel).values(channels)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[OpticalChannelModel.channel_uuid],
                    set_=dict(
                        channel_name        = stmt.excluded.channel_name,
                        frequency           = stmt.excluded.frequency,
                        operational_mode    = stmt.excluded.operational_mode,
                        target_output_power = stmt.excluded.target_output_power,
                        status              = stmt.excluded.status,
                    )
                )
                stmt = stmt.returning(OpticalChannelModel.channel_uuid)
                opticalChannel_id = session.execute(stmt).fetchone()
        if config_type == DeviceTypeEnum.OPTICAL_ROADM._value_:
            if len(roadms) > 0:
                stmt = insert(RoadmTypeModel).values(roadms)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[RoadmTypeModel.roadm_uuid],
                    set_=dict(
                        circuits = stmt.excluded.circuits
                    )
                )
                stmt = stmt.returning(RoadmTypeModel.roadm_uuid)
                roadm_id = session.execute(stmt).fetchone()
                
            if (channels is not None and  len(channels) > 0):
                stmt = insert(ChannelModel).values(channels)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[ChannelModel.channel_uuid ],
                    set_=dict(
                        band_name       = stmt.excluded.band_name,
                        lower_frequency = stmt.excluded.lower_frequency,
                        upper_frequency = stmt.excluded.upper_frequency,
                        type            = stmt.excluded.type,
                        status          = stmt.excluded.status,
                        dest_port       = stmt.excluded.dest_port,
                        src_port        = stmt.excluded.src_port,
                    )
                )
                stmt = stmt.returning(ChannelModel.channel_uuid)
                opticalChannel_id = session.execute(stmt).fetchone()
               
    opticalconfig_id = run_transaction(sessionmaker(bind=db_engine), callback)
    if is_optical_band: set_optical_band(db_engine,optical_bands)

    return {'opticalconfig_uuid': opticalconfig_id}

def select_opticalconfig(db_engine : Engine, request : OpticalConfigId):
    def callback(session : Session) -> OpticalConfig:
        result = OpticalConfig()
        stmt = session.query(OpticalConfigModel)
        stmt = stmt.filter_by(opticalconfig_uuid=request.opticalconfig_uuid)
        obj = stmt.first()
        if obj is not None:
            result.config = json.dumps(obj.dump())
            ids_obj = obj.dump_id()
            result.opticalconfig_id.opticalconfig_uuid = ids_obj["opticalconfig_uuid"]
            result.device_id.device_uuid.uuid=ids_obj["device_uuid"]
        return result
    return run_transaction(sessionmaker(bind=db_engine, expire_on_commit=False), callback)

def delete_opticalconfig(db_engine : Engine, messagebroker : MessageBroker, request : OpticalConfigId):
    opticalconfig_uuid = request.opticalconfig_uuid
    def callback(session : Session):
        #query = session.query(OpticalConfigModel)
        num_deleted = session.query(OpticalConfigModel).filter_by(opticalconfig_uuid=opticalconfig_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    if deleted:
        notify_event_opticalconfig(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, opticalconfig_uuid)
    return Empty()

def delete_opticalchannel(db_engine : Engine, messagebroker : MessageBroker, request : OpticalConfig):
    config = json.loads(request.config)
    device_id = request.device_id
    device_uuid =  request.device_id.device_uuid.uuid
    opticalconfig_uuid = request.opticalconfig_id.opticalconfig_uuid
    channels = []
    config_type = None
    logging.info(f"DeleteOpticalchannel {request.config}")
    if "type" in config :
        config_type= config["type"]    
    if 'new_config' in config:
        new_cfg = config['new_config']
        flow_id = new_cfg['flow_id'] if 'flow_id' in new_cfg else 0 
        if 'flow' in config:
            if config_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_:  
                for flow in config['flow']:
                    src,dest = flow
                    channel_index= src if src is not None and  src!='0' else dest
                    channel_name= f"channel-{channel_index}"
                    channels.append({
                        # "opticalconfig_uuid":opticalconfig_uuid,
                        "transponder_uuid"   : transponder_get_uuid(device_id),
                        "channel_uuid"       : channel_get_uuid(channel_name ,device_uuid),
                        "channel_name"       : channel_name ,
                        "frequency"          : 0,
                        "operational_mode"   : None,
                        "target_output_power": None,
                        "status"             : "DISABLED"
                    })
                    
            elif config_type == DeviceTypeEnum.OPEN_ROADM._value_:    
                    if 'new_config' in config and 'interfaces' in config['new_config']:
                        for i in config['new_config']['interfaces']:
                            channels.append({
                            "interface_uuid"      : interface_get_uuid(i['interface_name'],device_uuid),
                            'name'                : i["interface_name"],
                            "type"                :'Null',
                            "administrative_state": "Null",
                            "circuit_pack_name"   : 'Null',
                            "port"                : "Null",
                            "interface_list"      :'Null',
                            "frequency"           : "Null",
                            "width"               :  0,
                            "roadm_uuid"          : roadm_get_uuid(device_id),
                        })
                            
            elif config_type == DeviceTypeEnum.OPTICAL_ROADM._value_:
                channel_num = flow_id
               
                if 'is_opticalband' in config : 
                     if config['is_opticalband']: 
                        ob_id = config['new_config']['ob_id'] if 'ob_id' in config['new_config'] else None
                        if len(config['flow']) == 0:
                            channel_index = ob_id + channel_num
                            channel_name = f'optical_bands_{channel_index}' 
                            channels.append(channel_get_uuid(channel_name, device_uuid))
                        else:
                            for flow in config['flow']:
                                channel_index = ob_id+channel_num
                                channel_num +=1
                                channel_name = f'optical_bands_{channel_index}' 
                                channels.append(channel_get_uuid(channel_name, device_uuid))
                     else :            
                   
                        if len(config['flow']) == 0:
                        
                            channel_name = f'media_channel_{channel_num}'
                            channels.append(channel_get_uuid(channel_name, device_uuid))
                        else:
                            for flow in config['flow']:
                                channel_name = f'media_channel_{channel_num}'
                                channels.append(channel_get_uuid(channel_name, device_uuid))
                                channel_num += 1
    
                     

    def callback(session : Session):
        all_suceed = []
        if config_type == DeviceTypeEnum.OPTICAL_ROADM._value_:
            for channel_uuid in channels:
                num_deleted = session.query(ChannelModel).filter_by(channel_uuid=channel_uuid).delete()
                all_suceed.append(num_deleted > 0)
        elif config_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_:
            if len(channels) > 0:
                stmt = insert(OpticalChannelModel).values(channels)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[OpticalChannelModel.channel_uuid ],
                    set_=dict(
                        channel_name        = stmt.excluded.channel_name ,
                        frequency           = stmt.excluded.frequency,
                        operational_mode    = stmt.excluded.operational_mode,
                        target_output_power = stmt.excluded.target_output_power,
                        status              = stmt.excluded.status
                    )
                )
                stmt = stmt.returning(OpticalChannelModel.channel_uuid)
                opticalChannel_id = session.execute(stmt).fetchone()
                all_suceed.append(True)
        elif config_type == DeviceTypeEnum.OPEN_ROADM._value_:
            if len(channels) > 0:
                for i in channels : 
                    num_deleted = session.query(ORInterfaceModel).filter_by(interface_uuid=i['interface_uuid']).delete()
                    all_suceed.append(num_deleted > 0)

        return all_suceed

    all_deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    for stat in all_deleted:
        if not stat: return
    notify_event_opticalconfig(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, opticalconfig_uuid)
    return Empty()
