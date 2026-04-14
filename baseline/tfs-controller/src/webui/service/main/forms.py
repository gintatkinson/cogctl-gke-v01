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
from wtforms.validators import DataRequired, Length


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
