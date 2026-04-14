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

from yattag import Doc, indent

def ip_link_mgmt(data,vendor, delete):
    doc, tag, text = Doc().tagtext()

    ID    = data['endpoint_id']['endpoint_uuid']['uuid']
    DATA  = data["rule_set"]
    
    with tag('interfaces', xmlns="http://openconfig.net/yang/interfaces"):
        if delete == True: 
            with tag('interface' ,'xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                with tag('name'):text(ID)
        else:
            with tag('interface'):
                with tag('name'):text(ID)
                with tag('config'):
                    with tag('name'):text(ID)
                    with tag('type', 'xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type"'):text('ianaift:l3ipvlan')
                    with tag('enabled'):text('true')    
                with tag('subinterfaces'):
                    with tag('subinterface'):
                        if vendor is None or vendor == 'ADVA':
                            with tag('index'): text('0')
                        with tag('config'):
                            with tag('index'): text('0')
                            if vendor == 'ADVA' and not 'vlan'in data: 
                                with tag('untagged-allowed', 'xmlns="http://www.advaoptical.com/cim/adva-dnos-oc-interfaces"'):text('true')
                        with tag('vlan',  xmlns="http://openconfig.net/yang/vlan"):
                            with tag('match'):
                                with tag('single-tagged'):
                                    with tag('config'):
                                        with tag('vlan-id'):text(DATA['vlan'])
                        with tag('ipv4',  xmlns="http://openconfig.net/yang/interfaces/ip"):
                            with tag('addresses'):
                                with tag('address'):
                                    with tag('ip'):text(DATA['ip'])
                                    with tag('config'):
                                        with tag('ip'):text(DATA['ip'])
                                        with tag('prefix-length'):text(DATA['mask'])
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result
