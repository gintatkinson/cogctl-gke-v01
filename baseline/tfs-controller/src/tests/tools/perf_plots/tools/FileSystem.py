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

import pathlib
from typing import Dict

def create_folders(root_folder : str, experiment_id : str) -> Dict[str, str]:
    experiment_folder = root_folder + '/' + experiment_id
    folders = {
        'csv'  : experiment_folder + '/csv' ,
        'json' : experiment_folder + '/json',
        'png'  : experiment_folder + '/png' ,
    }
    for folder in folders.values():
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    return folders
