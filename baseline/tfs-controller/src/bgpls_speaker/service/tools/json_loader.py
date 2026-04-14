# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

def getInterfaceFromJson():
    json_file = open('interfaces.json', 'r',encoding='utf-8')
    interface_data = json.load(json_file)
    return interface_data

def getInterfaceFromNodeNames(json_file,node_name_src,node_name_dst):

    interface_src=[]
    interface_dst=[]
    for device in json_file['devices']:
        print("dev: %s",device.keys())
        if device['name'] == node_name_src:
            interface_src=list(device['links'].keys())[list(device['links'].values()).index(node_name_dst)]
        if device['name'] == node_name_dst:
            interface_dst=list(device['links'].keys())[list(device['links'].values()).index(node_name_src)]

    return interface_src,interface_dst
    

if __name__ == "__main__":
    data=getInterfaceFromJson()
    print("data: %s",data['devices'])
    # for device in data['devices']:
    #     print(device['interfaces'].keys())

    print(getInterfaceFromNodeNames(data,"HL2-2-1","HL2-2-2"))