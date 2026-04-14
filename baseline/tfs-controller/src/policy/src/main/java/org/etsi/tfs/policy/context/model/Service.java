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
import org.etsi.tfs.policy.common.Util;

public class Service {

    private final ServiceId serviceId;
    private final ServiceTypeEnum serviceType;
    private final List<EndPointId> serviceEndPointIds;
    private final List<Constraint> serviceConstraints;
    private final ServiceStatus serviceStatus;
    private ServiceConfig serviceConfig;
    private final double timestamp;

    public Service(
            ServiceId serviceId,
            ServiceTypeEnum serviceType,
            List<EndPointId> serviceEndPointIds,
            List<Constraint> serviceConstraints,
            ServiceStatus serviceStatus,
            ServiceConfig serviceConfig,
            double timestamp) {
        this.serviceId = serviceId;
        this.serviceType = serviceType;
        this.serviceEndPointIds = serviceEndPointIds;
        this.serviceConstraints = serviceConstraints;
        this.serviceStatus = serviceStatus;
        this.serviceConfig = serviceConfig;
        this.timestamp = timestamp;
    }

    public ServiceId getServiceId() {
        return serviceId;
    }

    public ServiceTypeEnum getServiceType() {
        return serviceType;
    }

    public List<EndPointId> getServiceEndPointIds() {
        return serviceEndPointIds;
    }

    public List<Constraint> getServiceConstraints() {
        return serviceConstraints;
    }

    public void appendServiceConstraints(List<Constraint> serviceConstraints) {
        this.serviceConstraints.addAll(serviceConstraints);
    }

    public ServiceStatus getServiceStatus() {
        return serviceStatus;
    }

    public void setServiceConfig(ServiceConfig serviceConfig) {
        this.serviceConfig = serviceConfig;
    }

    public ServiceConfig getServiceConfig() {
        return serviceConfig;
    }

    public double getTimestamp() {
        return timestamp;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{%s, serviceType:\"%s\", [%s], [%s], %s, %s, timestamp:\"%f\"}",
                getClass().getSimpleName(),
                serviceId,
                serviceType.toString(),
                Util.toString(serviceEndPointIds),
                Util.toString(serviceConstraints),
                serviceStatus,
                serviceConfig,
                timestamp);
    }
}
