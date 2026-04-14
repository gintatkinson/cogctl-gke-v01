#!/usr/bin/python
# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import json

IP='localhost'
PORT='8181'
USER='onos'
PASSWORD='rocks'

URL = 'http://' + IP + ':' + PORT + '/onos/v1/flows/'

def insertFlow( nodeId, priority, inport, outport ):

    flow='{ "priority": '+priority+', "timeout": 0, "isPermanent": true, "deviceId": "'+nodeId+'", "treatment": { "instructions": [ { "type": "OUTPUT", "port": "'+outport+'" } ] }, "selector": { "criteria": [ { "type": "IN_PORT", "port": "'+inport+'" } ] } }'


    print ("Flow: " + flow)
    url = URL + nodeId + '?appId=tuto' 
    headers = {'content-type': 'application/json'}
    print (url)
    response = requests.post(url, data=flow,
	                    headers=headers, auth=HTTPBasicAuth(USER,
	                    PASSWORD))
    print (response)
    return response.status_code

def deleteFlows():
    
    url = URL + '' + 'application/'+'tuto' 
    response = requests.delete(url, auth=HTTPBasicAuth(USER, PASSWORD))
    print (response)
    return response.status_code



if __name__ == "__main__":

    print ("Setting flow")
    
    res = insertFlow(nodeId="of:0000000000000001", priority="40001", inport="1", outport="2")
    print (res)
 
    #deleteFlows()






    
