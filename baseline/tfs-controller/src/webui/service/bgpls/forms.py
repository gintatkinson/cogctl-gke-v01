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

# external imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SelectField, FileField, SubmitField

from wtforms import StringField, SelectField, TextAreaField, SubmitField, BooleanField, Form
from wtforms.validators import DataRequired, Length, NumberRange, Regexp, ValidationError
from common.proto.context_pb2 import DeviceOperationalStatusEnum
from webui.utils.form_validators import key_value_validator

class AddDeviceForm(FlaskForm):
    device_id = StringField('ID', 
                           validators=[DataRequired(), Length(min=5)])
    device_type = SelectField('Type', choices = [])                                                     
    operational_status = SelectField('Operational Status',
                        #    choices=[(-1, 'Select...'), (0, 'Undefined'), (1, 'Disabled'), (2, 'Enabled')],
                           coerce=int,
                           validators=[NumberRange(min=0)])
    device_drivers_undefined = BooleanField('UNDEFINED / EMULATED')
    device_drivers_openconfig = BooleanField('OPENCONFIG')
    device_drivers_transport_api = BooleanField('TRANSPORT_API')
    device_drivers_p4 = BooleanField('P4')
    device_drivers_ietf_network_topology = BooleanField('IETF_NETWORK_TOPOLOGY')
    device_drivers_onf_tr_532 = BooleanField('ONF_TR_352')
    device_drivers_xr = BooleanField('XR')
    device_config_address = StringField('connect/address',default='127.0.0.1',validators=[DataRequired(), Length(min=5)])
    device_config_port = StringField('connect/port',default='0',validators=[DataRequired(), Length(min=1)])
    device_config_settings = TextAreaField('connect/settings',default='{}',validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Add')

    def validate_operational_status(form, field):
        if field.data not in DeviceOperationalStatusEnum.DESCRIPTOR.values_by_number:
            raise ValidationError('The operational status value selected is incorrect!')

class ConfigForm(FlaskForm):
    device_key_config = StringField('Key configuration')
    device_value_config = StringField('Value configuration')    
    submit = SubmitField('Add')


class UpdateDeviceForm(FlaskForm):
    update_operational_status = SelectField('Operational Status',
                           choices=[(-1, 'Select...'), (0, 'Undefined'), (1, 'Disabled'), (2, 'Enabled')],
                           coerce=int,
                           validators=[NumberRange(min=0)])
                        
    submit = SubmitField('Update')

class ContextTopologyForm(FlaskForm):
    context_topology = SelectField(
        'Ctx/Topo',
        choices=[],
        validators=[
            DataRequired(),
            Length(min=1)
        ])
    submit = SubmitField('Submit')
    
class DescriptorForm(FlaskForm):
    descriptors = FileField(
        'Descriptors',
        validators=[
            FileAllowed(['json'], 'JSON Descriptors only!')
        ])
    submit = SubmitField('Submit')

class SpeakerForm(FlaskForm):
    
    speaker_address = StringField('ip',default='127.0.0.1',validators=[DataRequired(), Length(min=5)])
    speaker_port = StringField('port',default='179',validators=[DataRequired(), Length(min=1)])
    speaker_as = StringField('as',default='65000',validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Submit')