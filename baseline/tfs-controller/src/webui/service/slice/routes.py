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
from typing import Dict, Optional, Tuple
import grpc
from flask import current_app, redirect, render_template, Blueprint, flash, session, url_for
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from common.proto.context_pb2 import IsolationLevelEnum, Slice, SliceId, SliceStatusEnum, EndPointId, SliceConfig, ConfigRule
from common.tools.context_queries.Context import get_context
from common.tools.context_queries.EndPoint import get_endpoint_names
from common.tools.context_queries.Slice import get_slice_by_uuid, get_uuid_from_string
from common.Constants import DEFAULT_CONTEXT_NAME
from context.client.ContextClient import ContextClient
from slice.client.SliceClient import SliceClient

slice = Blueprint('slice', __name__, url_prefix='/slice')

context_client = ContextClient()
slice_client = SliceClient()


RUNNING_RESOURCE_KEY = "running_ietf_slice"
CANDIDATE_RESOURCE_KEY = "candidate_ietf_slice"


class ConfigRuleNotFoundError(Exception):
    ...

def get_custom_config_rule(
    slice_config: SliceConfig, resource_key: str
) -> Optional[ConfigRule]:
    """
    Retrieve the custom config rule with the given resource_key from a ServiceConfig.
    """
    for cr in slice_config.config_rules:
        if (
            cr.WhichOneof("config_rule") == "custom"
            and cr.custom.resource_key == resource_key
        ):
            return cr
    return None


def get_ietf_data_from_config(slice_request: Slice, resource_key: str) -> Dict:
    """
    Retrieve the IETF data (as a Python dict) from a slice's config rule for the specified resource_key.
    Raises an exception if not found.
    """
    config_rule = get_custom_config_rule(slice_request.slice_config, resource_key)
    if not config_rule:
        raise ConfigRuleNotFoundError(f"IETF data not found for resource_key: {resource_key}")
    return json.loads(config_rule.custom.resource_value)


def endpoint_get_uuid(
    endpoint_id : EndPointId, endpoint_name : str = '', allow_random : bool = False
) -> Tuple[str, str, str]:
    device_uuid = endpoint_id.device_id.device_uuid.uuid
    topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
    raw_endpoint_uuid = endpoint_id.endpoint_uuid.uuid

    if len(raw_endpoint_uuid) > 0:
        prefix_for_name = '{:s}/{:s}'.format(topology_uuid, device_uuid)
        return topology_uuid, device_uuid, get_uuid_from_string(raw_endpoint_uuid, prefix_for_name=prefix_for_name)
    if len(endpoint_name) > 0:
        prefix_for_name = '{:s}/{:s}'.format(topology_uuid, device_uuid)
        return topology_uuid, device_uuid, get_uuid_from_string(endpoint_name, prefix_for_name=prefix_for_name)

    raise InvalidArgumentsException([
        ('endpoint_id.endpoint_uuid.uuid', raw_endpoint_uuid),
        ('name', endpoint_name),
    ], extra_details=['At least one is required to produce a EndPoint UUID'])

def get_slice_endpoints(slice_obj: Slice) -> list[EndPointId]:
    '''
    Get the list of endpoint ids for a slice.
    If the slice has a `running_ietf_slice` config rule, return the list of endpoint ids from the config rule,
    otherwise return the slice's list of endpoint ids.
    '''
    try:
        first_slice_endpoint_id = slice_obj.slice_endpoint_ids[0]
        topology_uuid = first_slice_endpoint_id.topology_id.topology_uuid.uuid
        context_uuid = slice_obj.slice_id.context_id.context_uuid.uuid
        running_ietf_data = get_ietf_data_from_config(slice_obj, RUNNING_RESOURCE_KEY)
        slice_service = running_ietf_data["network-slice-services"]["slice-service"][0]
        slice_sdps = slice_service["sdps"]["sdp"]
        list_endpoint_ids = []
        for sdp in slice_sdps:
            endpoint = EndPointId()
            endpoint.topology_id.context_id.context_uuid.uuid = context_uuid
            endpoint.topology_id.topology_uuid.uuid = topology_uuid
            device_uuid = get_uuid_from_string(sdp["node-id"])
            endpoint.device_id.device_uuid.uuid = device_uuid
            attachment_circuits = sdp["attachment-circuits"]["attachment-circuit"]
            endpoint_name = attachment_circuits[0]["ac-tp-id"]
            endpoint.endpoint_uuid.uuid = endpoint_name
            _, _, endpoint_uuid = endpoint_get_uuid(endpoint)
            endpoint.endpoint_uuid.uuid = endpoint_uuid
            list_endpoint_ids.append(endpoint)
        del slice_obj.slice_endpoint_ids[:]
        slice_obj.slice_endpoint_ids.extend(list_endpoint_ids)

    except ConfigRuleNotFoundError:
        # The slice does not have `running_ietf_slice` config rule, return slice's list of endpoint ids
        list_endpoint_ids = slice_obj.slice_endpoint_ids

    return list_endpoint_ids

@slice.get('/')
def home():
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))
    context_uuid = session['context_uuid']

    context_client.connect()

    context_obj = get_context(context_client, context_uuid, rw_copy=False)
    if context_obj is None:
        flash('Context({:s}) not found'.format(str(context_uuid)), 'danger')
        device_names, endpoints_data = list(), list()
    else:
        try:
            slices = context_client.ListSlices(context_obj.context_id)
            slices = slices.slices
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.NOT_FOUND: raise
            if e.details() != 'Context({:s}) not found'.format(context_uuid): raise
            slices, device_names, endpoints_data = list(), dict(), dict()
        else:
            endpoint_ids = list()
            for slice_ in slices:
                slice_endpoint_ids = get_slice_endpoints(slice_)
                endpoint_ids.extend(slice_endpoint_ids)
            device_names, endpoints_data = get_endpoint_names(context_client, endpoint_ids)

    context_client.close()
    return render_template(
        'slice/home.html', slices=slices, device_names=device_names, endpoints_data=endpoints_data,
        sse=SliceStatusEnum)


@slice.route('add', methods=['GET', 'POST'])
def add():
    flash('Add slice route called', 'danger')
    raise NotImplementedError()
    #return render_template('slice/home.html')


@slice.get('<path:slice_uuid>/detail')
def detail(slice_uuid: str):
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))
    context_uuid = session['context_uuid']

    try:
        context_client.connect()

        slice_obj = get_slice_by_uuid(context_client, slice_uuid, rw_copy=False)
        if slice_obj is None:
            flash('Context({:s})/Slice({:s}) not found'.format(str(context_uuid), str(slice_uuid)), 'danger')
            slice_obj = Slice()
        else:
            slice_endpoint_ids = get_slice_endpoints(slice_obj)
            device_names, endpoints_data = get_endpoint_names(context_client, slice_endpoint_ids)

        context_client.close()

        return render_template(
            'slice/detail.html', slice=slice_obj, device_names=device_names, endpoints_data=endpoints_data,
            sse=SliceStatusEnum, ile=IsolationLevelEnum)
    except Exception as e:
        flash('The system encountered an error and cannot show the details of this slice.', 'warning')
        current_app.logger.exception(e)
        return redirect(url_for('slice.home'))

@slice.get('<path:slice_uuid>/delete')
def delete(slice_uuid: str):
    if 'context_uuid' not in session or 'topology_uuid' not in session:
        flash("Please select a context!", "warning")
        return redirect(url_for("main.home"))
    context_uuid = session['context_uuid']

    try:
        request = SliceId()
        request.slice_uuid.uuid = slice_uuid
        request.context_id.context_uuid.uuid = context_uuid
        slice_client.connect()
        slice_client.DeleteSlice(request)
        slice_client.close()

        flash('Slice "{:s}" deleted successfully!'.format(slice_uuid), 'success')
    except Exception as e:
        flash('Problem deleting slice "{:s}": {:s}'.format(slice_uuid, str(e.details())), 'danger')
        current_app.logger.exception(e)
    return redirect(url_for('slice.home'))
