package device;

import io.grpc.BindableService;
import io.quarkus.grpc.GrpcService;
import io.quarkus.grpc.MutinyBean;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: device.proto")
public class DeviceServiceBean extends MutinyDeviceServiceGrpc.DeviceServiceImplBase implements BindableService, MutinyBean {

    private final DeviceService delegate;

    DeviceServiceBean(@GrpcService DeviceService delegate) {
        this.delegate = delegate;
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> addDevice(context.ContextOuterClass.Device request) {
        try {
            return delegate.addDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> configureDevice(context.ContextOuterClass.Device request) {
        try {
            return delegate.configureDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteDevice(context.ContextOuterClass.DeviceId request) {
        try {
            return delegate.deleteDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceConfig> getInitialConfig(context.ContextOuterClass.DeviceId request) {
        try {
            return delegate.getInitialConfig(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorDeviceKpi(device.Device.MonitoringSettings request) {
        try {
            return delegate.monitorDeviceKpi(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.SSEMonitoringSubscriptionResponse> sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request) {
        try {
            return delegate.sSETelemetrySubscribe(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }
}
