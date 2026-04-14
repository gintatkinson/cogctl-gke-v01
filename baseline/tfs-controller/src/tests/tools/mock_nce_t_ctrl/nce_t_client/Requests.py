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


OSU_TUNNEL_NAME = 'osu_tunnel_1'
URL_OSU_TUNNEL_ITEM = '/ietf-te:te/tunnels/tunnel={:s}'.format(OSU_TUNNEL_NAME)
REQUEST_OSU_TUNNEL = {"ietf-te:te": {"tunnels": {"tunnel": [
    {
        "name": OSU_TUNNEL_NAME,
        "title": "OSU_TUNNEL_1",
        "admin-state": "ietf-te-types:tunnel-admin-state-up",
        "delay": 20,
        "te-bandwidth": {
            "layer": "odu",
            "odu-type": "osuflex",
            "number": 40
        },
        "bidirectional": True,
        "destination-endpoints": {
            "destination-endpoint": [
                {
                    "node-id": "10.0.30.1",
                    "tp-id": "200",
                    "ttp-channel-name": "och:1-odu2:1-oduflex:3-osuflex:1",
                    "protection-role": "work"
                }
            ]
        },
        "source-endpoints": {
            "source-endpoint": [
                {
                    "node-id": "10.0.10.1",
                    "tp-id": "200",
                    "ttp-channel-name": "och:1-odu2:1-oduflex:1-osuflex:2",
                    "protection-role": "work"
                }
            ]
        },
        "restoration": {
            "restoration-type": "ietf-te-types:lsp-restoration-not-applicable",
            "restoration-lock": False
        },
        "protection": {
            "protection-type": "ietf-te-types:lsp-protection-unprotected",
            "protection-reversion-disable": True
        }
    }
]}}}

ETHT_SERVICE_NAME = 'etht_service_1'
URL_ETHT_SERVICE_ITEM = '/ietf-eth-tran-service:etht-svc/etht-svc-instances={:s}'.format(ETHT_SERVICE_NAME)
REQUEST_ETHT_SERVICE = {"ietf-eth-tran-service:etht-svc": {"etht-svc-instances": [
    {
        "etht-svc-name": ETHT_SERVICE_NAME,
        "etht-svc-title": "ETHT_SERVICE_1",
        "etht-svc-type": "op-mp2mp-svc",
        "source-endpoints": {
            "source-endpoint": [
                {
                    "node-id": "10.0.10.1",
                    "tp-id": "200",
                    "protection-role": "work",
                    "layer-specific": {
                        "access-type": "port"
                    },
                    "is-extendable": False,
                    "is-terminal": True,
                    "static-route-list": [
                        {
                            "destination": "128.32.10.5",
                            "destination-mask": 24,
                            "next-hop": "128.32.33.5"
                        },
                        {
                            "destination": "128.32.20.5",
                            "destination-mask": 24,
                            "next-hop": "128.32.33.5"
                        }
                    ],
                    "outer-tag": {
                        "tag-type": "ietf-eth-tran-types:classify-c-vlan",
                        "vlan-value": 21
                    },
                    "service-classification-type": "ietf-eth-tran-type:vlan-classification",
                    "ingress-egress-bandwidth-profile" : {
                        "bandwidth-profile-type": "ietf-eth-tran-types:mef-10-bwp",
                        "CIR": 10000000,
                        "EIR": 10000000
                    }
                }
            ]
        },
        "destination-endpoints": {
            "destination-endpoint": [
                {
                    "node-id": "10.0.30.1",
                    "tp-id": "200",
                    "protection-role": "work",
                    "layer-specific": {
                        "access-type": "port"
                    },
                    "is-extendable": False,
                    "is-terminal": True,
                    "static-route-list": [
                        {
                            "destination": "172.1.101.22",
                            "destination-mask": 24,
                            "next-hop": "172.10.33.5"
                        }
                    ],
                    "outer-tag": {
                        "tag-type": "ietf-eth-tran-types:classify-c-vlan",
                        "vlan-value": 101
                    },
                    "service-classification-type": "ietf-eth-tran-type:vlan-classification",
                    "ingress-egress-bandwidth-profile" : {
                        "bandwidth-profile-type": "ietf-eth-tran-types:mef-10-bwp",
                        "CIR": 10000000,
                        "EIR": 10000000
                    }
                }
            ]
        },
        "svc-tunnel": [
            {
                "tunnel-name": "OSU_TUNNEL_NAME"
            }
        ],
        "optimizations": {
            "optimization-metric": [
                {
                    "metric-role": "work",
                    "metric-type": "ietf-te-types:path-metric-te"
                }
            ]
        }
    }
]}}
