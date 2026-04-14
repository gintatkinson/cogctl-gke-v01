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
from wtforms import StringField, SelectField, SubmitField

class UpdateDeviceForm(FlaskForm):
   power            = StringField('Power')
   frequency        = StringField("Frequency")
   operational_mode = StringField("Operational Mode")
   line_port        = SelectField("Line Port")
   submit           = SubmitField('Update')

class AddTrancseiver(FlaskForm):
   transceiver = StringField("Transceiver")
   submit      = SubmitField('Add')

class UpdateInterfaceForm(FlaskForm):
   ip            = StringField("IP Address")
   prefix_length = StringField("Prefix Length")

DEVICE_STATUS = [
   ('', 'Select...'),
   ('DISABLED', 'DISABLED'),
   ('ENABLED', 'ENABLED')
]

class UpdateStatusForm(FlaskForm):
   status = SelectField("Device Status", choices=DEVICE_STATUS)
