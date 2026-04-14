package policy;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.quarkus.grpc.common.Generated(value = "by gRPC proto compiler (version 1.55.1)", comments = "Source: policy.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class PolicyServiceGrpc {

    private PolicyServiceGrpc() {
    }

    public static final String SERVICE_NAME = "policy.PolicyService";

    // Static method descriptors that strictly reflect the proto.
    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState> getPolicyAddServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "PolicyAddService", requestType = policy.Policy.PolicyRuleService.class, responseType = policy.Policy.PolicyRuleState.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState> getPolicyAddServiceMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState> getPolicyAddServiceMethod;
        if ((getPolicyAddServiceMethod = PolicyServiceGrpc.getPolicyAddServiceMethod) == null) {
            synchronized (PolicyServiceGrpc.class) {
                if ((getPolicyAddServiceMethod = PolicyServiceGrpc.getPolicyAddServiceMethod) == null) {
                    PolicyServiceGrpc.getPolicyAddServiceMethod = getPolicyAddServiceMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "PolicyAddService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleService.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleState.getDefaultInstance())).setSchemaDescriptor(new PolicyServiceMethodDescriptorSupplier("PolicyAddService")).build();
                }
            }
        }
        return getPolicyAddServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState> getPolicyAddDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "PolicyAddDevice", requestType = policy.Policy.PolicyRuleDevice.class, responseType = policy.Policy.PolicyRuleState.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState> getPolicyAddDeviceMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState> getPolicyAddDeviceMethod;
        if ((getPolicyAddDeviceMethod = PolicyServiceGrpc.getPolicyAddDeviceMethod) == null) {
            synchronized (PolicyServiceGrpc.class) {
                if ((getPolicyAddDeviceMethod = PolicyServiceGrpc.getPolicyAddDeviceMethod) == null) {
                    PolicyServiceGrpc.getPolicyAddDeviceMethod = getPolicyAddDeviceMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "PolicyAddDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleDevice.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleState.getDefaultInstance())).setSchemaDescriptor(new PolicyServiceMethodDescriptorSupplier("PolicyAddDevice")).build();
                }
            }
        }
        return getPolicyAddDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState> getPolicyUpdateServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "PolicyUpdateService", requestType = policy.Policy.PolicyRuleService.class, responseType = policy.Policy.PolicyRuleState.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState> getPolicyUpdateServiceMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState> getPolicyUpdateServiceMethod;
        if ((getPolicyUpdateServiceMethod = PolicyServiceGrpc.getPolicyUpdateServiceMethod) == null) {
            synchronized (PolicyServiceGrpc.class) {
                if ((getPolicyUpdateServiceMethod = PolicyServiceGrpc.getPolicyUpdateServiceMethod) == null) {
                    PolicyServiceGrpc.getPolicyUpdateServiceMethod = getPolicyUpdateServiceMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "PolicyUpdateService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleService.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleState.getDefaultInstance())).setSchemaDescriptor(new PolicyServiceMethodDescriptorSupplier("PolicyUpdateService")).build();
                }
            }
        }
        return getPolicyUpdateServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState> getPolicyUpdateDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "PolicyUpdateDevice", requestType = policy.Policy.PolicyRuleDevice.class, responseType = policy.Policy.PolicyRuleState.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState> getPolicyUpdateDeviceMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState> getPolicyUpdateDeviceMethod;
        if ((getPolicyUpdateDeviceMethod = PolicyServiceGrpc.getPolicyUpdateDeviceMethod) == null) {
            synchronized (PolicyServiceGrpc.class) {
                if ((getPolicyUpdateDeviceMethod = PolicyServiceGrpc.getPolicyUpdateDeviceMethod) == null) {
                    PolicyServiceGrpc.getPolicyUpdateDeviceMethod = getPolicyUpdateDeviceMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "PolicyUpdateDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleDevice.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleState.getDefaultInstance())).setSchemaDescriptor(new PolicyServiceMethodDescriptorSupplier("PolicyUpdateDevice")).build();
                }
            }
        }
        return getPolicyUpdateDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleState> getPolicyDeleteMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "PolicyDelete", requestType = policy.Policy.PolicyRuleId.class, responseType = policy.Policy.PolicyRuleState.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleState> getPolicyDeleteMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleState> getPolicyDeleteMethod;
        if ((getPolicyDeleteMethod = PolicyServiceGrpc.getPolicyDeleteMethod) == null) {
            synchronized (PolicyServiceGrpc.class) {
                if ((getPolicyDeleteMethod = PolicyServiceGrpc.getPolicyDeleteMethod) == null) {
                    PolicyServiceGrpc.getPolicyDeleteMethod = getPolicyDeleteMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleState>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "PolicyDelete")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleState.getDefaultInstance())).setSchemaDescriptor(new PolicyServiceMethodDescriptorSupplier("PolicyDelete")).build();
                }
            }
        }
        return getPolicyDeleteMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleService> getGetPolicyServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetPolicyService", requestType = policy.Policy.PolicyRuleId.class, responseType = policy.Policy.PolicyRuleService.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleService> getGetPolicyServiceMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleService> getGetPolicyServiceMethod;
        if ((getGetPolicyServiceMethod = PolicyServiceGrpc.getGetPolicyServiceMethod) == null) {
            synchronized (PolicyServiceGrpc.class) {
                if ((getGetPolicyServiceMethod = PolicyServiceGrpc.getGetPolicyServiceMethod) == null) {
                    PolicyServiceGrpc.getGetPolicyServiceMethod = getGetPolicyServiceMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleService>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetPolicyService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleService.getDefaultInstance())).setSchemaDescriptor(new PolicyServiceMethodDescriptorSupplier("GetPolicyService")).build();
                }
            }
        }
        return getGetPolicyServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleDevice> getGetPolicyDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetPolicyDevice", requestType = policy.Policy.PolicyRuleId.class, responseType = policy.Policy.PolicyRuleDevice.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleDevice> getGetPolicyDeviceMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleDevice> getGetPolicyDeviceMethod;
        if ((getGetPolicyDeviceMethod = PolicyServiceGrpc.getGetPolicyDeviceMethod) == null) {
            synchronized (PolicyServiceGrpc.class) {
                if ((getGetPolicyDeviceMethod = PolicyServiceGrpc.getGetPolicyDeviceMethod) == null) {
                    PolicyServiceGrpc.getGetPolicyDeviceMethod = getGetPolicyDeviceMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleDevice>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetPolicyDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleDevice.getDefaultInstance())).setSchemaDescriptor(new PolicyServiceMethodDescriptorSupplier("GetPolicyDevice")).build();
                }
            }
        }
        return getGetPolicyDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, policy.Policy.PolicyRuleServiceList> getGetPolicyByServiceIdMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetPolicyByServiceId", requestType = context.ContextOuterClass.ServiceId.class, responseType = policy.Policy.PolicyRuleServiceList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, policy.Policy.PolicyRuleServiceList> getGetPolicyByServiceIdMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, policy.Policy.PolicyRuleServiceList> getGetPolicyByServiceIdMethod;
        if ((getGetPolicyByServiceIdMethod = PolicyServiceGrpc.getGetPolicyByServiceIdMethod) == null) {
            synchronized (PolicyServiceGrpc.class) {
                if ((getGetPolicyByServiceIdMethod = PolicyServiceGrpc.getGetPolicyByServiceIdMethod) == null) {
                    PolicyServiceGrpc.getGetPolicyByServiceIdMethod = getGetPolicyByServiceIdMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ServiceId, policy.Policy.PolicyRuleServiceList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetPolicyByServiceId")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleServiceList.getDefaultInstance())).setSchemaDescriptor(new PolicyServiceMethodDescriptorSupplier("GetPolicyByServiceId")).build();
                }
            }
        }
        return getGetPolicyByServiceIdMethod;
    }

    /**
     * Creates a new async stub that supports all call types for the service
     */
    public static PolicyServiceStub newStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<PolicyServiceStub> factory = new io.grpc.stub.AbstractStub.StubFactory<PolicyServiceStub>() {

            @java.lang.Override
            public PolicyServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new PolicyServiceStub(channel, callOptions);
            }
        };
        return PolicyServiceStub.newStub(factory, channel);
    }

    /**
     * Creates a new blocking-style stub that supports unary and streaming output calls on the service
     */
    public static PolicyServiceBlockingStub newBlockingStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<PolicyServiceBlockingStub> factory = new io.grpc.stub.AbstractStub.StubFactory<PolicyServiceBlockingStub>() {

            @java.lang.Override
            public PolicyServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new PolicyServiceBlockingStub(channel, callOptions);
            }
        };
        return PolicyServiceBlockingStub.newStub(factory, channel);
    }

    /**
     * Creates a new ListenableFuture-style stub that supports unary calls on the service
     */
    public static PolicyServiceFutureStub newFutureStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<PolicyServiceFutureStub> factory = new io.grpc.stub.AbstractStub.StubFactory<PolicyServiceFutureStub>() {

            @java.lang.Override
            public PolicyServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new PolicyServiceFutureStub(channel, callOptions);
            }
        };
        return PolicyServiceFutureStub.newStub(factory, channel);
    }

    /**
     */
    public interface AsyncService {

        /**
         */
        default void policyAddService(policy.Policy.PolicyRuleService request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPolicyAddServiceMethod(), responseObserver);
        }

        /**
         */
        default void policyAddDevice(policy.Policy.PolicyRuleDevice request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPolicyAddDeviceMethod(), responseObserver);
        }

        /**
         */
        default void policyUpdateService(policy.Policy.PolicyRuleService request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPolicyUpdateServiceMethod(), responseObserver);
        }

        /**
         */
        default void policyUpdateDevice(policy.Policy.PolicyRuleDevice request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPolicyUpdateDeviceMethod(), responseObserver);
        }

        /**
         */
        default void policyDelete(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPolicyDeleteMethod(), responseObserver);
        }

        /**
         */
        default void getPolicyService(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleService> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetPolicyServiceMethod(), responseObserver);
        }

        /**
         */
        default void getPolicyDevice(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleDevice> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetPolicyDeviceMethod(), responseObserver);
        }

        /**
         */
        default void getPolicyByServiceId(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleServiceList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetPolicyByServiceIdMethod(), responseObserver);
        }
    }

    /**
     * Base class for the server implementation of the service PolicyService.
     */
    public static abstract class PolicyServiceImplBase implements io.grpc.BindableService, AsyncService {

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return PolicyServiceGrpc.bindService(this);
        }
    }

    /**
     * A stub to allow clients to do asynchronous rpc calls to service PolicyService.
     */
    public static class PolicyServiceStub extends io.grpc.stub.AbstractAsyncStub<PolicyServiceStub> {

        private PolicyServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected PolicyServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new PolicyServiceStub(channel, callOptions);
        }

        /**
         */
        public void policyAddService(policy.Policy.PolicyRuleService request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getPolicyAddServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void policyAddDevice(policy.Policy.PolicyRuleDevice request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getPolicyAddDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void policyUpdateService(policy.Policy.PolicyRuleService request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getPolicyUpdateServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void policyUpdateDevice(policy.Policy.PolicyRuleDevice request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getPolicyUpdateDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void policyDelete(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getPolicyDeleteMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getPolicyService(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleService> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetPolicyServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getPolicyDevice(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleDevice> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetPolicyDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getPolicyByServiceId(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleServiceList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetPolicyByServiceIdMethod(), getCallOptions()), request, responseObserver);
        }
    }

    /**
     * A stub to allow clients to do synchronous rpc calls to service PolicyService.
     */
    public static class PolicyServiceBlockingStub extends io.grpc.stub.AbstractBlockingStub<PolicyServiceBlockingStub> {

        private PolicyServiceBlockingStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected PolicyServiceBlockingStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new PolicyServiceBlockingStub(channel, callOptions);
        }

        /**
         */
        public policy.Policy.PolicyRuleState policyAddService(policy.Policy.PolicyRuleService request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getPolicyAddServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleState policyAddDevice(policy.Policy.PolicyRuleDevice request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getPolicyAddDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleState policyUpdateService(policy.Policy.PolicyRuleService request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getPolicyUpdateServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleState policyUpdateDevice(policy.Policy.PolicyRuleDevice request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getPolicyUpdateDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleState policyDelete(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getPolicyDeleteMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleService getPolicyService(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetPolicyServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleDevice getPolicyDevice(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetPolicyDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleServiceList getPolicyByServiceId(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetPolicyByServiceIdMethod(), getCallOptions(), request);
        }
    }

    /**
     * A stub to allow clients to do ListenableFuture-style rpc calls to service PolicyService.
     */
    public static class PolicyServiceFutureStub extends io.grpc.stub.AbstractFutureStub<PolicyServiceFutureStub> {

        private PolicyServiceFutureStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected PolicyServiceFutureStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new PolicyServiceFutureStub(channel, callOptions);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleState> policyAddService(policy.Policy.PolicyRuleService request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getPolicyAddServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleState> policyAddDevice(policy.Policy.PolicyRuleDevice request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getPolicyAddDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleState> policyUpdateService(policy.Policy.PolicyRuleService request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getPolicyUpdateServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleState> policyUpdateDevice(policy.Policy.PolicyRuleDevice request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getPolicyUpdateDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleState> policyDelete(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getPolicyDeleteMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleService> getPolicyService(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetPolicyServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleDevice> getPolicyDevice(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetPolicyDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleServiceList> getPolicyByServiceId(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetPolicyByServiceIdMethod(), getCallOptions()), request);
        }
    }

    private static final int METHODID_POLICY_ADD_SERVICE = 0;

    private static final int METHODID_POLICY_ADD_DEVICE = 1;

    private static final int METHODID_POLICY_UPDATE_SERVICE = 2;

    private static final int METHODID_POLICY_UPDATE_DEVICE = 3;

    private static final int METHODID_POLICY_DELETE = 4;

    private static final int METHODID_GET_POLICY_SERVICE = 5;

    private static final int METHODID_GET_POLICY_DEVICE = 6;

    private static final int METHODID_GET_POLICY_BY_SERVICE_ID = 7;

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
                case METHODID_POLICY_ADD_SERVICE:
                    serviceImpl.policyAddService((policy.Policy.PolicyRuleService) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver);
                    break;
                case METHODID_POLICY_ADD_DEVICE:
                    serviceImpl.policyAddDevice((policy.Policy.PolicyRuleDevice) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver);
                    break;
                case METHODID_POLICY_UPDATE_SERVICE:
                    serviceImpl.policyUpdateService((policy.Policy.PolicyRuleService) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver);
                    break;
                case METHODID_POLICY_UPDATE_DEVICE:
                    serviceImpl.policyUpdateDevice((policy.Policy.PolicyRuleDevice) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver);
                    break;
                case METHODID_POLICY_DELETE:
                    serviceImpl.policyDelete((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver);
                    break;
                case METHODID_GET_POLICY_SERVICE:
                    serviceImpl.getPolicyService((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleService>) responseObserver);
                    break;
                case METHODID_GET_POLICY_DEVICE:
                    serviceImpl.getPolicyDevice((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleDevice>) responseObserver);
                    break;
                case METHODID_GET_POLICY_BY_SERVICE_ID:
                    serviceImpl.getPolicyByServiceId((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleServiceList>) responseObserver);
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
        return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(getPolicyAddServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState>(service, METHODID_POLICY_ADD_SERVICE))).addMethod(getPolicyAddDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState>(service, METHODID_POLICY_ADD_DEVICE))).addMethod(getPolicyUpdateServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState>(service, METHODID_POLICY_UPDATE_SERVICE))).addMethod(getPolicyUpdateDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState>(service, METHODID_POLICY_UPDATE_DEVICE))).addMethod(getPolicyDeleteMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleState>(service, METHODID_POLICY_DELETE))).addMethod(getGetPolicyServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleService>(service, METHODID_GET_POLICY_SERVICE))).addMethod(getGetPolicyDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleDevice>(service, METHODID_GET_POLICY_DEVICE))).addMethod(getGetPolicyByServiceIdMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, policy.Policy.PolicyRuleServiceList>(service, METHODID_GET_POLICY_BY_SERVICE_ID))).build();
    }

    private static abstract class PolicyServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {

        PolicyServiceBaseDescriptorSupplier() {
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
            return policy.Policy.getDescriptor();
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
            return getFileDescriptor().findServiceByName("PolicyService");
        }
    }

    private static final class PolicyServiceFileDescriptorSupplier extends PolicyServiceBaseDescriptorSupplier {

        PolicyServiceFileDescriptorSupplier() {
        }
    }

    private static final class PolicyServiceMethodDescriptorSupplier extends PolicyServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {

        private final String methodName;

        PolicyServiceMethodDescriptorSupplier(String methodName) {
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
            synchronized (PolicyServiceGrpc.class) {
                result = serviceDescriptor;
                if (result == null) {
                    serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME).setSchemaDescriptor(new PolicyServiceFileDescriptorSupplier()).addMethod(getPolicyAddServiceMethod()).addMethod(getPolicyAddDeviceMethod()).addMethod(getPolicyUpdateServiceMethod()).addMethod(getPolicyUpdateDeviceMethod()).addMethod(getPolicyDeleteMethod()).addMethod(getGetPolicyServiceMethod()).addMethod(getGetPolicyDeviceMethod()).addMethod(getGetPolicyByServiceIdMethod()).build();
                }
            }
        }
        return result;
    }
}
