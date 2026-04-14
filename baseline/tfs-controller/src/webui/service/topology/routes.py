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

import json,logging
from flask import current_app, render_template, Blueprint, flash, session, redirect, url_for, request
from common.proto.context_pb2 import (
    ConfigActionEnum, ConfigRule, ConfigRule_Custom, Device, DeviceConfig, DeviceDriverEnum, DeviceId, DeviceList, DeviceOperationalStatusEnum, 
    Empty, EndPoint, EndPointId, TopologyId, Uuid)
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from webui.service.device.forms import AddDeviceForm
from common.DeviceTypes import DeviceTypeEnum
from webui.service.topology.forms import ConfigForm, SpeakerForm
from webui.service.topology.forms import UpdateDeviceForm

from bgpls_speaker.client.BgplsClient import BgplsClient
from common.proto.bgpls_pb2 import (BgplsSpeaker, DiscoveredDeviceList,DiscoveredDevice,DiscoveredLinkList,DiscoveredLink, NodeDescriptors)

topology = Blueprint('topology', __name__, url_prefix='/topology')
context_client = ContextClient()
device_client = DeviceClient()
bgpls_client = BgplsClient()
logger = logging.getLogger(__name__)

@topology.get('/')
def home():
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))

    context_uuid = session['context_uuid']
    topology_uuid = session['topology_uuid']

    context_client.connect()
    json_topo_id = json_topology_id(topology_uuid, context_id=json_context_id(context_uuid))
    grpc_topology = context_client.GetTopology(TopologyId(**json_topo_id))
    topo_device_uuids = {device_id.device_uuid.uuid for device_id in grpc_topology.device_ids}
    
    if grpc_topology is None:
        flash('Context({:s})/Topology({:s}) not found'.format(str(context_uuid), str(topology_uuid)), 'danger')
        devices = []
    else:
        topo_device_uuids = {device_id.device_uuid.uuid for device_id in grpc_topology.device_ids}
        grpc_devices: DeviceList = context_client.ListDevices(Empty())
        devices = [
            device for device in grpc_devices.devices
            if device.device_id.device_uuid.uuid in topo_device_uuids
        ]

    # ListNewDevices discovered from bgpls
    logger.info('topology/home')
    bgpls_client.connect()
    logger.info('bgpls_client.connect %s',bgpls_client)
    discovered_device_list = bgpls_client.ListDiscoveredDevices(Empty())
    logger.info('discoveredDeviceList %s',discovered_device_list)
    # List Links discovered from bgpls
    discovered_link_list = bgpls_client.ListDiscoveredLinks(Empty())
    logger.info('discoveredLinkList %s',discovered_link_list)
    # List current open speaker connections
    speaker_list=bgpls_client.ListBgplsSpeakers(Empty())


    context_client.close()
    bgpls_client.close()

    return render_template(
        'topology/home.html', devices=devices, dde=DeviceDriverEnum,
        dose=DeviceOperationalStatusEnum,disdev=discovered_device_list.discovereddevices,
        dislink=discovered_link_list.discoveredlinks,speakers=speaker_list.speakers)

@topology.route('add/<path:device_name>', methods=['GET', 'POST'])
def add(device_name):
    """"
    Add a discovered device from bgpls protocol. Populate form from
    existent info in bgpls. 
    """
    # TODO: Conect to device and get necessary info
    form = AddDeviceForm()

    logger.info('topology/add')    
    
    # listing enum values
    form.operational_status.choices = []
    for key, _ in DeviceOperationalStatusEnum.DESCRIPTOR.values_by_name.items():
        form.operational_status.choices.append(
            (DeviceOperationalStatusEnum.Value(key), key.replace('DEVICEOPERATIONALSTATUS_', '')))
        
    form.device_type.choices = []
    # items for Device Type field
    for device_type in DeviceTypeEnum:
        form.device_type.choices.append((device_type.value,device_type.value))    

    if form.validate_on_submit():
        device_obj = Device()
        # Device UUID: 
        device_obj.device_id.device_uuid.uuid = form.device_id.data # pylint: disable=no-member

        # Device type: 
        device_obj.device_type = str(form.device_type.data)

        # Device configurations: 
        config_rule = device_obj.device_config.config_rules.add() # pylint: disable=no-member
        config_rule.action = ConfigActionEnum.CONFIGACTION_SET
        config_rule.custom.resource_key = '_connect/address'
        config_rule.custom.resource_value = form.device_config_address.data

        config_rule = device_obj.device_config.config_rules.add() # pylint: disable=no-member
        config_rule.action = ConfigActionEnum.CONFIGACTION_SET
        config_rule.custom.resource_key = '_connect/port'
        config_rule.custom.resource_value = form.device_config_port.data

        config_rule = device_obj.device_config.config_rules.add() # pylint: disable=no-member
        config_rule.action = ConfigActionEnum.CONFIGACTION_SET
        config_rule.custom.resource_key = '_connect/settings'

        try:
            device_config_settings = json.loads(form.device_config_settings.data)
        except: # pylint: disable=bare-except
            device_config_settings = form.device_config_settings.data
        logger.info('(topology/add) config settings %s', form.device_config_settings.data)    
        if isinstance(device_config_settings, dict):
            config_rule.custom.resource_value = json.dumps(device_config_settings)
            logger.info('(topology/add) config settings is instance to json')
        else:
            config_rule.custom.resource_value = str(device_config_settings)

        # Device status: 
        device_obj.device_operational_status = form.operational_status.data

        # Device drivers: 
        if form.device_drivers_undefined.data:
            device_obj.device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_UNDEFINED)
        if form.device_drivers_openconfig.data:
            device_obj.device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG)
        if form.device_drivers_transport_api.data:
            device_obj.device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API)
        if form.device_drivers_p4.data:
            device_obj.device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_P4)
        if form.device_drivers_ietf_network_topology.data:
            device_obj.device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_IETF_NETWORK_TOPOLOGY)
        if form.device_drivers_onf_tr_352.data:
            device_obj.device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_ONF_TR_352)
        if form.device_drivers_xr.data:
            device_obj.device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_XR)

        try:
            device_client.connect()
            logger.info('add device from speaker:%s',device_obj)
            response: DeviceId = device_client.AddDevice(device_obj)
            device_client.close()
            flash(f'New device was created with ID "{response.device_uuid.uuid}".', 'success')
            bgpls_client.connect()
            bgpls_client.NotifyAddNodeToContext(NodeDescriptors(nodeName=device_obj.device_id.device_uuid.uuid))
            bgpls_client.close()
            return redirect(url_for('device.home'))
        except Exception as e:
            flash(f'Problem adding the device. {e.details()}', 'danger')
        
    # Prefill data with discovered info from speaker
    # Device Name from bgpls
    form.device_name=device_name
    device=device_name
    form.device_id.data=device_name
    # Default values (TODO: NOT WORKING)
    form.device_type.data=DeviceTypeEnum.EMULATED_PACKET_ROUTER
    form.device_config_settings.data=str('{"username": "admin", "password": "admin"}')

    return render_template('topology/add.html', form=form, device=device,
                        submit_text='Add New Device')

@topology.route('detail/<path:device_uuid>', methods=['GET', 'POST'])
def detail(device_uuid: str):
    request = DeviceId()
    request.device_uuid.uuid = device_uuid
    context_client.connect()
    response = context_client.GetDevice(request)
    context_client.close()
    return render_template('topology/detail.html', device=response,
                                                 dde=DeviceDriverEnum,
                                                 dose=DeviceOperationalStatusEnum)

@topology.route('addSpeaker', methods=['GET', 'POST'])
def addSpeaker():
    # Conectar con bgpls¿
    bgpls_client.connect()
    form = SpeakerForm()
    if form.validate_on_submit():
        logger.info('addSpeaker ip:%s',form.speaker_address.data)
        bgpls_client.AddBgplsSpeaker(BgplsSpeaker(address=form.speaker_address.data,port=form.speaker_port.data,asNumber=form.speaker_as.data))
        flash(f'Speaker "{form.speaker_address.data}:{form.speaker_port.data}" added successfully!', 'success')
    bgpls_client.close()
    return render_template('topology/addSpeaker.html',form=form)

@topology.route('formSpeaker', methods=['GET','POST'])
def formSpeaker():
    # Conectar con bgpls¿
    form = SpeakerForm()
    if request.method=="POST":
        address = form.speaker_address.data
        port = form.speaker_port.data
        as_ = form.speaker_as.data
        logger.info("FORM formSpeaker: %s %s %s", address,port,as_)
        
        flash(f'Speaker "{address}:{port}" added successfully!', 'success')

    return redirect(url_for('topology.home'))
    # return 'Form submitted'


@topology.route('editSpeakers', methods=['GET','POST'])
def editSpeakers():

    speakers=[]
    bgpls_client.connect()
    speaker_list=bgpls_client.ListBgplsSpeakers(Empty())
    speakers_ids=[speaker for speaker in speaker_list.speakers if speaker.id]
    speakers=[bgpls_client.GetSpeakerInfoFromId(ids) for ids in speakers_ids]
        
    bgpls_client.close()
    return render_template('topology/editSpeakers.html',speakers=speakers)


@topology.route('disconnectSpeaker/<path:speaker_address>', methods=['GET','POST'])
def disconnectSpeaker(speaker_address):

    bgpls_client.connect()
    current_speaker=BgplsSpeaker(address=speaker_address)
    logger.info('Disconnecting speaker: %s...',speaker_address)
    bgpls_client.DisconnectFromSpeaker(current_speaker)
    bgpls_client.close()

    return redirect(url_for('topology.editSpeakers'))