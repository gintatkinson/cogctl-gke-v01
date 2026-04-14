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


from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import ServiceTypeEnum

NETWORK_DEVICE_TYPES = {
    DeviceTypeEnum.NETWORK,
}

PACKET_DEVICE_TYPES = {
    DeviceTypeEnum.TERAFLOWSDN_CONTROLLER,
    DeviceTypeEnum.IETF_SLICE, DeviceTypeEnum.NCE,
    DeviceTypeEnum.IP_SDN_CONTROLLER, DeviceTypeEnum.EMULATED_IP_SDN_CONTROLLER,
    DeviceTypeEnum.PACKET_POP,
    DeviceTypeEnum.PACKET_ROUTER, DeviceTypeEnum.EMULATED_PACKET_ROUTER,
    DeviceTypeEnum.PACKET_SWITCH, DeviceTypeEnum.EMULATED_PACKET_SWITCH,
}

L2_DEVICE_TYPES = {
    DeviceTypeEnum.PACKET_SWITCH, DeviceTypeEnum.EMULATED_PACKET_SWITCH,
    DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM, DeviceTypeEnum.EMULATED_MICROWAVE_RADIO_SYSTEM,
    DeviceTypeEnum.PACKET_RADIO_ROUTER, DeviceTypeEnum.EMULATED_PACKET_RADIO_ROUTER,
    DeviceTypeEnum.P4_SWITCH, DeviceTypeEnum.EMULATED_P4_SWITCH,
}

OPTICAL_DEVICE_TYPES = {
    DeviceTypeEnum.OPEN_LINE_SYSTEM, DeviceTypeEnum.EMULATED_OPEN_LINE_SYSTEM,
    DeviceTypeEnum.XR_CONSTELLATION, DeviceTypeEnum.EMULATED_XR_CONSTELLATION,
    DeviceTypeEnum.OPTICAL_ROADM, DeviceTypeEnum.EMULATED_OPTICAL_ROADM,
    DeviceTypeEnum.OPTICAL_TRANSPONDER, DeviceTypeEnum.EMULATED_OPTICAL_TRANSPONDER,
}

SERVICE_TYPE_L2NM     = {ServiceTypeEnum.SERVICETYPE_L2NM}
SERVICE_TYPE_L3NM     = {ServiceTypeEnum.SERVICETYPE_L3NM}
SERVICE_TYPE_LXNM     = {ServiceTypeEnum.SERVICETYPE_L3NM, ServiceTypeEnum.SERVICETYPE_L2NM}
SERVICE_TYPE_TAPI     = {ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE}
SERVICE_TYPE_IP_LINK  = {ServiceTypeEnum.SERVICETYPE_IP_LINK}
SERVICE_TYPE_IPOWDM   = {ServiceTypeEnum.SERVICETYPE_IPOWDM}
SERVICE_TYPE_TAPI_LSP = {ServiceTypeEnum.SERVICETYPE_TAPI_LSP}

def get_service_type(device_type : DeviceTypeEnum, prv_service_type : ServiceTypeEnum) -> ServiceTypeEnum:
    if device_type in PACKET_DEVICE_TYPES and prv_service_type in SERVICE_TYPE_LXNM: return prv_service_type


def get_service_type(
    device_type : DeviceTypeEnum, prv_service_type : ServiceTypeEnum
) -> ServiceTypeEnum:
    if device_type is DeviceTypeEnum.NCE: return ServiceTypeEnum.SERVICETYPE_L3NM
    if device_type is DeviceTypeEnum.TERAFLOWSDN_CONTROLLER: return ServiceTypeEnum.SERVICETYPE_L3NM
    if (
        device_type in PACKET_DEVICE_TYPES and
        prv_service_type in SERVICE_TYPE_LXNM
    ): return prv_service_type
    if (
        device_type in PACKET_DEVICE_TYPES and
        prv_service_type in SERVICE_TYPE_IP_LINK
    ): return prv_service_type
    if device_type in L2_DEVICE_TYPES: return ServiceTypeEnum.SERVICETYPE_L2NM
    if device_type in OPTICAL_DEVICE_TYPES: return ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE
    if device_type in NETWORK_DEVICE_TYPES: return prv_service_type
    if (
        device_type in PACKET_DEVICE_TYPES and
        prv_service_type in SERVICE_TYPE_IPOWDM
    ): return ServiceTypeEnum.SERVICETYPE_IPOWDM
    if (
        device_type in PACKET_DEVICE_TYPES and
        prv_service_type in SERVICE_TYPE_TAPI_LSP
    ): return prv_service_type

    str_fields = ', '.join([
        'device_type={:s}'.format(str(device_type)),
        'prv_service_type={:s}'.format(str(prv_service_type)),
    ])
    raise Exception('Undefined Service Type for ({:s})'.format(str_fields))
