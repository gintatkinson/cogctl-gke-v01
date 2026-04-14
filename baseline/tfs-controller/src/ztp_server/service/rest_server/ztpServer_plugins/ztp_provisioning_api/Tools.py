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

import os

def returnConfigFile(config_db):
    try:
        configFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..','..','..','..', 'data', config_db)
        with open(configFilePath, 'r', encoding='utf-8') as configFile:
            content = configFile.read()
    except FileNotFoundError:
        return None

    return content
