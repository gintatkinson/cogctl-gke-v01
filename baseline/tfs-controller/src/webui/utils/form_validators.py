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

from wtforms.validators import ValidationError

def key_value_validator():
    def _validate(form, field):
        if len(field.data) > 0:
            if '\n' not in field.data:  # case in which there is only one configuration
                if '=' not in field.data:
                    raise ValidationError(f'Configuration "{field.data}" does not follow the key=value pattern.')
            else:  # case in which there are several configurations
                configurations = field.data.split('\n')
                for configutation in configurations:
                    if '=' not in configutation:
                        raise ValidationError(f'Configuration "{configutation}" does not follow the key=value pattern.')
    return _validate
