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


from flask import (
    current_app, render_template, Blueprint, flash, session, redirect, url_for
)
from common.proto.context_pb2 import Empty, Link, LinkId, LinkList, LinkTypeEnum
from common.tools.context_queries.EndPoint import get_endpoint_names
from common.tools.context_queries.Link import get_link
from common.tools.context_queries.Topology import get_topology
from context.client.ContextClient import ContextClient
from vnt_manager.client.VNTManagerClient import VNTManagerClient


link = Blueprint('link', __name__, url_prefix='/link')
context_client = ContextClient()
vntm_client = VNTManagerClient()

@link.get('/')
def home():
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))

    context_uuid = session['context_uuid']
    topology_uuid = session['topology_uuid']

    links, endpoint_ids = list(), list()
    device_names, endpoints_data = dict(), dict()

    context_client.connect()
    grpc_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid, rw_copy=False)
    if grpc_topology is None:
        flash('Context({:s})/Topology({:s}) not found'.format(str(context_uuid), str(topology_uuid)), 'danger')
    else:
        topo_link_uuids = {link_id.link_uuid.uuid for link_id in grpc_topology.link_ids}
        grpc_links: LinkList = context_client.ListLinks(Empty())
        for link_ in grpc_links.links:
            if link_.link_id.link_uuid.uuid not in topo_link_uuids: continue
            links.append(link_)
            endpoint_ids.extend(link_.link_endpoint_ids)
        device_names, endpoints_data = get_endpoint_names(context_client, endpoint_ids)
    context_client.close()

    return render_template(
        'link/home.html', links=links, device_names=device_names,
        endpoints_data=endpoints_data, lte=LinkTypeEnum
    )


@link.route('detail/<path:link_uuid>', methods=('GET', 'POST'))
def detail(link_uuid: str):
    context_client.connect()
    link_obj = get_link(context_client, link_uuid, rw_copy=False)
    if link_obj is None:
        flash('Link({:s}) not found'.format(str(link_uuid)), 'danger')
        link_obj = Link()
        device_names, endpoints_data = dict(), dict()
    else:
        device_names, endpoints_data = get_endpoint_names(context_client, link_obj.link_endpoint_ids)
    context_client.close()
    return render_template(
        'link/detail.html', link=link_obj, device_names=device_names,
        endpoints_data=endpoints_data, lte=LinkTypeEnum
    )

@link.get('<path:link_uuid>/delete')
def delete(link_uuid):
    try:
        context_client.connect()

        link_obj = get_link(context_client, link_uuid, rw_copy=False)
        if link_obj is None:
            flash('Link({:s}) not found'.format(str(link_uuid)), 'danger')
        else:
            link_type = link_obj.link_type
            if link_type == LinkTypeEnum.LINKTYPE_VIRTUAL:
                vntm_client.RemoveVirtualLink(link_obj.link_id)
            else:
                context_client.RemoveLink(link_obj.link_id)
            flash(f'Link "{link_uuid}" deleted successfully!', 'success')

        context_client.close()
    except Exception as e: # pylint: disable=broad-except
        flash(f'Problem deleting link "{link_uuid}": {e.details()}', 'danger')
        current_app.logger.exception(e)
    return redirect(url_for('link.home'))
