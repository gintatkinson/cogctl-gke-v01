package policy;

import static policy.PolicyServiceGrpc.getServiceDescriptor;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: policy.proto")
public final class MutinyPolicyServiceGrpc implements io.quarkus.grpc.MutinyGrpc {

    private MutinyPolicyServiceGrpc() {
    }

    public static MutinyPolicyServiceStub newMutinyStub(io.grpc.Channel channel) {
        return new MutinyPolicyServiceStub(channel);
    }

    public static class MutinyPolicyServiceStub extends io.grpc.stub.AbstractStub<MutinyPolicyServiceStub> implements io.quarkus.grpc.MutinyStub {

        private PolicyServiceGrpc.PolicyServiceStub delegateStub;

        private MutinyPolicyServiceStub(io.grpc.Channel channel) {
            super(channel);
            delegateStub = PolicyServiceGrpc.newStub(channel);
        }

        private MutinyPolicyServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
            delegateStub = PolicyServiceGrpc.newStub(channel).build(channel, callOptions);
        }

        @Override
        protected MutinyPolicyServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MutinyPolicyServiceStub(channel, callOptions);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddService(policy.Policy.PolicyRuleService request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::policyAddService);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddDevice(policy.Policy.PolicyRuleDevice request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::policyAddDevice);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateService(policy.Policy.PolicyRuleService request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::policyUpdateService);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateDevice(policy.Policy.PolicyRuleDevice request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::policyUpdateDevice);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyDelete(policy.Policy.PolicyRuleId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::policyDelete);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleService> getPolicyService(policy.Policy.PolicyRuleId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getPolicyService);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleDevice> getPolicyDevice(policy.Policy.PolicyRuleId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getPolicyDevice);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleServiceList> getPolicyByServiceId(context.ContextOuterClass.ServiceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getPolicyByServiceId);
        }
    }

    public static abstract class PolicyServiceImplBase implements io.grpc.BindableService {

        private String compression;

        /**
         * Set whether the server will try to use a compressed response.
         *
         * @param compression the compression, e.g {@code gzip}
         */
        public PolicyServiceImplBase withCompression(String compression) {
            this.compression = compression;
            return this;
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddService(policy.Policy.PolicyRuleService request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddDevice(policy.Policy.PolicyRuleDevice request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateService(policy.Policy.PolicyRuleService request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateDevice(policy.Policy.PolicyRuleDevice request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyDelete(policy.Policy.PolicyRuleId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleService> getPolicyService(policy.Policy.PolicyRuleId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleDevice> getPolicyDevice(policy.Policy.PolicyRuleId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleServiceList> getPolicyByServiceId(context.ContextOuterClass.ServiceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(policy.PolicyServiceGrpc.getPolicyAddServiceMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState>(this, METHODID_POLICY_ADD_SERVICE, compression))).addMethod(policy.PolicyServiceGrpc.getPolicyAddDeviceMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState>(this, METHODID_POLICY_ADD_DEVICE, compression))).addMethod(policy.PolicyServiceGrpc.getPolicyUpdateServiceMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleService, policy.Policy.PolicyRuleState>(this, METHODID_POLICY_UPDATE_SERVICE, compression))).addMethod(policy.PolicyServiceGrpc.getPolicyUpdateDeviceMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleDevice, policy.Policy.PolicyRuleState>(this, METHODID_POLICY_UPDATE_DEVICE, compression))).addMethod(policy.PolicyServiceGrpc.getPolicyDeleteMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleState>(this, METHODID_POLICY_DELETE, compression))).addMethod(policy.PolicyServiceGrpc.getGetPolicyServiceMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleService>(this, METHODID_GET_POLICY_SERVICE, compression))).addMethod(policy.PolicyServiceGrpc.getGetPolicyDeviceMethod(), asyncUnaryCall(new MethodHandlers<policy.Policy.PolicyRuleId, policy.Policy.PolicyRuleDevice>(this, METHODID_GET_POLICY_DEVICE, compression))).addMethod(policy.PolicyServiceGrpc.getGetPolicyByServiceIdMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, policy.Policy.PolicyRuleServiceList>(this, METHODID_GET_POLICY_BY_SERVICE_ID, compression))).build();
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

        private final PolicyServiceImplBase serviceImpl;

        private final int methodId;

        private final String compression;

        MethodHandlers(PolicyServiceImplBase serviceImpl, int methodId, String compression) {
            this.serviceImpl = serviceImpl;
            this.methodId = methodId;
            this.compression = compression;
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                case METHODID_POLICY_ADD_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleService) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver, compression, serviceImpl::policyAddService);
                    break;
                case METHODID_POLICY_ADD_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleDevice) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver, compression, serviceImpl::policyAddDevice);
                    break;
                case METHODID_POLICY_UPDATE_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleService) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver, compression, serviceImpl::policyUpdateService);
                    break;
                case METHODID_POLICY_UPDATE_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleDevice) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver, compression, serviceImpl::policyUpdateDevice);
                    break;
                case METHODID_POLICY_DELETE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleState>) responseObserver, compression, serviceImpl::policyDelete);
                    break;
                case METHODID_GET_POLICY_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleService>) responseObserver, compression, serviceImpl::getPolicyService);
                    break;
                case METHODID_GET_POLICY_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((policy.Policy.PolicyRuleId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleDevice>) responseObserver, compression, serviceImpl::getPolicyDevice);
                    break;
                case METHODID_GET_POLICY_BY_SERVICE_ID:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<policy.Policy.PolicyRuleServiceList>) responseObserver, compression, serviceImpl::getPolicyByServiceId);
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
