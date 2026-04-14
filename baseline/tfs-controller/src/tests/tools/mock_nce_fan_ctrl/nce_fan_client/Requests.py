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


QOS_PROFILE_NAME = 'AR_VR_Gaming'
URL_QOS_PROFILE_ITEM = '/huawei-nce-app-flow:qos-profiles/qos-profile={:s}'.format(QOS_PROFILE_NAME)
REQUEST_QOS_PROFILE = {"huawei-nce-app-flow:qos-profiles": {"qos-profile": [
    {
        "downstream": {
            "assure-bandwidth": "1000000000",
            "max-bandwidth": "2000000000"
        },
        "max-jitter": 10,
        "max-latency": 10,
        "max-loss": "0.001",
        "name": QOS_PROFILE_NAME,
        "upstream": {
            "assure-bandwidth": "5000000000",
            "max-bandwidth": "10000000000"
        }
    }
]}}

APPLICATION_NAME = 'App_1_2_slice1'
URL_APPLICATION_ITEM = '/huawei-nce-app-flow:applications/application={:s}'.format(APPLICATION_NAME)
REQUEST_APPLICATION = {"huawei-nce-app-flow:applications": {"application": [
    {
        "app-features": {
            "app-feature": [
                {
                    "dest-ip": "172.1.101.22",
                    "dest-port": "10200",
                    "id": "feature_1_2_slice1",
                    "protocol": "tcp",
                    "src-ip": "172.16.204.221",
                    "src-port": "10500"
                }
            ]
        },
        "app-id": ["app_1_2_slice1"],
        "name": APPLICATION_NAME
    }
]}}

APP_FLOW_NAME = "App_Flow_1_2_slice1"
URL_APP_FLOW_ITEM = '/huawei-nce-app-flow:app-flows/app-flow={:s}'.format(APP_FLOW_NAME)
REQUEST_APP_FLOW = {"huawei-nce-app-flow:app-flows": {"app-flow": [
    {
        "app-name": APPLICATION_NAME,
        "duration": 9999,
        "max-online-users": 1,
        "name": APP_FLOW_NAME,
        "qos-profile": QOS_PROFILE_NAME,
        "service-profile": "service_1_2_slice1",
        "stas": ["00:3D:E1:18:82:9E"],
        "user-id": "ad2c2a94-3415-4676-867a-39eedfb9f205"
    }
]}}
