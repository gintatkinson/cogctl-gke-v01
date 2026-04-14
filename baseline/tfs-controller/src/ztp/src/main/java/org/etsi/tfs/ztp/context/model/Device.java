/*
* Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

package org.etsi.tfs.ztp.context.model;

import java.util.List;
import org.etsi.tfs.ztp.common.Util;

public class Device {

    private final String deviceId;
    private final String deviceName;
    private final String deviceType;
    private DeviceConfig deviceConfig;
    private DeviceOperationalStatus deviceOperationalStatus;
    private List<DeviceDriverEnum> deviceDrivers;
    private List<EndPoint> endPoints;

    public Device(
            String deviceId,
            String deviceName,
            String deviceType,
            DeviceConfig deviceConfig,
            DeviceOperationalStatus deviceOperationalStatus,
            List<DeviceDriverEnum> deviceDrivers,
            List<EndPoint> endPoints) {

        this.deviceId = deviceId;
        this.deviceName = deviceName;
        this.deviceType = deviceType;
        this.deviceConfig = deviceConfig;
        this.deviceOperationalStatus = deviceOperationalStatus;
        this.deviceDrivers = deviceDrivers;
        this.endPoints = endPoints;
    }

    public Device(
            String deviceId,
            String deviceName,
            String deviceType,
            DeviceOperationalStatus deviceOperationalStatus,
            List<DeviceDriverEnum> deviceDrivers,
            List<EndPoint> endPoints) {
        this.deviceId = deviceId;
        this.deviceName = deviceName;
        this.deviceType = deviceType;
        this.deviceOperationalStatus = deviceOperationalStatus;
        this.deviceDrivers = deviceDrivers;
        this.endPoints = endPoints;
    }

    public boolean isEnabled() {
        return deviceOperationalStatus == DeviceOperationalStatus.ENABLED;
    }

    public boolean isDisabled() {
        return deviceOperationalStatus == DeviceOperationalStatus.DISABLED;
    }

    public void enableDevice() {
        this.deviceOperationalStatus = DeviceOperationalStatus.ENABLED;
    }

    public void disableDevice() {
        this.deviceOperationalStatus = DeviceOperationalStatus.DISABLED;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public String getDeviceName() {
        return deviceName;
    }

    public String getDeviceType() {
        return deviceType;
    }

    public DeviceConfig getDeviceConfig() {
        return deviceConfig;
    }

    public List<DeviceDriverEnum> getDeviceDrivers() {
        return deviceDrivers;
    }

    public List<EndPoint> getEndPoints() {
        return endPoints;
    }

    public DeviceOperationalStatus getDeviceOperationalStatus() {
        return deviceOperationalStatus;
    }

    public void setDeviceConfiguration(DeviceConfig deviceConfig) {
        this.deviceConfig = deviceConfig;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{deviceId:\"%s\", deviceName:\"%s\", deviceType:\"%s\", %s, deviceOperationalStatus=\"%s\", [%s], [%s]}",
                getClass().getSimpleName(),
                deviceId,
                deviceName,
                deviceType,
                deviceConfig,
                deviceOperationalStatus.toString(),
                Util.toString(deviceDrivers),
                Util.toString(endPoints));
    }
}
