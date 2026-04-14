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


import logging
from flask import request
from flask_restful import Api, Resource, abort
from typing import Set, Tuple
from .nft_model.DirectionEnum import DirectionEnum
from .nft_model.FamilyEnum import FamilyEnum
from .nft_model.NFTables import NFTables
from .nft_model.Rule import Rule
from .nft_model.TableEnum import TableEnum
from .AclRuleToInterfaceDirection import (
    CHAINS_INPUT, CHAINS_OUTPUT, AclRuleToInterfaceDirection,
    get_family_from_acl_set_type
)


LOGGER = logging.getLogger(__name__)


BASE_URL_ROOT = '/restconf/data/openconfig-acl:acl'
BASE_URL_ITEM = '/restconf/data/openconfig-acl:acl/acl-sets/acl-set=<name>'


class ACLs(Resource):
    def get(self):
        nft = NFTables()
        nft.load(FamilyEnum.IPV4, TableEnum.FILTER)
        return nft.to_openconfig(), 200

    def post(self):
        payload = request.get_json(force=True)
        if not isinstance(payload, dict):
            abort(400, message='invalid payload')

        content = payload.get('openconfig-acl:acl')
        if content is None:
            content = payload.get('acl')
            if content is None:
                abort(400, message='invalid payload')

        if not isinstance(content, dict):
            abort(400, message='invalid content')

        interfaces = content['interfaces']['interface']
        if not isinstance(interfaces, list):
            abort(400, message='invalid interfaces')

        nft = NFTables()
        nft.load(skip_rules=True)

        arid = AclRuleToInterfaceDirection(nft)
        arid.add_interfaces(interfaces)

        acl_sets = content['acl-sets']['acl-set']
        if not isinstance(acl_sets, list):
            abort(400, message='invalid acl_sets')

        for acl_set in acl_sets:
            acl_set_name = acl_set['config']['name']
            acl_set_type = acl_set['config']['type']

            family = get_family_from_acl_set_type(acl_set_type)
            table = TableEnum.FILTER

            for acl_entry in acl_set['acl-entries']['acl-entry']:
                interfaces_directions = arid.get_interfaces_directions(
                    acl_set_name, acl_entry['config']['sequence-id']
                )
                for if_name, direction in interfaces_directions:
                    if direction == DirectionEnum.INGRESS:
                        chain_list = CHAINS_INPUT
                        input_if_name, output_if_name = if_name, None
                    elif direction == DirectionEnum.EGRESS:
                        chain_list = CHAINS_OUTPUT
                        input_if_name, output_if_name = None, if_name
                    else:
                        raise Exception('Unsupported direction: {:s}'.format(str(direction)))

                    for chain_name in chain_list:
                        rule = Rule.from_openconfig(family, table, chain_name, acl_entry)
                        rule.input_if_name = input_if_name
                        rule.output_if_name = output_if_name
                        nft.add_rule(rule)

        entries = nft.dump()
        for entry in entries:
            LOGGER.warning('POST rules: {:s}'.format(str(entry)))

        nft.execute(verbose=True)

        return {}, 201


def load_nftables_by_rule_comment(rule_comment : str) -> NFTables:
    nft = NFTables()
    nft.load(FamilyEnum.IPV4, TableEnum.FILTER)

    tables_to_remove : Set[Tuple[FamilyEnum, TableEnum]] = set()
    for table_key, table in nft.tables.items():

        chains_to_remove : Set[str] = set()
        for chain_name, chain in table.chains.items():

            for rule in reversed(chain.rules):
                if rule.comment == rule_comment: continue
                chain.rules.remove(rule) # not a rule of interest

            if len(chain.rules) > 0: continue
            chains_to_remove.add(chain_name)

        for chain_name in chains_to_remove:
            table.chains.pop(chain_name)

        if len(nft.tables) > 0: continue
        tables_to_remove.add(table_key)

    for table_key in tables_to_remove:
        nft.tables.pop(table_key)

    return nft


class ACL(Resource):
    def get(self, name : str):
        nft = load_nftables_by_rule_comment(name)
        return nft.to_openconfig(), 200

    def delete(self, name : str):
        nft = load_nftables_by_rule_comment(name)
        nft.execute(removal=True, verbose=True)
        return {}, 204


def register_restconf_openconfig_acls(api : Api):
    api.add_resource(ACLs, BASE_URL_ROOT)
    api.add_resource(ACL, BASE_URL_ITEM)
