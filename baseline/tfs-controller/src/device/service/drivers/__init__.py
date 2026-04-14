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
from common.proto.context_pb2 import DeviceDriverEnum
from device.Config import LOAD_ALL_DEVICE_DRIVERS
from ..driver_api.FilterFields import FilterFieldEnum

DRIVERS = []

from .emulated.EmulatedDriver import EmulatedDriver # pylint: disable=wrong-import-position
DRIVERS.append(
    (EmulatedDriver, [
        {
            FilterFieldEnum.DEVICE_TYPE: [], # any device type
            FilterFieldEnum.DRIVER: [
                DeviceDriverEnum.DEVICEDRIVER_UNDEFINED,
            ],
        }
    ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .ietf_l2vpn.IetfL2VpnDriver import IetfL2VpnDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (IetfL2VpnDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.TERAFLOWSDN_CONTROLLER,
                FilterFieldEnum.DRIVER: DeviceDriverEnum.DEVICEDRIVER_IETF_L2VPN,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .ietf_l3vpn.IetfL3VpnDriver import IetfL3VpnDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (IetfL3VpnDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.TERAFLOWSDN_CONTROLLER,
                FilterFieldEnum.DRIVER: DeviceDriverEnum.DEVICEDRIVER_IETF_L3VPN,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .ietf_actn.IetfActnDriver import IetfActnDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (IetfActnDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: [
                    DeviceTypeEnum.OPEN_LINE_SYSTEM,
                    DeviceTypeEnum.NCE,
                ],
                FilterFieldEnum.DRIVER: DeviceDriverEnum.DEVICEDRIVER_IETF_ACTN,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .ietf_slice.IetfSliceDriver import IetfSliceDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (IetfSliceDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.TERAFLOWSDN_CONTROLLER,
                FilterFieldEnum.DRIVER: DeviceDriverEnum.DEVICEDRIVER_IETF_SLICE,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .nce.NCEDriver import NCEDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (NCEDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.NCE,
                FilterFieldEnum.DRIVER: DeviceDriverEnum.DEVICEDRIVER_NCE,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .openconfig.OpenConfigDriver import OpenConfigDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (OpenConfigDriver, [
            {
                # Real Packet Router, specifying OpenConfig Driver => use OpenConfigDriver
                FilterFieldEnum.DEVICE_TYPE: [
                    DeviceTypeEnum.PACKET_POP,
                    DeviceTypeEnum.PACKET_ROUTER,
                ],
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .gnmi_openconfig.GnmiOpenConfigDriver import GnmiOpenConfigDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (GnmiOpenConfigDriver, [
            {
                # Real Packet Router, specifying gNMI OpenConfig Driver => use GnmiOpenConfigDriver
                FilterFieldEnum.DEVICE_TYPE: [
                    DeviceTypeEnum.PACKET_POP,
                    DeviceTypeEnum.PACKET_ROUTER,
                ],
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_GNMI_OPENCONFIG,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .gnmi_nokia_srlinux.GnmiNokiaSrLinuxDriver import GnmiNokiaSrLinuxDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (GnmiNokiaSrLinuxDriver, [
            {
                # Real Packet Router, specifying gNMI Nokia SR Linux Driver => use GnmiNokiaSrLinuxDriver
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.PACKET_ROUTER,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_GNMI_NOKIA_SRLINUX,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .transport_api.TransportApiDriver import TransportApiDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (TransportApiDriver, [
            {
                # Real OLS, specifying TAPI Driver => use TransportApiDriver
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.OPEN_LINE_SYSTEM,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .p4.p4_driver import P4Driver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (P4Driver, [
            {
                # Real P4 Switch, specifying P4 Driver => use P4Driver
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.P4_SWITCH,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_P4,
            }
        ]))
    
if LOAD_ALL_DEVICE_DRIVERS:
    from .smartnic.SmartnicDriver import SmartnicDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (SmartnicDriver, [
            {
                # Real SmartNics device => use SmartNicsDriver
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.SMARTNIC,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_SMARTNIC,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .morpheus.MorpheusApiDriver import MorpheusApiDriver
    DRIVERS.append(
        (MorpheusApiDriver, [
            {
                # Close enough, it does optical switching
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.MORPHEUS,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_MORPHEUS,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .microwave.IETFApiDriver import IETFApiDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (IETFApiDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_IETF_NETWORK_TOPOLOGY,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .ryu.RyuDriver import RyuDriver
    DRIVERS.append(
        (RyuDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.OPENFLOW_RYU_CONTROLLER,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_RYU,
            }
        ])
    )

if LOAD_ALL_DEVICE_DRIVERS:
    from .xr.XrDriver import XrDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (XrDriver, [
            {
                # Close enough, it does optical switching
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.XR_CONSTELLATION,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_XR,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .optical_tfs.OpticalTfsDriver import OpticalTfsDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (OpticalTfsDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: [
                    DeviceTypeEnum.OPEN_LINE_SYSTEM,
                    DeviceTypeEnum.TERAFLOWSDN_CONTROLLER,
                ],
                FilterFieldEnum.DRIVER: DeviceDriverEnum.DEVICEDRIVER_OPTICAL_TFS,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    from .oc_driver.OCDriver import OCDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (OCDriver, [
            {
                # Real Packet Router, specifying OpenConfig Driver => use OpenConfigDriver
                FilterFieldEnum.DEVICE_TYPE: [
                    DeviceTypeEnum.OPTICAL_ROADM,
                    DeviceTypeEnum.OPTICAL_TRANSPONDER
                ],
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_OC,
            }
        ]))
    
if LOAD_ALL_DEVICE_DRIVERS:
    from .openroadm.OpenROADMDriver import OpenROADMDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (OpenROADMDriver, [
            {
                # Real Packet Router, specifying OpenConfig Driver => use OpenConfigDriver
                FilterFieldEnum.DEVICE_TYPE: [
                    DeviceTypeEnum.OPEN_ROADM,
                ],
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_OPENROADM,
            }
        ]))    

if LOAD_ALL_DEVICE_DRIVERS:
    from .qkd.QKDDriver2 import QKDDriver # pylint: disable=wrong-import-position
    DRIVERS.append(
        (QKDDriver, [
            {
                # Close enough, it does optical switching
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.QKD_NODE,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_QKD,
            }
        ]))

if LOAD_ALL_DEVICE_DRIVERS:
    # pylint: disable=wrong-import-position
    from .restconf_openconfig.RestConfOpenConfigDriver import RestConfOpenConfigDriver
    DRIVERS.append(
        (RestConfOpenConfigDriver, [
            {
                FilterFieldEnum.DEVICE_TYPE: [
                    DeviceTypeEnum.CLIENT,
                    DeviceTypeEnum.DATACENTER,
                    DeviceTypeEnum.EMULATED_CLIENT,
                    DeviceTypeEnum.EMULATED_COMPUTER,
                    DeviceTypeEnum.EMULATED_DATACENTER,
                    DeviceTypeEnum.EMULATED_PACKET_FIREWALL,
                    DeviceTypeEnum.EMULATED_VIRTUAL_MACHINE,
                    DeviceTypeEnum.NETWORK,
                    DeviceTypeEnum.PACKET_FIREWALL,
                ],
                FilterFieldEnum.DRIVER : DeviceDriverEnum.DEVICEDRIVER_RESTCONF_OPENCONFIG,
            }
        ]))
