package device;

import static device.DeviceServiceGrpc.getServiceDescriptor;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: device.proto")
public final class MutinyDeviceServiceGrpc implements io.quarkus.grpc.MutinyGrpc {

    private MutinyDeviceServiceGrpc() {
    }

    public static MutinyDeviceServiceStub newMutinyStub(io.grpc.Channel channel) {
        return new MutinyDeviceServiceStub(channel);
    }

    public static class MutinyDeviceServiceStub extends io.grpc.stub.AbstractStub<MutinyDeviceServiceStub> implements io.quarkus.grpc.MutinyStub {

        private DeviceServiceGrpc.DeviceServiceStub delegateStub;

        private MutinyDeviceServiceStub(io.grpc.Channel channel) {
            super(channel);
            delegateStub = DeviceServiceGrpc.newStub(channel);
        }

        private MutinyDeviceServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
            delegateStub = DeviceServiceGrpc.newStub(channel).build(channel, callOptions);
        }

        @Override
        protected MutinyDeviceServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MutinyDeviceServiceStub(channel, callOptions);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> addDevice(context.ContextOuterClass.Device request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::addDevice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> configureDevice(context.ContextOuterClass.Device request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::configureDevice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteDevice(context.ContextOuterClass.DeviceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteDevice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceConfig> getInitialConfig(context.ContextOuterClass.DeviceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getInitialConfig);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorDeviceKpi(device.Device.MonitoringSettings request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::monitorDeviceKpi);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.SSEMonitoringSubscriptionResponse> sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::sSETelemetrySubscribe);
        }
    }

    public static abstract class DeviceServiceImplBase implements io.grpc.BindableService {

        private String compression;

        /**
         * Set whether the server will try to use a compressed response.
         *
         * @param compression the compression, e.g {@code gzip}
         */
        public DeviceServiceImplBase withCompression(String compression) {
            this.compression = compression;
            return this;
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> addDevice(context.ContextOuterClass.Device request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> configureDevice(context.ContextOuterClass.Device request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteDevice(context.ContextOuterClass.DeviceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceConfig> getInitialConfig(context.ContextOuterClass.DeviceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorDeviceKpi(device.Device.MonitoringSettings request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.SSEMonitoringSubscriptionResponse> sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(device.DeviceServiceGrpc.getAddDeviceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>(this, METHODID_ADD_DEVICE, compression))).addMethod(device.DeviceServiceGrpc.getConfigureDeviceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>(this, METHODID_CONFIGURE_DEVICE, compression))).addMethod(device.DeviceServiceGrpc.getDeleteDeviceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty>(this, METHODID_DELETE_DEVICE, compression))).addMethod(device.DeviceServiceGrpc.getGetInitialConfigMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, context.ContextOuterClass.DeviceConfig>(this, METHODID_GET_INITIAL_CONFIG, compression))).addMethod(device.DeviceServiceGrpc.getMonitorDeviceKpiMethod(), asyncUnaryCall(new MethodHandlers<device.Device.MonitoringSettings, context.ContextOuterClass.Empty>(this, METHODID_MONITOR_DEVICE_KPI, compression))).addMethod(device.DeviceServiceGrpc.getSSETelemetrySubscribeMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.SSEMonitoringSubscriptionConfig, monitoring.Monitoring.SSEMonitoringSubscriptionResponse>(this, METHODID_S_SETELEMETRY_SUBSCRIBE, compression))).build();
        }
    }

    private static final int METHODID_ADD_DEVICE = 0;

    private static final int METHODID_CONFIGURE_DEVICE = 1;

    private static final int METHODID_DELETE_DEVICE = 2;

    private static final int METHODID_GET_INITIAL_CONFIG = 3;

    private static final int METHODID_MONITOR_DEVICE_KPI = 4;

    private static final int METHODID_S_SETELEMETRY_SUBSCRIBE = 5;

    private static final class MethodHandlers<Req, Resp> implements io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>, io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {

        private final DeviceServiceImplBase serviceImpl;

        private final int methodId;

        private final String compression;

        MethodHandlers(DeviceServiceImplBase serviceImpl, int methodId, String compression) {
            this.serviceImpl = serviceImpl;
            this.methodId = methodId;
            this.compression = compression;
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                case METHODID_ADD_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Device) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId>) responseObserver, compression, serviceImpl::addDevice);
                    break;
                case METHODID_CONFIGURE_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Device) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId>) responseObserver, compression, serviceImpl::configureDevice);
                    break;
                case METHODID_DELETE_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteDevice);
                    break;
                case METHODID_GET_INITIAL_CONFIG:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceConfig>) responseObserver, compression, serviceImpl::getInitialConfig);
                    break;
                case METHODID_MONITOR_DEVICE_KPI:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((device.Device.MonitoringSettings) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::monitorDeviceKpi);
                    break;
                case METHODID_S_SETELEMETRY_SUBSCRIBE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.SSEMonitoringSubscriptionConfig) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.SSEMonitoringSubscriptionResponse>) responseObserver, compression, serviceImpl::sSETelemetrySubscribe);
                    break;
                default:
                    throw new java.lang.AssertionError();
            }
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public io.grpc.stub.StreamObserver<Req> invoke(io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                default:
                    throw new java.lang.AssertionError();
            }
        }
    }
}
