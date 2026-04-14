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

from common.DeviceTypes           import DeviceTypeEnum
from common.proto.context_pb2     import DeviceDriverEnum
from telemetry.backend.Config     import LOAD_ALL_DEVICE_DRIVERS
from ..collector_api.FilterFields import FilterFieldEnum

COLLECTORS = []

from .emulated.EmulatedCollector import EmulatedCollector # pylint: disable=wrong-import-position
COLLECTORS.append(
    (EmulatedCollector, [
        # TODO: multi-filter is not working
        {
            FilterFieldEnum.DEVICE_TYPE: [
                DeviceTypeEnum.EMULATED_PACKET_ROUTER,
                DeviceTypeEnum.EMULATED_PACKET_SWITCH,
            ],
            FilterFieldEnum.DRIVER: [
                DeviceDriverEnum.DEVICEDRIVER_UNDEFINED,
            ],
        },
    ]))

# TODO: Import for gNMI OpenConfig Collector ...

if LOAD_ALL_DEVICE_DRIVERS:
    from .gnmi_oc.GnmiOpenConfigCollector import GNMIOpenConfigCollector # pylint: disable=wrong-import-position
    COLLECTORS.append(
        (GNMIOpenConfigCollector, [
            {
                # Real Packet Router, specifying GNMI Driver => use GnmiDriver
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.PACKET_ROUTER,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_GNMI_OPENCONFIG,
            }
        ])
    )

if LOAD_ALL_DEVICE_DRIVERS:
    from .intcollector.INTCollector import INTCollector # pylint: disable=wrong-import-position
    COLLECTORS.append(
        (INTCollector, [
            {
                FilterFieldEnum.DEVICE_TYPE: DeviceTypeEnum.P4_SWITCH,
                FilterFieldEnum.DRIVER     : DeviceDriverEnum.DEVICEDRIVER_P4,
            }
        ])
    )
