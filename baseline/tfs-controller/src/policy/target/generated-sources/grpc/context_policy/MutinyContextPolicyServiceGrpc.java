package context_policy;

import static context_policy.ContextPolicyServiceGrpc.getServiceDescriptor;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: context_policy.proto")
public final class MutinyContextPolicyServiceGrpc implements io.quarkus.grpc.MutinyGrpc {

    private MutinyContextPolicyServiceGrpc() {
    }

    public static MutinyContextPolicyServiceStub newMutinyStub(io.grpc.Channel channel) {
        return new MutinyContextPolicyServiceStub(channel);
    }

    /**
     * <pre>
     *  created as a separate service to prevent import-loops in context and policy
     * </pre>
     */
    public static class MutinyContextPolicyServiceStub extends io.grpc.stub.AbstractStub<MutinyContextPolicyServiceStub> implements io.quarkus.grpc.MutinyStub {

        private ContextPolicyServiceGrpc.ContextPolicyServiceStub delegateStub;

        private MutinyContextPolicyServiceStub(io.grpc.Channel channel) {
            super(channel);
            delegateStub = ContextPolicyServiceGrpc.newStub(channel);
        }

        private MutinyContextPolicyServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
            delegateStub = ContextPolicyServiceGrpc.newStub(channel).build(channel, callOptions);
        }

        @Override
        protected MutinyContextPolicyServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MutinyContextPolicyServiceStub(channel, callOptions);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleIdList> listPolicyRuleIds(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listPolicyRuleIds);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleList> listPolicyRules(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listPolicyRules);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRule> getPolicyRule(policy.Policy.PolicyRuleId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getPolicyRule);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleId> setPolicyRule(policy.Policy.PolicyRule request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setPolicyRule);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removePolicyRule(policy.Policy.PolicyRuleId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::removePolicyRule);
        }
    }

    /**
     * <pre>
     *  created as a separate service to prevent import-loops in context and policy
     * </pre>
     */
    public static abstract class ContextPolicyServiceImplBase implements io.grpc.BindableService {

        private String compression;

        /**
         * Set whether the server will try to use a compressed response.
         *
         * @param compression the compression, e.g {@code gzip}
         */
        public ContextPolicyServiceImplBase withCompression(String compression) {
            this.compression = compression;
            return this;
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleIdList> listPolicyRuleIds(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleList> listPolicyRules(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRule> getPolicyRule(policy.Policy.PolicyRuleId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleId> setPolicyRule(policy.Policy.PolicyRule request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removePolicyRule(policy.Policy.PolicyRuleId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(context_policy.ContextPolicyServiceGrpc.getListPolicyRuleIdsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleIdList>(this, METHODID_LIST_POLICY_RULE_IDS, compression))).addMethod(context_policy.ContextPolicyServiceGrpc.getListPolicyRulesMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, policy.Policy.PolicyRuleList>(this, METHODID_LIST_POLICY_RULES, compression))).addMethod(context_policy.ContextPolicyServiceGrpc.getGetPolicyRuleMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, policy.Policy.PolicyRule>(this, METHODID_GET_POLICY_RULE, compression))).addMethod(context_policy.ContextPolicyServiceGrpc.getSetPolicyRuleMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRule, policy.Policy.PolicyRuleId>(this, METHODID_SET_POLICY_RULE, compression))).addMethod(context_policy.ContextPolicyServiceGrpc.getRemovePolicyRuleMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, context.ContextOuterClass.Empty>(this, METHODID_REMOVE_POLICY_RULE, compression))).build();
        }
    }

    private static final int METHODID_LIST_POLICY_RULE_IDS = 0;

    private static final int METHODID_LIST_POLICY_RULES = 1;

    private static final int METHODID_GET_POLICY_RULE = 2;

    private static final int METHODID_SET_POLICY_RULE = 3;

    private static final int METHODID_REMOVE_POLICY_RULE = 4;

    private static final class MethodHandlers<Req, Resp> implements io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>, io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {

        private final ContextPolicyServiceImplBase serviceImpl;

        private final int methodId;

        private final String compression;

        MethodHandlers(ContextPolicyServiceImplBase serviceImpl, int methodId, String compression) {
            this.serviceImpl = serviceImpl;
            this.methodId = methodId;
            this.compression = compression;
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                case METHODID_LIST_POLICY_RULE_IDS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleIdList>) responseObserver, compression, serviceImpl::listPolicyRuleIds);
                    break;
                case METHODID_LIST_POLICY_RULES:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleList>) responseObserver, compression, serviceImpl::listPolicyRules);
                    break;
                case METHODID_GET_POLICY_RULE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRule>) responseObserver, compression, serviceImpl::getPolicyRule);
                    break;
                case METHODID_SET_POLICY_RULE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRule) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleId>) responseObserver, compression, serviceImpl::setPolicyRule);
                    break;
                case METHODID_REMOVE_POLICY_RULE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::removePolicyRule);
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
