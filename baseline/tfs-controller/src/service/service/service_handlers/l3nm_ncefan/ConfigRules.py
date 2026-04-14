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

from typing import Dict, List

from common.tools.object_factory.ConfigRule import (
    json_config_rule_delete,
    json_config_rule_set,
)


def setup_config_rules(service_name: str, json_settings: Dict) -> List[Dict]:
    operation_type: str = json_settings["operation_type"]
    app_flow_id: str = json_settings["app_flow_id"]
    app_flow_user_id: str = json_settings["app_flow_user_id"]
    max_latency: int = json_settings["max_latency"]
    max_jitter: int = json_settings["max_jitter"]
    max_loss: float = json_settings["max_loss"]
    upstream_assure_bw: str = json_settings["upstream_assure_bw"]
    upstream_max_bw: str = json_settings["upstream_max_bw"]
    downstream_assure_bw: str = json_settings["downstream_assure_bw"]
    downstream_max_bw: str = json_settings["downstream_max_bw"]
    src_ip: str = json_settings["src_ip"]
    src_port: str = json_settings["src_port"]
    dst_ip: str = json_settings["dst_ip"]
    dst_port: str = json_settings["dst_port"]

    app_flow_app_name: str = f"App_Flow_{app_flow_id}"
    app_flow_service_profile: str = f"service_{app_flow_id}"
    app_id: str = f"app_{app_flow_id}"
    app_feature_id: str = f"feature_{app_flow_id}"
    app_flow_name: str = f"App_Flow_{app_flow_id}"
    qos_profile_name: str = f"AR_VR_Gaming_{app_flow_id}"

    app_flow_max_online_users: int = json_settings.get("app_flow_max_online_users", 1)
    app_flow_stas: str = json_settings.get("stas", "00:3D:E1:18:82:9E")
    app_flow_duration: int = json_settings.get("app_flow_duration", 9999)
    protocol: str = json_settings.get("protocol", "tcp")

    app_flow = {
        "name": app_flow_name,
        "user-id": app_flow_user_id,
        "app-name": app_flow_app_name,
        "max-online-users": app_flow_max_online_users,
        "stas": [app_flow_stas],
        "qos-profile": qos_profile_name,
        "service-profile": app_flow_service_profile,
        "duration": app_flow_duration,
    }
    qos_profile = {
        "name": qos_profile_name,
        "max-latency": max_latency,
        "max-jitter": max_jitter,
        "max-loss": str(max_loss),
        "upstream": {
            "assure-bandwidth": str(int(upstream_assure_bw)),
            "max-bandwidth": str(int(upstream_max_bw)),
        },
        "downstream": {
            "assure-bandwidth": str(int(downstream_assure_bw)),
            "max-bandwidth": str(int(downstream_max_bw)),
        },
    }
    application = {
        "name": app_flow_app_name,
        "app-id": [app_id],
        "app-features": {
            "app-feature": [
                {
                    "id": app_feature_id,
                    "dest-ip": dst_ip,
                    "dest-port": dst_port,
                    "src-ip": src_ip,
                    "src-port": src_port,
                    "protocol": protocol,
                }
            ]
        },
    }
    app_flow_datamodel = {
        "huawei-nce-app-flow:app-flows": {
            "app-flow": [app_flow],
            "qos-profiles": {"qos-profile": [qos_profile]},
            "applications": {"application": [application]},
        }
    }
    json_config_rules = [
        json_config_rule_set(
            "/service[{:s}]/AppFlow".format(service_name), app_flow_datamodel
        ),
        #json_config_rule_set(
        #    "/service[{:s}]/AppFlow/operation".format(service_name),
        #    {"type": operation_type},
        #),
    ]
    return json_config_rules


def teardown_config_rules(service_name: str, json_settings: Dict) -> List[Dict]:
    app_flow_id      : str = json_settings["app_flow_id"]
    app_flow_app_name: str = f"App_Flow_{app_flow_id}"
    app_flow_name    : str = f"App_Flow_{app_flow_id}"
    qos_profile_name : str = f"AR_VR_Gaming_{app_flow_id}"

    app_flow    = {"name": app_flow_name    }
    qos_profile = {"name": qos_profile_name }
    application = {"name": app_flow_app_name}

    app_flow_datamodel = {
        "huawei-nce-app-flow:app-flows": {
            "app-flow": [app_flow],
            "qos-profiles": {"qos-profile": [qos_profile]},
            "applications": {"application": [application]},
        }
    }

    json_config_rules = [
        json_config_rule_delete(
            "/service[{:s}]/AppFlow".format(service_name),
            app_flow_datamodel
        ),
        #json_config_rule_delete(
        #    "/service[{:s}]/AppFlow/operation".format(service_name),
        #    {},
        #),
    ]

    return json_config_rules
