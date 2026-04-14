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

import grpc
import logging
from flask import current_app, render_template, Blueprint, flash, session, redirect, url_for
from common.proto.qkd_app_pb2 import App, AppId, QKDAppStatusEnum, QKDAppTypesEnum
from common.proto.context_pb2 import Uuid, ContextId
from common.tools.context_queries.Context import get_context
from common.tools.context_queries.Device import get_device
from context.client.ContextClient import ContextClient
from qkd_app.client.QKDAppClient import QKDAppClient

# Set up logging
LOGGER = logging.getLogger(__name__)

# Blueprint for QKDApp routes
qkd_app = Blueprint('qkd_app', __name__, url_prefix='/qkd_app')

# Initialize clients
qkd_app_client = QKDAppClient()
context_client = ContextClient()

@qkd_app.get('/')
def home():
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))
    
    context_uuid = session['context_uuid']
    topology_uuid = session['topology_uuid']

    # Connect to context client
    context_client.connect()
    device_names = dict()

    try:

        # Fetch context object
        context_obj = get_context(context_client, context_uuid, rw_copy=False)
        if context_obj is None:
            flash('Context({:s}) not found'.format(str(context_uuid)), 'danger')
            apps = list()
        else:
            try:
                # Call ListApps using the context_id
                apps_response = qkd_app_client.ListApps(context_obj.context_id)
                apps = apps_response.apps
            except grpc.RpcError as e:
                LOGGER.error(f"gRPC error while fetching apps: {e.details()}")
                if e.code() != grpc.StatusCode.NOT_FOUND: raise
                if e.details() != 'Context({:s}) not found'.format(context_uuid): raise
                apps = list()
            else:
                # Map local and remote device names
                for app in apps:
                    if app.local_device_id.device_uuid.uuid not in device_names:
                        device = get_device(context_client, app.local_device_id.device_uuid.uuid)
                        if device:
                            device_names[app.local_device_id.device_uuid.uuid] = device.name

                    if app.remote_device_id.device_uuid.uuid and app.remote_device_id.device_uuid.uuid not in device_names:
                        device = get_device(context_client, app.remote_device_id.device_uuid.uuid)
                        if device:
                            device_names[app.remote_device_id.device_uuid.uuid] = device.name
    finally:
        context_client.close()

    # Render the template with app list and device names
    return render_template(
        'qkd_app/home.html', 
        apps=apps, 
        device_names=device_names, 
        ate=QKDAppTypesEnum, 
        ase=QKDAppStatusEnum
    )

@qkd_app.route('detail/<path:app_uuid>', methods=['GET', 'POST'])
def detail(app_uuid: str):
    """
    Displays details for a specific QKD app identified by its UUID.
    """
    try:
        qkd_app_client.connect()

        # Wrap the app_uuid in a Uuid object and fetch details
        uuid_message = Uuid(uuid=app_uuid)
        app_id = AppId(app_uuid=uuid_message)
        app_detail = qkd_app_client.GetApp(app_id)

        if not app_detail:
            flash(f"App with UUID {app_uuid} not found", "danger")
            return redirect(url_for("qkd_app.home"))

        # Fetch device details
        context_client.connect()
        device_names = {}

        try:
            if app_detail.local_device_id.device_uuid.uuid:
                local_device = get_device(context_client, app_detail.local_device_id.device_uuid.uuid)
                if local_device:
                    device_names[app_detail.local_device_id.device_uuid.uuid] = local_device.name

            if app_detail.remote_device_id.device_uuid.uuid:
                remote_device = get_device(context_client, app_detail.remote_device_id.device_uuid.uuid)
                if remote_device:
                    device_names[app_detail.remote_device_id.device_uuid.uuid] = remote_device.name

        except grpc.RpcError as e:
            LOGGER.error(f"Failed to retrieve device details for app {app_uuid}: {e}")
            flash(f"Error retrieving device details: {e.details()}", "danger")
            return redirect(url_for("qkd_app.home"))

        finally:
            context_client.close()

        return render_template(
            'qkd_app/detail.html', 
            app=app_detail, 
            ase=QKDAppStatusEnum, 
            ate=QKDAppTypesEnum, 
            device_names=device_names
        )

    except grpc.RpcError as e:
        LOGGER.error(f"Failed to retrieve app details for {app_uuid}: {e}")
        flash(f"Error retrieving app details: {e.details()}", "danger")
        return redirect(url_for("qkd_app.home"))

    finally:
        qkd_app_client.close()

@qkd_app.get('<path:app_uuid>/delete')
def delete(app_uuid: str):
    """
    Deletes a specific QKD app identified by its UUID.
    """
    try:
        request = AppId(app_uuid=Uuid(uuid=app_uuid))

        qkd_app_client.connect()
        qkd_app_client.DeleteApp(request)  # Call the DeleteApp method
        qkd_app_client.close()

        flash(f'App "{app_uuid}" deleted successfully!', 'success')

    except grpc.RpcError as e:
        LOGGER.error(f"Problem deleting app {app_uuid}: {e}")
        flash(f"Problem deleting app {app_uuid}: {e.details()}", 'danger')

    except Exception as e:
        LOGGER.exception(f"Unexpected error while deleting app {app_uuid}: {e}")
        flash(f"Unexpected error: {str(e)}", 'danger')

    return redirect(url_for('qkd_app.home'))
