package context_policy;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 * <pre>
 * created as a separate service to prevent import-loops in context and policy
 * </pre>
 */
@io.quarkus.grpc.common.Generated(value = "by gRPC proto compiler (version 1.55.1)", comments = "Source: context_policy.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class ContextPolicyServiceGrpc {

    private ContextPolicyServiceGrpc() {
    }

    public static final String SERVICE_NAME = "context_policy.ContextPolicyService";

    // Static method descriptors that strictly reflect the proto.
    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleIdList> getListPolicyRuleIdsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListPolicyRuleIds", requestType = context.ContextOuterClass.Empty.class, responseType = policy.Policy.PolicyRuleIdList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleIdList> getListPolicyRuleIdsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleIdList> getListPolicyRuleIdsMethod;
        if ((getListPolicyRuleIdsMethod = ContextPolicyServiceGrpc.getListPolicyRuleIdsMethod) == null) {
            synchronized (ContextPolicyServiceGrpc.class) {
                if ((getListPolicyRuleIdsMethod = ContextPolicyServiceGrpc.getListPolicyRuleIdsMethod) == null) {
                    ContextPolicyServiceGrpc.getListPolicyRuleIdsMethod = getListPolicyRuleIdsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleIdList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListPolicyRuleIds")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleIdList.getDefaultInstance())).setSchemaDescriptor(new ContextPolicyServiceMethodDescriptorSupplier("ListPolicyRuleIds")).build();
                }
            }
        }
        return getListPolicyRuleIdsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleList> getListPolicyRulesMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListPolicyRules", requestType = context.ContextOuterClass.Empty.class, responseType = policy.Policy.PolicyRuleList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleList> getListPolicyRulesMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleList> getListPolicyRulesMethod;
        if ((getListPolicyRulesMethod = ContextPolicyServiceGrpc.getListPolicyRulesMethod) == null) {
            synchronized (ContextPolicyServiceGrpc.class) {
                if ((getListPolicyRulesMethod = ContextPolicyServiceGrpc.getListPolicyRulesMethod) == null) {
                    ContextPolicyServiceGrpc.getListPolicyRulesMethod = getListPolicyRulesMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListPolicyRules")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleList.getDefaultInstance())).setSchemaDescriptor(new ContextPolicyServiceMethodDescriptorSupplier("ListPolicyRules")).build();
                }
            }
        }
        return getListPolicyRulesMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRule> getGetPolicyRuleMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetPolicyRule", requestType = policy.Policy.PolicyRuleId.class, responseType = policy.Policy.PolicyRule.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRule> getGetPolicyRuleMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, policy.Policy.PolicyRule> getGetPolicyRuleMethod;
        if ((getGetPolicyRuleMethod = ContextPolicyServiceGrpc.getGetPolicyRuleMethod) == null) {
            synchronized (ContextPolicyServiceGrpc.class) {
                if ((getGetPolicyRuleMethod = ContextPolicyServiceGrpc.getGetPolicyRuleMethod) == null) {
                    ContextPolicyServiceGrpc.getGetPolicyRuleMethod = getGetPolicyRuleMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleId, policy.Policy.PolicyRule>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetPolicyRule")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRule.getDefaultInstance())).setSchemaDescriptor(new ContextPolicyServiceMethodDescriptorSupplier("GetPolicyRule")).build();
                }
            }
        }
        return getGetPolicyRuleMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRule, policy.Policy.PolicyRuleId> getSetPolicyRuleMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetPolicyRule", requestType = policy.Policy.PolicyRule.class, responseType = policy.Policy.PolicyRuleId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRule, policy.Policy.PolicyRuleId> getSetPolicyRuleMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRule, policy.Policy.PolicyRuleId> getSetPolicyRuleMethod;
        if ((getSetPolicyRuleMethod = ContextPolicyServiceGrpc.getSetPolicyRuleMethod) == null) {
            synchronized (ContextPolicyServiceGrpc.class) {
                if ((getSetPolicyRuleMethod = ContextPolicyServiceGrpc.getSetPolicyRuleMethod) == null) {
                    ContextPolicyServiceGrpc.getSetPolicyRuleMethod = getSetPolicyRuleMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRule, policy.Policy.PolicyRuleId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetPolicyRule")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRule.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleId.getDefaultInstance())).setSchemaDescriptor(new ContextPolicyServiceMethodDescriptorSupplier("SetPolicyRule")).build();
                }
            }
        }
        return getSetPolicyRuleMethod;
    }

    private static volatile io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, context.ContextOuterClass.Empty> getRemovePolicyRuleMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RemovePolicyRule", requestType = policy.Policy.PolicyRuleId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, context.ContextOuterClass.Empty> getRemovePolicyRuleMethod() {
        io.grpc.MethodDescriptor<policy.Policy.PolicyRuleId, context.ContextOuterClass.Empty> getRemovePolicyRuleMethod;
        if ((getRemovePolicyRuleMethod = ContextPolicyServiceGrpc.getRemovePolicyRuleMethod) == null) {
            synchronized (ContextPolicyServiceGrpc.class) {
                if ((getRemovePolicyRuleMethod = ContextPolicyServiceGrpc.getRemovePolicyRuleMethod) == null) {
                    ContextPolicyServiceGrpc.getRemovePolicyRuleMethod = getRemovePolicyRuleMethod = io.grpc.MethodDescriptor.<policy.Policy.PolicyRuleId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RemovePolicyRule")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(policy.Policy.PolicyRuleId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextPolicyServiceMethodDescriptorSupplier("RemovePolicyRule")).build();
                }
            }
        }
        return getRemovePolicyRuleMethod;
    }

    /**
     * Creates a new async stub that supports all call types for the service
     */
    public static ContextPolicyServiceStub newStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ContextPolicyServiceStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ContextPolicyServiceStub>() {

            @java.lang.Override
            public ContextPolicyServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ContextPolicyServiceStub(channel, callOptions);
            }
        };
        return ContextPolicyServiceStub.newStub(factory, channel);
    }

    /**
     * Creates a new blocking-style stub that supports unary and streaming output calls on the service
     */
    public static ContextPolicyServiceBlockingStub newBlockingStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ContextPolicyServiceBlockingStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ContextPolicyServiceBlockingStub>() {

            @java.lang.Override
            public ContextPolicyServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ContextPolicyServiceBlockingStub(channel, callOptions);
            }
        };
        return ContextPolicyServiceBlockingStub.newStub(factory, channel);
    }

    /**
     * Creates a new ListenableFuture-style stub that supports unary calls on the service
     */
    public static ContextPolicyServiceFutureStub newFutureStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ContextPolicyServiceFutureStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ContextPolicyServiceFutureStub>() {

            @java.lang.Override
            public ContextPolicyServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ContextPolicyServiceFutureStub(channel, callOptions);
            }
        };
        return ContextPolicyServiceFutureStub.newStub(factory, channel);
    }

    /**
     * <pre>
     * created as a separate service to prevent import-loops in context and policy
     * </pre>
     */
    public interface AsyncService {

        /**
         */
        default void listPolicyRuleIds(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleIdList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListPolicyRuleIdsMethod(), responseObserver);
        }

        /**
         */
        default void listPolicyRules(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListPolicyRulesMethod(), responseObserver);
        }

        /**
         */
        default void getPolicyRule(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRule> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetPolicyRuleMethod(), responseObserver);
        }

        /**
         */
        default void setPolicyRule(policy.Policy.PolicyRule request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetPolicyRuleMethod(), responseObserver);
        }

        /**
         */
        default void removePolicyRule(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRemovePolicyRuleMethod(), responseObserver);
        }
    }

    /**
     * Base class for the server implementation of the service ContextPolicyService.
     * <pre>
     * created as a separate service to prevent import-loops in context and policy
     * </pre>
     */
    public static abstract class ContextPolicyServiceImplBase implements io.grpc.BindableService, AsyncService {

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return ContextPolicyServiceGrpc.bindService(this);
        }
    }

    /**
     * A stub to allow clients to do asynchronous rpc calls to service ContextPolicyService.
     * <pre>
     * created as a separate service to prevent import-loops in context and policy
     * </pre>
     */
    public static class ContextPolicyServiceStub extends io.grpc.stub.AbstractAsyncStub<ContextPolicyServiceStub> {

        private ContextPolicyServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ContextPolicyServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ContextPolicyServiceStub(channel, callOptions);
        }

        /**
         */
        public void listPolicyRuleIds(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleIdList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListPolicyRuleIdsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listPolicyRules(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListPolicyRulesMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getPolicyRule(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRule> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetPolicyRuleMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setPolicyRule(policy.Policy.PolicyRule request, io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetPolicyRuleMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void removePolicyRule(policy.Policy.PolicyRuleId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRemovePolicyRuleMethod(), getCallOptions()), request, responseObserver);
        }
    }

    /**
     * A stub to allow clients to do synchronous rpc calls to service ContextPolicyService.
     * <pre>
     * created as a separate service to prevent import-loops in context and policy
     * </pre>
     */
    public static class ContextPolicyServiceBlockingStub extends io.grpc.stub.AbstractBlockingStub<ContextPolicyServiceBlockingStub> {

        private ContextPolicyServiceBlockingStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ContextPolicyServiceBlockingStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ContextPolicyServiceBlockingStub(channel, callOptions);
        }

        /**
         */
        public policy.Policy.PolicyRuleIdList listPolicyRuleIds(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListPolicyRuleIdsMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleList listPolicyRules(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListPolicyRulesMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRule getPolicyRule(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetPolicyRuleMethod(), getCallOptions(), request);
        }

        /**
         */
        public policy.Policy.PolicyRuleId setPolicyRule(policy.Policy.PolicyRule request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetPolicyRuleMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty removePolicyRule(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRemovePolicyRuleMethod(), getCallOptions(), request);
        }
    }

    /**
     * A stub to allow clients to do ListenableFuture-style rpc calls to service ContextPolicyService.
     * <pre>
     * created as a separate service to prevent import-loops in context and policy
     * </pre>
     */
    public static class ContextPolicyServiceFutureStub extends io.grpc.stub.AbstractFutureStub<ContextPolicyServiceFutureStub> {

        private ContextPolicyServiceFutureStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ContextPolicyServiceFutureStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ContextPolicyServiceFutureStub(channel, callOptions);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleIdList> listPolicyRuleIds(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListPolicyRuleIdsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleList> listPolicyRules(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListPolicyRulesMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRule> getPolicyRule(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetPolicyRuleMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<policy.Policy.PolicyRuleId> setPolicyRule(policy.Policy.PolicyRule request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetPolicyRuleMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> removePolicyRule(policy.Policy.PolicyRuleId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRemovePolicyRuleMethod(), getCallOptions()), request);
        }
    }

    private static final int METHODID_LIST_POLICY_RULE_IDS = 0;

    private static final int METHODID_LIST_POLICY_RULES = 1;

    private static final int METHODID_GET_POLICY_RULE = 2;

    private static final int METHODID_SET_POLICY_RULE = 3;

    private static final int METHODID_REMOVE_POLICY_RULE = 4;

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
                case METHODID_LIST_POLICY_RULE_IDS:
                    serviceImpl.listPolicyRuleIds((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleIdList>) responseObserver);
                    break;
                case METHODID_LIST_POLICY_RULES:
                    serviceImpl.listPolicyRules((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleList>) responseObserver);
                    break;
                case METHODID_GET_POLICY_RULE:
                    serviceImpl.getPolicyRule((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRule>) responseObserver);
                    break;
                case METHODID_SET_POLICY_RULE:
                    serviceImpl.setPolicyRule((policy.Policy.PolicyRule) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleId>) responseObserver);
                    break;
                case METHODID_REMOVE_POLICY_RULE:
                    serviceImpl.removePolicyRule((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
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
        return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(getListPolicyRuleIdsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleIdList>(service, METHODID_LIST_POLICY_RULE_IDS))).addMethod(getListPolicyRulesMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleList>(service, METHODID_LIST_POLICY_RULES))).addMethod(getGetPolicyRuleMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, policy.Policy.PolicyRule>(service, METHODID_GET_POLICY_RULE))).addMethod(getSetPolicyRuleMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRule, policy.Policy.PolicyRuleId>(service, METHODID_SET_POLICY_RULE))).addMethod(getRemovePolicyRuleMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, context.ContextOuterClass.Empty>(service, METHODID_REMOVE_POLICY_RULE))).build();
    }

    private static abstract class ContextPolicyServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {

        ContextPolicyServiceBaseDescriptorSupplier() {
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
            return context_policy.ContextPolicy.getDescriptor();
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
            return getFileDescriptor().findServiceByName("ContextPolicyService");
        }
    }

    private static final class ContextPolicyServiceFileDescriptorSupplier extends ContextPolicyServiceBaseDescriptorSupplier {

        ContextPolicyServiceFileDescriptorSupplier() {
        }
    }

    private static final class ContextPolicyServiceMethodDescriptorSupplier extends ContextPolicyServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {

        private final String methodName;

        ContextPolicyServiceMethodDescriptorSupplier(String methodName) {
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
            synchronized (ContextPolicyServiceGrpc.class) {
                result = serviceDescriptor;
                if (result == null) {
                    serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME).setSchemaDescriptor(new ContextPolicyServiceFileDescriptorSupplier()).addMethod(getListPolicyRuleIdsMethod()).addMethod(getListPolicyRulesMethod()).addMethod(getGetPolicyRuleMethod()).addMethod(getSetPolicyRuleMethod()).addMethod(getRemovePolicyRuleMethod()).build();
                }
            }
        }
        return result;
    }
}
