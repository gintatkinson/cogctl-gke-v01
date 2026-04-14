package ztp;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.quarkus.grpc.common.Generated(value = "by gRPC proto compiler (version 1.55.1)", comments = "Source: ztp.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class ZtpServiceGrpc {

    private ZtpServiceGrpc() {
    }

    public static final String SERVICE_NAME = "ztp.ZtpService";

    // Static method descriptors that strictly reflect the proto.
    private static volatile io.grpc.MethodDescriptor<ztp.Ztp.DeviceRoleId, ztp.Ztp.DeviceRole> getZtpGetDeviceRoleMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ZtpGetDeviceRole", requestType = ztp.Ztp.DeviceRoleId.class, responseType = ztp.Ztp.DeviceRole.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<ztp.Ztp.DeviceRoleId, ztp.Ztp.DeviceRole> getZtpGetDeviceRoleMethod() {
        io.grpc.MethodDescriptor<ztp.Ztp.DeviceRoleId, ztp.Ztp.DeviceRole> getZtpGetDeviceRoleMethod;
        if ((getZtpGetDeviceRoleMethod = ZtpServiceGrpc.getZtpGetDeviceRoleMethod) == null) {
            synchronized (ZtpServiceGrpc.class) {
                if ((getZtpGetDeviceRoleMethod = ZtpServiceGrpc.getZtpGetDeviceRoleMethod) == null) {
                    ZtpServiceGrpc.getZtpGetDeviceRoleMethod = getZtpGetDeviceRoleMethod = io.grpc.MethodDescriptor.<ztp.Ztp.DeviceRoleId, ztp.Ztp.DeviceRole>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ZtpGetDeviceRole")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRoleId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRole.getDefaultInstance())).setSchemaDescriptor(new ZtpServiceMethodDescriptorSupplier("ZtpGetDeviceRole")).build();
                }
            }
        }
        return getZtpGetDeviceRoleMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, ztp.Ztp.DeviceRoleList> getZtpGetDeviceRolesByDeviceIdMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ZtpGetDeviceRolesByDeviceId", requestType = context.ContextOuterClass.DeviceId.class, responseType = ztp.Ztp.DeviceRoleList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, ztp.Ztp.DeviceRoleList> getZtpGetDeviceRolesByDeviceIdMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, ztp.Ztp.DeviceRoleList> getZtpGetDeviceRolesByDeviceIdMethod;
        if ((getZtpGetDeviceRolesByDeviceIdMethod = ZtpServiceGrpc.getZtpGetDeviceRolesByDeviceIdMethod) == null) {
            synchronized (ZtpServiceGrpc.class) {
                if ((getZtpGetDeviceRolesByDeviceIdMethod = ZtpServiceGrpc.getZtpGetDeviceRolesByDeviceIdMethod) == null) {
                    ZtpServiceGrpc.getZtpGetDeviceRolesByDeviceIdMethod = getZtpGetDeviceRolesByDeviceIdMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.DeviceId, ztp.Ztp.DeviceRoleList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ZtpGetDeviceRolesByDeviceId")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRoleList.getDefaultInstance())).setSchemaDescriptor(new ZtpServiceMethodDescriptorSupplier("ZtpGetDeviceRolesByDeviceId")).build();
                }
            }
        }
        return getZtpGetDeviceRolesByDeviceIdMethod;
    }

    private static volatile io.grpc.MethodDescriptor<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState> getZtpAddMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ZtpAdd", requestType = ztp.Ztp.DeviceRole.class, responseType = ztp.Ztp.DeviceRoleState.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState> getZtpAddMethod() {
        io.grpc.MethodDescriptor<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState> getZtpAddMethod;
        if ((getZtpAddMethod = ZtpServiceGrpc.getZtpAddMethod) == null) {
            synchronized (ZtpServiceGrpc.class) {
                if ((getZtpAddMethod = ZtpServiceGrpc.getZtpAddMethod) == null) {
                    ZtpServiceGrpc.getZtpAddMethod = getZtpAddMethod = io.grpc.MethodDescriptor.<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ZtpAdd")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRole.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRoleState.getDefaultInstance())).setSchemaDescriptor(new ZtpServiceMethodDescriptorSupplier("ZtpAdd")).build();
                }
            }
        }
        return getZtpAddMethod;
    }

    private static volatile io.grpc.MethodDescriptor<ztp.Ztp.DeviceRoleConfig, ztp.Ztp.DeviceRoleState> getZtpUpdateMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ZtpUpdate", requestType = ztp.Ztp.DeviceRoleConfig.class, responseType = ztp.Ztp.DeviceRoleState.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<ztp.Ztp.DeviceRoleConfig, ztp.Ztp.DeviceRoleState> getZtpUpdateMethod() {
        io.grpc.MethodDescriptor<ztp.Ztp.DeviceRoleConfig, ztp.Ztp.DeviceRoleState> getZtpUpdateMethod;
        if ((getZtpUpdateMethod = ZtpServiceGrpc.getZtpUpdateMethod) == null) {
            synchronized (ZtpServiceGrpc.class) {
                if ((getZtpUpdateMethod = ZtpServiceGrpc.getZtpUpdateMethod) == null) {
                    ZtpServiceGrpc.getZtpUpdateMethod = getZtpUpdateMethod = io.grpc.MethodDescriptor.<ztp.Ztp.DeviceRoleConfig, ztp.Ztp.DeviceRoleState>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ZtpUpdate")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRoleConfig.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRoleState.getDefaultInstance())).setSchemaDescriptor(new ZtpServiceMethodDescriptorSupplier("ZtpUpdate")).build();
                }
            }
        }
        return getZtpUpdateMethod;
    }

    private static volatile io.grpc.MethodDescriptor<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState> getZtpDeleteMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ZtpDelete", requestType = ztp.Ztp.DeviceRole.class, responseType = ztp.Ztp.DeviceRoleState.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState> getZtpDeleteMethod() {
        io.grpc.MethodDescriptor<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState> getZtpDeleteMethod;
        if ((getZtpDeleteMethod = ZtpServiceGrpc.getZtpDeleteMethod) == null) {
            synchronized (ZtpServiceGrpc.class) {
                if ((getZtpDeleteMethod = ZtpServiceGrpc.getZtpDeleteMethod) == null) {
                    ZtpServiceGrpc.getZtpDeleteMethod = getZtpDeleteMethod = io.grpc.MethodDescriptor.<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ZtpDelete")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRole.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceRoleState.getDefaultInstance())).setSchemaDescriptor(new ZtpServiceMethodDescriptorSupplier("ZtpDelete")).build();
                }
            }
        }
        return getZtpDeleteMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, ztp.Ztp.DeviceDeletionResult> getZtpDeleteAllMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ZtpDeleteAll", requestType = context.ContextOuterClass.Empty.class, responseType = ztp.Ztp.DeviceDeletionResult.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, ztp.Ztp.DeviceDeletionResult> getZtpDeleteAllMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, ztp.Ztp.DeviceDeletionResult> getZtpDeleteAllMethod;
        if ((getZtpDeleteAllMethod = ZtpServiceGrpc.getZtpDeleteAllMethod) == null) {
            synchronized (ZtpServiceGrpc.class) {
                if ((getZtpDeleteAllMethod = ZtpServiceGrpc.getZtpDeleteAllMethod) == null) {
                    ZtpServiceGrpc.getZtpDeleteAllMethod = getZtpDeleteAllMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, ztp.Ztp.DeviceDeletionResult>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ZtpDeleteAll")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(ztp.Ztp.DeviceDeletionResult.getDefaultInstance())).setSchemaDescriptor(new ZtpServiceMethodDescriptorSupplier("ZtpDeleteAll")).build();
                }
            }
        }
        return getZtpDeleteAllMethod;
    }

    /**
     * Creates a new async stub that supports all call types for the service
     */
    public static ZtpServiceStub newStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ZtpServiceStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ZtpServiceStub>() {

            @java.lang.Override
            public ZtpServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ZtpServiceStub(channel, callOptions);
            }
        };
        return ZtpServiceStub.newStub(factory, channel);
    }

    /**
     * Creates a new blocking-style stub that supports unary and streaming output calls on the service
     */
    public static ZtpServiceBlockingStub newBlockingStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ZtpServiceBlockingStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ZtpServiceBlockingStub>() {

            @java.lang.Override
            public ZtpServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ZtpServiceBlockingStub(channel, callOptions);
            }
        };
        return ZtpServiceBlockingStub.newStub(factory, channel);
    }

    /**
     * Creates a new ListenableFuture-style stub that supports unary calls on the service
     */
    public static ZtpServiceFutureStub newFutureStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ZtpServiceFutureStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ZtpServiceFutureStub>() {

            @java.lang.Override
            public ZtpServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ZtpServiceFutureStub(channel, callOptions);
            }
        };
        return ZtpServiceFutureStub.newStub(factory, channel);
    }

    /**
     */
    public interface AsyncService {

        /**
         */
        default void ztpGetDeviceRole(ztp.Ztp.DeviceRoleId request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRole> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getZtpGetDeviceRoleMethod(), responseObserver);
        }

        /**
         */
        default void ztpGetDeviceRolesByDeviceId(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getZtpGetDeviceRolesByDeviceIdMethod(), responseObserver);
        }

        /**
         */
        default void ztpAdd(ztp.Ztp.DeviceRole request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getZtpAddMethod(), responseObserver);
        }

        /**
         */
        default void ztpUpdate(ztp.Ztp.DeviceRoleConfig request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getZtpUpdateMethod(), responseObserver);
        }

        /**
         */
        default void ztpDelete(ztp.Ztp.DeviceRole request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getZtpDeleteMethod(), responseObserver);
        }

        /**
         */
        default void ztpDeleteAll(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceDeletionResult> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getZtpDeleteAllMethod(), responseObserver);
        }
    }

    /**
     * Base class for the server implementation of the service ZtpService.
     */
    public static abstract class ZtpServiceImplBase implements io.grpc.BindableService, AsyncService {

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return ZtpServiceGrpc.bindService(this);
        }
    }

    /**
     * A stub to allow clients to do asynchronous rpc calls to service ZtpService.
     */
    public static class ZtpServiceStub extends io.grpc.stub.AbstractAsyncStub<ZtpServiceStub> {

        private ZtpServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ZtpServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ZtpServiceStub(channel, callOptions);
        }

        /**
         */
        public void ztpGetDeviceRole(ztp.Ztp.DeviceRoleId request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRole> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getZtpGetDeviceRoleMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void ztpGetDeviceRolesByDeviceId(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getZtpGetDeviceRolesByDeviceIdMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void ztpAdd(ztp.Ztp.DeviceRole request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getZtpAddMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void ztpUpdate(ztp.Ztp.DeviceRoleConfig request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getZtpUpdateMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void ztpDelete(ztp.Ztp.DeviceRole request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getZtpDeleteMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void ztpDeleteAll(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<ztp.Ztp.DeviceDeletionResult> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getZtpDeleteAllMethod(), getCallOptions()), request, responseObserver);
        }
    }

    /**
     * A stub to allow clients to do synchronous rpc calls to service ZtpService.
     */
    public static class ZtpServiceBlockingStub extends io.grpc.stub.AbstractBlockingStub<ZtpServiceBlockingStub> {

        private ZtpServiceBlockingStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ZtpServiceBlockingStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ZtpServiceBlockingStub(channel, callOptions);
        }

        /**
         */
        public ztp.Ztp.DeviceRole ztpGetDeviceRole(ztp.Ztp.DeviceRoleId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getZtpGetDeviceRoleMethod(), getCallOptions(), request);
        }

        /**
         */
        public ztp.Ztp.DeviceRoleList ztpGetDeviceRolesByDeviceId(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getZtpGetDeviceRolesByDeviceIdMethod(), getCallOptions(), request);
        }

        /**
         */
        public ztp.Ztp.DeviceRoleState ztpAdd(ztp.Ztp.DeviceRole request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getZtpAddMethod(), getCallOptions(), request);
        }

        /**
         */
        public ztp.Ztp.DeviceRoleState ztpUpdate(ztp.Ztp.DeviceRoleConfig request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getZtpUpdateMethod(), getCallOptions(), request);
        }

        /**
         */
        public ztp.Ztp.DeviceRoleState ztpDelete(ztp.Ztp.DeviceRole request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getZtpDeleteMethod(), getCallOptions(), request);
        }

        /**
         */
        public ztp.Ztp.DeviceDeletionResult ztpDeleteAll(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getZtpDeleteAllMethod(), getCallOptions(), request);
        }
    }

    /**
     * A stub to allow clients to do ListenableFuture-style rpc calls to service ZtpService.
     */
    public static class ZtpServiceFutureStub extends io.grpc.stub.AbstractFutureStub<ZtpServiceFutureStub> {

        private ZtpServiceFutureStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ZtpServiceFutureStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ZtpServiceFutureStub(channel, callOptions);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<ztp.Ztp.DeviceRole> ztpGetDeviceRole(ztp.Ztp.DeviceRoleId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getZtpGetDeviceRoleMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<ztp.Ztp.DeviceRoleList> ztpGetDeviceRolesByDeviceId(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getZtpGetDeviceRolesByDeviceIdMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<ztp.Ztp.DeviceRoleState> ztpAdd(ztp.Ztp.DeviceRole request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getZtpAddMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<ztp.Ztp.DeviceRoleState> ztpUpdate(ztp.Ztp.DeviceRoleConfig request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getZtpUpdateMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<ztp.Ztp.DeviceRoleState> ztpDelete(ztp.Ztp.DeviceRole request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getZtpDeleteMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<ztp.Ztp.DeviceDeletionResult> ztpDeleteAll(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getZtpDeleteAllMethod(), getCallOptions()), request);
        }
    }

    private static final int METHODID_ZTP_GET_DEVICE_ROLE = 0;

    private static final int METHODID_ZTP_GET_DEVICE_ROLES_BY_DEVICE_ID = 1;

    private static final int METHODID_ZTP_ADD = 2;

    private static final int METHODID_ZTP_UPDATE = 3;

    private static final int METHODID_ZTP_DELETE = 4;

    private static final int METHODID_ZTP_DELETE_ALL = 5;

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
                case METHODID_ZTP_GET_DEVICE_ROLE:
                    serviceImpl.ztpGetDeviceRole((ztp.Ztp.DeviceRoleId) request, (io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRole>) responseObserver);
                    break;
                case METHODID_ZTP_GET_DEVICE_ROLES_BY_DEVICE_ID:
                    serviceImpl.ztpGetDeviceRolesByDeviceId((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleList>) responseObserver);
                    break;
                case METHODID_ZTP_ADD:
                    serviceImpl.ztpAdd((ztp.Ztp.DeviceRole) request, (io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState>) responseObserver);
                    break;
                case METHODID_ZTP_UPDATE:
                    serviceImpl.ztpUpdate((ztp.Ztp.DeviceRoleConfig) request, (io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState>) responseObserver);
                    break;
                case METHODID_ZTP_DELETE:
                    serviceImpl.ztpDelete((ztp.Ztp.DeviceRole) request, (io.grpc.stub.StreamObserver<ztp.Ztp.DeviceRoleState>) responseObserver);
                    break;
                case METHODID_ZTP_DELETE_ALL:
                    serviceImpl.ztpDeleteAll((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<ztp.Ztp.DeviceDeletionResult>) responseObserver);
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
        return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(getZtpGetDeviceRoleMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<ztp.Ztp.DeviceRoleId, ztp.Ztp.DeviceRole>(service, METHODID_ZTP_GET_DEVICE_ROLE))).addMethod(getZtpGetDeviceRolesByDeviceIdMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, ztp.Ztp.DeviceRoleList>(service, METHODID_ZTP_GET_DEVICE_ROLES_BY_DEVICE_ID))).addMethod(getZtpAddMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState>(service, METHODID_ZTP_ADD))).addMethod(getZtpUpdateMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<ztp.Ztp.DeviceRoleConfig, ztp.Ztp.DeviceRoleState>(service, METHODID_ZTP_UPDATE))).addMethod(getZtpDeleteMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<ztp.Ztp.DeviceRole, ztp.Ztp.DeviceRoleState>(service, METHODID_ZTP_DELETE))).addMethod(getZtpDeleteAllMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, ztp.Ztp.DeviceDeletionResult>(service, METHODID_ZTP_DELETE_ALL))).build();
    }

    private static abstract class ZtpServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {

        ZtpServiceBaseDescriptorSupplier() {
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
            return ztp.Ztp.getDescriptor();
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
            return getFileDescriptor().findServiceByName("ZtpService");
        }
    }

    private static final class ZtpServiceFileDescriptorSupplier extends ZtpServiceBaseDescriptorSupplier {

        ZtpServiceFileDescriptorSupplier() {
        }
    }

    private static final class ZtpServiceMethodDescriptorSupplier extends ZtpServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {

        private final String methodName;

        ZtpServiceMethodDescriptorSupplier(String methodName) {
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
            synchronized (ZtpServiceGrpc.class) {
                result = serviceDescriptor;
                if (result == null) {
                    serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME).setSchemaDescriptor(new ZtpServiceFileDescriptorSupplier()).addMethod(getZtpGetDeviceRoleMethod()).addMethod(getZtpGetDeviceRolesByDeviceIdMethod()).addMethod(getZtpAddMethod()).addMethod(getZtpUpdateMethod()).addMethod(getZtpDeleteMethod()).addMethod(getZtpDeleteAllMethod()).build();
                }
            }
        }
        return result;
    }
}
