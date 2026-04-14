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

import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import jakarta.inject.Inject;
import java.time.Duration;
import org.etsi.tfs.ztp.context.ContextService;
import org.etsi.tfs.ztp.context.model.Event;
import org.etsi.tfs.ztp.context.model.EventTypeEnum;
import org.jboss.logging.Logger;

@ApplicationScoped
public class ContextSubscriber {

    private static final Logger LOGGER = Logger.getLogger(ContextSubscriber.class);

    private final ContextService contextService;
    private final ZtpService ztpService;
    private final ZtpConfiguration ztpConfiguration;

    @Inject
    public ContextSubscriber(
            ContextService contextService, ZtpService ztpService, ZtpConfiguration ztpConfiguration) {
        this.contextService = contextService;
        this.ztpService = ztpService;
        this.ztpConfiguration = ztpConfiguration;
    }

    public void listenForDeviceEvents() {

        contextService
                .getDeviceEvents()
                .onFailure()
                .retry()
                .withBackOff(Duration.ofSeconds(1))
                .withJitter(0.2)
                .atMost(10)
                .onFailure()
                .recoverWithCompletion()
                .subscribe()
                .with(
                        deviceEvent -> {
                            LOGGER.debugf("Received %s via contextService:getDeviceEvents", deviceEvent);
                            if (deviceEvent == null || deviceEvent.getEvent() == null) {
                                LOGGER.warn("Received device event is null, ignoring...");
                                return;
                            }
                            final var eventType = deviceEvent.getEvent().getEventTypeEnum();
                            final var deviceId = deviceEvent.getDeviceId();
                            final var event = deviceEvent.getEvent();

                            switch (eventType) {
                                case CREATE:
                                    LOGGER.infof("Received %s for device [%s]", event, deviceId);
                                    ztpService.addDevice(deviceEvent.getDeviceId());
                                    break;
                                case REMOVE:
                                    LOGGER.infof("Received %s for device [%s]", event, deviceId);
                                    ztpService.deleteDevice(deviceEvent.getDeviceId());
                                    break;
                                case UPDATE:
                                    LOGGER.warnf(
                                            "Received %s for device [%s]. "
                                                    + "No ztp action on an already updated device",
                                            event, deviceId);
                                    break;
                                case UNDEFINED:
                                    logWarningMessage(event, deviceId, eventType);
                                    break;
                            }
                        });
    }

    void onStart(@Observes StartupEvent ev) {

        if (ztpConfiguration.shouldSubscribeToContextComponent()) {
            LOGGER.info("Subscribing to Context service for device events...");
            listenForDeviceEvents();
        } else {
            LOGGER.info("Not subscribing to Context service for device events...");
        }
    }

    private void logWarningMessage(Event event, String deviceId, EventTypeEnum eventType) {
        LOGGER.warnf(
                "Received %s for device [%s]. [%s] event handling is not yet implemented, ignoring...",
                event, deviceId, eventType);
    }
}
