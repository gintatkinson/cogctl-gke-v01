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

import json
from json import dumps

import requests

from device.service.drivers.ietf_l3vpn.IetfL3VpnDriver import IetfL3VpnDriver
from device.service.Tools import RESOURCE_ENDPOINTS

settings = {
    "endpoints": [
        {
            "uuid": "access-pe",
            "name": "access-pe",
            "type": "copper",
            "ce-ip": "1.1.1.1",
            "address_ip": "3.3.2.1",
            "address_prefix": 24,
            "location": "access",
            "mtu": 1500,
            "ipv4_lan_prefixes": [
                {"lan": "128.32.10.0/24", "lan_tag": 10},
                {"lan": "128.32.20.0/24", "lan_tag": 20},
            ],
        },
        {
            "uuid": "cloud-pe",
            "name": "cloud-pe",
            "type": "copper",
            "ce-ip": "1.1.1.1",
            "address_ip": "3.3.2.1",
            "address_prefix": 24,
            "location": "cloud",
            "mtu": 1500,
            "ipv4_lan_prefixes": [{"lan": "172.1.101.0/24", "lan_tag": 101}],
        },
    ],
    "scheme": "http",
    "username": "admin",
    "password": "admin",
    "base_url": "/restconf/v2/data",
    "timeout": 120,
    "verify": False,
}

post_request_data = []
get_request_data = []


def mock_post(*args, **kwargs):
    post_request_data.append((args, kwargs))


def mock_get(*args, **kwargs):
    get_request_data.append((args, kwargs))


driver = IetfL3VpnDriver(address="1.2.3.4", port=0, **settings)


def test_connect(monkeypatch):
    global post_request_data
    global get_request_data
    post_request_data = []
    get_request_data = []
    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "get", mock_get)

    driver.Connect()
    assert not post_request_data
    assert len(get_request_data) == 1
    assert get_request_data[0][0] == (
        "http://1.2.3.4:0/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services",
    )
    assert list(get_request_data[0][1].keys()) == ["timeout", "verify", "auth"]


def test_GetConfig(monkeypatch):
    global post_request_data
    global get_request_data
    post_request_data = []
    get_request_data = []
    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "get", mock_get)

    resources_to_get = [RESOURCE_ENDPOINTS]
    result_GetConfig = driver.GetConfig(resources_to_get)
    assert result_GetConfig == [
        (
            "/endpoints/endpoint[access-pe]",
            {
                "uuid": "access-pe",
                "name": "access-pe",
                "type": "copper",
                "location": "access",
                "ce-ip": "1.1.1.1",
                "address_ip": "3.3.2.1",
                "address_prefix": 24,
                "mtu": 1500,
                "ipv4_lan_prefixes": [
                    {"lan": "128.32.10.0/24", "lan_tag": 10},
                    {"lan": "128.32.20.0/24", "lan_tag": 20},
                ],
            },
        ),
        (
            "/endpoints/endpoint[cloud-pe]",
            {
                "uuid": "cloud-pe",
                "name": "cloud-pe",
                "type": "copper",
                "location": "cloud",
                "ce-ip": "1.1.1.1",
                "address_ip": "3.3.2.1",
                "address_prefix": 24,
                "mtu": 1500,
                "ipv4_lan_prefixes": [{"lan": "172.1.101.0/24", "lan_tag": 101}],
            },
        ),
    ]


def test_SetConfig(monkeypatch):
    global post_request_data
    global get_request_data
    post_request_data = []
    get_request_data = []
    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "get", mock_get)

    resources = [
        (
            "/services/service[vpn_A]",
            json.dumps(
                {
                    "uuid": "vpn_A",
                    "src_device_name": "ip-net-controller",
                    "src_endpoint_name": settings["endpoints"][0]["name"],
                    "src_site_location": settings["endpoints"][0]["location"],
                    "src_ipv4_lan_prefixes": settings["endpoints"][0][
                        "ipv4_lan_prefixes"
                    ],
                    "src_ce_address": settings["endpoints"][0]["ce-ip"],
                    "src_pe_address": settings["endpoints"][0]["address_ip"],
                    "src_ce_pe_network_prefix": settings["endpoints"][0][
                        "address_prefix"
                    ],
                    "src_mtu": settings["endpoints"][0]["mtu"],
                    "dst_device_name": "ip-net-controller",
                    "dst_endpoint_name": settings["endpoints"][1]["name"],
                    "dst_site_location": settings["endpoints"][1]["location"],
                    "dst_ipv4_lan_prefixes": settings["endpoints"][1][
                        "ipv4_lan_prefixes"
                    ],
                    "dst_ce_address": settings["endpoints"][1]["ce-ip"],
                    "dst_pe_address": settings["endpoints"][1]["address_ip"],
                    "dst_ce_pe_network_prefix": settings["endpoints"][1][
                        "address_prefix"
                    ],
                    "dst_mtu": settings["endpoints"][1]["mtu"],
                }
            ),
        )
    ]
    result_SetConfig = driver.SetConfig(resources)
    assert result_SetConfig == [("/services/service[vpn_A]", True)]
    assert len(get_request_data) == 1
    assert get_request_data[0][0] == (
        "http://1.2.3.4:0/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service=vpn_A",
    )
    assert len(post_request_data) == 1
    assert post_request_data[0][0] == (
        "http://1.2.3.4:0/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-services",
    )
    assert post_request_data[0][1]["json"] == {
        "ietf-l3vpn-svc:l3vpn-svc": {
            "vpn-services": {"vpn-service": [{"vpn-id": "vpn_A"}]},
            "sites": {
                "site": [
                    {
                        "site-id": "site_access",
                        "management": {"type": "ietf-l3vpn-svc:customer-managed"},
                        "locations": {"location": [{"location-id": "access"}]},
                        "devices": {
                            "device": [
                                {
                                    "device-id": "ip-net-controller",
                                    "location": "access",
                                }
                            ]
                        },
                        "routing-protocols": {
                            "routing-protocol": [
                                {
                                    "type": "ietf-l3vpn-svc:static",
                                    "static": {
                                        "cascaded-lan-prefixes": {
                                            "ipv4-lan-prefixes": [
                                                {
                                                    "lan": "128.32.10.0/24",
                                                    "lan-tag": 10,
                                                    "next-hop": "3.3.2.1",
                                                },
                                                {
                                                    "lan": "128.32.20.0/24",
                                                    "lan-tag": 20,
                                                    "next-hop": "3.3.2.1",
                                                },
                                            ]
                                        }
                                    },
                                }
                            ]
                        },
                        "site-network-accesses": {
                            "site-network-access": [
                                {
                                    "site-network-access-id": "access-pe",
                                    "site-network-access-type": "ietf-l3vpn-svc:multipoint",
                                    "device-reference": "ip-net-controller",
                                    "vpn-attachment": {
                                        "vpn-id": "vpn_A",
                                        "site-role": "ietf-l3vpn-svc:hub-role",
                                    },
                                    "ip-connection": {
                                        "ipv4": {
                                            "address-allocation-type": "ietf-l3vpn-svc:static-address",
                                            "addresses": {
                                                "provider-address": "3.3.2.1",
                                                "customer-address": "1.1.1.1",
                                                "prefix-length": 24,
                                            },
                                        }
                                    },
                                    "service": {
                                        "svc-mtu": 1500,
                                        "svc-input-bandwidth": 1000000000,
                                        "svc-output-bandwidth": 1000000000,
                                        "qos": {
                                            "qos-profile": {
                                                "classes": {
                                                    "class": [
                                                        {
                                                            "class-id": "src_qos_profile",
                                                            "direction": (
                                                                "ietf-l3vpn-svc:both",
                                                            ),
                                                            "latency": {
                                                                "latency-boundary": 10
                                                            },
                                                            "bandwidth": {
                                                                "guaranteed-bw-percent": 100
                                                            },
                                                        }
                                                    ]
                                                }
                                            }
                                        },
                                    },
                                }
                            ]
                        },
                    },
                    {
                        "site-id": "site_cloud",
                        "management": {"type": "ietf-l3vpn-svc:customer-managed"},
                        "locations": {"location": [{"location-id": "cloud"}]},
                        "devices": {
                            "device": [
                                {
                                    "device-id": "ip-net-controller",
                                    "location": "cloud",
                                }
                            ]
                        },
                        "routing-protocols": {
                            "routing-protocol": [
                                {
                                    "type": "ietf-l3vpn-svc:static",
                                    "static": {
                                        "cascaded-lan-prefixes": {
                                            "ipv4-lan-prefixes": [
                                                {
                                                    "lan": "172.1.101.0/24",
                                                    "lan-tag": 101,
                                                    "next-hop": "3.3.2.1",
                                                }
                                            ]
                                        }
                                    },
                                }
                            ]
                        },
                        "site-network-accesses": {
                            "site-network-access": [
                                {
                                    "site-network-access-id": "cloud-pe",
                                    "site-network-access-type": "ietf-l3vpn-svc:multipoint",
                                    "device-reference": "ip-net-controller",
                                    "vpn-attachment": {
                                        "vpn-id": "vpn_A",
                                        "site-role": "ietf-l3vpn-svc:spoke-role",
                                    },
                                    "ip-connection": {
                                        "ipv4": {
                                            "address-allocation-type": "ietf-l3vpn-svc:static-address",
                                            "addresses": {
                                                "provider-address": "3.3.2.1",
                                                "customer-address": "1.1.1.1",
                                                "prefix-length": 24,
                                            },
                                        }
                                    },
                                    "service": {
                                        "svc-mtu": 1500,
                                        "svc-input-bandwidth": 1000000000,
                                        "svc-output-bandwidth": 1000000000,
                                        "qos": {
                                            "qos-profile": {
                                                "classes": {
                                                    "class": [
                                                        {
                                                            "class-id": "dst_qos_profile",
                                                            "direction": (
                                                                "ietf-l3vpn-svc:both",
                                                            ),
                                                            "latency": {
                                                                "latency-boundary": 10
                                                            },
                                                            "bandwidth": {
                                                                "guaranteed-bw-percent": 100
                                                            },
                                                        }
                                                    ]
                                                }
                                            }
                                        },
                                    },
                                }
                            ]
                        },
                    },
                ]
            },
        }
    }
