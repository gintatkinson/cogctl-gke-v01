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

package org.etsi.tfs.ztp.model;

public class DeviceRoleId {

    private final String id;
    private final String deviceId;

    public DeviceRoleId(String id, String deviceId) {
        this.id = id;
        this.deviceId = deviceId;
    }

    public String getId() {
        return id;
    }

    public String getDeviceId() {
        return deviceId;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{id:\"%s\", deviceId:\"%s\"}", getClass().getSimpleName(), id, deviceId);
    }
}
