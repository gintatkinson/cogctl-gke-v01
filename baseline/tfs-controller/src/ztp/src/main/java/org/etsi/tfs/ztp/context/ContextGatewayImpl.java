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

package org.etsi.tfs.ztp.context;

import context.ContextOuterClass;
import context.MutinyContextServiceGrpc.MutinyContextServiceStub;
import io.quarkus.grpc.GrpcClient;
import io.smallrye.mutiny.Multi;
import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.etsi.tfs.ztp.Serializer;
import org.etsi.tfs.ztp.context.model.Device;
import org.etsi.tfs.ztp.context.model.DeviceEvent;

@ApplicationScoped
public class ContextGatewayImpl implements ContextGateway {

    @GrpcClient("context")
    MutinyContextServiceStub streamingDelegateContext;

    private final Serializer serializer;

    @Inject
    public ContextGatewayImpl(Serializer serializer) {
        this.serializer = serializer;
    }

    @Override
    public Multi<DeviceEvent> getDeviceEvents() {
        final var serializedEmpty = ContextOuterClass.Empty.newBuilder().build();

        return streamingDelegateContext
                .getDeviceEvents(serializedEmpty)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<Device> getDevice(String deviceId) {
        final var serializedDeviceId = serializer.serializeDeviceId(deviceId);

        return streamingDelegateContext
                .getDevice(serializedDeviceId)
                .onItem()
                .transform(serializer::deserialize);
    }
}
