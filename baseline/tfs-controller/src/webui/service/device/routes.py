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

import json
from flask import (
    current_app, render_template, Blueprint, flash, session, redirect, url_for
)
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import (
    ConfigActionEnum, Device, DeviceDriverEnum, DeviceId, DeviceList,
    DeviceOperationalStatusEnum, Empty
)
from common.tools.context_queries.Device import get_device
from common.tools.context_queries.Topology import get_topology
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from webui.service.device.forms import AddDeviceForm, ConfigForm, UpdateDeviceForm

device = Blueprint('device', __name__, url_prefix='/device')
context_client = ContextClient()
device_client = DeviceClient()

@device.get('/')
def home():
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))

    context_uuid = session['context_uuid']
    topology_uuid = session['topology_uuid']

    context_client.connect()
    grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
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
    context_client.close()

    return render_template(
        'device/home.html', devices=devices, dde=DeviceDriverEnum,
        dose=DeviceOperationalStatusEnum)

@device.route('add', methods=['GET', 'POST'])
def add():
    form = AddDeviceForm()

    # listing enum values
    form.operational_status.choices = []
    for key, _ in DeviceOperationalStatusEnum.DESCRIPTOR.values_by_name.items():
        form.operational_status.choices.append(
            (DeviceOperationalStatusEnum.Value(key), key.replace('DEVICEOPERATIONALSTATUS_', '')))

    # items for Device Type field
    form.device_type.choices = []
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

        if isinstance(device_config_settings, dict):
            config_rule.custom.resource_value = json.dumps(device_config_settings)
        else:
            config_rule.custom.resource_value = str(device_config_settings)

        # Device status: 
        device_obj.device_operational_status = form.operational_status.data

        # Device drivers: 
        device_drivers = list()
        if form.device_drivers_undefined.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_UNDEFINED)
        if form.device_drivers_openconfig.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG)
        if form.device_drivers_transport_api.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API)
        if form.device_drivers_p4.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_P4)
        if form.device_drivers_ietf_network_topology.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_IETF_NETWORK_TOPOLOGY)
        if form.device_drivers_onf_tr_532.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_ONF_TR_532)
        if form.device_drivers_xr.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_XR)
        if form.device_drivers_ietf_l2vpn.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_IETF_L2VPN)
        if form.device_drivers_gnmi_openconfig.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_GNMI_OPENCONFIG)
        if form.device_drivers_optical_tfs.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_OPTICAL_TFS)
        if form.device_drivers_ietf_actn.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_IETF_ACTN)
        if form.device_drivers_oc.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_OC)
        if form.device_drivers_qkd.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_QKD)
        if form.device_drivers_ietf_l3vpn.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_IETF_L3VPN)
        if form.device_drivers_ietf_slice.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_IETF_SLICE)
        if form.device_drivers_nce.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_NCE)
        if form.device_drivers_smartnic.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_SMARTNIC)
        if form.device_drivers_morpheus.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_MORPHEUS)
        if form.device_drivers_ryu.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_RYU)
        if form.device_drivers_gnmi_nokia_srlinux.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_GNMI_NOKIA_SRLINUX)
        if form.device_drivers_openroadm.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_OPENROADM)
        if form.device_drivers_restconf_openconfig.data:
            device_drivers.append(DeviceDriverEnum.DEVICEDRIVER_RESTCONF_OPENCONFIG)
        device_obj.device_drivers.extend(device_drivers) # pylint: disable=no-member

        try:
            device_client.connect()
            response: DeviceId = device_client.AddDevice(device_obj)
            device_client.close()
            flash(f'New device was created with ID "{response.device_uuid.uuid}".', 'success')
            return redirect(url_for('device.home'))
        except Exception as e: # pylint: disable=broad-except
            flash(f'Problem adding the device. {e.details()}', 'danger')
        
    return render_template('device/add.html', form=form,
                        submit_text='Add New Device')

@device.route('detail/<path:device_uuid>', methods=['GET', 'POST'])
def detail(device_uuid: str):
    context_client.connect()
    device_obj = get_device(context_client, device_uuid, rw_copy=False)
    if device_obj is None:
        flash('Device({:s}) not found'.format(str(device_uuid)), 'danger')
        device_obj = Device()
    context_client.close()

    return render_template(
        'device/detail.html', device=device_obj, dde=DeviceDriverEnum, dose=DeviceOperationalStatusEnum)
    
@device.route('inventory/<path:device_uuid>', methods=['GET', 'POST'])
def inventory(device_uuid: str):
    context_client.connect()
    device_obj = get_device(context_client, device_uuid, rw_copy=False)
    if device_obj is None:
        flash('Device({:s}) not found'.format(str(device_uuid)), 'danger')
        device_obj = Device()
    context_client.close()
    return render_template('device/inventory.html', device=device_obj)

@device.route('logical/<path:device_uuid>', methods=['GET', 'POST'])
def logical(device_uuid: str):
    context_client.connect()
    device_obj = get_device(context_client, device_uuid, rw_copy=False)
    if device_obj is None:
        flash('Device({:s}) not found'.format(str(device_uuid)), 'danger')
        device_obj = Device()
    context_client.close()
    return render_template('device/logical.html', device=device_obj)

@device.get('<path:device_uuid>/delete')
def delete(device_uuid):
    try:
        context_client.connect()

        device_obj = get_device(
            context_client, device_uuid, rw_copy=False, include_components=False,
            include_config_rules=False, include_endpoints=False
        )
        if device_obj is None:
            flash('Device({:s}) not found'.format(str(device_uuid)), 'danger')
        else:
            device_client.connect()
            device_client.DeleteDevice(device_obj.device_id)
            device_client.close()
            flash(f'Device "{device_uuid}" deleted successfully!', 'success')

        context_client.close()
    except Exception as e: # pylint: disable=broad-except
        flash(f'Problem deleting device "{device_uuid}": {e.details()}', 'danger')
        current_app.logger.exception(e)
    return redirect(url_for('device.home'))

@device.route('<path:device_uuid>/addconfig', methods=['GET', 'POST'])
def addconfig(device_uuid):
    form = ConfigForm()
    request = DeviceId()
    request.device_uuid.uuid = device_uuid # pylint: disable=no-member
    context_client.connect()
    response = context_client.GetDevice(request)
    context_client.close()

    if form.validate_on_submit():
        device_obj = Device()
        device_obj.CopyFrom(response)
        config_rule = device_obj.device_config.config_rules.add() # pylint: disable=no-member
        config_rule.action = ConfigActionEnum.CONFIGACTION_SET
        config_rule.custom.resource_key = form.device_key_config.data
        config_rule.custom.resource_value = form.device_value_config.data
        try:
            device_client.connect()
            response: DeviceId = device_client.ConfigureDevice(device_obj)
            device_client.close()
            flash(f'New configuration was created with ID "{response.device_uuid.uuid}".', 'success')
            return redirect(url_for('device.home'))
        except Exception as e: # pylint: disable=broad-except
             flash(f'Problem adding the device. {e.details()}', 'danger')

    return render_template('device/addconfig.html', form=form,  submit_text='Add New Configuration')

@device.route('updateconfig', methods=['GET', 'POST'])
def updateconfig():

        
    return render_template('device/updateconfig.html')


@device.route('<path:device_uuid>/update', methods=['GET', 'POST'])
def update(device_uuid):
    form = UpdateDeviceForm()
    request = DeviceId()
    request.device_uuid.uuid = device_uuid # pylint: disable=no-member
    context_client.connect()
    response = context_client.GetDevice(request)
    context_client.close()

    # listing enum values
    form.update_operational_status.choices = []
    for key, _ in DeviceOperationalStatusEnum.DESCRIPTOR.values_by_name.items():
        item = (DeviceOperationalStatusEnum.Value(key), key.replace('DEVICEOPERATIONALSTATUS_', ''))
        form.update_operational_status.choices.append(item)

    form.update_operational_status.default = response.device_operational_status

    if form.validate_on_submit():
        device_obj = Device()
        device_obj.CopyFrom(response)
        device_obj.device_operational_status = form.update_operational_status.data
        try:
            device_client.connect()
            response: DeviceId = device_client.ConfigureDevice(device_obj)
            device_client.close()
            flash(f'Status of device with ID "{response.device_uuid.uuid}" was updated.', 'success')
            return redirect(url_for('device.home'))
        except Exception as e: # pylint: disable=broad-except
             flash(f'Problem updating the device. {e.details()}', 'danger')  
    return render_template('device/update.html', device=response, form=form, submit_text='Update Device')
