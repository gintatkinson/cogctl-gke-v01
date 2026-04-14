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

import enum, functools
from common.proto.context_pb2 import DeviceDriverEnum
from ._GrpcToEnum import grpc_to_enum

# IMPORTANT: Entries of enum class ORM_DeviceDriverEnum should be named as in
#            the proto files removing the prefixes. For example, proto item
#            DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG should be included as
#            OPENCONFIG. If item name does not match, automatic mapping of
#            proto enums to database enums will fail.
class ORM_DeviceDriverEnum(enum.Enum):
    UNDEFINED             = DeviceDriverEnum.DEVICEDRIVER_UNDEFINED
    OPENCONFIG            = DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG
    TRANSPORT_API         = DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API
    P4                    = DeviceDriverEnum.DEVICEDRIVER_P4
    IETF_NETWORK_TOPOLOGY = DeviceDriverEnum.DEVICEDRIVER_IETF_NETWORK_TOPOLOGY
    ONF_TR_532            = DeviceDriverEnum.DEVICEDRIVER_ONF_TR_532
    XR                    = DeviceDriverEnum.DEVICEDRIVER_XR
    IETF_L2VPN            = DeviceDriverEnum.DEVICEDRIVER_IETF_L2VPN
    GNMI_OPENCONFIG       = DeviceDriverEnum.DEVICEDRIVER_GNMI_OPENCONFIG
    OPTICAL_TFS           = DeviceDriverEnum.DEVICEDRIVER_OPTICAL_TFS
    IETF_ACTN             = DeviceDriverEnum.DEVICEDRIVER_IETF_ACTN
    OC                    = DeviceDriverEnum.DEVICEDRIVER_OC
    QKD                   = DeviceDriverEnum.DEVICEDRIVER_QKD
    IETF_L3VPN            = DeviceDriverEnum.DEVICEDRIVER_IETF_L3VPN
    IETF_SLICE            = DeviceDriverEnum.DEVICEDRIVER_IETF_SLICE
    NCE                   = DeviceDriverEnum.DEVICEDRIVER_NCE
    SMARTNIC              = DeviceDriverEnum.DEVICEDRIVER_SMARTNIC
    MORPHEUS              = DeviceDriverEnum.DEVICEDRIVER_MORPHEUS
    RYU                   = DeviceDriverEnum.DEVICEDRIVER_RYU
    GNMI_NOKIA_SRLINUX    = DeviceDriverEnum.DEVICEDRIVER_GNMI_NOKIA_SRLINUX
    OPENROADM             = DeviceDriverEnum.DEVICEDRIVER_OPENROADM
    RESTCONF_OPENCONFIG   = DeviceDriverEnum.DEVICEDRIVER_RESTCONF_OPENCONFIG

grpc_to_enum__device_driver = functools.partial(
    grpc_to_enum, DeviceDriverEnum, ORM_DeviceDriverEnum)
