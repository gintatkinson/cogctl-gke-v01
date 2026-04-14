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

package org.etsi.tfs.ztp;

import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.etsi.tfs.ztp.context.ContextService;
import org.etsi.tfs.ztp.context.model.Device;
import org.etsi.tfs.ztp.context.model.DeviceConfig;
import org.etsi.tfs.ztp.device.DeviceService;
import org.etsi.tfs.ztp.exception.ExternalServiceFailureException;
import org.jboss.logging.Logger;

@ApplicationScoped
public class ZtpServiceImpl implements ZtpService {
    private static final Logger LOGGER = Logger.getLogger(ZtpServiceImpl.class);

    private final DeviceService deviceService;
    private final ContextService contextService;

    @Inject
    public ZtpServiceImpl(DeviceService deviceService, ContextService contextService) {
        this.deviceService = deviceService;
        this.contextService = contextService;
    }

    @Override
    public Uni<Device> addDevice(String deviceId) {
        return contextService
                .getDevice(deviceId)
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transformToUni(
                        device -> {
                            if (device.isEnabled()) {
                                LOGGER.warnf("%s has already been enabled. Ignoring...", device);
                                return Uni.createFrom().failure(new Exception("Device is already enabled"));
                            } else {
                                return addDeviceTo(device, deviceId);
                            }
                        });
    }

    public Uni<Device> addDeviceTo(Device device, String deviceId) {
        LOGGER.infof("Enabling device with ID [%s]", deviceId);
        device.enableDevice();

        final Uni<DeviceConfig> initialConfiguration = deviceService.getInitialConfiguration(deviceId);

        return initialConfiguration
                .onItem()
                .transformToUni(
                        deviceConfig -> {
                            device.setDeviceConfiguration(deviceConfig);
                            LOGGER.infof(
                                    "Configuring device with ID [%s] with initial configuration %s",
                                    deviceId, deviceConfig);
                            return deviceService
                                    .configureDevice(device)
                                    .map(
                                            configuredDeviceId -> {
                                                LOGGER.infof(
                                                        "Device with ID [%s] has been successfully enabled and configured.",
                                                        deviceId);
                                                return device;
                                            });
                        });
    }

    @Override
    public Uni<Device> deleteDevice(String deviceId) {
        return contextService
                .getDevice(deviceId)
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transformToUni(
                        device -> {
                            if (device.isDisabled()) {
                                LOGGER.warnf("Device with ID %s has already been disabled. Ignoring...", deviceId);
                                return Uni.createFrom().nullItem();
                            } else {
                                LOGGER.infof("Disabling device with ID [%s]", deviceId);
                                device.disableDevice();

                                return deviceService
                                        .deleteDevice(deviceId)
                                        .onItem()
                                        .transform(
                                                emptyMessage -> {
                                                    LOGGER.infof(
                                                            "Device with ID [%s] has been successfully deleted.", deviceId);
                                                    return device;
                                                });
                            }
                        });
    }

    @Override
    public Uni<Device> updateDevice(String deviceId, DeviceConfig deviceConfig) {
        return contextService
                .getDevice(deviceId)
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transformToUni(
                        device -> {
                            if (!device.isEnabled()) {
                                LOGGER.warnf("Cannot update disabled device %s. Ignoring...", deviceId);
                                return Uni.createFrom().nullItem();
                            } else {
                                LOGGER.infof("Updating configuration of device with ID [%s]", deviceId);
                                device.setDeviceConfiguration(deviceConfig);

                                return deviceService
                                        .configureDevice(device)
                                        .onItem()
                                        .transform(
                                                configuredDeviceId -> {
                                                    LOGGER.infof(
                                                            "Device with ID [%s] has been successfully updated with %s.",
                                                            deviceId, deviceConfig);
                                                    return device;
                                                });
                            }
                        });
    }
}
