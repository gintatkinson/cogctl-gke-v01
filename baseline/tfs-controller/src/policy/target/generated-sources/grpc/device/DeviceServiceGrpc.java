package device;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.quarkus.grpc.common.Generated(value = "by gRPC proto compiler (version 1.55.1)", comments = "Source: device.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class DeviceServiceGrpc {

    private DeviceServiceGrpc() {
    }

    public static final String SERVICE_NAME = "device.DeviceService";

    // Static method descriptors that strictly reflect the proto.
    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getAddDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "AddDevice", requestType = context.ContextOuterClass.Device.class, responseType = context.ContextOuterClass.DeviceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getAddDeviceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getAddDeviceMethod;
        if ((getAddDeviceMethod = DeviceServiceGrpc.getAddDeviceMethod) == null) {
            synchronized (DeviceServiceGrpc.class) {
                if ((getAddDeviceMethod = DeviceServiceGrpc.getAddDeviceMethod) == null) {
                    DeviceServiceGrpc.getAddDeviceMethod = getAddDeviceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "AddDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Device.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceId.getDefaultInstance())).setSchemaDescriptor(new DeviceServiceMethodDescriptorSupplier("AddDevice")).build();
                }
            }
        }
        return getAddDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getConfigureDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ConfigureDevice", requestType = context.ContextOuterClass.Device.class, responseType = context.ContextOuterClass.DeviceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getConfigureDeviceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getConfigureDeviceMethod;
        if ((getConfigureDeviceMethod = DeviceServiceGrpc.getConfigureDeviceMethod) == null) {
            synchronized (DeviceServiceGrpc.class) {
                if ((getConfigureDeviceMethod = DeviceServiceGrpc.getConfigureDeviceMethod) == null) {
                    DeviceServiceGrpc.getConfigureDeviceMethod = getConfigureDeviceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ConfigureDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Device.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceId.getDefaultInstance())).setSchemaDescriptor(new DeviceServiceMethodDescriptorSupplier("ConfigureDevice")).build();
                }
            }
        }
        return getConfigureDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty> getDeleteDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteDevice", requestType = context.ContextOuterClass.DeviceId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty> getDeleteDeviceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty> getDeleteDeviceMethod;
        if ((getDeleteDeviceMethod = DeviceServiceGrpc.getDeleteDeviceMethod) == null) {
            synchronized (DeviceServiceGrpc.class) {
                if ((getDeleteDeviceMethod = DeviceServiceGrpc.getDeleteDeviceMethod) == null) {
                    DeviceServiceGrpc.getDeleteDeviceMethod = getDeleteDeviceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new DeviceServiceMethodDescriptorSupplier("DeleteDevice")).build();
                }
            }
        }
        return getDeleteDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.DeviceConfig> getGetInitialConfigMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetInitialConfig", requestType = context.ContextOuterClass.DeviceId.class, responseType = context.ContextOuterClass.DeviceConfig.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.DeviceConfig> getGetInitialConfigMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.DeviceConfig> getGetInitialConfigMethod;
        if ((getGetInitialConfigMethod = DeviceServiceGrpc.getGetInitialConfigMethod) == null) {
            synchronized (DeviceServiceGrpc.class) {
                if ((getGetInitialConfigMethod = DeviceServiceGrpc.getGetInitialConfigMethod) == null) {
                    DeviceServiceGrpc.getGetInitialConfigMethod = getGetInitialConfigMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.DeviceId, context.ContextOuterClass.DeviceConfig>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetInitialConfig")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceConfig.getDefaultInstance())).setSchemaDescriptor(new DeviceServiceMethodDescriptorSupplier("GetInitialConfig")).build();
                }
            }
        }
        return getGetInitialConfigMethod;
    }

    private static volatile io.grpc.MethodDescriptor<device.Device.MonitoringSettings, context.ContextOuterClass.Empty> getMonitorDeviceKpiMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "MonitorDeviceKpi", requestType = device.Device.MonitoringSettings.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<device.Device.MonitoringSettings, context.ContextOuterClass.Empty> getMonitorDeviceKpiMethod() {
        io.grpc.MethodDescriptor<device.Device.MonitoringSettings, context.ContextOuterClass.Empty> getMonitorDeviceKpiMethod;
        if ((getMonitorDeviceKpiMethod = DeviceServiceGrpc.getMonitorDeviceKpiMethod) == null) {
            synchronized (DeviceServiceGrpc.class) {
                if ((getMonitorDeviceKpiMethod = DeviceServiceGrpc.getMonitorDeviceKpiMethod) == null) {
                    DeviceServiceGrpc.getMonitorDeviceKpiMethod = getMonitorDeviceKpiMethod = io.grpc.MethodDescriptor.<device.Device.MonitoringSettings, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "MonitorDeviceKpi")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(device.Device.MonitoringSettings.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new DeviceServiceMethodDescriptorSupplier("MonitorDeviceKpi")).build();
                }
            }
        }
        return getMonitorDeviceKpiMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.SSEMonitoringSubscriptionConfig, monitoring.Monitoring.SSEMonitoringSubscriptionResponse> getSSETelemetrySubscribeMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SSETelemetrySubscribe", requestType = monitoring.Monitoring.SSEMonitoringSubscriptionConfig.class, responseType = monitoring.Monitoring.SSEMonitoringSubscriptionResponse.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.SSEMonitoringSubscriptionConfig, monitoring.Monitoring.SSEMonitoringSubscriptionResponse> getSSETelemetrySubscribeMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.SSEMonitoringSubscriptionConfig, monitoring.Monitoring.SSEMonitoringSubscriptionResponse> getSSETelemetrySubscribeMethod;
        if ((getSSETelemetrySubscribeMethod = DeviceServiceGrpc.getSSETelemetrySubscribeMethod) == null) {
            synchronized (DeviceServiceGrpc.class) {
                if ((getSSETelemetrySubscribeMethod = DeviceServiceGrpc.getSSETelemetrySubscribeMethod) == null) {
                    DeviceServiceGrpc.getSSETelemetrySubscribeMethod = getSSETelemetrySubscribeMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.SSEMonitoringSubscriptionConfig, monitoring.Monitoring.SSEMonitoringSubscriptionResponse>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SSETelemetrySubscribe")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.SSEMonitoringSubscriptionConfig.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.SSEMonitoringSubscriptionResponse.getDefaultInstance())).setSchemaDescriptor(new DeviceServiceMethodDescriptorSupplier("SSETelemetrySubscribe")).build();
                }
            }
        }
        return getSSETelemetrySubscribeMethod;
    }

    /**
     * Creates a new async stub that supports all call types for the service
     */
    public static DeviceServiceStub newStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<DeviceServiceStub> factory = new io.grpc.stub.AbstractStub.StubFactory<DeviceServiceStub>() {

            @java.lang.Override
            public DeviceServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new DeviceServiceStub(channel, callOptions);
            }
        };
        return DeviceServiceStub.newStub(factory, channel);
    }

    /**
     * Creates a new blocking-style stub that supports unary and streaming output calls on the service
     */
    public static DeviceServiceBlockingStub newBlockingStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<DeviceServiceBlockingStub> factory = new io.grpc.stub.AbstractStub.StubFactory<DeviceServiceBlockingStub>() {

            @java.lang.Override
            public DeviceServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new DeviceServiceBlockingStub(channel, callOptions);
            }
        };
        return DeviceServiceBlockingStub.newStub(factory, channel);
    }

    /**
     * Creates a new ListenableFuture-style stub that supports unary calls on the service
     */
    public static DeviceServiceFutureStub newFutureStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<DeviceServiceFutureStub> factory = new io.grpc.stub.AbstractStub.StubFactory<DeviceServiceFutureStub>() {

            @java.lang.Override
            public DeviceServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new DeviceServiceFutureStub(channel, callOptions);
            }
        };
        return DeviceServiceFutureStub.newStub(factory, channel);
    }

    /**
     */
    public interface AsyncService {

        /**
         */
        default void addDevice(context.ContextOuterClass.Device request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getAddDeviceMethod(), responseObserver);
        }

        /**
         */
        default void configureDevice(context.ContextOuterClass.Device request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getConfigureDeviceMethod(), responseObserver);
        }

        /**
         */
        default void deleteDevice(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteDeviceMethod(), responseObserver);
        }

        /**
         */
        default void getInitialConfig(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceConfig> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetInitialConfigMethod(), responseObserver);
        }

        /**
         */
        default void monitorDeviceKpi(device.Device.MonitoringSettings request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getMonitorDeviceKpiMethod(), responseObserver);
        }

        /**
         */
        default void sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request, io.grpc.stub.StreamObserver<monitoring.Monitoring.SSEMonitoringSubscriptionResponse> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSSETelemetrySubscribeMethod(), responseObserver);
        }
    }

    /**
     * Base class for the server implementation of the service DeviceService.
     */
    public static abstract class DeviceServiceImplBase implements io.grpc.BindableService, AsyncService {

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return DeviceServiceGrpc.bindService(this);
        }
    }

    /**
     * A stub to allow clients to do asynchronous rpc calls to service DeviceService.
     */
    public static class DeviceServiceStub extends io.grpc.stub.AbstractAsyncStub<DeviceServiceStub> {

        private DeviceServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected DeviceServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new DeviceServiceStub(channel, callOptions);
        }

        /**
         */
        public void addDevice(context.ContextOuterClass.Device request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getAddDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void configureDevice(context.ContextOuterClass.Device request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getConfigureDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteDevice(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getInitialConfig(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceConfig> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetInitialConfigMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void monitorDeviceKpi(device.Device.MonitoringSettings request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getMonitorDeviceKpiMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request, io.grpc.stub.StreamObserver<monitoring.Monitoring.SSEMonitoringSubscriptionResponse> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSSETelemetrySubscribeMethod(), getCallOptions()), request, responseObserver);
        }
    }

    /**
     * A stub to allow clients to do synchronous rpc calls to service DeviceService.
     */
    public static class DeviceServiceBlockingStub extends io.grpc.stub.AbstractBlockingStub<DeviceServiceBlockingStub> {

        private DeviceServiceBlockingStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected DeviceServiceBlockingStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new DeviceServiceBlockingStub(channel, callOptions);
        }

        /**
         */
        public context.ContextOuterClass.DeviceId addDevice(context.ContextOuterClass.Device request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getAddDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.DeviceId configureDevice(context.ContextOuterClass.Device request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getConfigureDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteDevice(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.DeviceConfig getInitialConfig(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetInitialConfigMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty monitorDeviceKpi(device.Device.MonitoringSettings request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getMonitorDeviceKpiMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.SSEMonitoringSubscriptionResponse sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSSETelemetrySubscribeMethod(), getCallOptions(), request);
        }
    }

    /**
     * A stub to allow clients to do ListenableFuture-style rpc calls to service DeviceService.
     */
    public static class DeviceServiceFutureStub extends io.grpc.stub.AbstractFutureStub<DeviceServiceFutureStub> {

        private DeviceServiceFutureStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected DeviceServiceFutureStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new DeviceServiceFutureStub(channel, callOptions);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.DeviceId> addDevice(context.ContextOuterClass.Device request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getAddDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.DeviceId> configureDevice(context.ContextOuterClass.Device request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getConfigureDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteDevice(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.DeviceConfig> getInitialConfig(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetInitialConfigMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> monitorDeviceKpi(device.Device.MonitoringSettings request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getMonitorDeviceKpiMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.SSEMonitoringSubscriptionResponse> sSETelemetrySubscribe(monitoring.Monitoring.SSEMonitoringSubscriptionConfig request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSSETelemetrySubscribeMethod(), getCallOptions()), request);
        }
    }

    private static final int METHODID_ADD_DEVICE = 0;

    private static final int METHODID_CONFIGURE_DEVICE = 1;

    private static final int METHODID_DELETE_DEVICE = 2;

    private static final int METHODID_GET_INITIAL_CONFIG = 3;

    private static final int METHODID_MONITOR_DEVICE_KPI = 4;

    private static final int METHODID_SSETELEMETRY_SUBSCRIBE = 5;

    private static final class MethodHandlers<Req, Resp> implements io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>, io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {

        private final AsyncService serviceImpl;

        private final int methodId;

        MethodHandlers(AsyncService serviceImpl, int methodId) {
            this.serviceImpl = serviceImpl;
            this.methodId = methodId;
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                case METHODID_ADD_DEVICE:
                    serviceImpl.addDevice((context.ContextOuterClass.Device) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId>) responseObserver);
                    break;
                case METHODID_CONFIGURE_DEVICE:
                    serviceImpl.configureDevice((context.ContextOuterClass.Device) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId>) responseObserver);
                    break;
                case METHODID_DELETE_DEVICE:
                    serviceImpl.deleteDevice((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_INITIAL_CONFIG:
                    serviceImpl.getInitialConfig((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceConfig>) responseObserver);
                    break;
                case METHODID_MONITOR_DEVICE_KPI:
                    serviceImpl.monitorDeviceKpi((device.Device.MonitoringSettings) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_SSETELEMETRY_SUBSCRIBE:
                    serviceImpl.sSETelemetrySubscribe((monitoring.Monitoring.SSEMonitoringSubscriptionConfig) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.SSEMonitoringSubscriptionResponse>) responseObserver);
                    break;
                default:
                    throw new AssertionError();
            }
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public io.grpc.stub.StreamObserver<Req> invoke(io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                default:
                    throw new AssertionError();
            }
        }
    }

    public static io.grpc.ServerServiceDefinition bindService(AsyncService service) {
        return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(getAddDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>(service, METHODID_ADD_DEVICE))).addMethod(getConfigureDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>(service, METHODID_CONFIGURE_DEVICE))).addMethod(getDeleteDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty>(service, METHODID_DELETE_DEVICE))).addMethod(getGetInitialConfigMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, context.ContextOuterClass.DeviceConfig>(service, METHODID_GET_INITIAL_CONFIG))).addMethod(getMonitorDeviceKpiMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<device.Device.MonitoringSettings, context.ContextOuterClass.Empty>(service, METHODID_MONITOR_DEVICE_KPI))).addMethod(getSSETelemetrySubscribeMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.SSEMonitoringSubscriptionConfig, monitoring.Monitoring.SSEMonitoringSubscriptionResponse>(service, METHODID_SSETELEMETRY_SUBSCRIBE))).build();
    }

    private static abstract class DeviceServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {

        DeviceServiceBaseDescriptorSupplier() {
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
            return device.Device.getDescriptor();
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
            return getFileDescriptor().findServiceByName("DeviceService");
        }
    }

    private static final class DeviceServiceFileDescriptorSupplier extends DeviceServiceBaseDescriptorSupplier {

        DeviceServiceFileDescriptorSupplier() {
        }
    }

    private static final class DeviceServiceMethodDescriptorSupplier extends DeviceServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {

        private final String methodName;

        DeviceServiceMethodDescriptorSupplier(String methodName) {
            this.methodName = methodName;
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
            return getServiceDescriptor().findMethodByName(methodName);
        }
    }

    private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

    public static io.grpc.ServiceDescriptor getServiceDescriptor() {
        io.grpc.ServiceDescriptor result = serviceDescriptor;
        if (result == null) {
            synchronized (DeviceServiceGrpc.class) {
                result = serviceDescriptor;
                if (result == null) {
                    serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME).setSchemaDescriptor(new DeviceServiceFileDescriptorSupplier()).addMethod(getAddDeviceMethod()).addMethod(getConfigureDeviceMethod()).addMethod(getDeleteDeviceMethod()).addMethod(getGetInitialConfigMethod()).addMethod(getMonitorDeviceKpiMethod()).addMethod(getSSETelemetrySubscribeMethod()).build();
                }
            }
        }
        return result;
    }
}
