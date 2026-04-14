/*
* Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

package org.etsi.tfs.ztp;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import context.ContextOuterClass;
import io.quarkus.runtime.StartupEvent;
import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.junit.mockito.InjectMock;
import io.smallrye.mutiny.Multi;
import jakarta.inject.Inject;
import java.util.UUID;
import org.etsi.tfs.ztp.context.ContextGateway;
import org.etsi.tfs.ztp.context.model.DeviceEvent;
import org.etsi.tfs.ztp.context.model.Event;
import org.etsi.tfs.ztp.context.model.EventTypeEnum;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import ztp.Ztp;

@QuarkusTest
class ContextSubscriberTest {

    private static final String UUID_FOR_DEVICE_ROLE_ID =
            UUID.fromString("0f14d0ab-9608-7862-a9e4-5ed26688389b").toString();
    private static final String UUID_FOR_DEVICE_ID =
            UUID.fromString("9f14d0ab-9608-7862-a9e4-5ed26688389c").toString();

    @Inject ContextSubscriber contextSubscriber;

    @InjectMock ContextGateway contextGateway;

    @InjectMock ZtpService ztpService;

    @InjectMock ZtpConfiguration ztpConfiguration;

    @Test
    void shouldCallAddDeviceUponCreateEvent() {
        final var uuidForDeviceRoleId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ROLE_ID).build();

        final var uuidForDeviceId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ID).build();

        final var outDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(uuidForDeviceId).build();

        final var outDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(uuidForDeviceRoleId)
                        .setDevId(outDeviceId)
                        .build();

        String deviceId = outDeviceRoleId.getDevId().toString();

        Event event = new Event(3.4, EventTypeEnum.CREATE);
        DeviceEvent deviceEvent = new DeviceEvent(deviceId, event);
        final var deviceEventsMulti = Multi.createFrom().item(deviceEvent);

        Mockito.when(contextGateway.getDeviceEvents()).thenReturn(deviceEventsMulti);

        contextSubscriber.listenForDeviceEvents();

        verify(ztpService, times(0)).deleteDevice(deviceId);
        verify(ztpService, times(1)).addDevice(deviceId);
    }

    @Test
    void shouldNotCallAddDeviceUponUpdateEvent() {
        final var uuidForDeviceRoleId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ROLE_ID).build();

        final var uuidForDeviceId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ID).build();

        final var outDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(uuidForDeviceId).build();

        final var outDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(uuidForDeviceRoleId)
                        .setDevId(outDeviceId)
                        .build();

        String deviceId = outDeviceRoleId.getDevId().toString();

        Event event = new Event(3.4, EventTypeEnum.UPDATE);
        DeviceEvent deviceEvent = new DeviceEvent(deviceId, event);
        final var deviceEventsMulti = Multi.createFrom().item(deviceEvent);

        Mockito.when(contextGateway.getDeviceEvents()).thenReturn(deviceEventsMulti);

        contextSubscriber.listenForDeviceEvents();

        // verify(ztpService, times(0)).addDevice(deviceId);
    }

    @Test
    void shouldCallRemoveDeviceUponRemoveEvent() {
        final var uuidForDeviceRoleId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ROLE_ID).build();

        final var uuidForDeviceId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ID).build();

        final var outDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(uuidForDeviceId).build();

        final var outDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(uuidForDeviceRoleId)
                        .setDevId(outDeviceId)
                        .build();

        String deviceId = outDeviceRoleId.getDevId().toString();

        Event event = new Event(3.4, EventTypeEnum.REMOVE);
        DeviceEvent deviceEvent = new DeviceEvent(deviceId, event);
        final var deviceEventsMulti = Multi.createFrom().item(deviceEvent);

        Mockito.when(contextGateway.getDeviceEvents()).thenReturn(deviceEventsMulti);

        contextSubscriber.listenForDeviceEvents();

        verify(ztpService, times(0)).addDevice(deviceId);
        verify(ztpService, times(1)).deleteDevice(deviceId);
    }

    @Test
    void shouldNotCallAddDeviceUponNullEvent() {
        final var uuidForDeviceRoleId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ROLE_ID).build();

        final var uuidForDeviceId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ID).build();

        final var outDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(uuidForDeviceId).build();

        final var outDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(uuidForDeviceRoleId)
                        .setDevId(outDeviceId)
                        .build();

        String deviceId = outDeviceRoleId.getDevId().toString();

        DeviceEvent deviceEvent = new DeviceEvent(deviceId, null);
        final var deviceEventsMulti = Multi.createFrom().item(deviceEvent);

        Mockito.when(contextGateway.getDeviceEvents()).thenReturn(deviceEventsMulti);

        contextSubscriber.listenForDeviceEvents();

        verify(ztpService, times(0)).addDevice(deviceId);
    }

    @Test
    void shouldCallListenForDeviceEventsUponStart() {
        final var uuidForDeviceRoleId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ROLE_ID).build();

        final var uuidForDeviceId =
                ContextOuterClass.Uuid.newBuilder().setUuid(UUID_FOR_DEVICE_ID).build();

        final var outDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(uuidForDeviceId).build();

        final var outDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(uuidForDeviceRoleId)
                        .setDevId(outDeviceId)
                        .build();

        String deviceId = outDeviceRoleId.getDevId().toString();

        Event event = new Event(3.4, EventTypeEnum.CREATE);
        DeviceEvent deviceEvent = new DeviceEvent(deviceId, event);
        final var deviceEventsMulti = Multi.createFrom().item(deviceEvent);

        Mockito.when(contextGateway.getDeviceEvents()).thenReturn(deviceEventsMulti);
        Mockito.when(ztpConfiguration.shouldSubscribeToContextComponent()).thenReturn(true);

        StartupEvent y = new StartupEvent();
        contextSubscriber.onStart(y);

        verify(contextGateway, times(1)).getDeviceEvents();
        verify(ztpService, times(1)).addDevice(deviceId);
    }

    @Test
    void shouldNotCallListenForDeviceEventsUponStart() {
        final var ztpConfiguration = Mockito.mock(ZtpConfiguration.class);
        Mockito.when(ztpConfiguration.shouldSubscribeToContextComponent()).thenReturn(false);

        StartupEvent y = new StartupEvent();
        contextSubscriber.onStart(y);

        verify(contextGateway, times(0)).getDeviceEvents();
    }
}
