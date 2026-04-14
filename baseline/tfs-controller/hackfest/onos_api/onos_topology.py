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

IP='127.0.0.1'
PORT='8181'
USER='onos'
PASSWORD='rocks'

def retrieveTopology(ip, port, user, password):
    http_json = 'http://' + ip + ':' + port + '/onos/v1/links'
    response = requests.get(http_json, auth=HTTPBasicAuth(user, password))
    topology = response.json()
    return topology

if __name__ == "__main__":

    print ("Reading network-topology")
    topo = retrieveTopology(IP, PORT, USER, PASSWORD)
    print ( json.dumps(topo, indent=4, sort_keys=True) )


    
