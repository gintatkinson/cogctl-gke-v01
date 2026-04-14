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

from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Regexp
from load_generator.tools.ListScalarRange import RE_SCALAR_RANGE_LIST

DEFAULT_AVAILABILITY   = '0.0..99.9999'
DEFAULT_CAPACITY_GBPS  = '0.1..100.00' #'10, 40, 50, 100, 400'
DEFAULT_E2E_LATENCY_MS = '5.0..100.00'

DEFAULT_REGEX = r'.+'

class LoadGenForm(FlaskForm):
    num_requests = IntegerField('Num Requests', default=100, validators=[DataRequired(), NumberRange(min=0)])
    num_generated = IntegerField('Num Generated', default=0, render_kw={'readonly': True})
    num_released = IntegerField('Num Released', default=0, render_kw={'readonly': True})

    request_type_service_l2nm = BooleanField('Service L2NM', default=False)
    request_type_service_l3nm = BooleanField('Service L3NM', default=False)
    request_type_service_mw = BooleanField('Service MW', default=False)
    request_type_service_tapi = BooleanField('Service TAPI', default=False)
    request_type_slice_l2nm = BooleanField('Slice L2NM', default=True)
    request_type_slice_l3nm = BooleanField('Slice L3NM', default=False)

    device_regex = StringField('Device selector [regex]', default=DEFAULT_REGEX)
    endpoint_regex = StringField('Endpoint selector [regex]', default=DEFAULT_REGEX)

    offered_load = FloatField('Offered Load [Erlang]', default=50, validators=[NumberRange(min=0.0)])
    holding_time = FloatField('Holding Time [seconds]', default=10, validators=[NumberRange(min=0.0)])
    inter_arrival_time = FloatField('Inter Arrival Time [seconds]', default=0, validators=[NumberRange(min=0.0)])

    availability   = StringField('Availability [%]', default=DEFAULT_AVAILABILITY,   validators=[Regexp(RE_SCALAR_RANGE_LIST)])
    capacity_gbps  = StringField('Capacity [Gbps]',  default=DEFAULT_CAPACITY_GBPS,  validators=[Regexp(RE_SCALAR_RANGE_LIST)])
    e2e_latency_ms = StringField('E2E Latency [ms]', default=DEFAULT_E2E_LATENCY_MS, validators=[Regexp(RE_SCALAR_RANGE_LIST)])

    max_workers = IntegerField('Max Workers', default=10, validators=[DataRequired(), NumberRange(min=1)])

    do_teardown = BooleanField('Do Teardown', default=True)

    record_to_dlt = BooleanField('Record to DLT', default=False)
    dlt_domain_id = StringField('DLT Domain Id', default='')

    infinite_loop = BooleanField('Infinite Loop', default=False, render_kw={'disabled': True})
    running = BooleanField('Running', default=False, render_kw={'disabled': True})

    submit = SubmitField('Start/Stop')
