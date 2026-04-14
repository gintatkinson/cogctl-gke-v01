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

from yattag import Doc, indent
import logging

def interface_template (interface_data:dict) :
    data={"name":"eth0","ip":"192.168.1.1","prefix-length":'24'}
    doc, tag, text = Doc().tagtext()
    with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
        with tag('interfaces', xmlns="http://openconfig.net/yang/interfaces"):
            with tag('interface'):
                with tag('name'):text(interface_data['name'])
                with tag('config'):
                    with tag('name'):text(interface_data['name'])
                    with tag("enabled"):text(interface_data["enabled"])
                with tag('ipv4',xmlns="http://openconfig.net/yang/interfaces/ip") :
                    with tag("addresses"):
                        with tag("address"):
                            with tag('ip'):text(interface_data["ip"])
                            with tag('config'):
                                with tag('ip'):text(interface_data["ip"])
                                with tag('prefix-length'):text(interface_data["prefix-length"])

    result = indent(
                doc.getvalue(),
                indentation = ' '*2,
                newline = '\r\n'
            )        
    return result
