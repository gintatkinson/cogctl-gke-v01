package device;

import java.util.function.BiFunction;
import io.quarkus.grpc.MutinyClient;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: device.proto")
public class DeviceServiceClient implements DeviceService, MutinyClient<MutinyDeviceServiceGrpc.MutinyDeviceServiceStub> {

    private final MutinyDeviceServiceGrpc.MutinyDeviceServiceStub stub;

    public DeviceServiceClient(String name, io.grpc.Channel channel, BiFunction<String, MutinyDeviceServiceGrpc.MutinyDeviceServiceStub, MutinyDeviceServiceGrpc.MutinyDeviceServiceStub> stubConfigurator) {
        this.stub = stubConfigurator.apply(name, MutinyDeviceServiceGrpc.newMutinyStub(channel));
    }

    private DeviceServiceClient(MutinyDeviceServiceGrpc.MutinyDeviceServiceStub stub) {
        this.stub = stub;
    }

    public DeviceServiceClient newInstanceWithStub(MutinyDeviceServiceGrpc.MutinyDeviceServiceStub stub) {
        return new DeviceServiceClient(stub);
    }

    @Override
    public MutinyDeviceServiceGrpc.MutinyDeviceServiceStub getStub() {
        return stub;
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> addDevice(context.ContextOuterClass.Device request) {
        return stub.addDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> configureDevice(context.ContextOuterClass.Device request) {
        return stub.configureDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteDevice(context.ContextOuterClass.DeviceId request) {
        return stub.deleteDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceConfig> getInitialConfig(context.ContextOuterClass.DeviceId request) {
        return stub.getInitialConfig(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorDeviceKpi(device.Device.MonitoringSettings request) {
        return stub.monitorDeviceKpi(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.SSEMonitoringSubscriptionResponse> sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request) {
        return stub.sSETelemetrySubscribe(request);
    }
}
