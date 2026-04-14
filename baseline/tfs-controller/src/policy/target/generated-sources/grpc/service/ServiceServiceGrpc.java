package service;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.quarkus.grpc.common.Generated(value = "by gRPC proto compiler (version 1.55.1)", comments = "Source: service.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class ServiceServiceGrpc {

    private ServiceServiceGrpc() {
    }

    public static final String SERVICE_NAME = "service.ServiceService";

    // Static method descriptors that strictly reflect the proto.
    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getCreateServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "CreateService", requestType = context.ContextOuterClass.Service.class, responseType = context.ContextOuterClass.ServiceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getCreateServiceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getCreateServiceMethod;
        if ((getCreateServiceMethod = ServiceServiceGrpc.getCreateServiceMethod) == null) {
            synchronized (ServiceServiceGrpc.class) {
                if ((getCreateServiceMethod = ServiceServiceGrpc.getCreateServiceMethod) == null) {
                    ServiceServiceGrpc.getCreateServiceMethod = getCreateServiceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "CreateService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Service.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setSchemaDescriptor(new ServiceServiceMethodDescriptorSupplier("CreateService")).build();
                }
            }
        }
        return getCreateServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getUpdateServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "UpdateService", requestType = context.ContextOuterClass.Service.class, responseType = context.ContextOuterClass.ServiceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getUpdateServiceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getUpdateServiceMethod;
        if ((getUpdateServiceMethod = ServiceServiceGrpc.getUpdateServiceMethod) == null) {
            synchronized (ServiceServiceGrpc.class) {
                if ((getUpdateServiceMethod = ServiceServiceGrpc.getUpdateServiceMethod) == null) {
                    ServiceServiceGrpc.getUpdateServiceMethod = getUpdateServiceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "UpdateService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Service.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setSchemaDescriptor(new ServiceServiceMethodDescriptorSupplier("UpdateService")).build();
                }
            }
        }
        return getUpdateServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty> getDeleteServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteService", requestType = context.ContextOuterClass.ServiceId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty> getDeleteServiceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty> getDeleteServiceMethod;
        if ((getDeleteServiceMethod = ServiceServiceGrpc.getDeleteServiceMethod) == null) {
            synchronized (ServiceServiceGrpc.class) {
                if ((getDeleteServiceMethod = ServiceServiceGrpc.getDeleteServiceMethod) == null) {
                    ServiceServiceGrpc.getDeleteServiceMethod = getDeleteServiceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ServiceServiceMethodDescriptorSupplier("DeleteService")).build();
                }
            }
        }
        return getDeleteServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.Empty> getRecomputeConnectionsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RecomputeConnections", requestType = context.ContextOuterClass.Service.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.Empty> getRecomputeConnectionsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.Empty> getRecomputeConnectionsMethod;
        if ((getRecomputeConnectionsMethod = ServiceServiceGrpc.getRecomputeConnectionsMethod) == null) {
            synchronized (ServiceServiceGrpc.class) {
                if ((getRecomputeConnectionsMethod = ServiceServiceGrpc.getRecomputeConnectionsMethod) == null) {
                    ServiceServiceGrpc.getRecomputeConnectionsMethod = getRecomputeConnectionsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Service, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RecomputeConnections")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Service.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ServiceServiceMethodDescriptorSupplier("RecomputeConnections")).build();
                }
            }
        }
        return getRecomputeConnectionsMethod;
    }

    /**
     * Creates a new async stub that supports all call types for the service
     */
    public static ServiceServiceStub newStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ServiceServiceStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ServiceServiceStub>() {

            @java.lang.Override
            public ServiceServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ServiceServiceStub(channel, callOptions);
            }
        };
        return ServiceServiceStub.newStub(factory, channel);
    }

    /**
     * Creates a new blocking-style stub that supports unary and streaming output calls on the service
     */
    public static ServiceServiceBlockingStub newBlockingStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ServiceServiceBlockingStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ServiceServiceBlockingStub>() {

            @java.lang.Override
            public ServiceServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ServiceServiceBlockingStub(channel, callOptions);
            }
        };
        return ServiceServiceBlockingStub.newStub(factory, channel);
    }

    /**
     * Creates a new ListenableFuture-style stub that supports unary calls on the service
     */
    public static ServiceServiceFutureStub newFutureStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ServiceServiceFutureStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ServiceServiceFutureStub>() {

            @java.lang.Override
            public ServiceServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ServiceServiceFutureStub(channel, callOptions);
            }
        };
        return ServiceServiceFutureStub.newStub(factory, channel);
    }

    /**
     */
    public interface AsyncService {

        /**
         */
        default void createService(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getCreateServiceMethod(), responseObserver);
        }

        /**
         */
        default void updateService(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getUpdateServiceMethod(), responseObserver);
        }

        /**
         */
        default void deleteService(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteServiceMethod(), responseObserver);
        }

        /**
         */
        default void recomputeConnections(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRecomputeConnectionsMethod(), responseObserver);
        }
    }

    /**
     * Base class for the server implementation of the service ServiceService.
     */
    public static abstract class ServiceServiceImplBase implements io.grpc.BindableService, AsyncService {

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return ServiceServiceGrpc.bindService(this);
        }
    }

    /**
     * A stub to allow clients to do asynchronous rpc calls to service ServiceService.
     */
    public static class ServiceServiceStub extends io.grpc.stub.AbstractAsyncStub<ServiceServiceStub> {

        private ServiceServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ServiceServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ServiceServiceStub(channel, callOptions);
        }

        /**
         */
        public void createService(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getCreateServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void updateService(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getUpdateServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteService(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void recomputeConnections(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRecomputeConnectionsMethod(), getCallOptions()), request, responseObserver);
        }
    }

    /**
     * A stub to allow clients to do synchronous rpc calls to service ServiceService.
     */
    public static class ServiceServiceBlockingStub extends io.grpc.stub.AbstractBlockingStub<ServiceServiceBlockingStub> {

        private ServiceServiceBlockingStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ServiceServiceBlockingStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ServiceServiceBlockingStub(channel, callOptions);
        }

        /**
         */
        public context.ContextOuterClass.ServiceId createService(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getCreateServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ServiceId updateService(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getUpdateServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteService(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty recomputeConnections(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRecomputeConnectionsMethod(), getCallOptions(), request);
        }
    }

    /**
     * A stub to allow clients to do ListenableFuture-style rpc calls to service ServiceService.
     */
    public static class ServiceServiceFutureStub extends io.grpc.stub.AbstractFutureStub<ServiceServiceFutureStub> {

        private ServiceServiceFutureStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ServiceServiceFutureStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ServiceServiceFutureStub(channel, callOptions);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ServiceId> createService(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getCreateServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ServiceId> updateService(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getUpdateServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteService(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> recomputeConnections(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRecomputeConnectionsMethod(), getCallOptions()), request);
        }
    }

    private static final int METHODID_CREATE_SERVICE = 0;

    private static final int METHODID_UPDATE_SERVICE = 1;

    private static final int METHODID_DELETE_SERVICE = 2;

    private static final int METHODID_RECOMPUTE_CONNECTIONS = 3;

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
                case METHODID_CREATE_SERVICE:
                    serviceImpl.createService((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId>) responseObserver);
                    break;
                case METHODID_UPDATE_SERVICE:
                    serviceImpl.updateService((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId>) responseObserver);
                    break;
                case METHODID_DELETE_SERVICE:
                    serviceImpl.deleteService((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_RECOMPUTE_CONNECTIONS:
                    serviceImpl.recomputeConnections((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
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
        return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(getCreateServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>(service, METHODID_CREATE_SERVICE))).addMethod(getUpdateServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>(service, METHODID_UPDATE_SERVICE))).addMethod(getDeleteServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty>(service, METHODID_DELETE_SERVICE))).addMethod(getRecomputeConnectionsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.Empty>(service, METHODID_RECOMPUTE_CONNECTIONS))).build();
    }

    private static abstract class ServiceServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {

        ServiceServiceBaseDescriptorSupplier() {
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
            return service.Service.getDescriptor();
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
            return getFileDescriptor().findServiceByName("ServiceService");
        }
    }

    private static final class ServiceServiceFileDescriptorSupplier extends ServiceServiceBaseDescriptorSupplier {

        ServiceServiceFileDescriptorSupplier() {
        }
    }

    private static final class ServiceServiceMethodDescriptorSupplier extends ServiceServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {

        private final String methodName;

        ServiceServiceMethodDescriptorSupplier(String methodName) {
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
            synchronized (ServiceServiceGrpc.class) {
                result = serviceDescriptor;
                if (result == null) {
                    serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME).setSchemaDescriptor(new ServiceServiceFileDescriptorSupplier()).addMethod(getCreateServiceMethod()).addMethod(getUpdateServiceMethod()).addMethod(getDeleteServiceMethod()).addMethod(getRecomputeConnectionsMethod()).build();
                }
            }
        }
        return result;
    }
}
