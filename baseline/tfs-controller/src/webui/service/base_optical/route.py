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


from flask import render_template, Blueprint
#from common.proto.context_pb2 import Empty, OpticalConfigList
#from context.client.ContextClient import ContextClient
#from device.client.DeviceClient import DeviceClient

base_optical = Blueprint('base_optical', __name__, url_prefix='/base_optical')
#device_client = DeviceClient()
#context_client = ContextClient()

@base_optical.get('/')
def home():
    # context_client.connect()
    # opticalConfig_list:OpticalConfigList = context_client.GetOpticalConfig(Empty())
    # context_client.close()
    # device_client.connect()
    # device_client.GetDeviceConfiguration(opticalConfig_list)
    # device_client.close()
    return render_template("base_optical/home.html")
