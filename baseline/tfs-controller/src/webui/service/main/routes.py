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

import base64, json, logging #, re
from flask import jsonify, redirect, render_template, Blueprint, flash, session, url_for, request
from common.proto.context_pb2 import ContextList, Empty, TopologyId, TopologyList
from common.tools.descriptor.Loader import DescriptorLoader, compose_notifications
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from slice.client.SliceClient import SliceClient
from webui.service.main.forms import ContextTopologyForm, DescriptorForm

main = Blueprint('main', __name__)

context_client = ContextClient()
device_client = DeviceClient()
service_client = ServiceClient()
slice_client = SliceClient()

LOGGER = logging.getLogger(__name__)

DESCRIPTOR_LOADER_NUM_WORKERS = 10

def process_descriptors(descriptors):
    try:
        descriptors_file = request.files[descriptors.name]
        descriptors_data = descriptors_file.read()
        descriptors = json.loads(descriptors_data)
    except Exception as e: # pylint: disable=broad-except
        flash(f'Unable to load descriptor file: {str(e)}', 'danger')
        return

    descriptor_loader = DescriptorLoader(descriptors, num_workers=DESCRIPTOR_LOADER_NUM_WORKERS)
    results = descriptor_loader.process()
    for message,level in compose_notifications(results):
        if level == 'error': LOGGER.warning('ERROR message={:s}'.format(str(message)))
        flash(message, level)

@main.route('/', methods=['GET', 'POST'])
def home():
    context_client.connect()
    device_client.connect()
    context_topology_form = ContextTopologyForm()
    context_topology_form.context_topology.choices.append(('', 'Select...'))

    contexts : ContextList = context_client.ListContexts(Empty())
    for context_ in contexts.contexts:
        #context_uuid : str = context_.context_id.context_uuid.uuid
        context_name : str = context_.name
        topologies : TopologyList = context_client.ListTopologies(context_.context_id)
        for topology_ in topologies.topologies:
            #topology_uuid : str = topology_.topology_id.topology_uuid.uuid
            topology_name : str = topology_.name
            raw_values = context_name, topology_name
            b64_values = [base64.b64encode(v.encode('utf-8')).decode('utf-8') for v in raw_values]
            context_topology_uuid = ','.join(b64_values)
            context_topology_name  = 'Context({:s}):Topology({:s})'.format(context_name, topology_name)
            context_topology_entry = (context_topology_uuid, context_topology_name)
            context_topology_form.context_topology.choices.append(context_topology_entry)

    if context_topology_form.validate_on_submit():
        context_topology_uuid = context_topology_form.context_topology.data
        if len(context_topology_uuid) > 0:
            b64_values = context_topology_uuid.split(',')
            raw_values = [base64.b64decode(v.encode('utf-8')).decode('utf-8') for v in b64_values]
            context_name, topology_name = raw_values
            #session.clear()
            session['context_topology_uuid'] = context_topology_uuid
            session['context_uuid'] = context_name
            #session['context_name'] = context_name
            session['topology_uuid'] = topology_name
            #session['topology_name'] = topology_name
            MSG = f'Context({context_name})/Topology({topology_name}) successfully selected.'
            flash(MSG, 'success')

            context_client.close()
            device_client.close()

            return redirect(url_for('main.home'))

            #match = re.match('ctx\[([^\]]+)\]\/topo\[([^\]]+)\]', context_topology_uuid)
            #if match is not None:
            #    session['context_topology_uuid'] = context_topology_uuid = match.group(0)
            #    session['context_uuid'] = context_uuid = match.group(1)
            #    session['topology_uuid'] = topology_uuid = match.group(2)
            #    MSG = f'Context({context_uuid})/Topology({topology_uuid}) successfully selected.'
            #    flash(MSG, 'success')
            #    return redirect(url_for('main.home'))

    if 'context_topology_uuid' in session:
        context_topology_form.context_topology.data = session['context_topology_uuid']

    descriptor_form = DescriptorForm()
    try:
        if descriptor_form.validate_on_submit():
            process_descriptors(descriptor_form.descriptors)
            return redirect(url_for("main.home"))

    except Exception as e: # pylint: disable=broad-except
        LOGGER.exception('Descriptor load failed')
        flash(f'Descriptor load failed: `{str(e)}`', 'danger')
    finally:
        context_client.close()
        device_client.close()

    return render_template(
        'main/home.html', context_topology_form=context_topology_form, descriptor_form=descriptor_form)

@main.route('/topology', methods=['GET'])
def topology():
    context_client.connect()
    try:
        if 'context_uuid' not in session or 'topology_uuid' not in session:
            return jsonify({'devices': [], 'links': []})

        context_uuid = session['context_uuid']
        topology_uuid = session['topology_uuid']

        json_topo_id = json_topology_id(topology_uuid, context_id=json_context_id(context_uuid))
        response = context_client.GetTopologyDetails(TopologyId(**json_topo_id))

        devices = []
        for device in response.devices:
            devices.append({
                'id': device.device_id.device_uuid.uuid,
                'name': device.name,
                'type': device.device_type,
            })

        links = []
        for link in response.links:
            if len(link.link_endpoint_ids) != 2:
                str_link = grpc_message_to_json_string(link)
                LOGGER.warning('Unexpected link with len(endpoints) != 2: {:s}'.format(str_link))
                continue
            links.append({
                'id': link.link_id.link_uuid.uuid,
                'name': link.name,
                'source': link.link_endpoint_ids[0].device_id.device_uuid.uuid,
                'target': link.link_endpoint_ids[1].device_id.device_uuid.uuid,
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
      
        return jsonify({'devices': devices, 'links': links, 'optical_links': optical_links})
    except: # pylint: disable=bare-except
        LOGGER.exception('Error retrieving topology')
        return jsonify({'devices': [], 'links': [], 'optical_links': []})
    finally:
        context_client.close()

@main.get('/about')
def about():
    return render_template('main/about.html')

@main.get('/debug')
def debug():
    return render_template('main/debug.html')

@main.get('/resetsession')
def reset_session():
    session.clear()
    return redirect(url_for("main.home"))
