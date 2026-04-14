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

import json, logging , time
from flask import (
    request, redirect, render_template, Blueprint, flash, session, url_for,
    current_app, make_response
)
from common.proto.context_pb2 import (
    Empty, OpticalConfig, OpticalConfigId, OpticalConfigList , TopologyId
)
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.context_queries.OpticalConfig import opticalconfig_get_uuid
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from common.DeviceTypes import DeviceTypeEnum
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from slice.client.SliceClient import SliceClient
from .forms import UpdateDeviceForm, AddTrancseiver, UpdateStatusForm

opticalconfig = Blueprint('opticalconfig', __name__, url_prefix="/opticalconfig")

context_client = ContextClient()
device_client = DeviceClient()
service_client = ServiceClient()
slice_client = SliceClient()

LOGGER = logging.getLogger(__name__)

DESCRIPTOR_LOADER_NUM_WORKERS = 10

@opticalconfig.get("/")
def home() :
    list_config = []
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        #time.sleep(5)
        flash("Please select a context!", "warning")
        
        return redirect(url_for("main.home"))

   
    context_client.connect()
    opticalConfig_list : OpticalConfigList = context_client.GetOpticalConfig(Empty())
    for configs in opticalConfig_list.opticalconfigs:
        value = json.loads(configs.config) if type(configs.config)==str else configs.config
        config_type = value["type"]
        if config_type != DeviceTypeEnum.OPEN_ROADM._value_ :
            if 'channels' in value:
                value["channels_number"] = len(value['channels'])
        else:
            if 'interfaces' in value:
                
                value["channels_number"] = len([i for i in value["interfaces"] if i["type"] != 'Null'])
        # value['operationalMode']=value['operational-mode']
        # value['targetOutputPower']=value['target-output-power']
        value['opticalconfig_id']=configs.opticalconfig_id
        # value['line_port']=value["line-port"]
        list_config.append(value)

    context_client.close()
    return render_template('opticalconfig/home.html', config=list_config)

@opticalconfig.route('<path:config_uuid>/detail',methods=['GET'])    
def show_details(config_uuid):
    opticalconfigId = OpticalConfigId()
    opticalconfigId.opticalconfig_uuid = config_uuid
    device_details = []
    
    context_client.connect()
    response = context_client.SelectOpticalConfig(opticalconfigId)
    context_client.close()
    if (response and response.opticalconfig_id.opticalconfig_uuid !=''):
        opticalConfig = OpticalConfig()
        opticalConfig.CopyFrom(response)

        device_name = ""
        config = json.loads(opticalConfig.config)
        logging.info(f"config {config}")
        if "device_name" in config:
            device_name = config["device_name"]

            config_type = config["type"]
            if config_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_:
                LOGGER.info("config details from show detail %s",config)
                if 'channels' in config:
                    for channel in config['channels'] :
                        new_config={}
                        new_config["name"]=channel['name']
                        new_config['operationalMode']=channel['operational-mode'] if 'operational-mode' in channel else ''
                        new_config['targetOutputPower']=channel['target-output-power'] if 'target-output-power' in channel else ''
                        new_config["frequency"]=channel['frequency'] if 'frequency' in channel else ''
                        new_config['line_port']=channel["line-port"] if 'line-port' in channel else ''
                        new_config["status"] = channel['status'] if 'status' in channel else ""
                        device_details.append(new_config)

            if config_type == DeviceTypeEnum.OPTICAL_ROADM._value_:
                LOGGER.info("config details from show detail %s",config)
                if 'channels' in config:
                    for channel in config['channels'] :
                        new_config={}
                        new_config["band_name"]=channel['band_name'] if 'band_name' in channel else None
                        new_config['type']=channel['type'] if 'type' in channel else ''
                        new_config['src_port']=channel['src_port'] if 'src_port' in channel else ''
                        new_config['dest_port']=channel['dest_port'] if 'dest_port' in channel else ''
                        new_config["lower_frequency"]=channel['lower_frequency'] if 'lower_frequency' in channel else ''
                        new_config["upper_frequency"]=channel['upper_frequency'] if 'upper_frequency' in channel else ''
                        new_config["status"] = channel['status'] if 'status' in channel else ""
                        new_config['optical_band_parent']= channel['optical_band_parent'] if 'optical_band_parent' in channel else ''
                        new_config['channel_index']= channel['channel_index'] if 'channel_index' in channel else ''
                        device_details.append(new_config)

            if config_type == DeviceTypeEnum.OPEN_ROADM._value_:
                if 'interfaces' in config :
                    for interface in config["interfaces"]:
                        if interface["type"] != "Null":
                            new_config={}
                            new_config["name"]=interface["name"] if "name" in interface else '' 
                            new_config["administrative_state"]=interface[ "administrative_state"]
                            new_config["circuit_pack_name"]=interface["circuit_pack_name"]
                            new_config["port"]=interface["port"]
                            new_config["interface_list"]=interface["interface_list"]
                            new_config["frequency"]=interface["frequency"]
                            new_config["width"]=interface[ "width"]
                            new_config["type"]=interface["type"]
                            device_details.append(new_config)

        LOGGER.info("device details  %s",device_details)
        return render_template('opticalconfig/details.html', device=device_details,config_id=config_uuid,device_name=device_name,type=config_type)

    return render_template(
        'opticalconfig/details.html', device=device_details, config_id=config_uuid,
        device_name=device_name, type=config_type
    )


@opticalconfig.route('<path:opticalconfig_uuid>/delete', methods=['GET'])
def delete_opitcalconfig (opticalconfig_uuid)  :
    try : 
        opticalconfigId = OpticalConfigId()
        opticalconfigId.opticalconfig_uuid = opticalconfig_uuid
        context_client.connect()
        context_client.DeleteOpticalConfig(opticalconfigId)
        context_client.close()
        flash(f'OpticalConfig "{opticalconfig_uuid}" deleted successfully!', 'success')
    except Exception as e: # pylint: disable=broad-except
        flash(f'Problem deleting optical config {opticalconfig_uuid}', 'danger')
        current_app.logger.exception(e)
    return redirect(url_for('opticalconfig.home'))


@opticalconfig.route('delete_all', methods=['GET'])
def delete_all_devices ()  :
    try : 
        context_uuid = session['context_uuid']
        topology_uuid = session['topology_uuid']
        json_topo_id = json_topology_id(topology_uuid, context_id=json_context_id(context_uuid))
        context_client.connect()
        response = context_client.GetTopologyDetails(TopologyId(**json_topo_id))
        context_client.close()
        
        devices = []
        for device in response.devices:
            devices.append({
                'device_id': device.device_id,
                'name': device.name,
                'type': device.device_type,
            })

      
        optical_links = []
        for link in response.optical_links:
            if len(link.link_endpoint_ids) != 2:
                str_link = grpc_message_to_json_string(link)
                LOGGER.warning('Unexpected link with len(endpoints) != 2: {:s}'.format(str_link))
                continue
            optical_links.append({
                'id': link.link_id.link_uuid.uuid,
                'name': link.name,
                'source': link.link_endpoint_ids[0].device_id.device_uuid.uuid,
                'target': link.link_endpoint_ids[1].device_id.device_uuid.uuid,
            })    
        if len(optical_links)!= 0 : 
            flash(f'you should delete all optical links before deleting all the devices ', 'danger')
            return redirect(url_for('opticalconfig.home'))
        if len(devices) > 0 : 
            LOGGER.info(f'devices to delete {devices}')
            device_client.connect()
            for d in devices: 
                if 'device_id' in d : 
                   device_client.DeleteDevice(d['device_id'])
             
            flash('All devices were deleted successfully','success') 
                     
            
    except Exception as e: # pylint: disable=broad-except
        flash(f'Problem deleting optical devices ', 'danger')
        current_app.logger.exception(e)
    return redirect(url_for('opticalconfig.home'))



@opticalconfig.route('/update_opticalconfig', methods=['POST'])
def update_externally():
    if (request.method == 'POST'):
        data = request.get_json()
        devices = data.get('devices')

        myResponse = []
        status_code = ''
        for device in devices :
            port = device.get("port")
            channel_name = f"channel-{port}"
            device_name = device.get("device_name")
        
            if device_name:
                opticalconfig_uuid = opticalconfig_get_uuid(device_name=device_name)
                opticalconfigId=OpticalConfigId()
                opticalconfigId.opticalconfig_uuid = opticalconfig_uuid
                context_client.connect()
                opticalconfig = context_client.SelectOpticalConfig(opticalconfigId)
                context_client.close()
            
                if opticalconfig and opticalconfig.opticalconfig_id.opticalconfig_uuid != '' :
                    new_opticalconfig = OpticalConfig()
                    new_opticalconfig.CopyFrom(opticalconfig)
                    config = json.loads(opticalconfig.config)
                    channels = config['channels']
                    target_channel = next((item for item in channels if item["name"]['index'] == channel_name) , None)
                    target_power = device.get( "target-output-power")
                    freq = device.get("frequency")
                    mode = device.get("operational-mode")
                    status = device.get("status","ENABLED")

                    if target_channel:
                        if target_power is not None :
                            target_channel["target-output-power"] =str(target_power)
                        if freq  is not None :
                            target_channel["frequency"] = freq
                        if mode is not None :
                            target_channel["operational-mode"] = mode
                        if status is not None :
                            target_channel["status"] = "ENABLED"
                        #del target_channel['name']
                        config["new_config"]=target_channel
                        config["new_config"]["channel_name"]=channel_name
                        config["flow"]=[(port,'0')]
                        opticalconfig.config =json.dumps(config)

                        try:
                            device_client.connect()
                            device_client.ConfigureOpticalDevice(opticalconfig)
                            device_client.close()

                            myResponse.append(f"device {device_name} port {port} is updated successfully")
                            status_code = 200
                        except Exception as e: # pylint: disable=broad-except
                            myResponse.append(f"Problem updating the device. {e}")
                            status_code = 500 
                            break   
                    else :
                        myResponse.append(f"requested channel {channel_name} is not existed")
                        status_code = 400
                        break         
                else :
                    myResponse.append(f"requested device {device_name} is not existed")
                    status_code = 400
                    break              

        response=make_response(f'{myResponse}')
        response.status_code=status_code
        return response

        #return redirect(url_for('opticalconfig.show_details',config_uuid=opticalconfig_uuid))
        #return redirect(url_for('opticalconfig.home'))
    
@opticalconfig.route('<path:config_uuid>/<path:channel_name>/update', methods=['GET', 'POST'])
def update(config_uuid, channel_name):
    form = UpdateDeviceForm()

    opticalconfigId = OpticalConfigId()
    opticalconfigId.opticalconfig_uuid = config_uuid
    context_client.connect()
    response = context_client.SelectOpticalConfig(opticalconfigId)
    context_client.close()

    opticalconfig = OpticalConfig()
    opticalconfig.CopyFrom(response)
    config =json.loads(opticalconfig.config)
    new_config={}
    for channel in config['channels']:
        if (channel["name"] == channel_name):
            new_config=channel
            form.frequency.default = channel["frequency"]
            form.operational_mode.default=channel["operational-mode"]
            form.power.default=channel["target-output-power"]
            form.line_port.choices = [("","")]

    for transceiver in config["transceivers"]['transceiver']:
        form.line_port.choices.append((transceiver,transceiver))

    # listing enum values
    if form.validate_on_submit():
        new_config["target-output-power"] =form.power.data if form.power.data != '' else  new_config['target-output-power']
        new_config["frequency"]=form.frequency.data if form.frequency.data != '' else new_config['frequency']
        new_config["operational-mode"]=form.operational_mode.data if form.operational_mode.data != '' else new_config['operational-mode']
        new_config["line-port"]=form.line_port.data if form.line_port.data != '' else new_config['line-port']
        opticalconfig.config =json.dumps(new_config)

        try:
            device_client.connect()
            device_client.ConfigureOpticalDevice(opticalconfig)
            device_client.close()
            flash(f' device  was updated.', 'success')
            return redirect(url_for('opticalconfig.show_details',config_uuid=config_uuid))
        except Exception as e: # pylint: disable=broad-except
             flash(f'Problem updating the device. {e}', 'danger')  
    return render_template('device/update.html', device=response, form=form, submit_text='Update Device',channel_name=channel_name)


@opticalconfig.route('refresh_all',methods=['POST','GET'])
def refresh_all ():
    try:
        context_client.connect()
        opticalConfig_list = context_client.GetOpticalConfig(Empty())
        device_client.connect()
        device_client.GetDeviceConfiguration(opticalConfig_list)
    except Exception as err : 
        flash(f'Connection is failed: `{str(err)}`', 'danger')
        return redirect(url_for("opticalconfig.home"))    

    finally:
       context_client.close()
       device_client.close()
       
    return home()


@opticalconfig.route('<path:config_uuid>/add_transceiver', methods=['GET','POST'])
def add_transceiver (config_uuid):
    config={}
    addtrancseiver=AddTrancseiver()
    opticalconfigId=OpticalConfig()
    opticalconfigId.opticalconfig_uuid=config_uuid
    context_client.connect()
    response = context_client.SelectOpticalConfig(opticalconfigId)
    context_client.close()
    opticlConfig=OpticalConfig()
    opticlConfig.CopyFrom(response)
   
    if addtrancseiver.validate_on_submit():
        config["add_transceiver"]=addtrancseiver.transceiver.data
        opticlConfig.config=json.dumps(config)
       
        try:
            device_client.connect()
            device_client.ConfigureOpticalDevice(opticlConfig)
            device_client.close()
            flash(f' device  was updated.', 'success')
            return redirect(url_for('opticalconfig.update',config_uuid=config_uuid))
        except Exception as e: # pylint: disable=broad-except
             flash(f'Problem updating the device. {e}', 'danger')  
    return render_template('opticalconfig/add_transceiver.html',form=addtrancseiver, submit_text='Add Trancseiver')         


@opticalconfig.route('<path:config_uuid>/<path:channel_name>/update_status', methods=['GET','POST'])
def update_status (config_uuid,channel_name):
    config = {}
    form = UpdateStatusForm()

    opticalconfigId=OpticalConfigId()
    opticalconfigId.opticalconfig_uuid=config_uuid
    context_client.connect()
    response = context_client.SelectOpticalConfig(opticalconfigId)
    context_client.close()
    opticlConfig=OpticalConfig()
    opticlConfig.CopyFrom(response)
    config=json.loads(opticlConfig.config)
    new_config={}
    port=""
    if form.validate_on_submit():
        if channel_name:
            port = channel_name.split('-')[1]
        new_config["status"]=form.status.data
        new_config["name"]=channel_name
        config["flow"]=[(port,'0')]
        config["new_config"]=new_config
        opticlConfig.config=json.dumps(config)

        try:
            device_client.connect()
            device_client.ConfigureOpticalDevice(opticlConfig)
            device_client.close()
            flash(f' device  was updated.', 'success')
            return redirect(url_for('opticalconfig.show_details',config_uuid=config_uuid))
        except Exception as e: # pylint: disable=broad-except
             flash(f'Problem updating the device. {e}', 'danger')  
    return render_template(
        'opticalconfig/update_status.html', form=form, channel_name=channel_name,
        submit_text='Update Device Status'
    )

@opticalconfig.route('/configure_openroadm', methods=['POST'])
def update_openroadm():
    if (request.method == 'POST'):
        ports_list= []
        data = request.get_json()
        LOGGER.info(f"data {data}")  
        devices=data.get('devices')
        LOGGER.info(f"devices {devices}")  
        myResponse =[]
        status_code=''
        config={}
        target_interface={}
        for device in devices :
            frequency = device.get("frequency")
            width= device.get("width")
            ports=device.get('ports')
            device_name=device.get("device_name")
            LOGGER.info(f"device from post {device}")
            target_interface["frequency"]=frequency
            target_interface["width"]=width
            target_interface["administrative-state"]="inService"
            target_interface["config_type"]=device.get("config_type")

            if (device_name):
                opticalconfig_uuid = opticalconfig_get_uuid(device_name=device_name)
                opticalconfigId=OpticalConfigId()
                opticalconfigId.opticalconfig_uuid=opticalconfig_uuid
                context_client.connect()
                opticalconfig = context_client.SelectOpticalConfig(opticalconfigId)
                context_client.close()
                config =json.loads(opticalconfig.config)    
                for port in ports :
                    ports_list.append({
                        "supporting-circuit-pack-name":port["circuit_pack"],
                        'supporting-interface-list':port["interface_list"],
                        'supporting-port':port["port"]
                    })
                target_interface["ports"]=ports_list    
                config["new_config"]=target_interface
                opticalconfig.config =json.dumps(config)    
                try:
                    device_client.connect()
                    device_client.ConfigureOpticalDevice(opticalconfig)
                    device_client.close()
                    myResponse.append(f"device {device_name} port {port} is updated successfully")
                    status_code = 200
                except Exception as e: # pylint: disable=broad-except
                    myResponse.append(f"Problem updating the device. {e}")
                    status_code = 500 
                    break   
            else :
                myResponse.append(f"requested device {device_name} is not existed")
                status_code = 400
                break              

        response=make_response(f'{myResponse}')
        response.status_code=status_code
        return response
