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

from typing import Any, Optional
from flask import redirect, render_template, Blueprint, flash, url_for
from common.proto.context_pb2 import Empty
from common.proto.load_generator_pb2 import Parameters, RequestTypeEnum
from load_generator.client.LoadGeneratorClient import LoadGeneratorClient
from load_generator.tools.ListScalarRange import (
    list_scalar_range__grpc_to_str, list_scalar_range__list_to_grpc, parse_list_scalar_range)
from .forms import LoadGenForm

load_gen = Blueprint('load_gen', __name__, url_prefix='/load_gen')

def set_properties(field, data : Any, readonly : Optional[bool] = None, disabled : Optional[bool] = None) -> None:
    if not hasattr(field, 'render_kw'):
        field.render_kw = dict()
    elif field.render_kw is None:
        field.render_kw = dict()

    if readonly is not None:
        field.render_kw['readonly'] = readonly
    if disabled is not None:
        field.render_kw['disabled'] = disabled

    if (readonly is not None and readonly) or (disabled is not None and disabled):
        field.data = data

@load_gen.route('home', methods=['GET'])
def home():
    load_gen_client = LoadGeneratorClient()

    load_gen_client.connect()
    status = load_gen_client.GetStatus(Empty())
    load_gen_client.close()

    request_types = status.parameters.request_types
    _request_type_service_l2nm = RequestTypeEnum.REQUESTTYPE_SERVICE_L2NM in request_types
    _request_type_service_l3nm = RequestTypeEnum.REQUESTTYPE_SERVICE_L3NM in request_types
    _request_type_service_mw   = RequestTypeEnum.REQUESTTYPE_SERVICE_MW   in request_types
    _request_type_service_tapi = RequestTypeEnum.REQUESTTYPE_SERVICE_TAPI in request_types
    _request_type_slice_l2nm   = RequestTypeEnum.REQUESTTYPE_SLICE_L2NM   in request_types
    _request_type_slice_l3nm   = RequestTypeEnum.REQUESTTYPE_SLICE_L3NM   in request_types

    _offered_load       = round(status.parameters.offered_load       , ndigits=4)
    _holding_time       = round(status.parameters.holding_time       , ndigits=4)
    _inter_arrival_time = round(status.parameters.inter_arrival_time , ndigits=4)

    _availability       = list_scalar_range__grpc_to_str(status.parameters.availability  )
    _capacity_gbps      = list_scalar_range__grpc_to_str(status.parameters.capacity_gbps )
    _e2e_latency_ms     = list_scalar_range__grpc_to_str(status.parameters.e2e_latency_ms)

    form = LoadGenForm()
    set_properties(form.num_requests             , status.parameters.num_requests  , readonly=status.running)
    set_properties(form.device_regex             , status.parameters.device_regex  , readonly=status.running)
    set_properties(form.endpoint_regex           , status.parameters.endpoint_regex, readonly=status.running)
    set_properties(form.offered_load             , _offered_load                   , readonly=status.running)
    set_properties(form.holding_time             , _holding_time                   , readonly=status.running)
    set_properties(form.inter_arrival_time       , _inter_arrival_time             , readonly=status.running)
    set_properties(form.availability             , _availability                   , readonly=status.running)
    set_properties(form.capacity_gbps            , _capacity_gbps                  , readonly=status.running)
    set_properties(form.e2e_latency_ms           , _e2e_latency_ms                 , readonly=status.running)
    set_properties(form.max_workers              , status.parameters.max_workers   , readonly=status.running)
    set_properties(form.do_teardown              , status.parameters.do_teardown   , disabled=status.running)
    set_properties(form.record_to_dlt            , status.parameters.record_to_dlt , disabled=status.running)
    set_properties(form.dlt_domain_id            , status.parameters.dlt_domain_id , readonly=status.running)
    set_properties(form.request_type_service_l2nm, _request_type_service_l2nm      , disabled=status.running)
    set_properties(form.request_type_service_l3nm, _request_type_service_l3nm      , disabled=status.running)
    set_properties(form.request_type_service_mw  , _request_type_service_mw        , disabled=status.running)
    set_properties(form.request_type_service_tapi, _request_type_service_tapi      , disabled=status.running)
    set_properties(form.request_type_slice_l2nm  , _request_type_slice_l2nm        , disabled=status.running)
    set_properties(form.request_type_slice_l3nm  , _request_type_slice_l3nm        , disabled=status.running)
    set_properties(form.num_generated            , status.num_generated            , disabled=True)
    set_properties(form.num_released             , status.num_released             , disabled=True)
    set_properties(form.infinite_loop            , status.infinite_loop            , disabled=True)
    set_properties(form.running                  , status.running                  , disabled=True)

    form.submit.label.text = 'Stop' if status.running else 'Start'
    form_action = url_for('load_gen.stop') if status.running else url_for('load_gen.start')
    return render_template('load_gen/home.html', form=form, form_action=form_action)

@load_gen.route('start', methods=['POST'])
def start():
    form = LoadGenForm()
    if form.validate_on_submit():
        try:
            _availability   = parse_list_scalar_range(form.availability.data  )
            _capacity_gbps  = parse_list_scalar_range(form.capacity_gbps.data )
            _e2e_latency_ms = parse_list_scalar_range(form.e2e_latency_ms.data)

            load_gen_params = Parameters()
            load_gen_params.num_requests       = form.num_requests.data
            load_gen_params.device_regex       = form.device_regex.data
            load_gen_params.endpoint_regex     = form.endpoint_regex.data
            load_gen_params.offered_load       = form.offered_load.data
            load_gen_params.holding_time       = form.holding_time.data
            load_gen_params.inter_arrival_time = form.inter_arrival_time.data
            load_gen_params.max_workers        = form.max_workers.data
            load_gen_params.do_teardown        = form.do_teardown.data
            load_gen_params.dry_mode           = False
            load_gen_params.record_to_dlt      = form.record_to_dlt.data
            load_gen_params.dlt_domain_id      = form.dlt_domain_id.data

            list_scalar_range__list_to_grpc(_availability,   load_gen_params.availability  ) # pylint: disable=no-member
            list_scalar_range__list_to_grpc(_capacity_gbps,  load_gen_params.capacity_gbps ) # pylint: disable=no-member
            list_scalar_range__list_to_grpc(_e2e_latency_ms, load_gen_params.e2e_latency_ms) # pylint: disable=no-member

            del load_gen_params.request_types[:] # pylint: disable=no-member
            request_types = list()
            if form.request_type_service_l2nm.data: request_types.append(RequestTypeEnum.REQUESTTYPE_SERVICE_L2NM)
            if form.request_type_service_l3nm.data: request_types.append(RequestTypeEnum.REQUESTTYPE_SERVICE_L3NM)
            if form.request_type_service_mw  .data: request_types.append(RequestTypeEnum.REQUESTTYPE_SERVICE_MW  )
            if form.request_type_service_tapi.data: request_types.append(RequestTypeEnum.REQUESTTYPE_SERVICE_TAPI)
            if form.request_type_slice_l2nm  .data: request_types.append(RequestTypeEnum.REQUESTTYPE_SLICE_L2NM  )
            if form.request_type_slice_l3nm  .data: request_types.append(RequestTypeEnum.REQUESTTYPE_SLICE_L3NM  )
            load_gen_params.request_types.extend(request_types) # pylint: disable=no-member

            load_gen_client = LoadGeneratorClient()
            load_gen_client.connect()
            load_gen_client.Start(load_gen_params)
            load_gen_client.close()
            flash('Load Generator Started.', 'success')
        except Exception as e: # pylint: disable=broad-except
            flash('Problem starting Load Generator. {:s}'.format(str(e)), 'danger')
    return redirect(url_for('load_gen.home'))

@load_gen.route('stop', methods=['POST'])
def stop():
    form = LoadGenForm()
    if form.validate_on_submit():
        try:
            load_gen_client = LoadGeneratorClient()
            load_gen_client.connect()
            load_gen_client.Stop(Empty())
            load_gen_client.close()
            flash('Load Generator Stopped.', 'success')
        except Exception as e: # pylint: disable=broad-except
            flash('Problem stopping Load Generator. {:s}'.format(str(e)), 'danger')
    return redirect(url_for('load_gen.home'))
