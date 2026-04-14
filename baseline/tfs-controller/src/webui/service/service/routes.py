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

import grpc, json, logging #, re
from collections import defaultdict
from flask import current_app, redirect, render_template, Blueprint, flash, session, url_for, request
from typing import Optional, Set
from wtforms.validators import ValidationError

from common.proto.context_pb2 import (
    ContextId, IsolationLevelEnum, Service, ServiceId, ServiceTypeEnum, ServiceStatusEnum, Connection,
    Empty, DeviceDriverEnum, ConfigActionEnum, Device, DeviceList
)
from common.tools.context_queries.Context import get_context
from common.tools.context_queries.EndPoint import get_endpoint_names
from common.tools.context_queries.Service import get_service_by_uuid
from common.tools.context_queries.Topology import get_topology
from common.tools.descriptor.Loader import DescriptorLoader, compose_notifications
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.tools.object_factory.Constraint import (
    json_constraint_sla_availability, json_constraint_sla_capacity, json_constraint_sla_isolation,
    json_constraint_sla_latency
)
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from common.tools.object_factory.Service import json_service_l2nm_planned, json_service_l3nm_planned, json_service_qkd_planned
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from webui.service.service.forms import (
    AddServiceForm_1, AddServiceForm_ACL_L2, AddServiceForm_ACL_IPV4, AddServiceForm_ACL_IPV6,
    AddServiceForm_L2VPN, AddServiceForm_L3VPN, AddServiceForm_QKD
)

LOGGER = logging.getLogger(__name__)
service = Blueprint('service', __name__, url_prefix='/service')

context_client = ContextClient()
service_client = ServiceClient()
device_client = DeviceClient()

ACL_TYPE = ["ACL_UNDEFINED", "ACL_IPV4","ACL_IPV6","ACL_L2","ACL_MPLS","ACL_MIXED"]
f_action = ["UNDEFINED", "DROP","ACCEPT","REJECT"]
l_action = ["UNDEFINED", "LOG_NONE","LOG_SYSLOG"]

def get_device_drivers_in_use(topology_uuid: str, context_uuid: str) -> Set[str]:
    active_drivers = set()
    grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
    topo_device_uuids = {device_id.device_uuid.uuid for device_id in grpc_topology.device_ids}
    grpc_devices: DeviceList = context_client.ListDevices(Empty())
    for device in grpc_devices.devices:
        if device.device_id.device_uuid.uuid in topo_device_uuids:
            for driver in device.device_drivers:
                active_drivers.add(DeviceDriverEnum.Name(driver))
    return active_drivers

@service.get('/')
def home():
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))
    context_uuid = session['context_uuid']
    topology_uuid = session['topology_uuid']

    context_client.connect()

    context_obj = get_context(context_client, context_uuid, rw_copy=False)
    if context_obj is None:
        flash('Context({:s}) not found'.format(str(context_uuid)), 'danger')
        services, device_names, endpoints_data = list(), list(), list()
    else:
        try:
            services = context_client.ListServices(context_obj.context_id)
            services = services.services
            active_drivers = get_device_drivers_in_use(topology_uuid, context_uuid)
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.NOT_FOUND: raise
            if e.details() != 'Context({:s}) not found'.format(context_uuid): raise
            services, device_names, endpoints_data = list(), dict(), dict()
            active_drivers = set()
        else:
            endpoint_ids = list()
            for service_ in services:
                endpoint_ids.extend(service_.service_endpoint_ids)
            device_names, endpoints_data = get_endpoint_names(context_client, endpoint_ids)

    context_client.close()
    return render_template(
        'service/home.html', services=services, device_names=device_names, endpoints_data=endpoints_data,
        ste=ServiceTypeEnum, sse=ServiceStatusEnum, active_drivers=active_drivers)

@service.route('add', methods=['GET', 'POST'])
def add():
    flash('Add service route called', 'danger')
    raise NotImplementedError()

def get_hub_module_name(dev: Device) -> Optional[str]:
    for cr in dev.device_config.config_rules:
        if cr.action != ConfigActionEnum.CONFIGACTION_SET: continue
        if not cr.custom: continue
        if cr.custom.resource_key != "_connect/settings": continue
        try:
            cr_dict = json.loads(cr.custom.resource_value)
            if "hub_module_name" in cr_dict:
                return cr_dict["hub_module_name"]
        except json.JSONDecodeError:
            pass
    return None

@service.route('add-xr', methods=['GET', 'POST'])
def add_xr():
    ### FIXME: copypaste
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))

    context_uuid = session['context_uuid']
    topology_uuid = session['topology_uuid']

    context_client.connect()
    grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
    if grpc_topology is None:
        flash('Context({:s})/Topology({:s}) not found'.format(str(context_uuid), str(topology_uuid)), 'danger')
        return redirect(url_for("main.home"))

    topo_device_uuids = {device_id.device_uuid.uuid for device_id in grpc_topology.device_ids}
    grpc_devices= context_client.ListDevices(Empty())
    devices = [
        device for device in grpc_devices.devices
        if device.device_id.device_uuid.uuid in topo_device_uuids and DeviceDriverEnum.DEVICEDRIVER_XR in device.device_drivers
    ]
    devices.sort(key=lambda dev: dev.name)

    hub_interfaces_by_device = defaultdict(list)
    leaf_interfaces_by_device = defaultdict(list)
    constellation_name_to_uuid = {}
    dev_ep_to_uuid = {}
    ep_uuid_to_name = {}
    for d in devices:
        constellation_name_to_uuid[d.name] = d.device_id.device_uuid.uuid
        hm_name = get_hub_module_name(d)
        if hm_name is not None:
            hm_if_prefix= hm_name + "|"
            for ep in d.device_endpoints:
                dev_ep_to_uuid[(d.name, ep.name)] = ep.endpoint_id.endpoint_uuid.uuid
                if ep.name.startswith(hm_if_prefix):
                    hub_interfaces_by_device[d.name].append(ep.name)
                else:
                    leaf_interfaces_by_device[d.name].append(ep.name)
                ep_uuid_to_name[ep.endpoint_id.endpoint_uuid.uuid] = (d.name, ep.name)
            hub_interfaces_by_device[d.name].sort()
            leaf_interfaces_by_device[d.name].sort()

    context_obj = get_context(context_client, context_uuid, rw_copy=False)
    if context_obj is None:
        flash('Context({:s}) not found'.format(str(context_uuid)), 'danger')
        return redirect(request.url)
    
    services = context_client.ListServices(context_obj.context_id)
    ep_used_by={}
    for service in services.services:
        if  service.service_type == ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE:
            for ep in service.service_endpoint_ids:
                ep_uuid = ep.endpoint_uuid.uuid
                if ep_uuid in ep_uuid_to_name:
                    dev_name, ep_name = ep_uuid_to_name[ep_uuid]
                    ep_used_by[f"{ep_name}@{dev_name}"] = service.name

    context_client.close()

    if request.method != 'POST':
        return render_template(
            'service/add-xr.html', devices=devices, hub_if=hub_interfaces_by_device,
            leaf_if=leaf_interfaces_by_device, ep_used_by=ep_used_by
        )

    service_name = request.form["service_name"]
    if service_name == "":
        flash(f"Service name must be specified", 'danger')

    constellation = request.form["constellation"]
    constellation_uuid = constellation_name_to_uuid.get(constellation, None)
    if constellation_uuid is None:
        flash(f"Invalid constellation \"{constellation}\"", 'danger')

    hub_if = request.form["hubif"]
    hub_if_uuid = dev_ep_to_uuid.get((constellation, hub_if), None)
    if hub_if_uuid is None:
        flash(f"Invalid hub interface \"{hub_if}\"", 'danger')

    leaf_if = request.form["leafif"]
    leaf_if_uuid = dev_ep_to_uuid.get((constellation, leaf_if), None)
    if leaf_if_uuid is None:
        flash(f"Invalid leaf interface \"{leaf_if}\"", 'danger')
    
    if service_name == "" or constellation_uuid is None or hub_if_uuid is None or leaf_if_uuid is None:
        return redirect(request.url)
    
    
    json_context_uuid=json_context_id(context_uuid)
    sr = {
        "name": service_name,
        "service_id": {
                "context_id": {"context_uuid": {"uuid": context_uuid}},
                "service_uuid": {"uuid": service_name}
        },
        'service_type'        : ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE,
        "service_endpoint_ids": [
            {
                'device_id': {'device_uuid': {'uuid': constellation_uuid}},
                'endpoint_uuid': {'uuid': hub_if_uuid},
                'topology_id': json_topology_id("admin", context_id=json_context_uuid)
            },
            {
                'device_id': {'device_uuid': {'uuid': constellation_uuid}},
                'endpoint_uuid': {'uuid': leaf_if_uuid},
                'topology_id': json_topology_id("admin", context_id=json_context_uuid)
            }
        ],
        'service_status'      : {'service_status': ServiceStatusEnum.SERVICESTATUS_PLANNED},
        'service_constraints' : [],
    }

    json_tapi_settings = {
        'capacity_value'  : 50.0,
        'capacity_unit'   : 'GHz',
        'layer_proto_name': 'PHOTONIC_MEDIA',
        'layer_proto_qual': 'tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC',
        'direction'       : 'UNIDIRECTIONAL',
    }
    config_rule = json_config_rule_set('/settings', json_tapi_settings)

    try:
        service_client.connect()

        endpoints, sr['service_endpoint_ids'] = sr['service_endpoint_ids'], []
        try:
            create_response = service_client.CreateService(Service(**sr))
        except Exception as e:
            flash(f'Failure to update service name {service_name} with endpoints and configuration, exception {str(e)}', 'danger')
            return redirect(request.url)
        
        sr['service_endpoint_ids'] = endpoints
        sr['service_config'] = {'config_rules': [config_rule]}

        try:
            update_response = service_client.UpdateService(Service(**sr))
            flash(f'Created service {update_response.service_uuid.uuid}', 'success')
        except Exception as e: 
            flash(f'Failure to update service {create_response.service_uuid.uuid} with endpoints and configuration, exception {str(e)}', 'danger')
            return redirect(request.url)

        return redirect(url_for('service.home'))
    finally:
        service_client.close()

@service.get('<path:service_uuid>/detail')
def detail(service_uuid: str):
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))
    context_uuid = session['context_uuid']

    try:
        context_client.connect()
        endpoint_ids = list()
        service_obj = get_service_by_uuid(context_client, service_uuid, rw_copy=False)
        if service_obj is None:
            flash('Context({:s})/Service({:s}) not found'.format(str(context_uuid), str(service_uuid)), 'danger')
            service_obj = Service()
        else:
            endpoint_ids.extend(service_obj.service_endpoint_ids)
            connections: Connection = context_client.ListConnections(service_obj.service_id)
            connections = connections.connections
            for connection in connections: endpoint_ids.extend(connection.path_hops_endpoint_ids)

        if len(endpoint_ids) > 0:
            device_names, endpoints_data = get_endpoint_names(context_client, endpoint_ids)
        else:
            device_names, endpoints_data = dict(), dict()

        context_client.close()
        return render_template(
            'service/detail.html', service=service_obj, connections=connections, device_names=device_names,
            endpoints_data=endpoints_data, ste=ServiceTypeEnum, sse=ServiceStatusEnum, ile=IsolationLevelEnum,
            type=ACL_TYPE, f_action=f_action, l_action=l_action
        )
    except Exception as e:
        flash('The system encountered an error and cannot show the details of this service.', 'warning')
        current_app.logger.exception(e)
        return redirect(url_for('service.home'))

@service.get('<path:service_uuid>/delete')
def delete(service_uuid: str):
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))
    context_uuid = session['context_uuid']

    try:
        request = ServiceId()
        request.service_uuid.uuid = service_uuid
        request.context_id.context_uuid.uuid = context_uuid
        service_client.connect()
        service_client.DeleteService(request)
        service_client.close()

        flash('Service "{:s}" deleted successfully!'.format(service_uuid), 'success')
    except Exception as e:
        flash('Problem deleting service "{:s}": {:s}'.format(service_uuid, str(e.details())), 'danger')
        current_app.logger.exception(e)
    return redirect(url_for('service.home'))

@service.route('add/configure', methods=['GET', 'POST'])
def add_configure():
    form_1 = AddServiceForm_1()
    if form_1.validate_on_submit():
        service_type = str(form_1.service_type.data)
        if service_type in {'ACL_L2', 'ACL_IPV4', 'ACL_IPV6', 'L2VPN', 'L3VPN', 'QKD'}:
            return redirect(url_for('service.add_configure_{:s}'.format(service_type)))
    return render_template('service/add.html', form_1=form_1, submit_text='Continue to configuraton')

@service.route('add/configure/QKD', methods=['GET', 'POST'])
def add_configure_QKD():
    form_qkd = AddServiceForm_QKD()
    service_obj = Service()

    context_uuid, topology_uuid = get_context_and_topology_uuids()
    if context_uuid and topology_uuid:
        context_client.connect()
        grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
        if grpc_topology:
            topo_device_uuids = {device_id.device_uuid.uuid for device_id in grpc_topology.device_ids}          
            devices = get_filtered_devices(context_client, topo_device_uuids)
            grpc_devices = context_client.ListDevices(Empty())                                          
            devices = [
                device for device in grpc_devices.devices
                if device.device_id.device_uuid.uuid in topo_device_uuids and DeviceDriverEnum.DEVICEDRIVER_QKD in device.device_drivers
            ]
            choices = get_device_choices(devices)
            add_device_choices_to_form(choices, form_qkd.service_device_1)
            add_device_choices_to_form(choices, form_qkd.service_device_2)
        else:
            flash('Context({:s})/Topology({:s}) not found'.format(str(context_uuid), str(topology_uuid)), 'danger')
    else:
        flash('Missing context or topology UUID', 'danger')

    if form_qkd.validate_on_submit():
        try:
            [selected_device_1, selected_device_2, selected_endpoint_1, selected_endpoint_2] = validate_selected_devices_and_endpoints(form_qkd, devices)
        except Exception as e:
            flash('{:s}'.format(str(e.args[0])), 'danger')
            current_app.logger.exception(e)
            return render_template('service/configure_QKD.html', form_qkd=form_qkd, submit_text='Add New Service')
        
        service_uuid, service_type, endpoint_ids = set_service_parameters(service_obj, form_qkd, selected_device_1, selected_device_2, selected_endpoint_1, selected_endpoint_2)
        constraints = add_constraints(form_qkd)
        params_device_1_with_data = get_device_params(form_qkd, 1, service_type)
        params_device_2_with_data = get_device_params(form_qkd, 2, service_type)
        print(params_device_1_with_data)
        print(params_device_2_with_data)
        params_settings = {}
        config_rules = [
            json_config_rule_set(
                    '/settings', params_settings
                ),
            json_config_rule_set(
                '/device[{:s}]/endpoint[{:s}]/settings'.format(str(selected_device_1.name), str(selected_endpoint_1)), params_device_1_with_data
            ),
            json_config_rule_set(
                '/device[{:s}]/endpoint[{:s}]/settings'.format(str(selected_device_2.name), str(selected_endpoint_2)), params_device_2_with_data
            )
        ]

        service_client.connect()
        context_client.connect()
        device_client.connect()
        descriptor_json = json_service_qkd_planned(service_uuid = service_uuid, endpoint_ids = endpoint_ids, constraints = constraints, config_rules = config_rules, context_uuid= context_uuid)
        descriptor_json = {"services": [descriptor_json]}
        try:
            process_descriptors(descriptor_json)
            flash('Service "{:s}" added successfully!'.format(service_obj.service_id.service_uuid.uuid), 'success')
            return redirect(url_for('service.home', service_uuid=service_obj.service_id.service_uuid.uuid))
        except Exception as e:
            flash('Problem adding service: {:s}'.format((str(e.args[0]))), 'danger')
            current_app.logger.exception(e)
        finally:
            context_client.close()                                                                                      
            device_client.close()
            service_client.close()

    
    return render_template('service/configure_QKD.html', form_qkd=form_qkd, submit_text='Add New Service')


@service.route('add/configure/ACL_L2', methods=['GET', 'POST'])
def add_configure_ACL_L2():
    form_acl = AddServiceForm_ACL_L2()
    service_obj = Service()   

    context_uuid, topology_uuid = get_context_and_topology_uuids()
    if context_uuid and topology_uuid:
        context_client.connect()
        grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
        if grpc_topology:
            topo_device_uuids = {device_id.device_uuid.uuid for device_id in grpc_topology.device_ids}          
            context_obj = get_context(context_client, context_uuid, rw_copy=False)
            if context_obj is None:
                flash('Context({:s}) not found'.format(str(context_uuid)), 'danger')
                return redirect(request.url)
            services = context_client.ListServices(context_obj.context_id)
            devices = []
            for service in services.services:
                devices_services = []
                if  service.service_type == ServiceTypeEnum.SERVICETYPE_L2NM:
                    LOGGER.warning('L2NM service')  
                    for ep in service.service_endpoint_ids:
                        device_uuid = ep.device_id.device_uuid.uuid
                        devices_services.append(device_uuid, service.service_name)
                        LOGGER.warning('device_uuid')  
                        LOGGER.warning(device_uuid)  
                    
                    grpc_devices = context_client.ListDevices(Empty())                                          
                    for device in grpc_devices.devices:
                        if device.device_id.device_uuid.uuid in devices_services:
                            devices.append(device)
           
            choices = get_device_choices(devices)
            add_device_choices_to_form(choices, form_acl.service_device_1)
            add_device_choices_to_form(choices, form_acl.service_device_2)
        else:
            flash('Context({:s})/Topology({:s}) not found'.format(str(context_uuid), str(topology_uuid)), 'danger')
    else:
        flash('Missing context or topology UUID', 'danger')
    if form_acl.validate_on_submit():    
        flash(f'New configuration was created', 'success')
        return redirect(url_for('service.home'))
    
    return render_template('service/configure_ACL_L2.html', form_acl=form_acl, submit_text='Add New Service')

@service.route('add/configure/ACL_IPV4', methods=['GET', 'POST'])
def add_configure_ACL_IPV4():
    form_acl = AddServiceForm_ACL_IPV4()
    if form_acl.validate_on_submit():
        flash(f'New configuration was created', 'success')
        return redirect(url_for('service.home'))
    print(form_acl.errors)
    return render_template('service/configure_ACL_IPV4.html', form_acl=form_acl, submit_text='Add New Service')

@service.route('add/configure/ACL_IPV6', methods=['GET', 'POST'])
def add_configure_ACL_IPV6():
    form_acl = AddServiceForm_ACL_IPV6()
    if form_acl.validate_on_submit():
        flash(f'New configuration was created', 'success')
        return redirect(url_for('service.home'))
    print(form_acl.errors)
    return render_template('service/configure_ACL_IPV6.html', form_acl=form_acl, submit_text='Add New Service')
 
@service.route('add/configure/L2VPN', methods=['GET', 'POST'])
def add_configure_L2VPN():
    form_l2vpn = AddServiceForm_L2VPN()
    service_obj = Service()

    context_uuid, topology_uuid = get_context_and_topology_uuids()
    if context_uuid and topology_uuid:
        context_client.connect()
        grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
        if grpc_topology:
            topo_device_uuids = {device_id.device_uuid.uuid for device_id in grpc_topology.device_ids}          
            devices = get_filtered_devices(context_client, topo_device_uuids)
            choices = get_device_choices(devices)
            add_device_choices_to_form(choices, form_l2vpn.service_device_1)
            add_device_choices_to_form(choices, form_l2vpn.service_device_2)
        else:
            flash('Context({:s})/Topology({:s}) not found'.format(str(context_uuid), str(topology_uuid)), 'danger')
    else:
        flash('Missing context or topology UUID', 'danger')

    if form_l2vpn.validate_on_submit():
        try:
            [selected_device_1, selected_device_2, selected_endpoint_1, selected_endpoint_2] = validate_selected_devices_and_endpoints(form_l2vpn, devices)
        except Exception as e:
            flash('{:s}'.format(str(e.args[0])), 'danger')
            current_app.logger.exception(e)
            return render_template('service/configure_L2VPN.html', form_l2vpn=form_l2vpn, submit_text='Add New Service')

        [vendor_1, vendor_2] = get_device_vendor(form_l2vpn, devices)
        try:
            validate_params_vendor(form_l2vpn, vendor_1, 1)
            validate_params_vendor(form_l2vpn, vendor_2, 2)
        except Exception as e:       
            flash('{:s}'.format(str(e.args[0])), 'danger')
            current_app.logger.exception(e)
            return render_template('service/configure_L2VPN.html', form_l2vpn=form_l2vpn, submit_text='Add New Service')

        service_uuid, service_type, endpoint_ids = set_service_parameters(service_obj, form_l2vpn, selected_device_1, selected_device_2, selected_endpoint_1, selected_endpoint_2)
        constraints = add_constraints(form_l2vpn)
        params_device_1_with_data = get_device_params(form_l2vpn, 1, service_type)
        params_device_2_with_data = get_device_params(form_l2vpn, 2, service_type)
        print(params_device_1_with_data)
        print(params_device_2_with_data)
        params_settings = {}
        config_rules = [
            json_config_rule_set(
                    '/settings', params_settings
                ),
            json_config_rule_set(
                '/device[{:s}]/endpoint[{:s}]/settings'.format(str(selected_device_1.name), str(selected_endpoint_1)), params_device_1_with_data
            ),
            json_config_rule_set(
                '/device[{:s}]/endpoint[{:s}]/settings'.format(str(selected_device_2.name), str(selected_endpoint_2)), params_device_2_with_data
            )
        ]
        service_client.connect()
        context_client.connect()
        device_client.connect()
        descriptor_json = json_service_l2nm_planned(service_uuid = service_uuid, endpoint_ids = endpoint_ids, constraints = constraints, config_rules = config_rules, context_uuid= context_uuid)
        descriptor_json = {"services": [descriptor_json]}
        try:
            process_descriptors(descriptor_json)
            flash('Service "{:s}" added successfully!'.format(service_obj.service_id.service_uuid.uuid), 'success')
            return redirect(url_for('service.home', service_uuid=service_obj.service_id.service_uuid.uuid))
        except Exception as e:
            flash('Problem adding service: {:s}'.format((str(e.args[0]))), 'danger')
            current_app.logger.exception(e)
        finally:
            context_client.close()                                                                                      
            device_client.close()
            service_client.close()
    return render_template('service/configure_L2VPN.html', form_l2vpn=form_l2vpn, submit_text='Add New Service')

@service.route('add/configure/L3VPN', methods=['GET', 'POST'])
def add_configure_L3VPN():
    form_l3vpn = AddServiceForm_L3VPN()
    service_obj = Service()

    context_uuid, topology_uuid = get_context_and_topology_uuids()
    if context_uuid and topology_uuid:
        context_client.connect()
        grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
        if grpc_topology:
            topo_device_uuids = {device_id.device_uuid.uuid for device_id in grpc_topology.device_ids}          
            devices = get_filtered_devices(context_client, topo_device_uuids)
            choices = get_device_choices(devices)
            add_device_choices_to_form(choices, form_l3vpn.service_device_1)
            add_device_choices_to_form(choices, form_l3vpn.service_device_2)
        else:
            flash('Context({:s})/Topology({:s}) not found'.format(str(context_uuid), str(topology_uuid)), 'danger')
    else:
        flash('Missing context or topology UUID', 'danger')

    if form_l3vpn.validate_on_submit():
        try:
            [selected_device_1, selected_device_2, selected_endpoint_1, selected_endpoint_2] = validate_selected_devices_and_endpoints(form_l3vpn, devices)
        except Exception as e:
            flash('{:s}'.format(str(e.args[0])), 'danger')
            current_app.logger.exception(e)
            return render_template('service/configure_L3VPN.html', form_l3vpn=form_l3vpn, submit_text='Add New Service')
        
        service_uuid, service_type, endpoint_ids = set_service_parameters(service_obj, form_l3vpn, selected_device_1, selected_device_2, selected_endpoint_1, selected_endpoint_2)
        constraints = add_constraints(form_l3vpn)
        params_device_1_with_data = get_device_params(form_l3vpn, 1, service_type)
        params_device_2_with_data = get_device_params(form_l3vpn, 2, service_type)
        params_settings = {}
        config_rules = [
            json_config_rule_set(
                    '/settings', params_settings
                ),
            json_config_rule_set(
                '/device[{:s}]/endpoint[{:s}]/settings'.format(str(selected_device_1.name), str(selected_endpoint_1)), params_device_1_with_data
            ),
            json_config_rule_set(
                '/device[{:s}]/endpoint[{:s}]/settings'.format(str(selected_device_2.name), str(selected_endpoint_2)), params_device_2_with_data
            )
        ]
        service_client.connect()
        context_client.connect()
        device_client.connect()
        descriptor_json = json_service_l3nm_planned(service_uuid = service_uuid, endpoint_ids = endpoint_ids, constraints = constraints, config_rules = config_rules, context_uuid= context_uuid)
        descriptor_json = {"services": [descriptor_json]}
        try:
            process_descriptors(descriptor_json)
            flash('Service "{:s}" added successfully!'.format(service_obj.service_id.service_uuid.uuid), 'success')
            return redirect(url_for('service.home', service_uuid=service_obj.service_id.service_uuid.uuid))
        except Exception as e:
            flash('Problem adding service: {:s}'.format((str(e.args[0]))), 'danger')
            current_app.logger.exception(e)
        finally:
            context_client.close()                                                                                        
            device_client.close()
            service_client.close()
    return render_template('service/configure_L3VPN.html', form_l3vpn=form_l3vpn, submit_text='Add New Service')


DESCRIPTOR_LOADER_NUM_WORKERS = 10

def process_descriptors(descriptors):
    descriptor_loader = DescriptorLoader(descriptors, num_workers=DESCRIPTOR_LOADER_NUM_WORKERS)
    results = descriptor_loader.process()
    for message,level in compose_notifications(results):
        if level == 'error':                                                                                
            LOGGER.warning('ERROR message={:s}'.format(str(message)))
        flash(message, level)


def get_context_and_topology_uuids():
    context_uuid = session.get('context_uuid')
    topology_uuid = session.get('topology_uuid')
    return context_uuid, topology_uuid

def get_filtered_devices(context_client, topo_device_uuids):
    grpc_devices = context_client.ListDevices(Empty())                                          
    return [device for device in grpc_devices.devices if device.device_id.device_uuid.uuid in topo_device_uuids]

def get_device_choices(devices):
    return [(i, str(device.name)) for i, device in enumerate(devices)]

def add_device_choices_to_form(choices, form):
    form.choices += choices

def validate_selected_devices_and_endpoints(form, devices):
    selected_device_1 = devices[int(form.service_device_1.data)]
    selected_device_2 = devices[int(form.service_device_2.data)]
    if selected_device_1 == selected_device_2:
        raise ValidationError('The devices must be different!. Please select two valid and different devices')
    elif form.service_endpoint_1.data not in [endpoint.name for endpoint in selected_device_1.device_endpoints]:
        raise ValidationError('The selected endpoint: ' + form.service_endpoint_1.data + ' is not a valid endpoint for: '+ selected_device_1.name + '. Please select an endpoint that is available for this device')
    elif form.service_endpoint_2.data not in [endpoint.name for endpoint in selected_device_2.device_endpoints]:
        raise ValidationError('The selected endpoint: ' + form.service_endpoint_2.data + ' is not a valid endpoint for: '+ selected_device_2.name + '. Please select an endpoint that is available for this device')
    else:
        selected_endpoint_1 = form.service_endpoint_1.data
        selected_endpoint_2 = form.service_endpoint_2.data
    return selected_device_1, selected_device_2, selected_endpoint_1, selected_endpoint_2

def get_device_vendor(form, devices):
    selected_device_1 = devices[int(form.service_device_1.data)]
    selected_device_2 = devices[int(form.service_device_2.data)]
    
    vendor_value_1 = None
    vendor_value_2 = None

    for config_rule in selected_device_1.device_config.config_rules:
        if "vendor" in config_rule.custom.resource_value:
            vendor_config_rule_1 = config_rule.custom.resource_value
            config_rule_dict_1 = json.loads(vendor_config_rule_1)
            if "vendor" in config_rule_dict_1:
                vendor_value_1 = config_rule_dict_1["vendor"]
            break

    for config_rule in selected_device_2.device_config.config_rules:
        if "vendor" in config_rule.custom.resource_value:
            vendor_config_rule_2 = config_rule.custom.resource_value
            config_rule_dict_2 = json.loads(vendor_config_rule_2)
            if "vendor" in config_rule_dict_2:
                vendor_value_2 = config_rule_dict_2["vendor"]
            break

    return vendor_value_1, vendor_value_2

def validate_params_vendor(form, vendor, device_num):
    if vendor != "ADVA": return

    if form.NI_name.data != f"ELAN-AC:{getattr(form, f'Device_{device_num}_IF_vlan_id').data}":
        raise ValidationError('For an ADVA device, the name of the Network Instance should have this name: "ELAN-AC:vlanID"')

    elif getattr(form, f'Device_{device_num}_NI_VC_ID').data != getattr(form, f'Device_{device_num}_IF_vlan_id').data:
        raise ValidationError('For an ADVA device, the value of the VlanID and the value of the VC_ID must be the same')

def set_service_parameters(service_obj, form, selected_device_1, selected_device_2, selected_endpoint_1, selected_endpoint_2):
    service_obj.service_id.service_uuid.uuid = str(form.service_name.data)
    service_uuid = service_obj.service_id.service_uuid.uuid
    service_obj.service_type = int(form.service_type.data)
    service_type = service_obj.service_type

    endpoint_ids = [
        json_endpoint_id(json_device_id(selected_device_1.name), str(selected_endpoint_1)),
        json_endpoint_id(json_device_id(selected_device_2.name), str(selected_endpoint_2))
    ]
    return service_uuid, service_type, endpoint_ids

def add_constraints(form):
    constraints = []
    if form.service_capacity.data:
        constraints.append(json_constraint_sla_capacity(float(form.service_capacity.data)))
    if form.service_latency.data:
        constraints.append(json_constraint_sla_latency(float(form.service_latency.data)))
    if form.service_availability.data:
        constraints.append(json_constraint_sla_availability(1, True, float(form.service_availability.data)))
    if form.service_isolation.data is not None and form.service_isolation.data != '':
        constraints.append(json_constraint_sla_isolation([getattr(IsolationLevelEnum, str(form.service_isolation.data))]))

    return constraints

def get_device_params(form, device_num, form_type):
    if form_type == 2:
        device_params = {
            'ni_name': str(getattr(form, 'NI_name').data),
            'sub_interface_index': str(getattr(form, f'Device_{device_num}_IF_index').data),
            'vlan_id': str(getattr(form, f'Device_{device_num}_IF_vlan_id').data),
            'remote_router': str(getattr(form, f'Device_{device_num}_NI_remote_system').data),
            'vc_id': str(getattr(form, f'Device_{device_num}_NI_VC_ID').data),
            'conn_point': str(getattr(form, f'Device_{device_num}_NI_connection_point').data),
            'mtu': str(getattr(form, f'Device_{device_num}_IF_mtu').data),
            'ni_description': str(getattr(form, 'NI_description').data),
            'subif_description': str(getattr(form, f'Device_{device_num}_IF_description').data),
        }
    elif form_type == 1:
        if device_num == 1:
            policy_az_field = 'NI_import_policy'
            policy_za_field = 'NI_export_policy'
        elif device_num == 2:
            policy_az_field = 'NI_export_policy'
            policy_za_field = 'NI_import_policy'
        device_params = {
            'ni_name': str(getattr(form, 'NI_name').data),
            'bgp_as':str(getattr(form, 'NI_as').data),
            'route_distinguisher': str(getattr(form, 'NI_route_distinguisher').data),
            'sub_interface_index': str(getattr(form, f'Device_{device_num}_IF_index').data),
            'router_id': str(getattr(form, 'NI_router_id').data),
            'vlan_id': str(getattr(form, f'Device_{device_num}_IF_vlan_id').data),
            'address_ip': str(getattr(form, f'Device_{device_num}_IF_address_ip').data),
            'address_prefix': str(getattr(form, f'Device_{device_num}_IF_address_prefix').data),
            'policy_AZ': str(getattr(form, policy_az_field).data),
            'policy_ZA': str(getattr(form, policy_za_field).data),
            'mtu': str(getattr(form, f'Device_{device_num}_IF_mtu').data),
            'ni_description': str(getattr(form, 'NI_description').data),
            'subif_description': str(getattr(form, f'Device_{device_num}_IF_description').data),
        }
    elif form_type == 6:
        device_params = {
        }
    else:
        raise ValueError(f'Unsupported form type: {form_type}')

    params_with_data = {k: v for k, v in device_params.items() if v is not None and str(v) != 'None' and v != ''}
    return params_with_data
