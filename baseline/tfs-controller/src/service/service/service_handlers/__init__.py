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

from common.proto.context_pb2 import DeviceDriverEnum, ServiceTypeEnum
from ..service_handler_api.FilterFields import FilterFieldEnum
from .ipowdm.IpowdmServiceHandler import IpowdmServiceHandler
from .l2nm_emulated.L2NMEmulatedServiceHandler import L2NMEmulatedServiceHandler
from .l2nm_ietfl2vpn.L2NM_IETFL2VPN_ServiceHandler import L2NM_IETFL2VPN_ServiceHandler
from .l2nm_openconfig.L2NMOpenConfigServiceHandler import L2NMOpenConfigServiceHandler
from .l3nm_emulated.L3NMEmulatedServiceHandler import L3NMEmulatedServiceHandler
from .l3nm_gnmi_openconfig.L3NMGnmiOpenConfigServiceHandler import L3NMGnmiOpenConfigServiceHandler
from .l3nm_ietfactn.L3NM_IETFACTN_ServiceHandler import L3NM_IETFACTN_ServiceHandler
from .l3nm_ietfl3vpn.L3NM_IETFL3VPN_ServiceHandler import L3NM_IETFL3VPN_ServiceHandler
from .l3nm_ietfslice.L3NM_IETFSlice_ServiceHandler import L3NM_IETFSlice_ServiceHandler
from .l3nm_ncefan.L3NM_NCEFAN_ServiceHandler import L3NM_NCEFAN_ServiceHandler
from .l3nm_openconfig.L3NMOpenConfigServiceHandler import L3NMOpenConfigServiceHandler
from .microwave.MicrowaveServiceHandler import MicrowaveServiceHandler
from .p4_dummy_l1.p4_dummy_l1_service_handler import P4DummyL1ServiceHandler
from .p4_fabric_tna_int.p4_fabric_tna_int_service_handler import P4FabricINTServiceHandler
from .p4_fabric_tna_l2_simple.p4_fabric_tna_l2_simple_service_handler import P4FabricL2SimpleServiceHandler
from .p4_fabric_tna_l3.p4_fabric_tna_l3_service_handler import P4FabricL3ServiceHandler
from .p4_fabric_tna_acl.p4_fabric_tna_acl_service_handler import P4FabricACLServiceHandler
from .tapi_lsp.Tapi_LSPServiceHandler import Tapi_LSPServiceHandler
from .tapi_tapi.TapiServiceHandler import TapiServiceHandler
from .tapi_xr.TapiXrServiceHandler import TapiXrServiceHandler
from .optical_tfs.OpticalTfsServiceHandler import OpticalTfsServiceHandler
from .oc.OCServiceHandler import OCServiceHandler
from .ip_link.IP_LinkServiceHandler import IP_LinkServiceHandler
from .qkd.qkd_service_handler import QKDServiceHandler
from .l3nm_ryu.L3NMRyuServiceHandler import L3NMRyuServiceHandler

SERVICE_HANDLERS = [
    (L2NMEmulatedServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_UNDEFINED,
        }
    ]),
    (L2NMOpenConfigServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG,
        }
    ]),
    (L3NMEmulatedServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_UNDEFINED,
        }
    ]),
    (L3NMOpenConfigServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG,
        }
    ]),
    (L3NMGnmiOpenConfigServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_GNMI_OPENCONFIG,
        }
    ]),
    (L3NM_IETFACTN_ServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_IETF_ACTN,
        }
    ]),
    (L3NM_IETFL3VPN_ServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_IETF_L3VPN,
        }
    ]),
    (L3NM_NCEFAN_ServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_NCE,
        }
    ]),
    (L3NM_IETFSlice_ServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER : DeviceDriverEnum.DEVICEDRIVER_IETF_SLICE,
        }
    ]),
    (TapiServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE,
            FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API],
        }
    ]),
    (TapiXrServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE,
            FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_XR],
        }
    ]),
    (MicrowaveServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
            FilterFieldEnum.DEVICE_DRIVER : [
                DeviceDriverEnum.DEVICEDRIVER_IETF_NETWORK_TOPOLOGY,
                DeviceDriverEnum.DEVICEDRIVER_ONF_TR_532
            ],
        }
    ]),
    (P4DummyL1ServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE: ServiceTypeEnum.SERVICETYPE_L1NM,
            FilterFieldEnum.DEVICE_DRIVER: DeviceDriverEnum.DEVICEDRIVER_P4,
        }
    ]),
    (P4FabricINTServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE: ServiceTypeEnum.SERVICETYPE_INT,
            FilterFieldEnum.DEVICE_DRIVER: DeviceDriverEnum.DEVICEDRIVER_P4,
        }
    ]),
    (P4FabricL2SimpleServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE: ServiceTypeEnum.SERVICETYPE_L2NM,
            FilterFieldEnum.DEVICE_DRIVER: DeviceDriverEnum.DEVICEDRIVER_P4,
        }
    ]),
    (P4FabricL3ServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE: ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER: DeviceDriverEnum.DEVICEDRIVER_P4,
        }
    ]),
    (P4FabricACLServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE: ServiceTypeEnum.SERVICETYPE_ACL,
            FilterFieldEnum.DEVICE_DRIVER: DeviceDriverEnum.DEVICEDRIVER_P4,
        }
    ]),
    (L2NM_IETFL2VPN_ServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
            FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_IETF_L2VPN],
        }
    ]),
    # (SMARTNIC_ServiceHandler, [
    #     {
    #         FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
    #         FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_SMARTNIC],
    #     }
    # ]),
    (OpticalTfsServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY,
            FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_OPTICAL_TFS],
        }
    ]),
    (OCServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY,
            FilterFieldEnum.DEVICE_DRIVER : [
                DeviceDriverEnum.DEVICEDRIVER_OC,
                DeviceDriverEnum.DEVICEDRIVER_OPENROADM
            ],
        }
    ]),
    (IP_LinkServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_IP_LINK,
            FilterFieldEnum.DEVICE_DRIVER : [
                DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG,
                DeviceDriverEnum.DEVICEDRIVER_OC,
            ],
        }
    ]),
    (QKDServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_QKD,
            FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_QKD],
        }
    ]),
    (L3NMRyuServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L3NM,
            FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_RYU],
        }
    ]),
    (IpowdmServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_IPOWDM,
            FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_IETF_L3VPN],
            }
        ]),
    (Tapi_LSPServiceHandler, [
        {
            FilterFieldEnum.SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_TAPI_LSP,
            FilterFieldEnum.DEVICE_DRIVER : [DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API],
        }
    ])
]
