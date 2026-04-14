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

import json
import logging
import os
import requests
from concurrent.futures import ThreadPoolExecutor

LOGGER = logging.getLogger(__name__)

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

executor = ThreadPoolExecutor()

site_template = {
    "site-id": "",
    "devices": {
        "device": [
            {
                "device-id": "",
                "location": ""
            }
        ]
    },
    "site-network-accesses": {
        "site-network-access": [
            {
                "site-network-access-id": "",
                "device-reference": "",
                "ip-connection": {
                    "ipv4": {
                        "address-allocation-type": "ietf-l3vpn-svc:static-address",
                        "addresses": {
                            "provider-address": "",
                            "customer-address": "",
                            "prefix-length": ""
                        }
                    }
                },
                "vpn-attachment": {
                    "vpn-id": "vpn-p2mp"
                },
                "site-network-access-type": "ietf-l3vpn-svc:multipoint"
            }
        ]
    }
}

def generate_l3vpn_template_pair(src, dst, vpn_id):

    return {
        "ietf-l3vpn-svc:l3vpn-svc": {
            "vpn-services": {
                "vpn-service": [{"vpn-id": vpn_id}]
            },
            "sites": {
                "site": [
                    {
                        "site-id": src["uuid"],
                        "management": {"type": "ietf-l3vpn-svc:provider-managed"},
                        "locations": {"location": [{"location-id": f"location-{src['uuid']}"}]},
                        "devices": {"device": [{
                            "device-id": "10.0.30.1",
                            "location": f"location-{src['uuid']}"
                        }]},
                        "routing-protocols": {"routing-protocol": [{
                            "type": "ietf-l3vpn-svc:static",
                            "static": {
                                "cascaded-lan-prefixes": {
                                    "ipv4-lan-prefixes": [
                                        {
                                        "lan": "128.32.10.1/24",
                                        "lan-tag": f"vlan{src['vlan_id']}",
                                        "next-hop": "10.0.30.10"
                                        }
                                    ]
                                }
                            }
                        }]},
                        "site-network-accesses": {
                            "site-network-access": [{
                                "site-network-access-id": f"{src['vlan_id']}",
                                "site-network-access-type": "ietf-l3vpn-svc:multipoint",
                                "device-reference": "10.0.30.1",
                                "vpn-attachment": {
                                    "vpn-id": vpn_id, "site-role": "ietf-l3vpn-svc:spoke-role"
                                },
                                "ip-connection": {
                                    "ipv4": {
                                        "address-allocation-type": "ietf-l3vpn-svc:static-address",
                                        "addresses": {
                                            "provider-address": "10.0.30.254",
                                            "customer-address": "10.0.30.10",
                                            "prefix-length": 24
                                        }
                                    }
                                },
                                "routing-protocols": {"routing-protocol": [{
                                    "type": "ietf-l3vpn-svc:static",
                                    "static": {
                                        "cascaded-lan-prefixes": {
                                            "ipv4-lan-prefixes": [
                                                {
                                                "lan": "172.1.101.1/24",
                                                "lan-tag": "vlan100",
                                                "next-hop": "10.0.30.254"
                                                }
                                            ]
                                        }
                                    }
                                }]},
                                "service": {
                                    "svc-mtu": 1500,
                                    "svc-input-bandwidth": 1000000000,
                                    "svc-output-bandwidth": 1000000000,
                                    "qos": {
                                        "qos-profile": {
                                        "classes": {
                                            "class": [
                                            {
                                                "class-id": "qos-realtime",
                                                "direction": "ietf-l3vpn-svc:both",
                                                "latency": {
                                                "latency-boundary": 10
                                                },
                                                "bandwidth": {
                                                "guaranteed-bw-percent": 100
                                                }
                                            }
                                            ]
                                        }
                                        }
                                    }
                                }
                            }]
                        }
                    },
                    {
                        "site-id": dst["uuid"],
                        "management": {"type": "ietf-l3vpn-svc:provider-managed"},
                        "locations": {"location": [{"location-id": f"location-{dst['uuid']}"}]},
                        "devices": {"device": [{
                            "device-id": "10.0.20.1",
                            "location": f"location-{dst['uuid']}"
                        }]},
                        "routing-protocols": {"routing-protocol": [{
                            "type": "ietf-l3vpn-svc:static",
                            "static": {
                                "cascaded-lan-prefixes": {
                                    "ipv4-lan-prefixes": [
                                        {
                                        "lan": "172.1.101.1/24",
                                        "lan-tag": "vlan200",
                                        "next-hop": "172.10.33.2"
                                        }
                                    ]
                                }
                            }
                        }]},
                        "site-network-accesses": {
                            "site-network-access": [{
                                "site-network-access-id": f"{dst['vlan_id']}",
                                "site-network-access-type": "ietf-l3vpn-svc:multipoint",
                                "device-reference": "10.0.20.1",
                                "vpn-attachment": {
                                    "vpn-id": vpn_id, "site-role": "ietf-l3vpn-svc:hub-role"
                                },
                                "ip-connection": {
                                    "ipv4": {
                                        "address-allocation-type": "ietf-l3vpn-svc:static-address",
                                        "addresses": {
                                            "provider-address": "172.10.33.254",
                                            "customer-address": "172.10.33.2",
                                            "prefix-length": 24
                                        }
                                    }
                                },
                                "routing-protocols": {"routing-protocol": [{
                                    "type": "ietf-l3vpn-svc:static",
                                    "static": {
                                        "cascaded-lan-prefixes": {
                                            "ipv4-lan-prefixes": [
                                                {
                                                "lan": "128.32.10.1/24",
                                                "lan-tag": "vlan200",
                                                "next-hop": "172.10.33.254"
                                                }
                                            ]
                                        }
                                    }
                                }]},
                                "service": {
                                    "svc-mtu": 1500,
                                    "svc-input-bandwidth": 1000000000,
                                    "svc-output-bandwidth": 1000000000,
                                    "qos": {
                                        "qos-profile": {
                                        "classes": {
                                            "class": [
                                            {
                                                "class-id": "qos-realtime",
                                                "direction": "ietf-l3vpn-svc:both",
                                                "latency": {
                                                "latency-boundary": 10
                                                },
                                                "bandwidth": {
                                                "guaranteed-bw-percent": 100
                                                }
                                            }
                                            ]
                                        }
                                        }
                                    }
                                }
                            }]
                        }
                    }
                ]
            }
        }
    }

def create_request(resource_value):
    """ Create and send HTTP request based on a JSON template and provided resource value.
        The JSON template is expected to be in the same directory as this script, named 'ipowdm.json'.
        Example resource_value:
            {"rule_set": {
                "uuid": "unique-service-uuid",
                "bw": 100,
                "src": [{"uuid": "src-device-uuid", "ip_address": "192.168.1.1", "ip_mask": "24", "vlan_id": 100, "power": 10, "frequency": 193100}],
                "dst": [{"uuid": "dst-device-uuid", "ip_address": "192.168.3.3", "ip_mask": "24", "vlan_id": 100, "power": 10, "frequency": 193100}]
            }}
        The src and dst fields are lists to accommodate future extensions for multi-endpoint scenarios.
        The request is sent to a predefined URL with appropriate headers.
        Returns a response-like object with status_code and text attributes.
        In case of error, returns a SimpleNamespace with status_code 500 and the error message in text.

        Note: The actual HTTP request sending is currently mocked for testing purposes.
        The URL and headers are hardcoded for demonstration and should be adapted as needed.
    """

    LOGGER.info("Creating request for resource_value: %s", resource_value)

    node_src = resource_value[1]['rule_set']['src'][0]
    src = [{
        'uuid': node_src["uuid"],
        'ip_address': node_src["ip_address"],
        'ip_mask': node_src["ip_mask"],
        'vlan_id': node_src["vlan_id"]
    }]
    dst_list = resource_value[1]['rule_set']['dst']
    dsts = []
    for node in dst_list:
        dsts.append({
            'uuid': node["uuid"],
            'ip_address': node["ip_address"],
            'ip_mask': node["ip_mask"],
            'vlan_id': node["vlan_id"]
        })

    sites_input = src + dsts

    components = resource_value[1]['rule_set']['transceiver']['components']
    for i, device in enumerate(components):
        name = sites_input[i]['uuid']

        if name == "T2.1":device["frequency"]= 195000000
        if name == "T1.1":device["frequency"]= 195006250
        if name == "T1.2":device["frequency"]= 195018750
        if name == "T1.3":device["frequency"]= 195031250

        LOGGER.debug(f"NODE TO CONFIGURE: \n{name}: {json.dumps(device, indent=2)}")
        response = patch_optical_channel_frequency(device, name)
        LOGGER.debug(f"RESPONSE :\n {response}")
    templates = []
    for dst in dsts:
        vpn = "L3VPN_"+src[0]['uuid']+"_"+dst['uuid']
        templates.append(generate_l3vpn_template_pair(src[0], dst,vpn))

    url = "http://192.168.202.254:80/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    for template in templates:
        LOGGER.info("Generated L3VPN P2MP service JSON:\n%s", json.dumps(template, indent=2))

        response = requests.post(url = url, headers= headers, json=template)
        LOGGER.debug(response)
    return None

def patch_optical_channel_frequency(data, DEVICE_ID):
    encoded_path = f"http://192.168.202.254:80/restconf/data/device={DEVICE_ID}/openconfig-platform:components/component=channel-1/optical-channel/config"

    patch_data = data
    response = requests.patch(f"{encoded_path}",
                            json=patch_data,
                            headers=HEADERS)
    assert response.status_code == 200
    return response
