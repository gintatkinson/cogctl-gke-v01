package device;

import io.quarkus.grpc.MutinyService;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: device.proto")
public interface DeviceService extends MutinyService {

    io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> addDevice(context.ContextOuterClass.Device request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> configureDevice(context.ContextOuterClass.Device request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteDevice(context.ContextOuterClass.DeviceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceConfig> getInitialConfig(context.ContextOuterClass.DeviceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorDeviceKpi(device.Device.MonitoringSettings request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.SSEMonitoringSubscriptionResponse> sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request);
}
