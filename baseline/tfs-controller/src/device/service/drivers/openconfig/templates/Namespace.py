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


NAMESPACE_NETCONF                             = 'urn:ietf:params:xml:ns:netconf:base:1.0'

NAMESPACE_ACL                                 = 'http://openconfig.net/yang/acl'
NAMESPACE_BGP_POLICY                          = 'http://openconfig.net/yang/bgp-policy'
NAMESPACE_INTERFACES                          = 'http://openconfig.net/yang/interfaces'
NAMESPACE_INTERFACES_IP                       = 'http://openconfig.net/yang/interfaces/ip'
NAMESPACE_NETWORK_INSTANCE                    = 'http://openconfig.net/yang/network-instance'
NAMESPACE_NETWORK_INSTANCE_TYPES              = 'http://openconfig.net/yang/network-instance-types'
NAMESPACE_OPENCONFIG_TYPES                    = 'http://openconfig.net/yang/openconfig-types'
NAMESPACE_PLATFORM                            = 'http://openconfig.net/yang/platform'
NAMESPACE_PLATFORM_PORT                       = 'http://openconfig.net/yang/platform/port'
NAMESPACE_POLICY_TYPES                        = 'http://openconfig.net/yang/policy-types'
NAMESPACE_POLICY_TYPES_2                      = 'http://openconfig.net/yang/policy_types'
NAMESPACE_ROUTING_POLICY                      = 'http://openconfig.net/yang/routing-policy'
NAMESPACE_VLAN                                = 'http://openconfig.net/yang/vlan'
NAMESPACE_PLATFORM_TRANSCEIVER                = 'http://openconfig.net/yang/platform/transceiver'
NAMESPACE_TERMINAL_DEVICE_DIGITAL_SUBCARRIERS = 'http://openconfig.net/yang/terminal-device-digital-subcarriers'

NAMESPACES = {
    'nc'   : NAMESPACE_NETCONF,
    'ocacl': NAMESPACE_ACL,
    'ocbp' : NAMESPACE_BGP_POLICY,
    'oci'  : NAMESPACE_INTERFACES,
    'ociip': NAMESPACE_INTERFACES_IP,
    'ocni' : NAMESPACE_NETWORK_INSTANCE,
    'ocnit': NAMESPACE_NETWORK_INSTANCE_TYPES,
    'ococt': NAMESPACE_OPENCONFIG_TYPES,
    'ocp'  : NAMESPACE_PLATFORM,
    'ocpp' : NAMESPACE_PLATFORM_PORT,
    'ocpt' : NAMESPACE_POLICY_TYPES,
    'ocpt2': NAMESPACE_POLICY_TYPES_2,
    'ocrp' : NAMESPACE_ROUTING_POLICY,
    'ocv'  : NAMESPACE_VLAN,
    'ocptr': NAMESPACE_PLATFORM_TRANSCEIVER,
    'octds': NAMESPACE_TERMINAL_DEVICE_DIGITAL_SUBCARRIERS,
}
