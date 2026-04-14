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

import java.util.Optional;

public class DeviceEvent {

    private final Event event;
    private final String deviceId;
    private final Optional<DeviceConfig> deviceConfig;

    public DeviceEvent(String deviceId, Event event) {
        this(deviceId, event, null);
    }

    public DeviceEvent(String deviceId, Event event, DeviceConfig deviceConfig) {
        this.event = event;
        this.deviceId = deviceId;
        this.deviceConfig =
                (deviceConfig == null) ? Optional.empty() : Optional.ofNullable(deviceConfig);
    }

    public Event getEvent() {
        return event;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public Optional<DeviceConfig> getDeviceConfig() {
        return deviceConfig;
    }

    @Override
    public String toString() {
        return String.format(
                "%s[%s, %s, %s]",
                getClass().getSimpleName(), deviceId, event.toString(), deviceConfig.orElse(null));
    }
}
