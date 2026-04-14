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

"""
Common objects and methods for In-band Network Telemetry (INT) dataplane
based on the SD-Fabric dataplane model.
This dataplane covers both software based and hardware-based Stratum-enabled P4 switches,
such as the BMv2 software switch and Intel's Tofino/Tofino-2 switches.

SD-Fabric repo: https://github.com/stratum/fabric-tna
SD-Fabric docs: https://docs.sd-fabric.org/master/index.html
"""

import logging
from typing import List, Tuple
from common.proto.context_pb2 import ConfigActionEnum
from common.tools.object_factory.ConfigRule import json_config_rule
from common.type_checkers.Checkers import chk_address_ipv4, chk_transport_port

from service.service.service_handlers.p4_fabric_tna_commons.p4_fabric_tna_commons import *

LOGGER = logging.getLogger(__name__)

# INT service handler settings
INT_COLLECTOR_INFO = "int_collector_info"
INT_REPORT_MIRROR_ID_LIST = "int_report_mirror_id_list"
PORT_INT = "int_port"           # In-band Network Telemetry transport port (of the collector)
DURATION_SEC = "duration_sec"
INTERVAL_SEC = "interval_sec"

# INT tables
TABLE_INT_WATCHLIST = "FabricIngress.int_watchlist.watchlist"
TABLE_INT_EGRESS_REPORT = "FabricEgress.int_egress.report"

# Mirror IDs for INT reports
INT_REPORT_MIRROR_ID_LIST_TNA = [0x200, 0x201, 0x202, 0x203]  # Tofino-2 (2-pipe Tofino switches use only the first 2 entries)
INT_REPORT_MIRROR_ID_LIST_V1MODEL = [0x1FA]                   # Variable V1MODEL_INT_MIRROR_SESSION in p4 source program

# INT report types
INT_REPORT_TYPE_NO_REPORT = 0
INT_REPORT_TYPE_FLOW = 1
INT_REPORT_TYPE_QUEUE = 2
INT_REPORT_TYPE_DROP = 4

# INT collection timings
DEF_DURATION_SEC = 3000
DEF_INTERVAL_SEC = 1


def rules_set_up_int_watchlist(action : ConfigActionEnum) -> List [Tuple]: # type: ignore
    rule_no = cache_rule(TABLE_INT_WATCHLIST, action)

    rules_int_watchlist = []
    rules_int_watchlist.append(
        json_config_rule(
            action,
            '/tables/table/'+TABLE_INT_WATCHLIST+'['+str(rule_no)+']',
            {
                'table-name': TABLE_INT_WATCHLIST,
                'match-fields': [
                    {
                        'match-field': 'ipv4_valid',
                        'match-value': '1'
                    }
                ],
                'action-name': 'FabricIngress.int_watchlist.mark_to_report',
                'action-params': [],
                'priority': 1
            }
        )
    )

    return rules_int_watchlist

def rules_set_up_int_report_collector(
        int_collector_ip : str,
        action : ConfigActionEnum) -> List [Tuple]: # type: ignore
    assert chk_address_ipv4(int_collector_ip), "Invalid INT collector IPv4 address to configure watchlist"

    rule_no = cache_rule(TABLE_INT_WATCHLIST, action)

    rules_int_col_report = []
    rules_int_col_report.append(
        json_config_rule(
            action,
            '/tables/table/'+TABLE_INT_WATCHLIST+'['+str(rule_no)+']',
            {
                'table-name': TABLE_INT_WATCHLIST,
                'match-fields': [
                    {
                        'match-field': 'ipv4_valid',
                        'match-value': '1'
                    },
                    {
                        'match-field': 'ipv4_dst',
                        'match-value': int_collector_ip+'&&&0xFFFFFFFF'
                    }
                ],
                'action-name': 'FabricIngress.int_watchlist.no_report_collector',
                'action-params': [],
                'priority': 10
            }
        )
    )

    return rules_int_col_report

def rules_set_up_int_recirculation_ports(
        recirculation_port_list : List,
        port_type : str,
        fwd_type : int,
        vlan_id : int,
        action : ConfigActionEnum): # type: ignore
    rules_list = []

    for port in recirculation_port_list:
        rules_list.extend(
            rules_set_up_port(
                port=port,
                port_type=port_type,
                fwd_type=fwd_type,
                vlan_id=vlan_id,
                action=action
            )
        )

    LOGGER.debug("INT recirculation ports configured:{}".format(recirculation_port_list))

    return rules_list

def rules_set_up_int_report_flow(
        switch_id : int,
        src_ip : str,
        int_collector_ip : str,
        int_collector_port : int,
        action : ConfigActionEnum) -> List [Tuple]: # type: ignore
    assert switch_id > 0, "Invalid switch identifier to configure egress INT report"
    assert chk_address_ipv4(src_ip), "Invalid source IPv4 address to configure egress INT report"
    assert chk_address_ipv4(int_collector_ip), "Invalid INT collector IPv4 address to configure egress INT report"
    assert chk_transport_port(int_collector_port), "Invalid INT collector port number to configure egress INT report"

    rule_no = cache_rule(TABLE_INT_EGRESS_REPORT, action)

    rules_int_egress = []

    # Rule #1
    rules_int_egress.append(
        json_config_rule(
            action,
            '/tables/table/'+TABLE_INT_EGRESS_REPORT+'['+str(rule_no)+']',
            {
                'table-name': TABLE_INT_EGRESS_REPORT,
                'match-fields': [
                    {
                        'match-field': 'bmd_type',
                        'match-value': str(BRIDGED_MD_TYPE_INT_INGRESS_DROP)
                    },
                    {
                        'match-field': 'mirror_type',
                        'match-value': str(MIRROR_TYPE_INVALID)
                    },
                    {
                        'match-field': 'int_report_type',
                        'match-value': str(INT_REPORT_TYPE_DROP)
                    }
                ],
                'action-name': 'FabricEgress.int_egress.do_drop_report_encap',
                'action-params': [
                    {
                        'action-param': 'switch_id',
                        'action-value': str(switch_id)
                    },
                    {
                        'action-param': 'src_ip',
                        'action-value': src_ip
                    },
                    {
                        'action-param': 'mon_ip',
                        'action-value': int_collector_ip
                    },
                    {
                        'action-param': 'mon_port',
                        'action-value': str(int_collector_port)
                    }
                ]
            }
        )
    )

    rule_no = cache_rule(TABLE_INT_EGRESS_REPORT, action)

    # Rule #2
    rules_int_egress.append(
        json_config_rule(
            action,
            '/tables/table/'+TABLE_INT_EGRESS_REPORT+'['+str(rule_no)+']',
            {
                'table-name': TABLE_INT_EGRESS_REPORT,
                'match-fields': [
                    {
                        'match-field': 'bmd_type',
                        'match-value': str(BRIDGED_MD_TYPE_EGRESS_MIRROR)
                    },
                    {
                        'match-field': 'mirror_type',
                        'match-value': str(MIRROR_TYPE_INT_REPORT)
                    },
                    {
                        'match-field': 'int_report_type',
                        'match-value': str(INT_REPORT_TYPE_DROP)
                    }
                ],
                'action-name': 'FabricEgress.int_egress.do_drop_report_encap',
                'action-params': [
                    {
                        'action-param': 'switch_id',
                        'action-value': str(switch_id)
                    },
                    {
                        'action-param': 'src_ip',
                        'action-value': src_ip
                    },
                    {
                        'action-param': 'mon_ip',
                        'action-value': int_collector_ip
                    },
                    {
                        'action-param': 'mon_port',
                        'action-value': str(int_collector_port)
                    }
                ]
            }
        )
    )

    rule_no = cache_rule(TABLE_INT_EGRESS_REPORT, action)

    # Rule #3
    rules_int_egress.append(
        json_config_rule(
            action,
            '/tables/table/'+TABLE_INT_EGRESS_REPORT+'['+str(rule_no)+']',
            {
                'table-name': TABLE_INT_EGRESS_REPORT,
                'match-fields': [
                    {
                        'match-field': 'bmd_type',
                        'match-value': str(BRIDGED_MD_TYPE_EGRESS_MIRROR)
                    },
                    {
                        'match-field': 'mirror_type',
                        'match-value': str(MIRROR_TYPE_INT_REPORT)
                    },
                    {
                        'match-field': 'int_report_type',
                        'match-value': str(INT_REPORT_TYPE_FLOW)
                    }
                ],
                'action-name': 'FabricEgress.int_egress.do_local_report_encap',
                'action-params': [
                    {
                        'action-param': 'switch_id',
                        'action-value': str(switch_id)
                    },
                    {
                        'action-param': 'src_ip',
                        'action-value': src_ip
                    },
                    {
                        'action-param': 'mon_ip',
                        'action-value': int_collector_ip
                    },
                    {
                        'action-param': 'mon_port',
                        'action-value': str(int_collector_port)
                    }
                ]
            }
        )
    )

    rule_no = cache_rule(TABLE_INT_EGRESS_REPORT, action)

    # Rule #4
    rules_int_egress.append(
        json_config_rule(
            action,
            '/tables/table/'+TABLE_INT_EGRESS_REPORT+'['+str(rule_no)+']',
            {
                'table-name': TABLE_INT_EGRESS_REPORT,
                'match-fields': [
                    {
                        'match-field': 'bmd_type',
                        'match-value': str(BRIDGED_MD_TYPE_DEFLECTED)
                    },
                    {
                        'match-field': 'mirror_type',
                        'match-value': str(MIRROR_TYPE_INVALID)
                    },
                    {
                        'match-field': 'int_report_type',
                        'match-value': str(INT_REPORT_TYPE_DROP)
                    }
                ],
                'action-name': 'FabricEgress.int_egress.do_drop_report_encap',
                'action-params': [
                    {
                        'action-param': 'switch_id',
                        'action-value': str(switch_id)
                    },
                    {
                        'action-param': 'src_ip',
                        'action-value': src_ip
                    },
                    {
                        'action-param': 'mon_ip',
                        'action-value': int_collector_ip
                    },
                    {
                        'action-param': 'mon_port',
                        'action-value': str(int_collector_port)
                    }
                ]
            }
        )
    )

    rule_no = cache_rule(TABLE_INT_EGRESS_REPORT, action)

    # Rule #5
    rules_int_egress.append(
        json_config_rule(
            action,
            '/tables/table/'+TABLE_INT_EGRESS_REPORT+'['+str(rule_no)+']',
            {
                'table-name': TABLE_INT_EGRESS_REPORT,
                'match-fields': [
                    {
                        'match-field': 'bmd_type',
                        'match-value': str(BRIDGED_MD_TYPE_EGRESS_MIRROR)
                    },
                    {
                        'match-field': 'mirror_type',
                        'match-value': str(MIRROR_TYPE_INT_REPORT)
                    },
                    {
                        'match-field': 'int_report_type',
                        'match-value': str(INT_REPORT_TYPE_QUEUE)
                    }
                ],
                'action-name': 'FabricEgress.int_egress.do_local_report_encap',
                'action-params': [
                    {
                        'action-param': 'switch_id',
                        'action-value': str(switch_id)
                    },
                    {
                        'action-param': 'src_ip',
                        'action-value': src_ip
                    },
                    {
                        'action-param': 'mon_ip',
                        'action-value': int_collector_ip
                    },
                    {
                        'action-param': 'mon_port',
                        'action-value': str(int_collector_port)
                    }
                ]
            }
        )
    )

    rule_no = cache_rule(TABLE_INT_EGRESS_REPORT, action)

    # Rule #6
    rules_int_egress.append(
        json_config_rule(
            action,
            '/tables/table/'+TABLE_INT_EGRESS_REPORT+'['+str(rule_no)+']',
            {
                'table-name': TABLE_INT_EGRESS_REPORT,
                'match-fields': [
                    {
                        'match-field': 'bmd_type',
                        'match-value': str(BRIDGED_MD_TYPE_EGRESS_MIRROR)
                    },
                    {
                        'match-field': 'mirror_type',
                        'match-value': str(MIRROR_TYPE_INT_REPORT)
                    },
                    {
                        'match-field': 'int_report_type',
                        'match-value': str(INT_REPORT_TYPE_QUEUE | INT_REPORT_TYPE_FLOW)
                    }
                ],
                'action-name': 'FabricEgress.int_egress.do_local_report_encap',
                'action-params': [
                    {
                        'action-param': 'switch_id',
                        'action-value': str(switch_id)
                    },
                    {
                        'action-param': 'src_ip',
                        'action-value': src_ip
                    },
                    {
                        'action-param': 'mon_ip',
                        'action-value': int_collector_ip
                    },
                    {
                        'action-param': 'mon_port',
                        'action-value': str(int_collector_port)
                    }
                ]
            }
        )
    )

    return rules_int_egress
