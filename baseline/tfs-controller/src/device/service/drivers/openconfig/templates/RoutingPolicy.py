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

import copy, logging, lxml.etree as ET
from typing import Any, Dict, List, Tuple
from .Namespace import NAMESPACES
from .Tools import add_value_from_tag

LOGGER = logging.getLogger(__name__)

XPATH_POLICY_DEFINITIONS = "//ocrp:routing-policy/ocrp:policy-definitions/ocrp:policy-definition"
XPATH_PD_STATEMENTS      = ".//ocrp:statements/ocrp:statement"
XPATH_PD_ST_CONDITIONS   = ".//ocrp:conditions/ocbp:bgp-conditions/ocbp:match-ext-community-set"
XPATH_PD_ST_ACTIONS      = ".//ocrp:actions"

XPATH_BGP_EXT_COMMUN_SET = "//ocrp:routing-policy/ocrp:defined-sets/ocbp:bgp-defined-sets/" + \
                           "ocbp:ext-community-sets/ocbp:ext-community-set"

def parse(xml_data : ET.Element) -> List[Tuple[str, Dict[str, Any]]]:
    #LOGGER.info('[RoutePolicy] xml_data = {:s}'.format(str(ET.tostring(xml_data))))

    response = []
    for xml_policy_definition in xml_data.xpath(XPATH_POLICY_DEFINITIONS, namespaces=NAMESPACES):
        #LOGGER.info('xml_policy_definition = {:s}'.format(str(ET.tostring(xml_policy_definition))))

        policy_definition = {}
        statement_name = ''
        policy_name = xml_policy_definition.find('ocrp:name', namespaces=NAMESPACES)
        if policy_name is None or policy_name.text is None: continue
        add_value_from_tag(policy_definition, 'policy_name', policy_name)

        resource_key = '/routing_policy/policy_definition[{:s}]'.format(policy_definition['policy_name'])
        response.append((resource_key, copy.deepcopy(policy_definition)))

        for xml_statement in xml_policy_definition.xpath(XPATH_PD_STATEMENTS, namespaces=NAMESPACES):
            statement_name = xml_statement.find('ocrp:name', namespaces=NAMESPACES)
            if len(statement_name) != 0:                                                                        #FIX: In case there is a route policy defined without a statement name
                add_value_from_tag(policy_definition, 'statement_name', statement_name)

            for xml_condition in xml_statement.xpath(XPATH_PD_ST_CONDITIONS, namespaces=NAMESPACES):
                ext_community_set_name = xml_condition.find('ocbp:config/ocbp:ext-community-set', namespaces=NAMESPACES)
                add_value_from_tag(policy_definition, 'ext_community_set_name', ext_community_set_name)

                match_set_options = xml_condition.find('ocbp:config/ocbp:match-set-options', namespaces=NAMESPACES)
                add_value_from_tag(policy_definition, 'match_set_options', match_set_options)

            for xml_action in xml_statement.xpath(XPATH_PD_ST_ACTIONS, namespaces=NAMESPACES):
                policy_result = xml_action.find('ocbp:config/ocbp:policy-result', namespaces=NAMESPACES)
                add_value_from_tag(policy_definition, 'policy_result', policy_result)

        if len(statement_name) != 0:                                                                            #FIX: In case there is a route policy defined without a statement name
            resource_key = '/routing_policy/policy_definition[{:s}]/statement[{:s}]'.format(
                policy_definition['policy_name'], policy_definition['statement_name'])
            response.append((resource_key, copy.deepcopy(policy_definition)))

    for xml_bgp_ext_community_set in xml_data.xpath(XPATH_BGP_EXT_COMMUN_SET, namespaces=NAMESPACES):
        #LOGGER.info('xml_bgp_ext_community_set = {:s}'.format(str(ET.tostring(xml_bgp_ext_community_set))))

        bgp_ext_community_set = {}

        ext_community_set_name = xml_bgp_ext_community_set.find('ocbp:ext-community-set-name', namespaces=NAMESPACES)
        if ext_community_set_name is None or ext_community_set_name.text is None: continue
        add_value_from_tag(bgp_ext_community_set, 'ext_community_set_name', ext_community_set_name)

        resource_key = '/routing_policy/bgp_defined_set[{:s}]'.format(bgp_ext_community_set['ext_community_set_name'])
        response.append((resource_key, copy.deepcopy(bgp_ext_community_set)))

        ext_community_member = xml_bgp_ext_community_set.find('ocbp:config/ocbp:ext-community-member', namespaces=NAMESPACES)
        if ext_community_member is not None and ext_community_member.text is not None:
            add_value_from_tag(bgp_ext_community_set, 'ext_community_member', ext_community_member)

            resource_key = '/routing_policy/bgp_defined_set[{:s}][{:s}]'.format(
                bgp_ext_community_set['ext_community_set_name'], bgp_ext_community_set['ext_community_member'])
            response.append((resource_key, copy.deepcopy(bgp_ext_community_set)))

    return response
