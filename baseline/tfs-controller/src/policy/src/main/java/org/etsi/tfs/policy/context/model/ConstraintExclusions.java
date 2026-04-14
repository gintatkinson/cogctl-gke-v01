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

package org.etsi.tfs.policy.context.model;

import java.util.List;

public class ConstraintExclusions {

    private final boolean isPermanent;
    private final List<String> deviceIds;
    private final List<EndPointId> endpointIds;
    private final List<LinkId> linkIds;

    public ConstraintExclusions(
            boolean isPermanent,
            List<String> deviceIds,
            List<EndPointId> endpointIds,
            List<LinkId> linkIds) {
        this.isPermanent = isPermanent;
        this.deviceIds = deviceIds;
        this.endpointIds = endpointIds;
        this.linkIds = linkIds;
    }

    public boolean isPermanent() {
        return isPermanent;
    }

    public List<String> getDeviceIds() {
        return deviceIds;
    }

    public List<EndPointId> getEndpointIds() {
        return endpointIds;
    }

    public List<LinkId> getLinkIds() {
        return linkIds;
    }

    @Override
    public String toString() {
        return "ConstraintExclusions{"
                + "permanent="
                + isPermanent
                + ", deviceIds="
                + deviceIds
                + ", endpointIds="
                + endpointIds
                + ", linkIds="
                + linkIds
                + '}';
    }
}
